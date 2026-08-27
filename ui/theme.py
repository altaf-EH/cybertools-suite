"""
CyberTools Suite - Centralized Theme
=====================================
Every color, font-size and QSS rule lives here. Import COLORS for use in
custom-drawn widgets (icons, charts, badges) and MAIN_STYLESHEET / apply
it once on the QMainWindow. Extending the app (new pages, new widgets)
should mean adding QSS here, not scattering inline setStyleSheet() calls
across files.
"""

# ============================================================
# COLOR PALETTE
# ============================================================

COLORS = {
    "bg_root": "#080c12",
    "bg_panel": "#0e151e",
    "bg_panel_alt": "#0b121a",
    "bg_sidebar": "#0b1119",
    "bg_input": "#080d13",
    "border": "#1c2937",
    "border_light": "#263646",
    "border_focus": "#2684d9",
    "accent": "#1677d2",
    "accent_hover": "#2588e5",
    "accent_pressed": "#0e5ea9",
    "accent_text": "#55a9ff",
    "text_primary": "#edf4fb",
    "text_secondary": "#dce6f2",
    "text_muted": "#78889a",
    "text_faint": "#5f7185",
    "success": "#55d98b",
    "warning": "#e6b85c",
    "error": "#ff7070",
}


# ============================================================
# MAIN STYLESHEET
# ============================================================

MAIN_STYLESHEET = """


        QMainWindow {
            background: #080c12;
        }

        QWidget {
            font-family: "Segoe UI";
            color: #dce6f2;
        }

        #sidebar {
            background: #0b1119;
            border-right: 1px solid #1b2735;
        }

        #brand {
            color: #55a9ff;
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 2px;
        }

        #brandSubtitle {
            color: #68788b;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1.5px;
        }
        #brandSubtitle {
            color: #68788b;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1.5px;
        }

        #navigation {
            background: transparent;
            border: none;
            outline: none;
        }

        #navigation::item {
            color: #8d9bad;
            padding: 13px 14px;
            margin: 2px 0;
            border-radius: 7px;
            font-size: 13px;
        }

        #navigation::item:hover {
            background: #131d29;
            color: #dce6f2;
        }

        #navigation::item:selected {
            background: #15283b;
            color: #55a9ff;
            border-left: 3px solid #3291ff;
        }

        #systemStatus {
            background: #0f1822;
            border: 1px solid #1c2b3a;
            border-radius: 8px;
        }

        #statusTitle {
            color: #637387;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        #statusOnline {
            color: #54d68a;
            font-size: 11px;
            font-weight: 700;
        }

        #version {
            color: #566577;
            font-size: 9px;
        }

        #mainArea {
            background: #080c12;
        }

        #headerTitle {
            color: #edf4fb;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        #secureSession {
            color: #55c98a;
            font-size: 10px;
            font-weight: 700;
            padding: 7px 12px;
            border: 1px solid #214e39;
            border-radius: 6px;
        }

        #separator {
            background: #17212d;
            max-height: 1px;
        }

        #pageTitle {
            color: #edf4fb;
            font-size: 28px;
            font-weight: 700;
        }

        #pageSubtitle {
            color: #718094;
            font-size: 12px;
        }

        #statCard {
            background: #0e151e;
            border: 1px solid #1c2937;
            border-radius: 10px;
            min-height: 135px;
        }

        #statCard:hover {
            border: 1px solid #2b4258;
        }

        #statTitle {
            color: #647487;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        #statValue {
            color: #edf4fb;
            font-size: 27px;
            font-weight: 700;
        }

        #statDescription {
            color: #657487;
            font-size: 10px;
        }

        #panel {
            background: #0e151e;
            border: 1px solid #1c2937;
            border-radius: 10px;
        }

        #inputField {
            background: #080d13;
            color: #dce6f2;
            border: 1px solid #223140;
            border-radius: 6px;
            padding: 11px 12px;
            font-size: 12px;
        }

        #inputField:focus {
            border: 1px solid #2684d9;
        }

        #sectionTitle {
            color: #e9f1f8;
            font-size: 15px;
            font-weight: 700;
        }

        #panelText {
            color: #78889a;
            font-size: 12px;
        }

        #activityRow {
            background: #0b121a;
            border: 1px solid #172432;
            border-radius: 6px;
        }

        #activityRow:hover {
            background: #101b27;
            border: 1px solid #26394c;
        }

        #activityName {
            color: #cbd6e2;
            font-size: 11px;
        }

        #activityTime {
            color: #5f7185;
            font-size: 10px;
        }

                #caseList,
        #reportList {
            background: #0b121a;
            border: 1px solid #1c2937;
            border-radius: 8px;
            outline: none;
            padding: 6px;
        }

        #caseList::item,
        #reportList::item {
            color: #aebdcd;
            padding: 13px 12px;
            margin: 2px;
            border-radius: 6px;
        }

        #caseList::item:hover,
        #reportList::item:hover {
            background: #121f2c;
            color: #e6eef7;
        }

        #caseList::item:selected,
        #reportList::item:selected {
            background: #15283b;
            color: #55a9ff;
        }

        #primaryButton {
            background: #1677d2;
            color: white;
            border: none;
            border-radius: 7px;
            padding: 10px 18px;
            font-size: 11px;
            font-weight: 700;
        }

        #primaryButton:hover {
            background: #2188e8;
        }

        #primaryButton:pressed {
            background: #1265b3;
        }

        #secondaryButton {
            background: #101b27;
            color: #9db0c4;
            border: 1px solid #26384a;
            border-radius: 7px;
            padding: 9px 15px;
            font-size: 10px;
            font-weight: 700;
        }

        #secondaryButton:hover {
            background: #162535;
            color: #dce8f3;
        }

                # ====================================================
        # REPORTS
        # ====================================================

        #reportCount {
            color: #55a9ff;
            font-size: 10px;
            font-weight: 700;
            padding: 6px 10px;
            border: 1px solid #244563;
            border-radius: 5px;
        }

        #reportList {
            background: transparent;
            border: none;
            outline: none;
        }

        #reportList::item {
            background: transparent;
            border: none;
            padding: 4px 0;
        }

        #reportCard {
            background: #0e151e;
            border: 1px solid #1c2937;
            border-radius: 9px;
            min-height: 78px;
        }

        #reportCard:hover {
            background: #111c28;
            border: 1px solid #2a4258;
        }

        #reportType {
            background: #142538;
            color: #55a9ff;
            border: 1px solid #244563;
            border-radius: 5px;
            font-size: 9px;
            font-weight: 800;
        }

        #reportName {
            color: #dce6f2;
            font-size: 12px;
            font-weight: 700;
        }

        #reportFolder {
            color: #65778b;
            font-size: 10px;
        }

        #reportTime {
            color: #526477;
            font-size: 9px;
        }

        #emptyReport {
            background: #0e151e;
            border: 1px dashed #253545;
            border-radius: 9px;
            min-height: 130px;
        }

        #emptyReportTitle {
            color: #8c9bad;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        #emptyReportText {
            color: #596a7d;
            font-size: 10px;
        }

        #secondaryButton {
            background: #111d29;
            color: #8fb7dc;
            border: 1px solid #263b50;
            border-radius: 5px;
            padding: 7px 14px;
            font-size: 9px;
            font-weight: 700;
        }

        #secondaryButton:hover {
            background: #17283a;
            color: #55a9ff;
            border: 1px solid #345777;
        }

        #secondaryButton:pressed {
            background: #0d1721;
        }

                #caseList {
            background: transparent;
            border: none;
            outline: none;
        }

        #caseList::item {
            background: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        }

        #caseList::item:selected {
            background: transparent;
        }

        #caseList::item:hover {
            background: transparent;
        }

        #primaryButton {
            background: #15283b;
            color: #55a9ff;
            border: 1px solid #265278;
            border-radius: 6px;
            padding: 8px 14px;
            font-size: 10px;
            font-weight: 700;
        }

        #primaryButton:hover {
            background: #1b344b;
            border: 1px solid #3291ff;
        }

        #primaryButton:pressed {
            background: #102333;
        }

        
"""


def apply_theme(window):
    """Apply the CyberTools Suite theme to any QMainWindow / QWidget."""
    window.setStyleSheet(MAIN_STYLESHEET)
