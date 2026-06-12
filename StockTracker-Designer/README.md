# Qt Designer — Stock Tracker

Canonical `.ui` files for the running app. Metrics come from `styles.py` and Siemens `gui_template.ui`.

## Layout files

| File | Runtime |
|------|---------|
| `gui_stocktracker.ui` | Components page (`stock_tracker_window.py`) |
| `gui_materials.ui` | Materials page (`materials_page.py`) — see `MATERIALS-LEIA-ME.txt` |
| `popups/components/gui_popup_*.ui` | Component dialogs |
| `popups/materials/gui_popup_*.ui` | Material dialogs |
| `popups/shared/gui_popup_*.ui` | Confirm + template |

## Regenerate from Python (template-aligned)

```text
python tools/generate_all_designer_uis.py
```

Or individually:

```text
python tools/generate_stocktracker_ui.py
python tools/generate_materials_ui.py
python tools/generate_popup_uis.py
```

## Export `.ui` → `.py` (after editing in Designer)

```text
tools\export-ui.bat
```

or:

```powershell
powershell -File tools\export_designer_uis.ps1
```

## Edit in Qt Designer

**In repo:**

```text
tools\ABRIR-DESIGNER.bat
```

**Designer package** (repo `StockTracker-Designer/` or Desktop copy):

```text
StockTracker-Designer\DESIGNER.bat
```

Sync package from canonical sources:

```powershell
powershell -File tools\sync_designer_package.ps1 -Target Repo
powershell -File tools\sync_designer_package.ps1 -Target Desktop
```

After editing `.ui` in the Designer package, copy changed files back to `src/gui/designer/` and run `export-ui.bat`.

## Shared layout rules

- Page margins: **16px** left and right (`TEMPLATE_PAGE_MARGINS`)
- Two columns: **50/50**, horizontal spacing **0**
- Row labels: **74px**; fields: **100px**; Copy: **60px**; action buttons: **124px**
- Row spacing: **6px**; row margins: `(0, 9, 9, 9)`

Built by `tools/gui_ui_builder.py` — keep generators and `styles.py` in sync.
