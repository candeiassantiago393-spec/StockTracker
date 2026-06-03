# Siemens Popups (Qt Designer)

Complete popup files for editing in Qt Designer (forms, tables, and action buttons).

| File | Designer content |
|------|------------------|
| `gui_popup_manual.ui` | Manual component form + Save/Cancel |
| `gui_popup_history.ui` | History table + Close |
| `gui_popup_search.ui` | Search results table + Ok/Cancel |
| `gui_popup_edit.ui` | Edit component form + Save/Cancel |
| `gui_popup_confirm.ui` | Confirmation dialog (Yes/No) |

At runtime, the app imports the generated `gui_popup_*.py` modules.

## Regenerate

```text
python tools/generate_popup_uis.py
.\.venv\Scripts\pyside6-uic.exe src\gui\designer\popups\gui_popup_manual.ui -o src\gui\designer\popups\gui_popup_manual.py
# or use tools\export_popup_uis.ps1 for all popups
```

To open these popup files in Designer quickly, use:
`Desktop\StockTracker-Designer\DESIGNER.bat` (options 2-7).
