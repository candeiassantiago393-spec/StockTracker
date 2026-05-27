# Qt Designer workflow (Siemens template)

Your tutor requires the **official Siemens UI** built in **Qt Widgets Designer**, then exported to Python — not a hand-coded layout.

## Export the current interface to Qt Designer (for your designer / tutor)

The layout was built in Python first; you can **regenerate** a matching `.ui` file anytime:

```powershell
cd C:\Users\z005027j\Downloads\StockTracker\StockTracker
python tools/generate_stocktracker_ui.py
```

This writes **`src/gui/designer/gui_stocktracker.ui`** (~full Stock Tracker screen, Siemens colours, English labels).

**Send to the designer / open in Qt Designer:**

1. File → Open → `src/gui/designer/gui_stocktracker.ui`
2. Preview: **Form → Preview** (or **Ctrl+R**)
3. If the logo is missing, open the project from the repo root so `../siemens_template/resources/resources.qrc` resolves.

After the designer edits the `.ui`:

```powershell
.\tools\export_stocktracker_ui.ps1
python -m src.main
```

You can zip and share only:

- `src/gui/designer/gui_stocktracker.ui`
- `src/gui/siemens_template/` (template + `resources/` for logo/fonts)

## Files

| File | Role |
|------|------|
| `src/gui/designer/gui_stocktracker.ui` | **Edit only in Qt Designer** |
| `src/gui/designer/gui_stocktracker.py` | **Generated** — do not edit by hand |
| `tools/generate_stocktracker_ui.py` | Python → `.ui` (sync layout for Designer) |
| `src/gui/ui_stock_tracker.py` | Fallback UI if Designer export is missing |
| `src/gui/siemens_template/gui_template.ui` | Reference template from Siemens |

## Steps

### 1. Open the project UI in Qt Designer

1. Install **Qt Designer** (with PySide6 / Qt 6).
2. Open: `src/gui/designer/gui_stocktracker.ui`
3. You should see the Siemens dark theme: header, **Inventory**, **Distributor** combo, etc.

If logos/fonts are missing, open the `.ui` from the repo root so the path `../siemens_template/resources/resources.qrc` resolves.

### 2. Build the full screen in Designer

Keep the Siemens layout (header + left operations + right details).  
Add widgets and set **objectName** exactly as below (English labels in the UI).

**Left panel (operations)**

| objectName | Widget type | Label (example) |
|------------|-------------|-----------------|
| `user_entry` | QLineEdit | User Name |
| `search_entry` | QLineEdit | Search Component |
| `btn_search` | QPushButton | SEARCH |
| `supplier_combo` | QComboBox | Distributor (catalog lookup) |
| `barcode_entry` | QLineEdit | Scan Barcode / Supplier Ref. |
| `quantity_entry` | QLineEdit | Quantity |
| `btn_scan` | QPushButton | SCAN |
| `btn_add_stock` | QPushButton | ADD STOCK |
| `btn_remove_stock` | QPushButton | REMOVE STOCK |
| `btn_history_all` | QPushButton | VIEW LAST 20 HISTORY |
| `btn_history_component` | QPushButton | VIEW CURRENT COMPONENT HISTORY |
| `btn_clear` | QPushButton | CLEAR |
| `status_label` | QLabel | (status text) |

**Right panel (component details)**

| objectName | Widget type | Label (example) |
|------------|-------------|-----------------|
| `val_mouser` | QLabel | Supplier Reference (value) |
| `val_manufacturer` | QLabel | Manufacturer |
| `val_manufacturer_ref` | QLabel | Manufacturer Reference |
| `val_description` | QLabel | Description |
| `val_stock` | QLabel | Current Stock |

Copy styles from existing labels/buttons in the template (Siemens colours).

### 3. Export to Python

From the project folder:

```powershell
.\tools\export_stocktracker_ui.ps1
```

Or manually:

```powershell
pyside6-uic src/gui/designer/gui_stocktracker.ui -o src/gui/designer/gui_stocktracker.py
```

Then fix the first `resources_rc` import line to:

```python
from src.gui.siemens_template.resources import resources_rc
```

(The script does this automatically.)

### 4. Run the app

```powershell
python -m src.main
```

When `gui_stocktracker.py` contains `barcode_entry`, the app switches to the **Designer UI** automatically. Until then, it uses the legacy layout so you can keep working.

## Rules (for the tutor)

1. **Do not** layout the main window in `ui_stock_tracker.py` for the final delivery — use `.ui` + export.
2. **Do not** edit `gui_stocktracker.py` by hand (it is overwritten on export).
3. **Do** keep Siemens styles/resources from `siemens_template`.
4. **Do** use English labels in the interface.

## Logic stays in Python

- `src/gui/stock_tracker_window.py` — buttons, search, distributors, Excel (no visual layout).
