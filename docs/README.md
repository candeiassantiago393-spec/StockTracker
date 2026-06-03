# Documentation — Stock Tracker

English documentation for developers and operators. Detailed guides are under [`user/`](user/).

## Specification

| Document | Content |
|----------|---------|
| [PROJETO_STOCKTRACKER.md](PROJETO_STOCKTRACKER.md) | Product specification (English, Siemens-style) |
| [PROJETO_STOCKTRACKER_PT.md](PROJETO_STOCKTRACKER_PT.md) | Same specification in Portuguese (optional) |

## User guides (`docs/user/`)

| Document | Content |
|----------|---------|
| [user/COMMANDS.md](user/COMMANDS.md) | Install, run, troubleshooting |
| [user/REPOSITORY_LAYOUT.md](user/REPOSITORY_LAYOUT.md) | Repository structure and key files |
| [user/ARCHITECTURE.md](user/ARCHITECTURE.md) | Architecture and data flows |
| [user/SUPPLIERS.md](user/SUPPLIERS.md) | Supplier APIs and credentials |
| [user/DIGIKEY_SETUP.md](user/DIGIKEY_SETUP.md) | DigiKey sandbox setup |
| [user/QT_DESIGNER.md](user/QT_DESIGNER.md) | Qt Designer workflow |
| [user/GITHUB.md](user/GITHUB.md) | GitHub publishing |
| [user/IDE_SETUP.md](user/IDE_SETUP.md) | VS Code / Cursor setup |
| [user/WORKSPACE.md](user/WORKSPACE.md) | Workspace and optional copies |

## Templates (`docs/modelos/`)

Reference layouts for documentation style: [modelos/README.md](modelos/README.md).

## Formal Word document

Optional deliverable: [`../word/`](../word/) — `StockTracker_Documentacao_Projeto.docx`

Regenerate:

```powershell
python tools/build_project_docx.py
```

Requires `python-docx`.

## Run the application

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.main
```

Or double-click `run.bat` at the repository root.
