# Qt Designer — Siemens UI (Stock Tracker)

The application uses **Siemens template** layouts in Qt Widgets Designer. Layout lives in `.ui` files and is exported to Python with `pyside6-uic`. Business logic stays in Python (`stock_tracker_window.py`, `equipments_page.py`).

---

## Layout files

| File | Runtime | Designer menu |
|------|---------|---------------|
| `src/gui/designer/gui_stocktracker.ui` | Components page | Option **1** |
| `src/gui/designer/gui_equipments.ui` | Equipments page | Option **2** |
| `popups/components/gui_popup_*.ui` | Component dialogs | Options **3–6** |
| `popups/equipments/gui_popup_*.ui` | Equipment dialogs | Options **7–9** |
| `popups/shared/gui_popup_*.ui` | Confirm + template | Options **10–11** |

Generated modules (`gui_stocktracker.py`, `gui_equipments.py`, `popups/**/gui_popup_*.py`) — **do not edit by hand**.

Reference: `src/gui/siemens_template/gui_template.ui`  
Shared metrics: `src/gui/styles.py`, `tools/gui_ui_builder.py`  
Portuguese Equipments guide: `src/gui/designer/EQUIPMENTS-LEIA-ME.txt`  
Flowcharts: `docs/fluxogramas/`

---

## Designer packages

| Location | Purpose |
|----------|---------|
| `src/gui/designer/` | **Canonical** — used by the running app |
| `StockTracker-Designer/` | Editing bundle inside the repo (`LEIA-ME.txt`, `DESIGNER.bat`) |
| `Desktop\StockTracker-Designer` | Desktop copy for Qt Designer |

Refresh repo package:

```powershell
powershell -File tools\sync_designer_package.ps1 -Target Repo
```

Refresh everything (repo + Desktop):

```text
tools\ORGANIZAR-DESKTOP.bat
```

---

## Open in Qt Designer

**From repository root:**

```powershell
.\tools\ABRIR-DESIGNER.bat
```

**From Designer package:**

```text
StockTracker-Designer\DESIGNER.bat
```

(Menu lists options **1–11** — all popups in subfolders `popups/components/`, `popups/equipments/`, `popups/shared/`.)

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

Then restart: `python -m src.main`

**Workflow after editing on Desktop:** copy changed `.ui` files back to `src/gui/designer/` before export.

---

## Shared layout rules

| Rule | Value |
|------|-------|
| Page margins | 16 px left and right (`TEMPLATE_PAGE_MARGINS`) |
| Main columns | 50/50, horizontal spacing **0** |
| Detail labels (Components) | 152 px fixed column |
| Fields | 100 px |
| Copy buttons | 60 px |
| Action buttons (SEARCH, etc.) | 124 px |
| Row spacing | 6 px |

---

## Components — layout (2025)

**Operations (left):** Search → Scan → **Quantity** → **Stock Actions** (ADD / REMOVE)

**Component Details (right)** — 5-column grid:

| Col | Content |
|-----|---------|
| 0 | Labels (fixed 152 px) |
| 1 | Offset gap (`COMPONENT_DETAIL_CONTENT_OFFSET` = 288 px) |
| 2 | Value fields + Copy |
| 3 | Flexible spacer (grows in fullscreen) |
| 4 | Catalog image **240×240 px**, flush right |

**Catalog row:** WEB + Datasheet (hidden when no URLs).  
**Runtime image:** `component_image_preview` → `CatalogImagePreview` (`catalog_image_preview.py`).

| Runtime behaviour | Detail |
|-------------------|--------|
| Empty detail click | Opens **ADD MANUAL** |
| Filled detail click | No action — use **EDIT** button |
| Short scan (≤4 chars) | Ignored |

---

## Equipments — key objectNames

**Left — Operations:** `search_entry`, `btn_search`, `supplier_ref_entry`, `btn_scan_supplier_ref`

**Left — Equipment image:** `equipment_image_panel`, `equipment_image_preview` (**300×320** min), `btn_set_equipment_image`, `btn_clear_equipment_image`

**Right — Details:** `val_supplier_reference`, `val_serial_number`, `val_name`, `val_description`, `val_calibration`, `val_expiration`, `val_datasheet` (+ Copy)

**Right — Support documentation:** `doc_search_entry`, `doc_results_list`, LINK / OPEN FOLDER / ADD DOC

| Runtime behaviour | Detail |
|-------------------|--------|
| Equipment image | `data/equipments/{id}/` + Excel **Image** column |
| Datasheet / docs | Per-equipment folder (not legacy `support_documentation/`) |
| Empty detail click | Opens **Add Equipment** |

Portuguese layout guide: `src/gui/designer/EQUIPMENTS-LEIA-ME.txt`

---

## Responsibilities

| Layer | Location |
|-------|----------|
| Components layout | `gui_stocktracker.ui` → `gui_stocktracker.py` |
| Equipments layout | `gui_equipments.ui` → `gui_equipments.py` |
| Components behaviour | `stock_tracker_window.py` |
| Equipments behaviour | `equipments_page.py` |
| Popups | `*_dialog.py` + `designer/popups/` |

See also: [WORKSPACE.md](WORKSPACE.md), [ARCHITECTURE.md](ARCHITECTURE.md), [../fluxogramas/README.md](../fluxogramas/README.md).
