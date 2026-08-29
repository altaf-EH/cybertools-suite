from pathlib import Path
from datetime import datetime
from ui.report_index import ReportIndex
import  sys


if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# User data folders - AppData me create karo
USER_DATA_DIR = Path.home() / "Documents" / "CyberTools Suite"
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

CASES_DIR = USER_DATA_DIR / "cases"
CASES_DIR.mkdir(parents=True, exist_ok=True)

REPORTS_DIR = USER_DATA_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

ENGINES_DIR = BASE_DIR / "engines"



def count_files(folder, extensions=None):
    if not folder.exists():
        return 0

    files = [
        p for p in folder.rglob("*")
        if p.is_file()
    ]

    if extensions:
        files = [
            p for p in files
            if p.suffix.lower() in extensions
        ]

    return len(files)


def count_directories(folder):
    if not folder.exists():
        return 0

    return len([
        p for p in folder.iterdir()
        if p.is_dir()
    ])


def get_active_cases():
    return count_directories(CASES_DIR)


def get_all_reports():
    """Central registry se sabhi reports — kahi bhi save hui ho."""
    return [entry["path"] for entry in ReportIndex.get_all()]


def get_reports():
    return len(ReportIndex.get_all())

def get_engines():
    if not ENGINES_DIR.exists():
        return 0

    return len([
        p for p in ENGINES_DIR.iterdir()
        if p.is_dir()
    ])


def get_recent_activity(limit=6):
    entries = ReportIndex.get_all()[:limit]

    items = []
    for entry in entries:
        try:
            ts = datetime.fromisoformat(entry["timestamp"])
        except Exception:
            continue

        items.append({
            "name": entry["name"],
            "path": entry["path"],
            "timestamp": ts.timestamp(),
            "time": ts,
        })

    return items

def get_system_stats():
    active_cases = 0
    if CASES_DIR.exists():
        active_cases = len([d for d in CASES_DIR.iterdir() if d.is_dir()])

    return {
        "active_cases": active_cases,
        "reports": get_reports(),
        "engines": get_engines(),
        "recent_activity": get_recent_activity(),
    }