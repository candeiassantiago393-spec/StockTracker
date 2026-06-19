# Documentation — Stock Tracker

## Quick start

| Audience | Document |
|----------|----------|
| **Portuguese (operators / GUI)** | [GUIA_RAPIDO_PT.md](GUIA_RAPIDO_PT.md) |
| **English (commands)** | [user/COMMANDS.md](user/COMMANDS.md) |
| **Run the app** | `python -m src.main` or `run.bat` |

---

## Specification

| Document | Content |
|----------|---------|
| [PROJETO_STOCKTRACKER.md](PROJETO_STOCKTRACKER.md) | Product specification (English, Siemens-style) |
| [PROJETO_STOCKTRACKER_PT.md](PROJETO_STOCKTRACKER_PT.md) | Same specification in Portuguese |

---

## User guides (`docs/user/`)

| Document | Content |
|----------|---------|
| [user/COMMANDS.md](user/COMMANDS.md) | Install, run, Designer sync, troubleshooting |
| [user/REPOSITORY_LAYOUT.md](user/REPOSITORY_LAYOUT.md) | Repository structure and key files |
| [user/ARCHITECTURE.md](user/ARCHITECTURE.md) | Architecture and data flows |
| [user/WORKSPACE.md](user/WORKSPACE.md) | Desktop folders and Qt Designer packages |
| [user/QT_DESIGNER.md](user/QT_DESIGNER.md) | Qt Designer — Components + Equipments |
| [user/SUPPLIERS.md](user/SUPPLIERS.md) | Supplier APIs and credentials |
| [user/DIGIKEY_SETUP.md](user/DIGIKEY_SETUP.md) | DigiKey sandbox setup |
| [user/GITHUB.md](user/GITHUB.md) | GitHub publishing |
| [user/IDE_SETUP.md](user/IDE_SETUP.md) | VS Code / Cursor setup |

---

## Fluxogramas (`docs/fluxogramas/`)

| Documento | Conteúdo |
|-----------|----------|
| [fluxogramas/README.md](fluxogramas/README.md) | Índice (diagramas Mermaid) |
| [fluxogramas/03-components.md](fluxogramas/03-components.md) | Fluxos Components |
| [fluxogramas/04-equipments.md](fluxogramas/04-equipments.md) | Fluxos Equipments |
| [fluxogramas/08-qt-designer.md](fluxogramas/08-qt-designer.md) | Workflow Qt Designer |

---

## GUI module (Portuguese)

| Document | Content |
|----------|---------|
| [../src/gui/ESTRUTURA.md](../src/gui/ESTRUTURA.md) | GUI file map |
| [../src/gui/designer/README.md](../src/gui/designer/README.md) | Designer `.ui` workflow |
| [../src/gui/designer/EQUIPMENTS-LEIA-ME.txt](../src/gui/designer/EQUIPMENTS-LEIA-ME.txt) | Equipments in Qt Designer (PT) |

---

## Templates (`docs/modelos/`)

Reference layouts for documentation style: [modelos/README.md](modelos/README.md).

---

## Tools (`tools/`)

| Script | Purpose |
|--------|---------|
| `tools/ORGANIZAR-DESKTOP.bat` | Sync Designer + Desktop project |
| `generate_all_designer_uis.py` | Regenerate all `.ui` files |
| `export-ui.bat` | Export `.ui` → `.py` |

Full list: [../tools/README.md](../tools/README.md).

---

## Roadmap / melhorias sugeridas

| Document | Content |
|----------|---------|
| [MELHORIAS_SUGERIDAS.md](MELHORIAS_SUGERIDAS.md) | Ideias de evolução (cache imagens, stock mínimo, backup, etc.) |

---

## Formal Word document

Optional: [`../word/`](../word/) — regenerate with `python tools/build_project_docx.py` (requires `python-docx`).
