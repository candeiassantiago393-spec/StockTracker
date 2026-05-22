"""Paths for GUI assets (logos, images)."""
from pathlib import Path

GUI_DIR = Path(__file__).resolve().parent
SIEMENS_TEMPLATE_DIR = GUI_DIR / "siemens_template"


def _resources_dir() -> Path:
    """Works before and after REORGANIZAR_GUI.bat."""
    for base in (SIEMENS_TEMPLATE_DIR, GUI_DIR):
        candidate = base / "resources"
        if candidate.is_dir():
            return candidate
    return SIEMENS_TEMPLATE_DIR / "resources"


RESOURCES_DIR = _resources_dir()
LOGOS_DIR = RESOURCES_DIR / "logos"

# Optional PNG logo (copy from old project if you have it)
ASSETS_DIR = RESOURCES_DIR / "assets"
LOGO_PNG = ASSETS_DIR / "assetssiemens_digital.png"
LOGO_SVG = LOGOS_DIR / "sie-logo-white-rgb.svg"
