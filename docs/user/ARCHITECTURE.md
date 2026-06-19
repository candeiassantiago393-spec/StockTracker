# Architecture — Stock Tracker

## Separation of concerns

```
UI (src/gui/)  --->  Business logic (src/core/stock.py)  --->  Data (Excel / supplier APIs)
```

The UI **does not** implement stock rules. It collects input, validates the operator name, and calls `StockTracker` methods.

---

## `StockTracker` class

| Area | Main methods |
|------|----------------|
| Excel | `get_workbook`, `get_components_sheet`, `get_equipments_sheet`, `get_history_sheet`, `save_workbook`, `ensure_workbook_sheets` |
| Components search | `search_in_excel`, `search_in_excel_all`, `find_component_any`, `extract_part_number` |
| Stock | `update_stock` (IN/OUT), `add_history`, `add_manual_component`, `update_component` |
| Equipments | `add_equipment`, `update_equipment`, `search_equipments_all`, `find_equipment_by_supplier_ref` |
| Suppliers | `search_supplier`, `search_any_supplier`, `add_from_supplier_and_stock_in` |

---

## Graphical interface

| Component | Responsibility |
|-----------|----------------|
| `StockTrackerWindow` | Navigation (Components / Equipments), shared title, user row, action bar |
| `Ui_StockTracker` | Components layout (from `gui_stocktracker.ui`) |
| `EquipmentsPage` + `Ui_EquipmentsPage` | Equipments layout and events (`gui_equipments.ui`) |
| Dialog modules | History, confirm, search, manual/edit component, equipments table/search |
| `styles.py` | Siemens visual identity and layout metrics |

### Navigation

- `QStackedWidget`: page 0 = Components (`container_main_body`), page 1 = Equipments
- Header buttons **COMPONENTS** / **EQUIPMENTS** switch pages
- Shared: title `Inventory — …`, user name row, bottom action bar (labels change per section)

### GUI rules

- Operator name required before stock/equipment operations
- Explicit confirmation before stock OUT
- Minimum reference length on component scan (validated in GUI)
- Clear errors when Excel is locked or an API call fails

---

## SCAN flow (Components)

1. User enters barcode or supplier reference
2. Search local Excel inventory
3. If not found — query configured distributor APIs (ordered chain)
4. New part: append row to Excel, then stock IN as requested
5. History row appended on each movement

---

## Equipments flow

1. User searches by text or supplier reference on Equipments page
2. Core reads/writes `Equipments` sheet (no distributor SCAN)
3. ADD MANUAL / EDIT open `EquipmentDialog` (Python popup, Siemens styles)
4. History buttons show equipment rows via `EquipmentsTableDialog` (reuses history popup layout)

---

## Data model (Excel)

### Components sheet

ID, Supplier Reference, Manufacturer, Manufacturer Reference, Value, Description, Stock

### Equipments sheet

ID, Supplier Reference, Serial Number, **Name**, Description, Calibration Date, Calibration Expiration Date, **Datasheet**, **Image**

Per-equipment files: `data/equipments/{id}/` (datasheet + image filenames in Excel columns).

### History sheet

Date, User, Supplier Reference, Movement, Quantity, Stock After

---

## Credentials

Loaded via `config/credentials.py` from `config/secrets.py` (local, gitignored).

Supplier modules live under `src/core/suppliers/`.
