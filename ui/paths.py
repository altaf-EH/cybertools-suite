from pathlib import Path
from ui.settings_manager import SettingsManager

DEFAULT_DATA_DIR = Path.home() / "Documents" / "CyberTools Suite"

# App ki apni internal bookkeeping files (index, cache) hamesha yahi
# fixed jagah rahengi — user jo bhi case-folder select kare, uska
# isse koi lena dena nahi. Kabhi Desktop/user-chosen folder me nahi jaayegi.
INTERNAL_DIR = Path.home() / "AppData" / "Local" / "CyberTools Suite"


def get_data_dir():
    """User ke Cases/Evidence kaha save honge, ye decide karta hai.
    Settings se custom folder choose kiya ho to wahi, warna default Documents."""

    settings = SettingsManager.load()
    custom_path = settings.get("data_directory", "").strip()

    if custom_path:
        data_dir = Path(custom_path)
    else:
        data_dir = DEFAULT_DATA_DIR

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_internal_dir():
    """App ki apni internal files (report index, cache) — user ke
    chune hue folder me kabhi nahi jaati, hamesha fixed jagah rehti hai."""

    INTERNAL_DIR.mkdir(parents=True, exist_ok=True)
    return INTERNAL_DIR