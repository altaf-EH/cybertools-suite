"""
CyberTools Suite - Main Application Entry Point
===================================================
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

# Import UI
from ui.dashboard import CyberToolsWindow
from ui.update_manager import UpdateManager

# Ensure subprocess can find python
if getattr(sys, 'frozen', False):
    # .exe me chal raha hai
    import subprocess
    subprocess.Popen = subprocess.Popen  # No-op, bas ensure karo


def check_for_updates():
    """Check for updates in background."""
    result = UpdateManager.check_for_update()
    
    if result.get("update_available"):
        # Show update dialog
        reply = QMessageBox.question(
            None,
            "Update Available",
            f"A new version ({result['latest_version']}) is available.\n\n"
            f"Would you like to download it?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            import webbrowser
            webbrowser.open(result["release_url"])
    
    return result


def main():
    """Main entry point."""
    
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("CyberTools Suite")
    app.setOrganizationName("CyberTools")
    app.setApplicationVersion("1.1.0")
    
    # Create main window
    window = CyberToolsWindow()
    window.show()
    
    # Check for updates (in background after window shows)
    QTimer.singleShot(2000, check_for_updates)
    
    # Run the app
    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Show error dialog if something goes wrong
        from PySide6.QtWidgets import QApplication, QMessageBox
        import traceback
        
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(
            None,
            "CyberTools Suite - Error",
            f"An unexpected error occurred:\n\n{str(e)}\n\n"
            f"Details:\n{traceback.format_exc()}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()