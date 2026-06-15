# Siemens Popups (Qt Designer)

Popups are split by section. **Equipments popups are not the same as Components** (different columns and forms).

## `components/`

| File | Used by |
|------|---------|
| `gui_popup_manual.ui` | Add manual component |
| `gui_popup_edit.ui` | Edit component |
| `gui_popup_search.ui` | Excel search results (components) |
| `gui_popup_history.ui` | Component movement history |

## `equipments/`

| File | Used by |
|------|---------|
| `gui_popup_equipment.ui` | Add / edit equipment |
| `gui_popup_search.ui` | Equipment search results |
| `gui_popup_history.ui` | Equipments table (Last 20 / Eq. hist.) |

## `shared/`

| File | Used by |
|------|---------|
| `gui_popup_confirm.ui` | Yes/No, user name, alerts |
| `gui_popup_template.ui` | Siemens base template reference |

## Regenerate

```text
python tools/generate_popup_uis.py
tools\export-ui.bat
```

Open in Designer: `StockTracker-Designer\DESIGNER.bat` (options 3–11).

Sync package: `tools\ORGANIZAR-DESKTOP.bat`
