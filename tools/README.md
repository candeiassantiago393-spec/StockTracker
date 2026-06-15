# Maintenance Tools

Helper scripts for design/export/documentation tasks.  
These are not required to run the app.

| File | Purpose |
|------|---------|
| `ABRIR-DESIGNER.bat` | Opens `gui_stocktracker.ui` in Qt Designer |
| `abrir-qt-designer.ps1` | Same as above (PowerShell) |
| `export-ui.bat` / `export_designer_uis.ps1` | Exports main + equipments + popup `.ui` → `.py` |
| `export_stocktracker_ui.ps1` | Exports only `gui_stocktracker.ui` (legacy) |
| `generate_all_designer_uis.py` | Regenerates all `.ui` from Python builders |
| `generate_stocktracker_ui.py` | Regenerates `gui_stocktracker.ui` |
| `generate_equipments_ui.py` | Regenerates `gui_equipments.ui` |
| `gui_ui_builder.py` | Shared Siemens layout XML builders |
| `generate_popup_uis.py` | Regenerates popup `.ui` files |
| `export_popup_uis.ps1` | Exports popup `.ui` files to `.py` |
| `sync_designer_package.ps1` | Syncs `StockTracker-Designer/` (repo and/or Desktop) |
| `DESIGNER-DESKTOP.bat` | Launcher copied into Designer package |
| `organizar-ambiente.ps1` | Regenerates UI, syncs Designer (repo + Desktop), copies project to Desktop |
| `ORGANIZAR-DESKTOP.bat` | Wrapper for `organizar-ambiente.ps1` (in this folder) |
| `sincronizar-desktop.ps1` | Legacy: copies project + Designer (use `organizar-ambiente.ps1` instead) |
| `build_project_docx.py` | Builds `word/StockTracker_Documentacao_Projeto.docx` |
| `seed_example_equipments.py` | Adds 5 demo equipments + sample datasheets in `data/` |

## Run the App

From project root:

```text
run.bat
```

or:

```powershell
python -m src.main
```

## DigiKey Auth Test

```powershell
python scripts/test_digikey_auth.py
```

## Optional Terminal Mode

```powershell
python -m src.test_terminal
```
