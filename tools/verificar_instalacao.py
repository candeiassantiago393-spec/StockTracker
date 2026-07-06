"""Verificar instalacao basica do Stock Tracker."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OK = "[OK]"
FAIL = "[FALTA]"


def check(label: str, ok: bool, hint: str = "") -> bool:
    suffix = f" — {hint}" if hint and not ok else ""
    print(f"{OK if ok else FAIL} {label}{suffix}")
    return ok


def main() -> int:
    print("Stock Tracker — verificacao de instalacao\n")
    passed = 0
    total = 0

    def run(label: str, ok: bool, hint: str = "") -> None:
        nonlocal passed, total
        total += 1
        if check(label, ok, hint):
            passed += 1

    run("Python 3.10+", sys.version_info >= (3, 10), sys.version.split()[0])

    for mod in ("PySide6", "openpyxl", "requests"):
        run(f"Modulo {mod}", importlib.util.find_spec(mod) is not None, "pip install -r requirements.txt")

    run("Ambiente .venv", (ROOT / ".venv").is_dir(), "execute INSTALAR.bat")
    run("run.bat", (ROOT / "run.bat").is_file())
    run("src/main.py", (ROOT / "src" / "main.py").is_file())
    run("config/secrets.example.py", (ROOT / "config" / "secrets.example.py").is_file())
    run(
        "config/secrets.py",
        (ROOT / "config" / "secrets.py").is_file(),
        "copy config\\secrets.example.py config\\secrets.py",
    )
    run(
        "Manual do utilizador",
        (ROOT / "docs" / "guias" / "MANUAL_UTILIZADOR.md").is_file(),
    )
    run(
        "data/stock.xlsx",
        (ROOT / "data" / "stock.xlsx").is_file(),
        "criado no primeiro arranque",
    )

    print(f"\n{passed}/{total} verificacoes OK")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
