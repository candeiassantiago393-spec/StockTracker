"""Verificar se o projeto esta pronto para entrega / primeira execucao."""
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
    print("Stock Tracker — verificacao de entrega\n")
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
    run("data/README.md", (ROOT / "data" / "README.md").is_file())
    run("docs/entrega/", (ROOT / "docs" / "entrega" / "README.md").is_file())
    run(
        "config/secrets.example.py",
        (ROOT / "config" / "secrets.example.py").is_file(),
    )
    has_secrets = (ROOT / "config" / "secrets.py").is_file()
    run(
        "config/secrets.py",
        has_secrets,
        "copy config\\secrets.example.py config\\secrets.py",
    )
    run(
        "Word formal",
        (ROOT / "word" / "StockTracker_Documentacao_Projeto.docx").is_file(),
        "python tools\\build_project_docx.py",
    )
    run(
        "Especificacao PT",
        (ROOT / "docs" / "especificacao" / "PROJETO_STOCKTRACKER_PT.md").is_file(),
    )

    stock = ROOT / "data" / "stock.xlsx"
    run(
        "data/stock.xlsx",
        stock.is_file(),
        "criado no primeiro arranque ou copie o seu ficheiro",
    )

    secrets_in_git = False
    gitignore = ROOT / ".gitignore"
    if gitignore.is_file():
        text = gitignore.read_text(encoding="utf-8", errors="ignore")
        secrets_in_git = "secrets.py" in text
    run("secrets.py no .gitignore", secrets_in_git)

    print(f"\n{passed}/{total} verificacoes OK")
    if passed < total:
        print("Corrija os itens [FALTA] antes da entrega.")
        return 1
    print("Projeto pronto para entrega.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
