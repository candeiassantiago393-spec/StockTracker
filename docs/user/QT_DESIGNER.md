# Qt Designer — Siemens UI (Stock Tracker)

The application uses **Siemens template** layouts in Qt Widgets Designer. Layout lives in `.ui` files and is exported to Python with `pyside6-uic`. Business logic stays in Python (`stock_tracker_window.py`, `equipments_page.py`).

---

## Layout files

| File | Runtime | Designer menu |
|------|---------|---------------|
| `src/gui/designer/gui_stocktracker.ui` | Components page | Option **1** |
| `src/gui/designer/gui_equipments.ui` | Equipments page | Option **2** |
| `src/gui/designer/popups/gui_popup_*.ui` | Dialogs | Options **3–8** |

Generated modules (`gui_stocktracker.py`, `gui_equipments.py`, `gui_popup_*.py`) — **do not edit by hand**.

Reference: `src/gui/siemens_template/gui_template.ui`  
Shared metrics: `src/gui/styles.py`, `tools/gui_ui_builder.py`  
Portuguese Equipments guide: `src/gui/designer/EQUIPMENTS-LEIA-ME.txt`

---

## Designer packages

| Location | Purpose |
|----------|---------|
| `src/gui/designer/` | **Canonical** — used by the running app |
| `StockTracker-Designer/` | Editing bundle inside the repo |
| `Desktop\StockTracker-Designer` | Desktop copy for Qt Designer |

Refresh everything (repo + Desktop):

```text
tools\ORGANIZAR-DESKTOP.bat
```

or:

```powershell
powershell -File tools\organizar-ambiente.ps1
```

---

## Open in Qt Designer

**From repository root:**

```powershell
.\tools\ABRIR-DESIGNER.bat
```

Choose **1** (Components) or **2** (Equipments).

**From Desktop package:**

```text
Desktop\StockTracker-Designer\DESIGNER.bat
```

---

## Regenerate `.ui` from Python (template sync)

```powershell
python tools/generate_all_designer_uis.py
```

Individual generators:

```powershell
python tools/generate_stocktracker_ui.py
python tools/generate_equipments_ui.py
python tools/generate_popup_uis.py
```

---

## Export `.ui` → `.py` (after editing in Designer)

```powershell
tools\export-ui.bat
```

or:

```powershell
powershell -File tools\export_designer_uis.ps1
```

Then restart: `python -m src.main`

**Workflow after editing on Desktop:** copy changed `.ui` files back to `src/gui/designer/` before export.

---

## Shared layout rules (Components + Equipments)

| Rule | Value |
|------|-------|
| Page margins | 16 px left and right (`TEMPLATE_PAGE_MARGINS`) |
| Columns | 50/50, horizontal spacing **0** |
| Labels | 74 px min width |
| Fields | 100 px |
| Copy buttons | 60 px |
| Action buttons (SEARCH, etc.) | 124 px |
| Row spacing | 6 px |

---

## Components — key objectNames

**Left (Operations):** `search_entry`, `btn_search`, `barcode_entry`, `quantity_entry`, `btn_scan`, `btn_add_stock`, `btn_remove_stock`

**Right (Details):** `val_mouser`, `val_manufacturer`, `val_manufacturer_ref`, `val_description`, `val_stock`

**Shared (moved above stack):** `user_entry`, `tab1_title`

---

## Equipments — key objectNames

**Left:** `search_entry`, `btn_search`, `supplier_ref_entry`, `btn_copy_supplier_ref`

**Right:** `val_supplier_reference`, `val_serial_number`, `val_description`, `val_calibration`, `val_expiration` (+ Copy buttons)

---

## Responsibilities

| Layer | Location |
|-------|----------|
| Components layout | `gui_stocktracker.ui` → `gui_stocktracker.py` |
| Equipments layout | `gui_equipments.ui` → `gui_equipments.py` |
| Components behaviour | `stock_tracker_window.py` |
| Equipments behaviour | `equipments_page.py` |
| Popups | `*_dialog.py` + `designer/popups/` |

See also: [WORKSPACE.md](WORKSPACE.md), [ARCHITECTURE.md](ARCHITECTURE.md), [../GUIA_RAPIDO_PT.md](../GUIA_RAPIDO_PT.md).
