"""
CyberTools Suite - AI Insights (Local LLM via Ollama)
=======================================================
No API keys, no per-request cost, no data leaving the user's PC.

How it works:
1. detect_ram_gb()      -> reads the machine's total RAM
2. recommend_model()    -> picks a model tier that fits that RAM
3. OllamaClient         -> talks to the local Ollama service
                           (http://localhost:11434), which must be
                           installed separately (see README / installer)
4. analyze_report()     -> combines the engine's findings with an
                           editable "known patterns" knowledge base
                           (data/known_patterns.json) and asks the local
                           model for a contextual read of the case

This is a genuine hybrid design, not a marketing claim:
- The hardcoded rules in each engine remain the fast, reliable, always-on
  detector for KNOWN patterns.
- The LLM adds reasoning/context on top - it can connect flags together
  and reason about combinations the rules didn't explicitly check for.
- It does NOT learn new patterns on its own in real time. New patterns
  the investigator discovers should be added to data/known_patterns.json
  so every future analysis (rules + AI) benefits from them immediately.
"""

from pathlib import Path
import json
import platform
import subprocess
import urllib.request
import urllib.error
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

KNOWN_PATTERNS_FILE = BASE_DIR / "data" / "known_patterns.json"

OLLAMA_HOST = "http://localhost:11434"

# ============================================================
# MODEL TIERS
# ============================================================
# Each tier maps to an Ollama model tag. Larger models need more RAM
# but reason better. "auto" picks based on detected hardware.

MODEL_TIERS = {
    "fast": {
        "model": "llama3.2:3b",
        "label": "Fast (llama3.2:3b, ~2GB, works on 8GB+ RAM)",
        "min_ram_gb": 8,
    },
    "balanced": {
        "model": "phi3:mini",
        "label": "Balanced (phi3:mini, ~2.3GB, works on 8GB+ RAM)",
        "min_ram_gb": 8,
    },
    "best": {
        "model": "llama3.1:8b",
        "label": "Best (llama3.1:8b, ~4.7GB, needs 16GB+ RAM)",
        "min_ram_gb": 16,
    },
}


# ============================================================
# HARDWARE DETECTION
# ============================================================

def detect_ram_gb():
    """Return total system RAM in GB (best-effort, cross-platform)."""

    try:
        import psutil
        return round(psutil.virtual_memory().total / (1024 ** 3), 1)
    except ImportError:
        pass

    system = platform.system()

    try:
        if system == "Windows":
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return round(stat.ullTotalPhys / (1024 ** 3), 1)

        elif system == "Linux":
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        kb = int(line.split()[1])
                        return round(kb / (1024 ** 2), 1)

        elif system == "Darwin":
            output = subprocess.check_output(
                ["sysctl", "-n", "hw.memsize"]
            )
            return round(int(output.strip()) / (1024 ** 3), 1)

    except Exception:
        pass

    return 0.0


def recommend_tier(ram_gb=None):
    """Pick the best model tier this machine can comfortably run."""

    if ram_gb is None:
        ram_gb = detect_ram_gb()

    if ram_gb >= 16:
        return "best"
    elif ram_gb >= 8:
        return "fast"
    else:
        return None  # too little RAM - AI unavailable


def resolve_tier(preference, ram_gb=None):
    """Resolve a user preference ('auto'/'fast'/'balanced'/'best') into
    an actual tier key, respecting hardware limits."""

    if ram_gb is None:
        ram_gb = detect_ram_gb()

    if preference == "auto" or not preference:
        return recommend_tier(ram_gb)

    tier = MODEL_TIERS.get(preference)

    if tier and ram_gb >= tier["min_ram_gb"]:
        return preference

    # Requested tier doesn't fit this hardware - fall back safely
    return recommend_tier(ram_gb)


# ============================================================
# KNOWLEDGE BASE (editable, growing pattern list)
# ============================================================

def load_known_patterns():
    if not KNOWN_PATTERNS_FILE.exists():
        return []

    try:
        with open(KNOWN_PATTERNS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("patterns", [])
    except Exception:
        return []


def add_known_pattern(title, description):
    KNOWN_PATTERNS_FILE.parent.mkdir(parents=True, exist_ok=True)

    patterns = load_known_patterns()
    patterns.append({"title": title, "description": description})

    with open(KNOWN_PATTERNS_FILE, "w", encoding="utf-8") as f:
        json.dump({"patterns": patterns}, f, indent=4)


# ============================================================
# OLLAMA CLIENT
# ============================================================

class OllamaClient:

    @staticmethod
    def is_running():
        try:
            urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=2)
            return True
        except Exception:
            return False

    @staticmethod
    def list_installed_models():
        try:
            with urllib.request.urlopen(
                f"{OLLAMA_HOST}/api/tags", timeout=3
            ) as response:
                data = json.loads(response.read().decode("utf-8"))
                return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []

    @staticmethod
    def has_model(model_name):
        installed = OllamaClient.list_installed_models()
        return any(model_name in name for name in installed)

    @staticmethod
    def pull_model(model_name, on_progress=None):
        """Triggers a model download. Streams progress lines back via
        on_progress(text) if provided. Blocking call - run from a
        background QThread in the GUI, never on the UI thread."""

        req = urllib.request.Request(
            f"{OLLAMA_HOST}/api/pull",
            data=json.dumps({"name": model_name}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=None) as response:
                for line in response:
                    if not line.strip():
                        continue
                    try:
                        payload = json.loads(line.decode("utf-8"))
                    except Exception:
                        continue

                    status = payload.get("status", "")

                    if on_progress:
                        on_progress(status)

                    if payload.get("error"):
                        return False, payload["error"]

            return True, "Model ready."

        except urllib.error.URLError as exc:
            return False, f"Could not reach Ollama: {exc}"
        except Exception as exc:
            return False, str(exc)

    @staticmethod
    def generate(model_name, prompt, on_chunk=None):
        """Blocking call to Ollama's generate endpoint. Run in a
        background QThread. Returns (success, text_or_error)."""

        req = urllib.request.Request(
            f"{OLLAMA_HOST}/api/generate",
            data=json.dumps({
                "model": model_name,
                "prompt": prompt,
                "stream": False,
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                payload = json.loads(response.read().decode("utf-8"))
                return True, payload.get("response", "").strip()

        except urllib.error.URLError as exc:
            return False, (
                "Could not reach Ollama. Make sure it is installed and "
                f"running. ({exc})"
            )
        except Exception as exc:
            return False, str(exc)


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(engine_name, case_id, findings_summary):
    """Builds the prompt sent to the local model. Keeps the known
    patterns knowledge base in context so new patterns the investigator
    has logged get checked automatically."""

    patterns = load_known_patterns()

    if patterns:
        pattern_lines = "\n".join(
            f"- {p['title']}: {p['description']}" for p in patterns
        )
    else:
        pattern_lines = "(no additional patterns logged yet)"

    prompt = f"""You are a digital-forensics assistant helping a licensed investigator
review the automated findings below. Be concise, factual, and avoid
speculation you can't support from the data given.

CASE ID: {case_id}
ENGINE: {engine_name}

AUTOMATED FINDINGS:
{findings_summary}

ADDITIONAL KNOWN THREAT PATTERNS THE INVESTIGATOR HAS LOGGED
(check whether the findings above match any of these too):
{pattern_lines}

Respond with:
1. A short plain-language summary of what stands out (2-4 sentences)
2. Any connections between individual flags that together suggest a
   bigger pattern (e.g. multiple weak signals combining into one
   strong one)
3. Whether anything matches a logged known pattern above
4. Suggested next investigative step
"""
    return prompt


def analyze_report(engine_name, case_id, findings_summary, model_tier="auto"):
    """High-level entry point used by the GUI. Returns (success, text)."""

    if not OllamaClient.is_running():
        return False, (
            "Ollama isn't running on this PC. Install it from "
            "ollama.com and make sure it's running, then try again."
        )

    ram_gb = detect_ram_gb()
    tier = resolve_tier(model_tier, ram_gb)

    if tier is None:
        return False, (
            f"This PC has {ram_gb} GB RAM, which is below the 8GB "
            "minimum for local AI analysis. The rest of the app "
            "works normally without it."
        )

    model_name = MODEL_TIERS[tier]["model"]

    if not OllamaClient.has_model(model_name):
        return False, (
            f"Model '{model_name}' isn't downloaded yet. Go to "
            "Settings > AI Insights and click 'Download Model' first."
        )

    prompt = build_prompt(engine_name, case_id, findings_summary)

    return OllamaClient.generate(model_name, prompt)
