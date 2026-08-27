from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QProgressDialog,
)

from ui.settings_manager import SettingsManager
from ui import ai_insights


# ============================================================
# BACKGROUND WORKERS (never block the UI thread)
# ============================================================

class OllamaCheckWorker(QThread):
    finished = Signal(bool, float, bool)  # running, ram_gb, model_installed

    def __init__(self, model_name, parent=None):
        super().__init__(parent)
        self.model_name = model_name

    def run(self):
        running = ai_insights.OllamaClient.is_running()
        ram_gb = ai_insights.detect_ram_gb()
        installed = (
            ai_insights.OllamaClient.has_model(self.model_name)
            if running else False
        )
        self.finished.emit(running, ram_gb, installed)


class ModelDownloadWorker(QThread):
    progress = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, model_name, parent=None):
        super().__init__(parent)
        self.model_name = model_name

    def run(self):
        success, message = ai_insights.OllamaClient.pull_model(
            self.model_name,
            on_progress=lambda text: self.progress.emit(text),
        )
        self.finished.emit(success, message)


# ============================================================
# SETTINGS PAGE
# ============================================================

class SettingsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._download_worker = None
        self._check_worker = None

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(6)

        title = QLabel("Settings")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Configure API access and local AI analysis. Everything "
            "here is optional except where an engine needs it."
        )
        subtitle.setObjectName("pageSubtitle")

        root.addWidget(title)
        root.addWidget(subtitle)
        root.addSpacing(24)

        body = QVBoxLayout()
        body.setSpacing(18)
        root.addLayout(body)
        root.addStretch()

        self.settings = SettingsManager.load()

        body.addWidget(self._build_api_panel())
        body.addWidget(self._build_ai_panel())

    # ========================================================
    # ABUSEIPDB PANEL
    # ========================================================

    def _build_api_panel(self):

        panel = QFrame()
        panel.setObjectName("panel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(10)

        title = QLabel("LOG ANALYZER — ABUSEIPDB API KEY")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        info = QLabel(
            "Used by the Log Analyzer to check IP reputation. Free key: "
            "abuseipdb.com/account/api  (no card required)."
        )
        info.setObjectName("panelText")
        info.setWordWrap(True)
        layout.addWidget(info)

        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Paste your AbuseIPDB API key here")
        self.api_key_input.setText(self.settings.get("abuseipdb_api_key", ""))
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setObjectName("inputField")
        layout.addWidget(self.api_key_input)

        row = QHBoxLayout()

        show_button = QPushButton("SHOW")
        show_button.setObjectName("secondaryButton")
        show_button.setCheckable(True)
        show_button.toggled.connect(self._toggle_key_visibility)

        save_button = QPushButton("SAVE KEY")
        save_button.setObjectName("primaryButton")
        save_button.clicked.connect(self._save_api_key)

        row.addWidget(show_button)
        row.addWidget(save_button)
        row.addStretch()

        layout.addLayout(row)

        return panel

    def _toggle_key_visibility(self, checked):
        self.api_key_input.setEchoMode(
            QLineEdit.EchoMode.Normal if checked
            else QLineEdit.EchoMode.Password
        )

    def _save_api_key(self):
        api_key = self.api_key_input.text().strip()
        
        if not api_key:
            QMessageBox.warning(
                self,
                "API Key Required",
                "Please enter an AbuseIPDB API key. If you don't have one, "
                "you can leave it blank - Log Analyzer will work without "
                "AbuseIPDB enrichment, but IP reputation checks won't be available.",
            )
            return

        self.settings["abuseipdb_api_key"] = api_key
        SettingsManager.save(self.settings)

        QMessageBox.information(
            self,
            "Saved",
            "AbuseIPDB key saved successfully. It will be used the next time "
            "Log Analyzer runs.",
        )

    # ========================================================
    # AI PANEL
    # ========================================================

    def _build_ai_panel(self):

        panel = QFrame()
        panel.setObjectName("panel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(10)

        title = QLabel("AI INSIGHTS — LOCAL, FREE, NO API KEY")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        info = QLabel(
            "Runs entirely on this PC via Ollama. No internet needed "
            "once the model is downloaded, no per-use cost, and no data "
            "ever leaves this machine."
        )
        info.setObjectName("panelText")
        info.setWordWrap(True)
        layout.addWidget(info)

        self.ai_enabled_checkbox = QCheckBox("Enable AI Insights")
        self.ai_enabled_checkbox.setChecked(
            bool(self.settings.get("ai_enabled", False))
        )
        layout.addWidget(self.ai_enabled_checkbox)

        tier_row = QHBoxLayout()

        tier_label = QLabel("Model quality:")
        tier_label.setObjectName("fieldLabel")

        self.tier_dropdown = QComboBox()
        self.tier_dropdown.addItem(
            "Auto (recommended for this PC)", "auto"
        )
        for key, tier in ai_insights.MODEL_TIERS.items():
            self.tier_dropdown.addItem(tier["label"], key)

        current_tier = self.settings.get("ai_model_tier", "auto")
        index = self.tier_dropdown.findData(current_tier)
        if index >= 0:
            self.tier_dropdown.setCurrentIndex(index)

        tier_row.addWidget(tier_label)
        tier_row.addWidget(self.tier_dropdown, 1)

        layout.addLayout(tier_row)

        self.hardware_label = QLabel("Checking this PC's hardware...")
        self.hardware_label.setObjectName("panelText")
        layout.addWidget(self.hardware_label)

        self.status_label = QLabel("Status: checking Ollama...")
        self.status_label.setObjectName("statusReady")
        layout.addWidget(self.status_label)

        button_row = QHBoxLayout()

        save_ai_button = QPushButton("SAVE AI SETTINGS")
        save_ai_button.setObjectName("primaryButton")
        save_ai_button.clicked.connect(self._save_ai_settings)

        recheck_button = QPushButton("RECHECK STATUS")
        recheck_button.setObjectName("secondaryButton")
        recheck_button.clicked.connect(self._run_check)

        self.download_button = QPushButton("DOWNLOAD MODEL")
        self.download_button.setObjectName("secondaryButton")
        self.download_button.clicked.connect(self._start_download)
        self.download_button.setVisible(False)  # Hide this button

        button_row.addWidget(save_ai_button)
        button_row.addWidget(recheck_button)
        button_row.addWidget(self.download_button)
        button_row.addStretch()

        layout.addLayout(button_row)

        install_note = QLabel(
            "AI Insights requires Ollama. Install it from https://ollama.com\n"
            "(free, ~1 minute), then click Recheck Status.\n\n"
            "Note: Download Model button is hidden - install Ollama first,\n"
            "then it will work automatically."
        )
        install_note.setObjectName("panelText")
        install_note.setWordWrap(True)
        layout.addWidget(install_note)

        self._run_check()

        return panel

    def _current_tier_key(self):
        preference = self.tier_dropdown.currentData()
        ram_gb = ai_insights.detect_ram_gb()
        resolved = ai_insights.resolve_tier(preference, ram_gb)
        return resolved

    def _current_model_name(self):
        tier = self._current_tier_key()
        if tier is None:
            return None
        return ai_insights.MODEL_TIERS[tier]["model"]

    def _save_ai_settings(self):
        self.settings["ai_enabled"] = self.ai_enabled_checkbox.isChecked()
        self.settings["ai_model_tier"] = self.tier_dropdown.currentData()
        SettingsManager.save(self.settings)

        QMessageBox.information(
            self,
            "Saved",
            "AI Insights settings saved.",
        )

    def _run_check(self):
        ram_gb = ai_insights.detect_ram_gb()

        self.hardware_label.setText(
            f"Detected RAM: {ram_gb} GB"
        )

        model_name = self._current_model_name()

        if model_name is None:
            self.status_label.setText(
                "Status: this PC's RAM is below the minimum for local AI."
            )
            self.download_button.setEnabled(False)
            return

        self.status_label.setText("Status: checking Ollama...")
        self.download_button.setEnabled(False)

        self._check_worker = OllamaCheckWorker(model_name)
        self._check_worker.finished.connect(self._on_check_finished)
        self._check_worker.start()

    def _on_check_finished(self, running, ram_gb, installed):

        if not running:
            self.status_label.setText(
                "Status: Ollama not detected. Install it from ollama.com."
            )
            self.download_button.setEnabled(False)
            return

        if installed:
            self.status_label.setText(
                "Status: Ollama running, model ready. AI Insights is good to go."
            )
            self.download_button.setEnabled(False)
        else:
            self.status_label.setText(
                "Status: Ollama running, model not downloaded yet."
            )
            self.download_button.setEnabled(True)

    def _start_download(self):
        model_name = self._current_model_name()

        if not model_name:
            return

        # Check if Ollama is running
        if not ai_insights.OllamaClient.is_running():
            QMessageBox.warning(
                self,
                "Ollama Not Running",
                "Ollama is not installed or not running on this PC.\n\n"
                "Please install Ollama from https://ollama.com first,\n"
                "then click 'Recheck Status' and try again.",
            )
            return

        self.download_button.setEnabled(False)
        self.status_label.setText(f"Downloading {model_name}... 0%")

        # Progress dialog show karo
        self.progress_dialog = QProgressDialog(
            f"Downloading {model_name}...",
            "Cancel",
            0, 0, self
        )
        self.progress_dialog.setWindowTitle("Downloading Model")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        self.progress_dialog.show()

        self._download_worker = ModelDownloadWorker(model_name)
        self._download_worker.progress.connect(self._on_download_progress)
        self._download_worker.finished.connect(self._on_download_finished)
        self._download_worker.start()

    def _on_download_progress(self, text):
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.setLabelText(f"Downloading: {text}")    

    def _on_download_finished(self, success, message):
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

        if success:
            self.status_label.setText(
                "Status: model downloaded. AI Insights is good to go."
            )
            self.download_button.setEnabled(False)
        else:
            self.status_label.setText(f"Download failed: {message}")
            self.download_button.setEnabled(True)
