"""Regenerate all Qt Designer .ui files from Python builders."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = (
    "generate_stocktracker_ui.py",
    "generate_equipments_ui.py",
    "generate_popup_uis.py",
)


def main() -> None:
    for name in SCRIPTS:
        path = ROOT / "tools" / name
        print(f"Running {name}...")
        subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)
    print("All designer .ui files generated.")


if __name__ == "__main__":
    main()
