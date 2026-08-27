"""
CyberTools Suite - Settings Manager
=====================================
Reads/writes app configuration to a local JSON file (config/settings.json).
Also mirrors the AbuseIPDB key into engines/log_analyzer/.env, because
loganalyzer.py reads it via python-dotenv from its own working directory.

API keys are lightly obfuscated (base64) before being written to disk.
This is NOT strong encryption - it just avoids the key sitting in plain
text if someone casually opens the JSON file. A local single-user desktop
app has no real "server" to protect the key from, so this is a reasonable
and honest trade-off (documented, not oversold).
"""

from pathlib import Path
import json
import base64
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# User config - AppData me create karo
USER_DATA_DIR = Path.home() / "AppData" / "Local" / "CyberTools Suite"
CONFIG_DIR = USER_DATA_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "settings.json"
LOG_ANALYZER_ENV = BASE_DIR / "engines" / "log_analyzer" / ".env"

DEFAULT_SETTINGS = {
    "abuseipdb_api_key": "",
    "ai_enabled": False,
    "ai_model_tier": "auto",   # auto | fast | balanced | best
    "ai_setup_done": False,
}


def _obfuscate(value):
    if not value:
        return ""
    return base64.b64encode(value.encode("utf-8")).decode("utf-8")


def _deobfuscate(value):
    if not value:
        return ""
    try:
        return base64.b64decode(value.encode("utf-8")).decode("utf-8")
    except Exception:
        return ""


class SettingsManager:

    @classmethod
    def ensure_directories(cls):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        (BASE_DIR / "engines" / "log_analyzer").mkdir(parents=True, exist_ok=True)

    @classmethod
    def load(cls):
        cls.ensure_directories()

        if not CONFIG_FILE.exists():
            return dict(DEFAULT_SETTINGS)

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception:
            return dict(DEFAULT_SETTINGS)

        settings = dict(DEFAULT_SETTINGS)
        settings.update(raw)

        settings["abuseipdb_api_key"] = _deobfuscate(
            settings.get("abuseipdb_api_key", "")
        )

        return settings

    @classmethod
    def save(cls, settings):
        cls.ensure_directories()

        to_write = dict(settings)
        to_write["abuseipdb_api_key"] = _obfuscate(
            settings.get("abuseipdb_api_key", "")
        )

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(to_write, f, indent=4)

        # Mirror the AbuseIPDB key into the Log Analyzer's .env file so
        # loganalyzer.py's load_dotenv() picks it up with zero code changes.
        api_key = settings.get("abuseipdb_api_key", "")

        with open(LOG_ANALYZER_ENV, "w", encoding="utf-8") as f:
            f.write(f'ABUSEIPDB_API_KEY="{api_key}"\n')

        return True

    @classmethod
    def get(cls, key, default=None):
        return cls.load().get(key, default)

    @classmethod
    def set(cls, key, value):
        settings = cls.load()
        settings[key] = value
        cls.save(settings)
        return settings
