from pathlib import Path
from datetime import datetime
import  sys


if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# User data folders - AppData me create karo
USER_DATA_DIR = Path.home() / "AppData" / "Local" / "CyberTools Suite"
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
    """Get all reports from both cases/ and reports/ folders."""
    all_reports = []
    
    # Case reports
    if CASES_DIR.exists():
        for case_dir in CASES_DIR.iterdir():
            if not case_dir.is_dir():
                continue
            reports_dir = case_dir / "reports"
            if reports_dir.exists():
                for file in reports_dir.rglob("*"):
                    if file.is_file() and file.suffix.lower() in {".pdf", ".txt", ".xlsx", ".csv", ".json", ".html"}:
                        all_reports.append(file)
    
    # Global reports
    if REPORTS_DIR.exists():
        for file in REPORTS_DIR.rglob("*"):
            if file.is_file() and file.suffix.lower() in {".pdf", ".txt", ".xlsx", ".csv", ".json", ".html"}:
                all_reports.append(file)
    
    return all_reports


def get_reports():
    return len(get_all_reports())

def get_engines():
    if not ENGINES_DIR.exists():
        return 0

    return len([
        p for p in ENGINES_DIR.iterdir()
        if p.is_dir()
    ])


def get_recent_activity(limit=6):

    items = []

    for root in (CASES_DIR, REPORTS_DIR):

        if not root.exists():
            continue

        for file in root.rglob("*"):

            if not file.is_file():
                continue

            # Only include relevant files
            if file.suffix.lower() not in {".pdf", ".txt", ".xlsx", ".csv", ".json", ".html", ".log"}:
                continue

            try:
                timestamp = file.stat().st_mtime
            except OSError:
                continue

            items.append({
                "name": file.name,
                "path": str(file),
                "timestamp": timestamp,
                "time": datetime.fromtimestamp(timestamp)
            })

    items.sort(
        key=lambda x: x["timestamp"],
        reverse=True
    )

    return items[:limit]

def get_system_stats():

    return {
        "active_cases": get_active_cases(),
        "reports": get_reports(),
        "engines": get_engines(),
        "recent_activity": get_recent_activity()
    }