from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)


class EngineWorkspace(QWidget):

    run_requested = Signal(str, str, str)
    status_changed = Signal(str)
    ai_insight_requested = Signal(str, str, str)  # engine, case_id, findings

    def __init__(
        self,
        engine_name,
        description,
        supported_extensions=None,
        parent=None,
    ):
        super().__init__(parent)

        self.engine_name = engine_name
        self.description = description
        self.supported_extensions = (
            supported_extensions or ["*"]
        )

        self.build_ui()
        self.apply_style()

    def build_ui(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(18)

        header = QFrame()
        header.setObjectName("workspaceHeader")

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(
            22,
            20,
            22,
            20,
        )

        title = QLabel(self.engine_name)
        title.setObjectName("workspaceTitle")

        description = QLabel(self.description)
        description.setObjectName(
            "workspaceDescription"
        )
        description.setWordWrap(True)

        header_layout.addWidget(title)
        header_layout.addWidget(description)

        root.addWidget(header)

        input_panel = QFrame()
        input_panel.setObjectName("workspacePanel")

        input_layout = QGridLayout(input_panel)
        input_layout.setContentsMargins(
            22,
            22,
            22,
            22,
        )

        case_label = QLabel("CASE ID")
        case_label.setObjectName("fieldLabel")

        self.case_input = QLineEdit()
        self.case_input.setPlaceholderText(
            "Example: CASE-001"
        )
        self.case_input.setObjectName(
            "fieldInput"
        )

        input_layout.addWidget(
            case_label,
            0,
            0,
        )

        input_layout.addWidget(
            self.case_input,
            0,
            1,
            1,
            2,
        )

        file_label = QLabel("INPUT FILE")
        file_label.setObjectName("fieldLabel")

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText(
            "Select investigation input file..."
        )
        self.file_input.setReadOnly(True)
        self.file_input.setObjectName(
            "fieldInput"
        )

        browse_button = QPushButton("BROWSE")
        browse_button.setObjectName(
            "secondaryButton"
        )

        browse_button.clicked.connect(
            self.select_input_file
        )

        input_layout.addWidget(
            file_label,
            1,
            0,
        )

        input_layout.addWidget(
            self.file_input,
            1,
            1,
        )

        input_layout.addWidget(
            browse_button,
            1,
            2,
        )

        output_label = QLabel(
            "OUTPUT DIRECTORY"
        )
        output_label.setObjectName(
            "fieldLabel"
        )

        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText(
            "Optional output directory..."
        )
        self.output_input.setReadOnly(True)
        self.output_input.setObjectName(
            "fieldInput"
        )

        output_button = QPushButton("BROWSE")
        output_button.setObjectName(
            "secondaryButton"
        )

        output_button.clicked.connect(
            self.select_output_directory
        )

        input_layout.addWidget(
            output_label,
            2,
            0,
        )

        input_layout.addWidget(
            self.output_input,
            2,
            1,
        )

        input_layout.addWidget(
            output_button,
            2,
            2,
        )

        root.addWidget(input_panel)

        status_panel = QFrame()
        status_panel.setObjectName(
            "statusPanel"
        )

        status_layout = QHBoxLayout(
            status_panel
        )

        status_caption = QLabel(
            "ENGINE STATUS"
        )
        status_caption.setObjectName(
            "statusCaption"
        )

        self.status_label = QLabel("READY")
        self.status_label.setObjectName(
            "statusReady"
        )

        status_layout.addWidget(
            status_caption
        )

        status_layout.addStretch()

        status_layout.addWidget(
            self.status_label
        )

        root.addWidget(status_panel)

        actions = QHBoxLayout()
        actions.setSpacing(10)

        self.run_button = QPushButton(
            f"RUN {self.engine_name.upper()}"
        )

        self.run_button.setObjectName(
            "primaryButton"
        )

        self.run_button.clicked.connect(
            self.request_run
        )

        clear_button = QPushButton("CLEAR")
        clear_button.setObjectName(
            "secondaryButton"
        )

        clear_button.clicked.connect(
            self.clear_form
        )

        actions.addWidget(
            self.run_button
        )

        actions.addWidget(
            clear_button
        )

        actions.addStretch()

        root.addLayout(actions)

        self.result_panel = QFrame()
        self.result_panel.setObjectName(
            "resultPanel"
        )

        result_layout = QVBoxLayout(
            self.result_panel
        )

        result_title = QLabel(
            "ANALYSIS RESULT"
        )
        result_title.setObjectName(
            "sectionTitle"
        )

        self.result_label = QLabel(
            "No analysis executed yet."
        )

        self.result_label.setObjectName(
            "resultText"
        )

        self.result_label.setWordWrap(True)

        result_layout.addWidget(
            result_title
        )

        result_layout.addWidget(
            self.result_label
        )

        self.ai_button = QPushButton(
            "GET AI INSIGHTS (LOCAL, FREE)"
        )
        self.ai_button.setObjectName(
            "secondaryButton"
        )
        self.ai_button.setEnabled(False)
        self.ai_button.clicked.connect(
            self.request_ai_insight
        )

        result_layout.addWidget(
            self.ai_button
        )

        self.ai_result_label = QLabel("")
        self.ai_result_label.setObjectName(
            "resultText"
        )
        self.ai_result_label.setWordWrap(True)
        self.ai_result_label.hide()

        result_layout.addWidget(
            self.ai_result_label
        )

        root.addWidget(
            self.result_panel
        )

        root.addStretch()

    def select_input_file(self):

        extensions = []

        for extension in (
            self.supported_extensions
        ):

            if extension == "*":
                continue

            extension = extension.replace(
                ".",
                "",
            )

            extensions.append(
                f"*.{extension}"
            )

        if extensions:

            filter_string = (
                "Supported Files ("
                + " ".join(extensions)
                + ")"
            )

        else:

            filter_string = (
                "All Files (*)"
            )

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Investigation Input",
            "",
            filter_string,
        )

        if not path:
            return

        self.file_input.setText(path)

        self.set_status(
            "INPUT SELECTED",
            "selected",
        )

    def select_output_directory(self):

        path = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
        )

        if not path:
            return

        self.output_input.setText(path)

    def request_run(self):

        case_id = self.case_input.text().strip()
        input_file = self.file_input.text().strip()
        output_dir = self.output_input.text().strip()

        if not case_id:
            self.set_status("CASE ID REQUIRED", "error")
            self.case_input.setFocus()
            return

        if not input_file:
            self.set_status("INPUT FILE REQUIRED", "error")
            return

        # File extension check karo
        file_ext = Path(input_file).suffix.lower()
        if self.supported_extensions and file_ext not in self.supported_extensions:
            self.set_status(f"UNSUPPORTED FORMAT: {file_ext}", "error")
            QMessageBox.warning(
                self,
                "Unsupported File Format",
                f"File format '{file_ext}' is not supported.\n\n"
                f"Supported formats: {', '.join(self.supported_extensions)}",
            )
            return

        self.result_label.setText("Analysis process started...")
        self.set_status("ANALYSIS STARTING", "running")
        self.run_button.setEnabled(False)

        self.run_requested.emit(case_id, input_file, output_dir)


    def set_status(
        self,
        text,
        state="ready",
    ):

        self.status_label.setText(text)

        self.status_label.setProperty(
            "statusState",
            state,
        )

        self.status_label.style().unpolish(
            self.status_label
        )

        self.status_label.style().polish(
            self.status_label
        )

        self.status_changed.emit(
            text
        )

    def analysis_finished(
        self,
        success=True,
        message=None,
    ):

        self.run_button.setEnabled(
            True
        )

        if success:

            self.set_status(
                "ANALYSIS COMPLETE",
                "success",
            )

            self.result_label.setText(
                message
                or
                "Analysis completed successfully."
            )

            self.ai_button.setEnabled(True)

        else:

            self.set_status(
                "ANALYSIS FAILED",
                "error",
            )

            self.result_label.setText(
                message
                or
                "Analysis failed. Check the terminal output."
            )

            self.ai_button.setEnabled(False)

    def request_ai_insight(self):

        case_id = self.case_input.text().strip()
        findings_summary = self.result_label.text()

        if not case_id:
            self.set_status("CASE ID REQUIRED", "error")
            self.case_input.setFocus()
            return

        self.ai_button.setEnabled(False)
        self.ai_button.setText("ANALYZING...")

        self.ai_insight_requested.emit(
            self.engine_name,
            case_id,
            findings_summary,
        )

    def ai_insight_finished(self, success, text):

        self.ai_button.setEnabled(True)
        self.ai_button.setText(
            "GET AI INSIGHTS (LOCAL, FREE)"
        )

        self.ai_result_label.setText(
            text if success else f"AI Insights unavailable: {text}"
        )
        self.ai_result_label.show()

    def clear_form(self):

        self.case_input.clear()
        self.file_input.clear()
        self.output_input.clear()

        self.result_label.setText(
            "No analysis executed yet."
        )

        self.run_button.setEnabled(
            True
        )

        self.set_status(
            "READY",
            "ready",
        )

    def apply_style(self):

        self.setStyleSheet("""

        #workspaceHeader {
            background: #0e151e;
            border: 1px solid #1c2937;
            border-radius: 10px;
        }

        #workspaceTitle {
            color: #edf4fb;
            font-size: 20px;
            font-weight: 700;
        }

        #workspaceDescription {
            color: #718094;
            font-size: 11px;
        }

        #workspacePanel {
            background: #0e151e;
            border: 1px solid #1c2937;
            border-radius: 10px;
        }

        #fieldLabel {
            color: #718094;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        #fieldInput {
            background: #080d13;
            color: #dce6f2;
            border: 1px solid #223140;
            border-radius: 6px;
            padding: 10px;
            font-size: 11px;
        }

        #fieldInput:focus {
            border: 1px solid #2684d9;
        }

        #statusPanel {
            background: #0b1219;
            border: 1px solid #1b2835;
            border-radius: 8px;
        }

        #statusCaption {
            color: #68798b;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        #statusReady {
            color: #55a9ff;
            font-size: 10px;
            font-weight: 700;
        }

        #statusReady[statusState="selected"] {
            color: #55a9ff;
        }

        #statusReady[statusState="running"] {
            color: #e6b85c;
        }

        #statusReady[statusState="success"] {
            color: #55d98b;
        }

        #statusReady[statusState="error"] {
            color: #ff7070;
        }

        #primaryButton {
            background: #1677d2;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 11px 20px;
            font-size: 10px;
            font-weight: 700;
        }

        #primaryButton:hover {
            background: #2588e5;
        }

        #primaryButton:pressed {
            background: #0e5ea9;
        }

        #primaryButton:disabled {
            background: #263442;
            color: #66788a;
        }

        #secondaryButton {
            background: #111a24;
            color: #aab8c7;
            border: 1px solid #263646;
            border-radius: 6px;
            padding: 11px 18px;
            font-size: 10px;
            font-weight: 700;
        }

        #secondaryButton:hover {
            background: #182431;
            color: #e1eaf3;
        }

        #resultPanel {
            background: #0e151e;
            border: 1px solid #1c2937;
            border-radius: 10px;
            padding: 5px;
        }

        #resultText {
            color: #7f90a3;
            font-size: 11px;
            padding: 4px;
        }

        #sectionTitle {
            color: #e9f1f8;
            font-size: 14px;
            font-weight: 700;
        }

        """)