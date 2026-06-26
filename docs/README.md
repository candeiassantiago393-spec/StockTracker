# Documentation — Stock Tracker

## Quick start

| Audience | Document |
|----------|----------|
| **Portuguese (operators / GUI)** | [guias/GUIA_RAPIDO_PT.md](guias/GUIA_RAPIDO_PT.md) |
| **English (commands)** | [user/COMMANDS.md](user/COMMANDS.md) |
| **Run the app** | `python -m src.main` or `run.bat` |

---

## Specification (`docs/especificacao/`)

| Document | Content |
|----------|---------|
| [especificacao/PROJETO_STOCKTRACKER.md](especificacao/PROJETO_STOCKTRACKER.md) | Product specification (English, Siemens-style) |
| [especificacao/PROJETO_STOCKTRACKER_PT.md](especificacao/PROJETO_STOCKTRACKER_PT.md) | Same specification in Portuguese |

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

## Qt Designer (`docs/designer/`)

| Document | Content |
|----------|---------|
| [designer/README.md](designer/README.md) | **Índice** — pacotes, estrutura, comandos |
| [../src/gui/designer/README.md](../src/gui/designer/README.md) | Canonical `.ui` workflow |
| [../StockTracker-Designer/LEIA-ME.txt](../StockTracker-Designer/LEIA-ME.txt) | Pacote Designer (PT) |

---

## Fluxogramas (`docs/fluxogramas/`)

| Documento | Conteúdo |
|-----------|----------|
| [fluxogramas/README.md](fluxogramas/README.md) | Índice (diagramas Mermaid) |
| [fluxogramas/03-components.md](fluxogramas/03-components.md) | Fluxos Components |
| [fluxogramas/04-equipments.md](fluxogramas/04-equipments.md) | Fluxos Equipments |
| [fluxogramas/08-qt-designer.md](fluxogramas/08-qt-designer.md) | Workflow Qt Designer |

---

## Layout (`docs/layout/`)

| Document | Content |
|----------|---------|
| [layout/EQUIPMENTS_CAIXA_IMAGEM.md](layout/EQUIPMENTS_CAIXA_IMAGEM.md) | Equipments image box reference |

---

## GUI module (Portuguese)

| Document | Content |
|----------|---------|
| [../src/gui/ESTRUTURA.md](../src/gui/ESTRUTURA.md) | GUI file map |
| [../src/gui/designer/EQUIPMENTS-LEIA-ME.txt](../src/gui/designer/EQUIPMENTS-LEIA-ME.txt) | Equipments in Qt Designer (PT) |

---

## Templates (`docs/modelos/`)

Reference layouts for documentation style: [modelos/README.md](modelos/README.md).

---

## Roadmap (`docs/roadmap/`)

| Document | Content |
|----------|---------|
| [roadmap/MELHORIAS_SUGERIDAS.md](roadmap/MELHORIAS_SUGERIDAS.md) | Ideias de evolução |

---

## Tools (`tools/`)

| Script | Purpose |
|--------|---------|
| `tools/ORGANIZAR-DESKTOP.bat` | Sync Designer + Desktop project |
| `generate_all_designer_uis.py` | Regenerate all `.ui` files |
| `export-ui.bat` | Export `.ui` → `.py` |

Full list: [../tools/README.md](../tools/README.md).

---

## Formal Word document

Optional: [`../word/`](../word/) — regenerate with `python tools/build_project_docx.py` (requires `python-docx`).
