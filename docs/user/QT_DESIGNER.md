# Qt Designer — Siemens UI (Stock Tracker)

The main window uses the **Siemens template** in **Qt Widgets Designer**: layout lives in `.ui` and is exported to Python with `pyside6-uic`. Business logic stays in `src/gui/stock_tracker_window.py` (do not build the main window layout only in Python).

---

## Key files

| File | Role |
|------|------|
| `src/gui/designer/gui_stocktracker.ui` | Layout — **edit only in Qt Designer** |
| `src/gui/designer/gui_stocktracker.py` | Generated code — **do not edit by hand** |
| `tools/generate_stocktracker_ui.py` | Regenerate `.ui` from Python layout (sync) |
| `tools/export_stocktracker_ui.ps1` | Export `.ui` → `.py` and fix resource import |
| `tools/abrir-qt-designer.ps1` | Launch Qt Designer with project `.ui` |
| `src/gui/siemens_template/gui_template.ui` | Siemens reference template |
| `src/gui/ESTRUTURA.md` | GUI module map |

> The folder `src/gui/designer/` holds layout assets, not end-user documentation.

---

## Prerequisites

- **PySide6** installed (`pip install -r requirements.txt`)
- **Qt Designer** (`pyside6-designer` with PySide6, or Qt installer)
- Shell at **repository root** (contains `src/`, `tools/`, `run.bat`)

---

## Open the layout in Qt Designer

1. From repository root:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   .\tools\abrir-qt-designer.ps1
   ```

   Or in Qt Designer: **File → Open** → `src/gui/designer/gui_stocktracker.ui`

2. Preview: **Form → Preview** (or **Ctrl+R**).

3. If logo or fonts are missing, open the `.ui` with the repo root as working directory so `../siemens_template/resources/resources.qrc` resolves.

---

## Generate `.ui` from Python layout (optional)

When the screen was changed in Python and the `.ui` file must be refreshed:

```powershell
python tools/generate_stocktracker_ui.py
```

Writes `src/gui/designer/gui_stocktracker.ui` (Stock Tracker screen, Siemens styling, English labels).

---

## Edit the form in Qt Designer

Keep the Siemens structure: header, left panel (operations), right panel (component details).

Set **objectName** exactly as in the tables (visible labels in English).

**Left panel (operations)**

| objectName | Type | Label (example) |
|------------|------|-----------------|
| `user_entry` | QLineEdit | User Name |
| `search_entry` | QLineEdit | Search Component |
| `btn_search` | QPushButton | SEARCH |
| `barcode_entry` | QLineEdit | Scan Barcode / Supplier Ref. |
| `quantity_entry` | QLineEdit | Quantity |
| `btn_scan` | QPushButton | SCAN |
| `btn_add_stock` | QPushButton | ADD STOCK |
| `btn_remove_stock` | QPushButton | REMOVE STOCK |
| `btn_history_all` | QPushButton | VIEW LAST 20 HISTORY |
| `btn_history_component` | QPushButton | VIEW CURRENT COMPONENT HISTORY |
| `btn_clear` | QPushButton | CLEAR |
| `status_label` | QLabel | (status text) |

**Right panel (details)**

| objectName | Type | Label (example) |
|------------|------|-----------------|
| `val_mouser` | QLabel | Supplier Reference (value) |
| `val_manufacturer` | QLabel | Manufacturer |
| `val_manufacturer_ref` | QLabel | Manufacturer Reference |
| `val_description` | QLabel | Description |
| `val_stock` | QLabel | Current Stock |

Reuse button and label styles from the template (Siemens palette).

---

## Export `.ui` to Python

After saving in Qt Designer, from repository root:

```powershell
.\tools\export_stocktracker_ui.ps1
```

Or manually:

```powershell
pyside6-uic src/gui/designer/gui_stocktracker.ui -o src/gui/designer/gui_stocktracker.py
```

The export script sets the resource import to:

```python
from src.gui.siemens_template.resources import resources_rc
```

---

## Run the application

```powershell
python -m src.main
```

Or double-click `run.bat`.

When the exported `gui_stocktracker.py` includes `barcode_entry`, the app loads the **`.ui`-based` UI**. Otherwise it may use the legacy Python layout until export is complete.

---

## Conventions

1. Main window layout in `.ui` + `pyside6-uic` export, not Python-only.
2. Do not hand-edit `gui_stocktracker.py` (overwritten on each export).
3. Keep styles and resources under `src/gui/siemens_template/`.
4. Keep on-screen labels in **English**.

---

## Minimal package to edit layout in another clone

Include:

- `src/gui/designer/gui_stocktracker.ui`
- `src/gui/siemens_template/` (template + `resources/` for logo and fonts)

Regenerate `gui_stocktracker.py` locally with `export_stocktracker_ui.ps1` or `pyside6-uic`.

---

## Responsibilities

| Layer | Location |
|-------|----------|
| Visual layout | `gui_stocktracker.ui` → `gui_stocktracker.py` (generated) |
| Behaviour | `src/gui/stock_tracker_window.py` — events, Excel, APIs, dialogs |

See also: [ARCHITECTURE.md](ARCHITECTURE.md), [COMMANDS.md](COMMANDS.md).
