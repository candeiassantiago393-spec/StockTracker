# Qt Designer — Stock Tracker

Canonical `.ui` files for the running app. Metrics come from `styles.py` and Siemens `gui_template.ui`.

## Layout files

| File | Runtime |
|------|---------|
| `gui_stocktracker.ui` | Components page (`stock_tracker_window.py`) |
| `gui_equipments.ui` | Equipments page (`equipments_page.py`) — see `EQUIPMENTS-LEIA-ME.txt` |
| `popups/components/gui_popup_*.ui` | Component dialogs |
| `popups/equipments/gui_popup_*.ui` | Equipment dialogs |
| `popups/shared/gui_popup_*.ui` | Confirm + template |

## Components page (summary)

| Area | Key widgets |
|------|-------------|
| Left — Operations | `search_entry`, `btn_search`, `barcode_entry`, `btn_scan`, `quantity_entry` |
| Left — Stock Actions | `label_stock_btn` (Stock Actions), `btn_add_stock`, `btn_remove_stock` |
| Right — Details | `val_mouser` … `val_stock` (+ Copy buttons) |
| Right — Catalog image | `component_image_preview` (runtime: `CatalogImagePreview` — zoom/lupa) |

## Equipments page (summary)

| Area | Key widgets |
|------|-------------|
| Left — Operations | `search_entry`, `supplier_ref_entry`, scan/copy buttons |
| Left — Image | `equipment_image_preview`, `btn_set_equipment_image` (Add), `btn_clear_equipment_image` (Delete) |
| Right — Details | `val_supplier_reference` … `val_datasheet` (all fields **100px** wide) |
| Right — Docs | `doc_search_entry`, `doc_results_list` (hidden until SEARCH), LINK / OPEN FOLDER / ADD DOC |

Runtime behaviour (images, list visibility, drag & drop) is in `equipments_page.py`, not in the `.ui` alone.

Full guide (PT): [EQUIPMENTS-LEIA-ME.txt](EQUIPMENTS-LEIA-ME.txt)  
User guide (EN): [docs/user/QT_DESIGNER.md](../../../docs/user/QT_DESIGNER.md)

## Regenerate from Python (template-aligned)

```text
python tools/generate_all_designer_uis.py
```

Or individually:

```text
python tools/generate_stocktracker_ui.py
python tools/generate_equipments_ui.py
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

Choose **1** (Components) or **2** (Equipments).

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
- Row labels: **74px**; value fields: **100px**; Copy: **60px**; action buttons: **124px**
- Compact buttons (Add/Delete image): **64px** (`BTN_COMPACT_STYLE`)
- Row spacing: **6px**; row margins: `(0, 9, 9, 9)`

Built by `tools/gui_ui_builder.py` — keep generators and `styles.py` in sync.
