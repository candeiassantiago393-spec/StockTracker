# Stock Tracker

Desktop application for electronic component inventory management (Siemens corporate UI).

> Portuguese version: [PROJETO_STOCKTRACKER_PT.md](PROJETO_STOCKTRACKER_PT.md)

# Specifications

- Local inventory stored in Excel (`data/stock.xlsx`);
- PySide6 GUI with Siemens corporate UI templates;
- Component search in Excel (supplier reference, manufacturer, MPN, description);
- Barcode / label parsing (Mouser-style `P…Q` patterns);
- Stock movements **IN** / **OUT** with audit trail on the **History** sheet;
- Multi-distributor catalog lookup on SCAN (configured APIs only);
- Manual add/edit of components without API;
- User name required for movements and history;
- Clear separation: business logic in `src/core/`, UI in `src/gui/`;
- Credentials in `config/secrets.py` (never committed).

# Communication Protocol

The application does not expose Modbus. External communication uses **HTTPS REST APIs** from distributor modules under `src/core/suppliers/`.

## Runtime entry

| Characteristic | Value |
|:---------------|:------|
| Entry command  | `python -m src.main` or `run.bat` |
| Python         | 3.10+ |
| Platform       | Windows 10/11 |
| Data file      | `data/stock.xlsx` (close Excel before save) |

## Multi-supplier SCAN order

When SCAN does not find a part in Excel, the core layer queries each **configured** supplier in this order until the first hit:

| Order | Supplier ID     | Module                    |
|:-----:|:----------------|:--------------------------|
| 1     | `mouser`        | `src/core/suppliers/mouser.py` |
| 2     | `tme`           | `src/core/suppliers/tme.py` |
| 3     | `rs`            | `src/core/suppliers/rs.py` |
| 4     | `digikey`       | `src/core/suppliers/digikey.py` |
| 5     | `robert_mauser` | `src/core/suppliers/robert_mauser.py` |

Credentials and enablement: `config/secrets.py` (see `config/secrets.example.py`).

## Normalized part structure (`PartInfo`)

All supplier modules return the same logical fields (see `src/core/suppliers/base.py`):

| Field                      | Description |
|:---------------------------|:------------|
| `supplier`                 | Internal ID (`mouser`, `digikey`, …) |
| `supplier_part_number`     | Distributor SKU / order code |
| `manufacturer`             | Manufacturer name |
| `manufacturer_part_number` | MPN |
| `description`              | Short description |

Legacy keys (`MouserPartNumber`, `Manufacturer`, …) are kept for Excel compatibility.

# Data Model (Excel)

Permissions (logical):

- **r**: read by app
- **w**: written on user action
- **h**: append-only history

## Sheet: Components

| Column | Index | Type   | Permission | Description |
|:-------|:-----:|:-------|:------------|:------------|
| ID     | A (0) | int    | w          | Auto-increment row identifier |
| Supplier Reference | B (1) | string | rw | Distributor part number (e.g. Mouser `581-…`) |
| Manufacturer | C (2) | string | rw | Manufacturer name |
| Manufacturer Reference | D (3) | string | rw | MPN |
| Value  | E (4) | string | rw | Reserved / optional |
| Description | F (5) | string | rw | Part description |
| Stock  | G (6) | int    | rw         | Current quantity |

## Sheet: Equipments

| Column | Index | Type | Permission | Description |
|:-------|:-----:|:-----|:-----------|:------------|
| ID | A (0) | int | w | Auto-increment identifier |
| Supplier Reference | B (1) | string | rw | Supplier / barcode reference |
| Serial Number | C (2) | string | rw | Serial number |
| Description | D (3) | string | rw | Equipment description |
| Calibration Date | E (4) | string | rw | Calibration date (`YYYY-MM-DD`) |
| Calibration Expiration Date | F (5) | string | rw | Calibration expiry date |

## Sheet: History

| Column | Index | Type   | Permission | Description |
|:-------|:-----:|:-------|:------------|:------------|
| Date   | A     | datetime string | h | Timestamp `YYYY-MM-DD HH:MM:SS` |
| User   | B     | string | h          | Operator name from GUI |
| Supplier Reference | C | string | h | Reference at time of movement |
| Movement | D   | string | h          | `IN` or `OUT` |
| Quantity | E     | int    | h          | Moved quantity |
| Stock After | F  | int    | h          | Balance after movement |

# GUI Operations

| Operation        | Trigger | Core method(s) |
|:-----------------|:--------|:-----------------|
| Search (Excel)   | SEARCH  | `search_in_excel_all`, dialogs |
| Scan / barcode   | SCAN    | `extract_part_number`, `add_from_supplier_and_stock_in` |
| Add stock        | ADD     | `update_stock("IN")` or scan flow |
| Remove stock     | REMOVE  | `update_stock("OUT")` + confirm dialog |
| History          | History buttons | `get_history_rows` |
| Manual component | Manual popup | `add_manual_component` |
| Edit component   | Edit / empty details click | `update_component` |
| Open Excel       | OPEN EXCEL | `ensure_workbook_sheets` + OS `startfile` on `stock.xlsx` |

## GUI — Equipments page

| Operation | Trigger | Core method(s) |
|:----------|:--------|:---------------|
| Search equipments | SEARCH | `search_equipments_all`, `EquipmentSearchDialog` |
| Lookup by supplier ref | Enter on scan field | `find_equipment_by_supplier_ref` |
| Add equipment | ADD MANUAL | `add_equipment` |
| Edit equipment | EDIT | `update_equipment` |
| History tables | Last 20 / Eq. hist. | `get_equipment_rows`, `EquipmentsTableDialog` |

Layout: `src/gui/designer/gui_equipments.ui` — see [user/QT_DESIGNER.md](user/QT_DESIGNER.md).

## User rules (GUI)

- User name must be set before stock changes;
- OUT requires confirmation;
- Scan reference minimum length enforced in GUI;
- If Excel is open, `save_workbook` fails with a clear message.

# Architecture

```
src/main.py
    └── src/gui/stock_tracker_window.py  (PySide6, QStackedWidget)
            ├── Components  ← designer/gui_stocktracker.ui
            ├── Equipments   ← equipments_page.py + designer/gui_equipments.ui
            └── src/core/stock.py        (StockTracker)
                    ├── openpyxl → data/stock.xlsx
                    └── src/core/suppliers/* → REST APIs
```

Module-level code documentation follows the Siemens template (numbered sections in `stock.py`, `main.py`, `suppliers/base.py`).

# Versions

Project versioning (application, not per-component):

| Version | Notes |
|:--------|:------|
| 2.x     | Single GUI; multi-supplier SCAN; Siemens Designer UI |
| 1.x     | Excel + Mouser-focused GUI |
| 0.x     | Console / prototype (`src/test_terminal.py`) |

Formal deliverable: `word/StockTracker_Documentacao_Projeto.docx` (regenerate with `python tools/build_project_docx.py`).

## Current changes

- **Equipments** inventory page and Excel sheet;
- Symmetric Siemens layout (Components + Equipments), Qt Designer package;
- `tools\ORGANIZAR-DESKTOP.bat` — sync Designer and Desktop copies;
- Multi-distributor SCAN, DigiKey diagnostics, OPEN EXCEL with sheet ensure.

# TODO

- DigiKey production keys / sandbox 403 resolution with DigiKey support;
- Robert Mauser integration when API details are available;
- Optional temperature / alerts N/A (not applicable to this app).
