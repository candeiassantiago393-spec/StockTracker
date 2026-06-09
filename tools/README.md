# Maintenance Tools

Helper scripts for design/export/documentation tasks.  
These are not required to run the app.

| File | Purpose |
|------|---------|
| `ABRIR-DESIGNER.bat` | Opens `gui_stocktracker.ui` in Qt Designer |
| `abrir-qt-designer.ps1` | Same as above (PowerShell) |
| `export-ui.bat` / `export_designer_uis.ps1` | Exports main + materials + popup `.ui` → `.py` |
| `export_stocktracker_ui.ps1` | Exports only `gui_stocktracker.ui` (legacy) |
| `generate_all_designer_uis.py` | Regenerates all `.ui` from Python builders |
| `generate_stocktracker_ui.py` | Regenerates `gui_stocktracker.ui` |
| `generate_materials_ui.py` | Regenerates `gui_materials.ui` |
| `gui_ui_builder.py` | Shared Siemens layout XML builders |
| `generate_popup_uis.py` | Regenerates popup `.ui` files |
| `export_popup_uis.ps1` | Exports popup `.ui` files to `.py` |
| `sync_designer_package.ps1` | Syncs `StockTracker-Designer/` (repo and/or Desktop) |
| `DESIGNER-DESKTOP.bat` | Launcher copied into Designer package |
| `sincronizar-desktop.ps1` | Syncs the project to Desktop (optional workflow) |
| `build_project_docx.py` | Builds `word/StockTracker_Documentacao_Projeto.docx` |

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
