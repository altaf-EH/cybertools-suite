from pathlib import Path
from ui.case_manager import CaseManager, CASES_DIR

from PySide6.QtWidgets import QSizePolicy
import os
from datetime import datetime
import subprocess
import sys

from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    QThread,
    Signal,
    QSize,
)

from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
    QLineEdit,
)

from ui.system_stats import get_system_stats, get_all_reports
from ui.engine_workspace import EngineWorkspace
from ui.engine_runner import EngineRunner
from ui.theme import apply_theme as apply_global_theme
from ui.settings_page import SettingsPage
from ui.settings_manager import SettingsManager
from ui import ai_insights


# ============================================================
# PATHS
# ============================================================

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

ENGINES_DIR = BASE_DIR / "engines"


# ============================================================
# STAT CARD
# ============================================================

class StatCard(QFrame):

    def __init__(self, title, value, description, parent=None):
        super().__init__(parent)

        self.setObjectName("statCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("statTitle")

        value_label = QLabel(value)
        value_label.setObjectName("statValue")

        description_label = QLabel(description)
        description_label.setObjectName("statDescription")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(description_label)


# ============================================================
# BASE PAGE
# ============================================================

class InvestigationPage(QWidget):

    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent)

        self.page_layout = QVBoxLayout(self)
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.page_layout.setSpacing(6)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("pageTitle")

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("pageSubtitle")

        self.page_layout.addWidget(self.title_label)
        self.page_layout.addWidget(self.subtitle_label)
        self.page_layout.addSpacing(24)

        self.body = QVBoxLayout()
        self.body.setSpacing(18)

        self.page_layout.addLayout(self.body)
        self.page_layout.addStretch()


# ============================================================
# DASHBOARD PAGE
# ============================================================

class DashboardPage(InvestigationPage):

    def __init__(self, parent=None):
        super().__init__(
            "Investigation Dashboard",
            "Central command center for digital investigation operations.",
            parent,
        )

        self.activity_panel = None
        self.build_dashboard()

    def build_dashboard(self):

        stats_data = get_system_stats()

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        self.case_card = StatCard(
            "ACTIVE CASES",
            str(stats_data["active_cases"]),
            "Currently open investigations",
        )

        self.report_card = StatCard(
            "REPORTS",
            str(stats_data["reports"]),
            "Generated investigation reports",
        )

        self.engine_card = StatCard(
            "ENGINES",
            str(stats_data["engines"]),
            "Available analysis engines",
        )

        self.system_card = StatCard(
            "SYSTEM",
            "READY",
            "CyberTools core status",
        )

        stats_layout.addWidget(self.case_card)
        stats_layout.addWidget(self.report_card)
        stats_layout.addWidget(self.engine_card)
        stats_layout.addWidget(self.system_card)
                # Refresh button
        refresh_row = QHBoxLayout()
        refresh_row.setSpacing(12)

        refresh_button = QPushButton("REFRESH DASHBOARD")
        refresh_button.setObjectName("secondaryButton")
        refresh_button.clicked.connect(self.refresh_dashboard)

        refresh_row.addStretch()
        refresh_row.addWidget(refresh_button)

        self.body.addLayout(refresh_row)

        self.body.addLayout(stats_layout)

        # ----------------------------------------------------
        # ACTIVITY PANEL
        # ----------------------------------------------------

        self.activity_panel = QFrame()
        self.activity_panel.setObjectName("panel")

        self.activity_layout = QVBoxLayout(
            self.activity_panel
        )

        self.activity_layout.setContentsMargins(
            22, 20, 22, 20
        )

        self.activity_layout.setSpacing(12)

        self.body.addWidget(
            self.activity_panel
        )

        self.refresh_activity()

    # ========================================================
    # REFRESH DASHBOARD
    # ========================================================

    def refresh_dashboard(self):

        stats_data = get_system_stats()

        self.case_card.findChild(
            QLabel,
            "statValue"
        ).setText(
            str(stats_data["active_cases"])
        )

        self.report_card.findChild(
            QLabel,
            "statValue"
        ).setText(
            str(stats_data["reports"])
        )

        self.engine_card.findChild(
            QLabel,
            "statValue"
        ).setText(
            str(stats_data["engines"])
        )

        self.refresh_activity()

    # ========================================================
    # REFRESH ACTIVITY
    # ========================================================

    def refresh_activity(self):

        while self.activity_layout.count():

            item = self.activity_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        activity_title = QLabel(
            "RECENT ACTIVITY"
        )

        activity_title.setObjectName(
            "sectionTitle"
        )

        self.activity_layout.addWidget(
            activity_title
        )

        stats_data = get_system_stats()

        recent_activity = stats_data.get(
            "recent_activity",
            []
        )

        if not recent_activity:

            empty_label = QLabel(
                "No investigation activity recorded yet."
            )

            empty_label.setObjectName(
                "panelText"
            )

            self.activity_layout.addWidget(
                empty_label
            )

            return

        for activity in recent_activity:

            row = QFrame()
            row.setObjectName(
                "activityRow"
            )

            row_layout = QHBoxLayout(row)

            row_layout.setContentsMargins(
                12, 10, 12, 10
            )

            name_label = QLabel(
                activity["name"]
            )

            name_label.setObjectName(
                "activityName"
            )

            time_label = QLabel(
                activity["time"].strftime(
                    "%d %b %Y  %H:%M"
                )
            )

            time_label.setObjectName(
                "activityTime"
            )

            row_layout.addWidget(
                name_label
            )

            row_layout.addStretch()

            row_layout.addWidget(
                time_label
            )

            self.activity_layout.addWidget(
                row
            )


# ============================================================
# ENGINE PAGE
# ============================================================

class EnginePage(QWidget):

    def __init__(
        self,
        engine_name,
        subtitle,
        description,
        extensions,
        parent=None,
    ):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.workspace = EngineWorkspace(
            engine_name=engine_name,
            description=description,
            supported_extensions=extensions,
        )

        layout.addWidget(self.workspace)

# ============================================================
# CASE MANAGEMENT PAGE
# ============================================================

class CasePage(InvestigationPage):

    def __init__(self, parent=None):

        super().__init__(
            "Case Management",
            "Create, organize and track investigation cases.",
            parent,
        )

        CaseManager.ensure_directories()

        self.current_case_id = None

        self.build_case_page()

        self.load_cases()


    # ========================================================
    # BUILD CASE PAGE
    # ========================================================

    def build_case_page(self):

        # ----------------------------------------------------
        # CREATE CASE PANEL
        # ----------------------------------------------------

        create_panel = QFrame()
        create_panel.setObjectName("panel")

        create_layout = QVBoxLayout(
            create_panel
        )

        create_layout.setContentsMargins(
            22,
            20,
            22,
            20,
        )

        create_layout.setSpacing(12)

        title = QLabel(
            "CREATE NEW CASE"
        )

        title.setObjectName(
            "sectionTitle"
        )

        create_layout.addWidget(title)


        # ----------------------------------------------------
        # CASE ID
        # ----------------------------------------------------

        self.case_id_input = QLineEdit()

        self.case_id_input.setPlaceholderText(
            "Example: CASE-001"
        )

        self.case_id_input.setObjectName(
            "inputField"
        )

        create_layout.addWidget(
            self.case_id_input
        )


        # ----------------------------------------------------
        # CASE TITLE
        # ----------------------------------------------------

        self.case_title_input = QLineEdit()

        self.case_title_input.setPlaceholderText(
            "Investigation title"
        )

        self.case_title_input.setObjectName(
            "inputField"
        )

        create_layout.addWidget(
            self.case_title_input
        )


        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        self.case_description_input = QLineEdit()

        self.case_description_input.setPlaceholderText(
            "Short case description"
        )

        self.case_description_input.setObjectName(
            "inputField"
        )

        create_layout.addWidget(
            self.case_description_input
        )


        # ----------------------------------------------------
        # CREATE BUTTON
        # ----------------------------------------------------

        create_button = QPushButton(
            "CREATE CASE"
        )

        create_button.setObjectName(
            "primaryButton"
        )

        create_button.clicked.connect(
            self.create_case
        )

        create_layout.addWidget(
            create_button
        )

        self.body.addWidget(
            create_panel
        )


        # ----------------------------------------------------
        # CASE LIST
        # ----------------------------------------------------

        list_panel = QFrame()

        list_panel.setObjectName(
            "panel"
        )

        list_layout = QVBoxLayout(
            list_panel
        )

        list_layout.setContentsMargins(
            22,
            20,
            22,
            20,
        )

        list_title = QLabel(
            "INVESTIGATION CASES"
        )

        list_title.setObjectName(
            "sectionTitle"
        )

        list_layout.addWidget(
            list_title
        )


        self.case_list = QListWidget()

        self.case_list.setObjectName(
            "reportList"
        )

        self.case_list.itemClicked.connect(
            self.select_case
        )

        list_layout.addWidget(
            self.case_list
        )

        self.body.addWidget(
            list_panel
        )


        # ----------------------------------------------------
        # SELECTED CASE PANEL
        # ----------------------------------------------------

        self.details_panel = QFrame()

        self.details_panel.setObjectName(
            "panel"
        )

        details_layout = QVBoxLayout(
            self.details_panel
        )

        details_layout.setContentsMargins(
            22,
            20,
            22,
            20,
        )

        details_title = QLabel(
            "CASE DETAILS"
        )

        details_title.setObjectName(
            "sectionTitle"
        )

        details_layout.addWidget(
            details_title
        )


        self.case_details_label = QLabel(
            "Select a case to view details."
        )

        self.case_details_label.setObjectName(
            "panelText"
        )

        self.case_details_label.setWordWrap(
            True
        )

        details_layout.addWidget(
            self.case_details_label
        )


        # ----------------------------------------------------
        # EVIDENCE BUTTON
        # ----------------------------------------------------

        self.add_evidence_button = QPushButton(
            "ADD EVIDENCE"
        )

        self.add_evidence_button.setObjectName(
            "secondaryButton"
        )

        self.add_evidence_button.setEnabled(
            False
        )

        self.add_evidence_button.clicked.connect(
            self.add_evidence
        )

        details_layout.addWidget(
            self.add_evidence_button
        )


        self.body.addWidget(
            self.details_panel
        )


    # ========================================================
    # LOAD CASES
    # ========================================================

    def load_cases(self):

        self.case_list.clear()

        cases = CaseManager.list_cases()

        if not cases:

            item = QListWidgetItem(
                "NO CASES CREATED"
            )

            self.case_list.addItem(
                item
            )

            return


        for case in cases:

            case_id = case.get(
                "case_id",
                "UNKNOWN",
            )

            title = case.get(
                "title",
                "Untitled Investigation",
            )

            status = case.get(
                "status",
                "OPEN",
            )

            text = (
                f"{case_id}    |    "
                f"{title}    |    "
                f"{status}"
            )

            item = QListWidgetItem(
                text
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                case_id,
            )

            self.case_list.addItem(
                item
            )


    # ========================================================
    # CREATE CASE
    # ========================================================

    def create_case(self):

        case_id = (
            self.case_id_input.text()
            .strip()
        )

        title = (
            self.case_title_input.text()
            .strip()
        )

        description = (
            self.case_description_input.text()
            .strip()
        )


        if not case_id:

            QMessageBox.warning(
                self,
                "Case Required",
                "Please enter a Case ID.",
            )

            return


        if not title:

            title = (
                "Investigation "
                + case_id
            )


        try:

            CaseManager.create_case(
                case_id,
                title,
                description,
            )

        except FileExistsError:

            QMessageBox.warning(
                self,
                "Case Exists",
                f"Case {case_id} already exists.",
            )

            return

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Case Creation Failed",
                str(exc),
            )

            return


        self.case_id_input.clear()
        self.case_title_input.clear()
        self.case_description_input.clear()


        self.load_cases()


        QMessageBox.information(
            self,
            "Case Created",
            f"Case {case_id} created successfully.",
        )


    # ========================================================
    # SELECT CASE
    # ========================================================

    def select_case(self, item):

        case_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not case_id:
            return


        self.current_case_id = case_id

        case = CaseManager.get_case(
            case_id
        )

        if case is None:
            return


        evidence = CaseManager.get_evidence(
            case_id
        )

        reports = CaseManager.get_reports(
            case_id
        )


        details = (
            f"CASE ID: {case.get('case_id')}\n"
            f"TITLE: {case.get('title')}\n"
            f"STATUS: {case.get('status')}\n"
            f"CREATED: {case.get('created_at', '')}\n"
            f"EVIDENCE FILES: {len(evidence)}\n"
            f"REPORTS: {len(reports)}\n"
            f"ANALYSES: {len(case.get('analyses', []))}\n\n"
            f"DESCRIPTION:\n"
            f"{case.get('description', '')}"
        )


        self.case_details_label.setText(
            details
        )

        self.add_evidence_button.setEnabled(
            True
        )


    # ========================================================
    # ADD EVIDENCE
    # ========================================================

    def add_evidence(self):

        if not self.current_case_id:

            return


        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Evidence File",
            "",
            "All Files (*.*)",
        )


        if not file_path:
            return


        try:

            destination = CaseManager.add_evidence(
                self.current_case_id,
                file_path,
            )

            self.select_case(
                self.case_list.currentItem()
            )

            QMessageBox.information(
                self,
                "Evidence Added",
                (
                    "Evidence added successfully.\n\n"
                    f"Stored as:\n{destination}"
                ),
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Evidence Error",
                str(exc),
            )


# ============================================================
# ENGINE PROCESS WORKER
# ============================================================

class EngineProcessWorker(QThread):
    finished = Signal(bool, str)

    def __init__(self, process, engine_name, case_id, input_file, parent=None):
        super().__init__(parent)
        self.process = process
        self.engine_name = engine_name
        self.case_id = case_id
        self.input_file = input_file

    def run(self):
        try:
            stdout, stderr = self.process.communicate()
            return_code = self.process.returncode

            if return_code == 0:
                message = f"{self.engine_name} analysis completed successfully.\n\nCase ID: {self.case_id}\nInput: {self.input_file}\n\nThe investigation results have been generated."
                self.finished.emit(True, message)
            else:
                error_text = stderr.strip()
                if not error_text:
                    error_text = f"{self.engine_name} exited with code {return_code}."
                self.finished.emit(False, error_text)

        except Exception as error:
            self.finished.emit(False, str(error))

# ============================================================
# AI INSIGHT WORKER (runs on a background thread, never the UI thread)
# ============================================================

class AIInsightWorker(QThread):

    finished = Signal(bool, str)

    def __init__(self, engine_name, case_id, findings_summary, model_tier, parent=None):
        super().__init__(parent)
        self.engine_name = engine_name
        self.case_id = case_id
        self.findings_summary = findings_summary
        self.model_tier = model_tier

    def run(self):
        success, text = ai_insights.analyze_report(
            self.engine_name,
            self.case_id,
            self.findings_summary,
            self.model_tier,
        )
        self.finished.emit(success, text)


# ============================================================
# REPORTS PAGE
# ============================================================

class ReportsPage(InvestigationPage):
    SUPPORTED_REPORTS = {
        ".pdf": "PDF",
        ".txt": "TXT",
        ".xlsx": "XLSX",
        ".csv": "CSV",
        ".json": "JSON",
    }

    def __init__(self, parent=None):
        super().__init__(
            "Investigation Reports",
            "Central repository for generated investigation reports.",
            parent,
        )

        # User reports folder - AppData me
        USER_DATA_DIR = Path.home() / "AppData" / "Local" / "CyberTools Suite"
        USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.reports_root = USER_DATA_DIR / "reports"
        self.reports_root.mkdir(parents=True, exist_ok=True)

        self.build_reports_page()

    # ========================================================
    # BUILD REPORTS PAGE
    # ========================================================

    def build_reports_page(self):

        header_panel = QFrame()
        header_panel.setObjectName("panel")

        header_layout = QHBoxLayout(header_panel)
        header_layout.setContentsMargins(
            22, 18, 22, 18
        )
        header_layout.setSpacing(12)

        title = QLabel("REPORT REPOSITORY")
        title.setObjectName("sectionTitle")

        self.report_count = QLabel("0 REPORTS")
        self.report_count.setObjectName("reportCount")

        refresh_button = QPushButton("REFRESH")
        refresh_button.setObjectName("secondaryButton")

        refresh_button.clicked.connect(
            self.load_reports
        )

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.report_count)
        header_layout.addWidget(refresh_button)

        self.body.addWidget(header_panel)

        # ----------------------------------------------------
        # REPORT LIST
        # ----------------------------------------------------

        self.report_list = QListWidget()

        self.report_list.setObjectName(
            "reportList"
        )

        self.report_list.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.report_list.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.report_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.report_list.setSpacing(8)

        self.body.addWidget(
            self.report_list,
            1,
        )

        self.load_reports()

    # ========================================================
    # LOAD REPORTS
    # ========================================================

    def load_reports(self):
        """Load ALL generated reports from the central report index —
        chahe woh kahi bhi save hui ho (case folder, global reports
        folder, ya koi bhi custom folder jo user ne choose kiya ho)."""

        self.report_list.clear()

        from ui.report_index import ReportIndex
        entries = ReportIndex.get_all()

        self.report_count.setText(f"{len(entries)} REPORTS")

        if not entries:
            empty_item = QListWidgetItem()
            empty_widget = QFrame()
            empty_widget.setObjectName("emptyReport")
            empty_widget.setMinimumHeight(120)
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setContentsMargins(30, 40, 30, 40)
            empty_layout.setSpacing(12)

            empty_title = QLabel("NO REPORTS AVAILABLE")
            empty_title.setObjectName("emptyReportTitle")
            empty_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            empty_text = QLabel("Generated investigation reports will appear here automatically.")
            empty_text.setObjectName("emptyReportText")
            empty_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_text.setWordWrap(True)

            empty_layout.addWidget(empty_title, alignment=Qt.AlignmentFlag.AlignCenter)
            empty_layout.addWidget(empty_text, alignment=Qt.AlignmentFlag.AlignCenter)

            empty_widget.adjustSize()
            empty_item.setSizeHint(QSize(0, empty_widget.sizeHint().height()))
            self.report_list.addItem(empty_item)
            self.report_list.setItemWidget(empty_item, empty_widget)
            return

        for entry in entries:
            file_path = Path(entry["path"])
            if not file_path.exists():
                continue
            item = QListWidgetItem()
            report_widget = self.create_report_card(file_path, str(file_path))
            report_widget.adjustSize()
            item.setSizeHint(QSize(0, 105))
            self.report_list.addItem(item)
            self.report_list.setItemWidget(item, report_widget)

    # ========================================================
    # REPORT CARD
    # ========================================================

    def create_report_card(
        self,
        file_path,
        relative_path,
    ):

        card = QFrame()

        card.setObjectName(
            "reportCard"
        )

        card.setMinimumHeight(
            105
        )

        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout = QHBoxLayout(
            card
        )

        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        layout.setSpacing(
            16
        )

        extension = file_path.suffix.lower()

        type_label = QLabel(
            extension.replace(
                ".",
                ""
            ).upper()
        )

        type_label.setObjectName(
            "reportType"
        )

        type_label.setFixedWidth(
            60
        )

        type_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            type_label
        )

        info_layout = QVBoxLayout()

        info_layout.setSpacing(
            5
        )

        name_label = QLabel(
            file_path.name
        )

        name_label.setObjectName(
            "reportName"
        )

        name_label.setWordWrap(
            True
        )

        folder_label = QLabel(
            f"Location: {relative_path}"
        )

        folder_label.setObjectName(
            "reportFolder"
        )

        folder_label.setWordWrap(
            True
        )

        modified_time = datetime.fromtimestamp(
            file_path.stat().st_mtime
        )

        time_label = QLabel(
            "Generated: "
            + modified_time.strftime(
                "%d %b %Y  %H:%M"
            )
        )

        time_label.setObjectName(
            "reportTime"
        )

        size_kb = (
            file_path.stat().st_size
            / 1024
        )

        size_label = QLabel(
            f"Size: {size_kb:.1f} KB"
        )

        size_label.setObjectName(
            "reportSize"
        )

        info_layout.addWidget(
            name_label
        )

        info_layout.addWidget(
            folder_label
        )

        info_layout.addWidget(
            time_label
        )

        info_layout.addWidget(
            size_label
        )

        layout.addLayout(
            info_layout,
            1
        )

        open_button = QPushButton(
            "OPEN"
        )

        open_button.setObjectName(
            "secondaryButton"
        )

        open_button.setFixedWidth(
            65
        )

        open_button.clicked.connect(
            lambda checked=False, path=file_path:
            self.open_report(path)
        )

        layout.addWidget(
            open_button
        )

        return card

    # ========================================================
    # OPEN REPORT
    # ========================================================

    def open_report(self, file_path):

        if not file_path.exists():
            return

        try:

            if sys.platform.startswith("win"):

                os.startfile(
                    str(file_path)
                )

            elif sys.platform == "darwin":

                subprocess.Popen(
                    ["open", str(file_path)]
                )

            else:

                subprocess.Popen(
                    ["xdg-open", str(file_path)]
                )

        except Exception as exc:

            print(
                f"[Reports] Unable to open report: {exc}"
            )            

# ============================================================
# MAIN WINDOW
# ============================================================

class CyberToolsWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CyberTools Suite")
        self.resize(1400, 850)
        self.setMinimumSize(1100, 700)

        self.pages = {}
        self.animation = None

        self.build_ui()
        self.apply_theme()

    # ========================================================
    # BUILD UI
    # ========================================================

    def run_engine(
        self,
        engine_name,
        workspace,
        case_id,
        input_file,
        output_dir,
    ):

        success, result = EngineRunner.run(
            engine_name=engine_name,
            case_id=case_id,
            input_file=input_file,
            output_dir=output_dir,
        )

        if not success:

            workspace.analysis_finished(
                False,
                str(result),
            )

            return

        # 🔥 Ab result ek pura context dict hai (process bhi usi ke andar hai)
        context = result
        process = context["process"]

        workspace.set_status(
            "ANALYSIS RUNNING",
            "running",
        )

        workspace.result_label.setText(
            f"{engine_name} is currently processing...\n\n"
            f"Case ID: {case_id}\n"
            f"Input: {input_file}"
        )

        worker = EngineProcessWorker(
            process=process,
            engine_name=engine_name,
            case_id=case_id,
            input_file=input_file,
        )

        worker.finished.connect(
            lambda success, message:
            self.engine_finished(
                workspace,
                success,
                message,
                context,
            )
        )

        worker.finished.connect(
            worker.deleteLater
        )

        self._engine_worker = worker

        worker.start()

    def engine_finished(
        self,
        workspace,
        success,
        message,
        context=None,
    ):

        # 🔥 Engine successfully complete hone par uske reports ko
        # ReportIndex me register karo — chahe woh case folder me
        # ho, global reports folder me ho, ya user ke chune hue
        # kisi bhi custom folder me ho.
        if success and context:

            try:

                EngineRunner.finalize_run(context)

            except Exception as exc:

                print(
                    f"[Dashboard] Unable to finalize reports: {exc}"
                )

        workspace.analysis_finished(
            success,
            message,
        )    

    def build_ui(self):

        root = QWidget()
        self.setCentralWidget(root)

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ----------------------------------------------------
        # SIDEBAR
        # ----------------------------------------------------

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 24, 20, 20)
        sidebar_layout.setSpacing(8)

        logo_path = BASE_DIR / "assets" / "logo.png"

        if logo_path.exists():

            logo_label = QLabel()
            logo_pixmap = QPixmap(str(logo_path))

            logo_label.setPixmap(
                logo_pixmap.scaledToHeight(
                    110,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sidebar_layout.addWidget(logo_label)
            sidebar_layout.addSpacing(15)

        brand = QLabel("CYBERTOOLS SUITE")
        brand.setObjectName("brand")

        brand_subtitle = QLabel("INVESTIGATION PLATFORM")
        brand_subtitle.setObjectName("brandSubtitle")

        sidebar_layout.addWidget(brand)
        sidebar_layout.addWidget(brand_subtitle)
        sidebar_layout.addSpacing(30)

        self.navigation = QListWidget()
        self.navigation.setObjectName("navigation")

        menu_items = [
            "Dashboard",
            "CDR Analyzer",
            "Log Analyzer",
            "FinTrack",
            "Case Management",
            "Reports",
            "Settings",
        ]

        for menu_name in menu_items:

            item = QListWidgetItem(menu_name)
            item.setData(
                Qt.ItemDataRole.UserRole,
                menu_name,
            )

            self.navigation.addItem(item)

        self.navigation.currentRowChanged.connect(
            self.change_page
        )

        sidebar_layout.addWidget(self.navigation)
        sidebar_layout.addStretch()

        status_frame = QFrame()
        status_frame.setObjectName("systemStatus")

        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(14, 12, 14, 12)
        status_layout.setSpacing(5)

        status_title = QLabel("SYSTEM STATUS")
        status_title.setObjectName("statusTitle")

        status = QLabel("●  OPERATIONAL")
        status.setObjectName("statusOnline")

        version = QLabel("CyberTools Suite v1.0")
        version.setObjectName("version")

        status_layout.addWidget(status_title)
        status_layout.addWidget(status)
        status_layout.addWidget(version)

        sidebar_layout.addWidget(status_frame)

        # ----------------------------------------------------
        # MAIN AREA
        # ----------------------------------------------------

        main_area = QFrame()
        main_area.setObjectName("mainArea")

        main_layout = QVBoxLayout(main_area)
        main_layout.setContentsMargins(38, 30, 38, 30)
        main_layout.setSpacing(20)

        header = QHBoxLayout()

        self.header_title = QLabel("DASHBOARD")
        self.header_title.setObjectName("headerTitle")

        header.addWidget(self.header_title)
        header.addStretch()

        secure_session = QLabel("SECURE SESSION")
        secure_session.setObjectName("secureSession")

        header.addWidget(secure_session)

        main_layout.addLayout(header)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("separator")

        main_layout.addWidget(separator)

        self.stack = QStackedWidget()
        self.stack.setObjectName("pageStack")

        main_layout.addWidget(self.stack)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(main_area)

        self.create_pages()

        self.navigation.setCurrentRow(0)

    # ========================================================
    # CREATE PAGES
    # ========================================================

    def create_pages(self):

        self.pages["Dashboard"] = DashboardPage()

        self.pages["CDR Analyzer"] = EnginePage(
            engine_name="CDR Analyzer",
            subtitle="Telecom & Call Detail Record Investigation",
            description=(
                "Analyze call records, subscriber relationships, "
                "communication patterns and investigation indicators."
            ),
            extensions=[
                ".csv",
                ".xlsx",
                ".xls",
            ],
        )

        self.pages["CDR Analyzer"].workspace.run_requested.connect(
            lambda case_id, input_file, output_dir:
            self.run_engine(
                "CDR Analyzer",
                self.pages["CDR Analyzer"].workspace,
                case_id,
                input_file,
                output_dir,
            )
        )    
        

        self.pages["Log Analyzer"] = EnginePage(
            engine_name="Log Analyzer",
            subtitle="Security Log Investigation",
            description=(
                "Investigate authentication events, failed attempts, "
                "IP activity and suspicious system behavior."
            ),
            extensions=[
                ".log",
                ".txt",
            ],
        )

        self.pages["Log Analyzer"].workspace.run_requested.connect(
            lambda case_id, input_file, output_dir:
            self.run_engine(
                "Log Analyzer",
                self.pages["Log Analyzer"].workspace,
                case_id,
                input_file,
                output_dir,
            )
        )

        self.pages["FinTrack"] = EnginePage(
            engine_name="FinTrack",
            subtitle="Financial Fraud & Mule Account Analysis",
            description=(
                "Analyze transaction networks, account behavior, "
                "risk indicators and suspicious financial relationships."
            ),
            extensions=[
                ".csv",
                ".xlsx",
                ".xls",
            ],
        )

        self.pages["FinTrack"].workspace.run_requested.connect(
            lambda case_id, input_file, output_dir:
            self.run_engine(
                "FinTrack",
                self.pages["FinTrack"].workspace,
                case_id,
                input_file,
                output_dir,
            )
        )

        for engine_name in ("CDR Analyzer", "Log Analyzer", "FinTrack"):
            self.pages[engine_name].workspace.ai_insight_requested.connect(
                lambda engine, case_id, findings, ws=self.pages[engine_name].workspace:
                self.run_ai_insight(engine, case_id, findings, ws)
            )

        self.pages["Case Management"] = CasePage()
        self.pages["Reports"] = ReportsPage()
        self.pages["Settings"] = SettingsPage()

        for page in self.pages.values():
            self.stack.addWidget(page)

    # ========================================================
    # AI INSIGHTS
    # ========================================================

    def run_ai_insight(self, engine_name, case_id, findings_summary, workspace):

        settings = SettingsManager.load()
        tier = settings.get("ai_model_tier", "auto")

        worker = AIInsightWorker(
            engine_name,
            case_id,
            findings_summary,
            tier,
        )

        worker.finished.connect(
            lambda success, text: workspace.ai_insight_finished(success, text)
        )

        worker.finished.connect(worker.deleteLater)

        self._ai_worker = worker

        worker.start()

    # ========================================================
    # PAGE NAVIGATION
    # ========================================================

    def change_page(self, index):

        if index < 0:
            return

        item = self.navigation.item(index)

        if item is None:
            return

        page_name = item.text()

        if page_name not in self.pages:
            return

        target_page = self.pages[page_name]

        self.header_title.setText(
            page_name.upper()
        )

        self.stack.setCurrentWidget(target_page)

        self.animate_page(target_page)

    # ========================================================
    # PAGE ANIMATION
    # ========================================================

    def animate_page(self, widget):

        opacity_effect = QGraphicsOpacityEffect(widget)

        widget.setGraphicsEffect(
            opacity_effect
        )

        self.animation = QPropertyAnimation(
            opacity_effect,
            b"opacity",
            self,
        )

        self.animation.setDuration(220)

        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)

        self.animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        self.animation.finished.connect(
            lambda: widget.setGraphicsEffect(None)
        )

        self.animation.start()

    # ========================================================
    # THEME
    # ========================================================

    def apply_theme(self):

        apply_global_theme(self)


# ============================================================
# NOTE: Application startup lives in main.py (project root), not here.
# Run `python main.py` from the project root to launch CyberTools Suite.
# ============================================================
