# Ferramentas de manutencao

Scripts auxiliares — fora do fluxo normal da aplicacao.

| Ficheiro | Descricao |
|----------|-----------|
| `export_stocktracker_ui.ps1` | `.ui` → `gui_stocktracker.py` (apos editar no Qt Designer) |
| `generate_stocktracker_ui.py` | Regenera `.ui` a partir do layout Python |
| `abrir-qt-designer.ps1` / `ABRIR-DESIGNER.bat` | Abre `gui_stocktracker.ui` no Designer |
| `sincronizar-desktop.ps1` | Copia projeto para `Desktop\StockTracker-Projeto` |
| `reorganize_gui_template.py` | Organiza templates Siemens (uso pontual) |
| `REORGANIZAR_GUI.bat` | Executa reorganize_gui_template.py |

A aplicacao arranca com `run.bat` ou `python -m src.main`.  
Demo (UI antiga verde/vermelho): `run-demo.bat`.
