# Maintenance Tools

Helper scripts for design/export/documentation tasks.  
These are not required to run the app.

| File | Purpose |
|------|---------|
| `ABRIR-DESIGNER.bat` | Opens `gui_stocktracker.ui` in Qt Designer |
| `abrir-qt-designer.ps1` | Same as above (PowerShell) |
| `export-ui.bat` / `export_stocktracker_ui.ps1` | Exports `.ui` -> `gui_stocktracker.py` and fixes `resources_rc` import |
| `generate_stocktracker_ui.py` | Regenerates `gui_stocktracker.ui` from the Python generator |
| `generate_popup_uis.py` | Regenerates popup `.ui` and `.py` files |
| `export_popup_uis.ps1` | Exports popup `.ui` files to `.py` |
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
