from pathlib import Path
from ui.report_index import ReportIndex
from ui.paths import get_data_dir, get_internal_dir
import subprocess
import sys
import shutil
import time


# ============================================================
# PATHS
# ============================================================

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# User data folders - user-selected folder me create karo
USER_DATA_DIR = get_data_dir()

CASES_DIR = USER_DATA_DIR / "cases"
CASES_DIR.mkdir(parents=True, exist_ok=True)

# Internal bookkeeping - hamesha fixed AppData me, user ke folder me kabhi nahi
REPORTS_DIR = get_internal_dir() / "reports"

ENGINES_DIR = BASE_DIR / "engines"


# ============================================================
# ENGINE RUNNER
# ============================================================

class EngineRunner:

    ENGINES = {

        "CDR Analyzer": {
            "folder": "cdr_analyzer",
            "script": "cdr_analyzer.py",
        },

        "Log Analyzer": {
            "folder": "log_analyzer",
            "script": "loganalyzer.py",
        },

        "FinTrack": {
            "folder": "fintrack",
            "script": "fintrack.py",
        },

    }


    SUPPORTED_REPORTS = {
        ".pdf",
        ".txt",
        ".xlsx",
        ".csv",
        ".json",
    }


    # ========================================================
    # ENGINE LOOKUP
    # ========================================================

    @classmethod
    def get_engine(cls, engine_name):

        return cls.ENGINES.get(
            engine_name
        )


    # ========================================================
    # VALIDATE ENGINE
    # ========================================================

    @classmethod
    def validate_engine(cls, engine_name):
        engine = cls.get_engine(engine_name)
        if engine is None:
            return False, "Unknown engine."

        engine_dir = ENGINES_DIR / engine["folder"]
        script = engine_dir / engine["script"]

        if not engine_dir.exists():
            return False, f"Engine directory not found: {engine_dir}"

        if not script.exists():
            return False, f"Engine script not found: {script}"

        return True, "Engine ready."


    # ========================================================
    # CASE DIRECTORY
    # ========================================================

    @classmethod
    def get_case_directory(
        cls,
        case_id,
    ):

        if not case_id:
            return None

        case_dir = (
            CASES_DIR
            / str(case_id)
        )

        case_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return case_dir


    # ========================================================
    # CASE REPORT DIRECTORY
    # ========================================================

    @classmethod
    def get_case_report_directory(
        cls,
        case_id,
    ):

        case_dir = cls.get_case_directory(
            case_id
        )

        if case_dir is None:
            return None

        report_dir = (
            case_dir
            / "reports"
        )

        report_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return report_dir


    # ========================================================
    # CASE ARTIFACT DIRECTORY
    # ========================================================

    @classmethod
    def get_case_artifact_directory(
        cls,
        case_id,
    ):

        case_dir = cls.get_case_directory(
            case_id
        )

        if case_dir is None:
            return None

        artifact_dir = (
            case_dir
            / "artifacts"
        )

        artifact_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return artifact_dir


    # ========================================================
    # BUILD COMMAND
    # ========================================================

    @classmethod
    def build_command(
        cls,
        engine_name,
        case_id,
        input_file,
        output_dir=None,
    ):

        engine = cls.get_engine(
            engine_name
        )

        if engine is None:

            raise ValueError(
                f"Unknown engine: {engine_name}"
            )


        engine_dir = (
            ENGINES_DIR
            / engine["folder"]
        )

        script = (
            engine_dir
            / engine["script"]
        )


        input_path = Path(
            input_file
        ).resolve()


        if output_dir:

            output_path = Path(
                output_dir
            ).resolve()

        elif case_id:

            output_path = (
                cls.get_case_report_directory(
                    case_id
                )
            )

        else:

            output_path = (
                REPORTS_DIR
            )


        output_path.mkdir(
            parents=True,
            exist_ok=True,
        )


        # ----------------------------------------------------
        # SAB ENGINES KO --output FLAG PASS KARO
        # ----------------------------------------------------

        # 🔥 FIXED: Ensure file path is passed correctly
        command = [
            sys.executable,  # Python executable (venv/system)
            str(script),
            str(input_path.resolve()),  # Absolute path
            "--output",
            str(output_path.resolve()),  # Absolute path
        ]


        return (
            command,
            engine_dir,
            output_path,
        )


    # ========================================================
    # SNAPSHOT REPORTS
    # ========================================================

    @classmethod
    def snapshot_reports(
        cls,
        directory,
    ):

        directory = Path(
            directory
        )

        if not directory.exists():
            return set()

        files = set()

        for path in directory.rglob("*"):

            if not path.is_file():
                continue

            if (
                path.suffix.lower()
                not in cls.SUPPORTED_REPORTS
            ):
                continue

            files.add(
                path.resolve()
            )

        return files


    # ========================================================
    # COLLECT NEW REPORTS
    # ========================================================

    @classmethod
    def collect_reports(
        cls,
        source_dir,
        case_id,
        before_files=None,
    ):

        source_dir = Path(
            source_dir
        )

        if not source_dir.exists():
            return []


        before_files = (
            before_files
            if before_files is not None
            else set()
        )


        case_report_dir = (
            cls.get_case_report_directory(
                case_id
            )
        )

        if case_report_dir is None:
            return []


        copied = []


        for file_path in source_dir.rglob("*"):

            if not file_path.is_file():
                continue


            if (
                file_path.suffix.lower()
                not in cls.SUPPORTED_REPORTS
            ):
                continue


            resolved = file_path.resolve()


            # ----------------------------------------------
            # Don't copy files already inside case reports
            # ----------------------------------------------

            try:

                resolved.relative_to(
                    case_report_dir.resolve()
                )

                continue

            except ValueError:

                pass


            # ----------------------------------------------
            # Only copy newly generated files
            # ----------------------------------------------

            if (
                before_files
                and resolved in before_files
            ):
                continue


            destination = (
                case_report_dir
                / file_path.name
            )


            # ----------------------------------------------
            # Prevent filename collision
            # ----------------------------------------------

            if destination.exists():

                timestamp = time.strftime(
                    "%Y%m%d_%H%M%S"
                )

                destination = (
                    case_report_dir
                    / (
                        f"{file_path.stem}_"
                        f"{timestamp}"
                        f"{file_path.suffix}"
                    )
                )


            try:

                shutil.copy2(
                    file_path,
                    destination,
                )

                copied.append(
                    destination
                )

            except Exception as exc:

                print(
                    "[EngineRunner] "
                    f"Unable to copy report "
                    f"{file_path}: {exc}"
                )


        return copied


    # ========================================================
    # BUILD RUN CONTEXT
    # ========================================================

    @classmethod
    def prepare_run(cls, engine_name, case_id, input_file, output_dir=None):
        valid, message = cls.validate_engine(engine_name)
        if not valid:
            return False, message

        input_path = Path(input_file).resolve()
        if not input_path.exists():
            return False, f"Input file not found: {input_path}"

        try:
            command, engine_dir, output_path = cls.build_command(engine_name, case_id, input_path, output_dir)
        except Exception as exc:
            return False, str(exc)

        before_files = cls.snapshot_reports(engine_dir)

        return True, {
            "command": command,
            "engine_dir": engine_dir,
            "output_dir": output_path,
            "before_files": before_files,
            "case_id": case_id,
            "engine_name": engine_name,
            "input_file": input_path,
        }

        
    # ========================================================
    # RUN ENGINE
    # ========================================================

        # ========================================================
    # RUN ENGINE
    # ========================================================

    @classmethod
    def run(
        cls,
        engine_name,
        case_id,
        input_file,
        output_dir=None,
    ):

        success, result = (
            cls.prepare_run(
                engine_name,
                case_id,
                input_file,
                output_dir,
            )
        )


        if not success:

            return (
                False,
                result,
            )


        context = result


        try:

            # System Python use karo - .exe ke andar bhi
            python_exe = "python"

            if sys.platform == "win32":
                python_exe = "python.exe"

            # Command me pehle element replace karo
            command = [python_exe] + context["command"][1:]

            process = subprocess.Popen(

                command,

                cwd=str(
                    context["engine_dir"]
                ),

                stdout=subprocess.PIPE,

                stderr=subprocess.PIPE,

                text=True,

            )

            # 🔥 Process ko context ke andar hi rakh do,
            # taaki caller (dashboard.py) process khatam hone ke baad
            # isi context se finalize_run() call kar sake aur
            # reports ko ReportIndex me register kar sake.
            context["process"] = process

            return (
                True,
                context,
            )


        except Exception as exc:

            return (
                False,
                str(exc),
            )


    # ========================================================
    # FINALIZE RUN
    # ========================================================

    @classmethod
    def finalize_run(
        cls,
        context,
    ):

        if not context:
            return []


        engine_name = (
            context.get(
                "engine_name"
            )
        )

        case_id = (
            context.get(
                "case_id"
            )
        )

        engine_dir = (
            context.get(
                "engine_dir"
            )
        )

        output_dir = (
            context.get(
                "output_dir"
            )
        )

        before_files = (
            context.get(
                "before_files",
                set(),
            )
        )


        # ----------------------------------------------------
        # SAB ENGINES AB DIRECTLY OUTPUT DIR ME LIKHTE HAIN
        # ----------------------------------------------------

        if output_dir:

            reports = [
                path
                for path in Path(
                    output_dir
                ).rglob("*")
                if (
                    path.is_file()
                    and path.suffix.lower()
                    in cls.SUPPORTED_REPORTS
                )
            ]

        else:

            # ----------------------------------------------------
            # FALLBACK: COLLECT FROM ENGINE DIR
            # ----------------------------------------------------

            reports = cls.collect_reports(
                engine_dir,
                case_id,
                before_files,
            )


        # ----------------------------------------------------
        # 🔥 CENTRAL REGISTRY ME REGISTER KARO
        # Report chahe kahi bhi save hui ho (case folder, global
        # reports folder, ya user ka koi bhi custom folder) —
        # ab Dashboard aur Reports page hamesha isse dhoondh lenge.
        # ----------------------------------------------------

        for report_path in reports:

            ReportIndex.register(
                report_path,
                engine_name=engine_name,
                case_id=case_id,
            )


        return reports