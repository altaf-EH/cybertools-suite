from pathlib import Path
from datetime import datetime
import json
from ui.paths import get_internal_dir

USER_DATA_DIR = get_internal_dir()

INDEX_FILE = USER_DATA_DIR / "reports_index.json"


class ReportIndex:
    """Central registry of every report the software has ever generated,
    no matter which folder it was actually saved into."""

    @classmethod
    def _load(cls):
        if not INDEX_FILE.exists():
            return []
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    @classmethod
    def _save(cls, entries):
        try:
            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=4)
        except Exception as exc:
            print(f"[ReportIndex] Unable to save index: {exc}")

    @classmethod
    def register(cls, file_path, engine_name=None, case_id=None):
        """Call this every time a report file is generated, wherever it is."""
        file_path = Path(file_path).resolve()

        entries = cls._load()

        # Same path dobara register ho to purani entry hata do (no duplicates)
        entries = [e for e in entries if e.get("path") != str(file_path)]

        entries.append({
            "path": str(file_path),
            "name": file_path.name,
            "engine": engine_name,
            "case_id": case_id,
            "timestamp": datetime.now().isoformat(),
        })

        cls._save(entries)

    @classmethod
    def register_many(cls, file_paths, engine_name=None, case_id=None):
        for path in file_paths:
            cls.register(path, engine_name, case_id)

    @classmethod
    def get_all(cls):
        """Sabhi registered reports jinki file abhi bhi exist karti hai,
        newest-first order me."""
        entries = cls._load()

        valid_entries = []
        changed = False

        for entry in entries:
            path = Path(entry.get("path", ""))
            if path.exists():
                valid_entries.append(entry)
            else:
                # File delete/move ho gayi, registry se bhi hata do
                changed = True

        if changed:
            cls._save(valid_entries)

        valid_entries.sort(
            key=lambda e: e.get("timestamp", ""),
            reverse=True,
        )

        return valid_entries