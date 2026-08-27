from pathlib import Path
from datetime import datetime
import json
import shutil
import sys


# ============================================================
# PATHS
# ============================================================

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# User data folders - AppData me create karo
USER_DATA_DIR = Path.home() / "AppData" / "Local" / "CyberTools Suite"
CASES_DIR = USER_DATA_DIR / "cases"
REPORTS_DIR = USER_DATA_DIR / "reports"

# Pehle se ensure karo ki folder exist kare
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
CASES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CASE MANAGER
# ============================================================

class CaseManager:

    # ========================================================
    # DIRECTORIES
    # ========================================================

    @classmethod
    def ensure_directories(cls):

        # USER_DATA_DIR create karo
        USER_DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        # CASES_DIR create karo
        CASES_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        # REPORTS_DIR create karo
        REPORTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )


    # ========================================================
    # CREATE CASE
    # ========================================================

    @classmethod
    def create_case(
        cls,
        case_id,
        title="Untitled Investigation",
        description="",
    ):

        cls.ensure_directories()

        case_id = str(case_id).strip()

        if not case_id:
            raise ValueError(
                "Case ID cannot be empty."
            )

        case_dir = CASES_DIR / case_id

        if case_dir.exists():
            raise FileExistsError(
                f"Case already exists: {case_id}"
            )

        # ----------------------------------------------------
        # CASE SUBDIRECTORIES
        # ----------------------------------------------------

        evidence_dir = case_dir / "evidence"
        reports_dir = case_dir / "reports"
        artifacts_dir = case_dir / "artifacts"

        evidence_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        reports_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        artifacts_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ----------------------------------------------------
        # CASE METADATA
        # ----------------------------------------------------

        created_at = datetime.now()

        case_data = {
            "case_id": case_id,
            "title": title,
            "description": description,
            "status": "OPEN",
            "created_at": created_at.isoformat(),
            "updated_at": created_at.isoformat(),
            "evidence_count": 0,
            "report_count": 0,
            "analyses": [],
        }

        metadata_path = case_dir / "case.json"

        with open(
            metadata_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                case_data,
                file,
                indent=4,
            )

        return case_data


    # ========================================================
    # CASE EXISTS
    # ========================================================

    @classmethod
    def case_exists(cls, case_id):

        return (
            CASES_DIR / str(case_id)
        ).exists()


    # ========================================================
    # GET CASE
    # ========================================================

    @classmethod
    def get_case(cls, case_id):

        case_dir = CASES_DIR / str(case_id)
        metadata_path = case_dir / "case.json"

        if not metadata_path.exists():
            return None

        try:

            with open(
                metadata_path,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except Exception:

            return None


    # ========================================================
    # LIST CASES
    # ========================================================

    @classmethod
    def list_cases(cls):

        cls.ensure_directories()

        cases = []

        for case_dir in CASES_DIR.iterdir():

            if not case_dir.is_dir():
                continue

            metadata_path = case_dir / "case.json"

            if not metadata_path.exists():
                continue

            try:

                with open(
                    metadata_path,
                    "r",
                    encoding="utf-8",
                ) as file:

                    case_data = json.load(file)

                cases.append(case_data)

            except Exception:

                continue

        cases.sort(
            key=lambda item: item.get(
                "updated_at",
                "",
            ),
            reverse=True,
        )

        return cases


    # ========================================================
    # UPDATE CASE
    # ========================================================

    @classmethod
    def update_case(
        cls,
        case_id,
        **updates,
    ):

        case_data = cls.get_case(
            case_id
        )

        if case_data is None:
            return False

        case_data.update(updates)

        case_data["updated_at"] = (
            datetime.now().isoformat()
        )

        metadata_path = (
            CASES_DIR
            / str(case_id)
            / "case.json"
        )

        with open(
            metadata_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                case_data,
                file,
                indent=4,
            )

        return True


    # ========================================================
    # ADD EVIDENCE
    # ========================================================

    @classmethod
    def add_evidence(
        cls,
        case_id,
        source_file,
    ):

        case_dir = CASES_DIR / str(case_id)

        if not case_dir.exists():
            raise FileNotFoundError(
                f"Case not found: {case_id}"
            )

        source = Path(source_file)

        if not source.exists():
            raise FileNotFoundError(
                f"Evidence file not found: {source}"
            )

        evidence_dir = case_dir / "evidence"

        evidence_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = (
            evidence_dir / source.name
        )

        # Prevent accidental overwrite
        if destination.exists():

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            destination = (
                evidence_dir
                / f"{source.stem}_{timestamp}{source.suffix}"
            )

        shutil.copy2(
            source,
            destination,
        )

        case_data = cls.get_case(
            case_id
        )

        if case_data:

            case_data["evidence_count"] = len(
                list(
                    evidence_dir.iterdir()
                )
            )

            case_data["updated_at"] = (
                datetime.now().isoformat()
            )

            metadata_path = (
                case_dir / "case.json"
            )

            with open(
                metadata_path,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    case_data,
                    file,
                    indent=4,
                )

        return destination


    # ========================================================
    # GET EVIDENCE
    # ========================================================

    @classmethod
    def get_evidence(cls, case_id):

        evidence_dir = (
            CASES_DIR
            / str(case_id)
            / "evidence"
        )

        if not evidence_dir.exists():
            return []

        return [
            path
            for path in evidence_dir.iterdir()
            if path.is_file()
        ]


    # ========================================================
    # GET REPORTS
    # ========================================================

    @classmethod
    def get_reports(cls, case_id):

        reports_dir = (
            CASES_DIR
            / str(case_id)
            / "reports"
        )

        if not reports_dir.exists():
            return []

        supported = {
            ".pdf",
            ".txt",
            ".xlsx",
            ".csv",
            ".json",
        }

        return sorted(
            [
                path
                for path in reports_dir.rglob("*")
                if (
                    path.is_file()
                    and path.suffix.lower()
                    in supported
                )
            ],
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )


    # ========================================================
    # REGISTER ANALYSIS
    # ========================================================

    @classmethod
    def register_analysis(
        cls,
        case_id,
        engine,
        input_file,
        status="COMPLETED",
    ):

        case_data = cls.get_case(
            case_id
        )

        if case_data is None:
            return False

        analysis = {
            "engine": engine,
            "input_file": str(input_file),
            "status": status,
            "timestamp": datetime.now().isoformat(),
        }

        case_data.setdefault(
            "analyses",
            []
        )

        case_data["analyses"].append(
            analysis
        )

        case_data["updated_at"] = (
            datetime.now().isoformat()
        )

        case_data["report_count"] = len(
            cls.get_reports(case_id)
        )

        metadata_path = (
            CASES_DIR
            / str(case_id)
            / "case.json"
        )

        with open(
            metadata_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                case_data,
                file,
                indent=4,
            )

        return True


    # ========================================================
    # CASE STATUS
    # ========================================================

    @classmethod
    def set_status(
        cls,
        case_id,
        status,
    ):

        return cls.update_case(
            case_id,
            status=status,
        )