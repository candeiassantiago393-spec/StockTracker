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
| Excel | `get_workbook`, `get_components_sheet`, `get_history_sheet`, `save_workbook` |
| Search | `search_in_excel`, `search_in_excel_all`, `find_component_any`, `extract_part_number` |
| Stock | `update_stock` (IN/OUT), `add_history`, `add_manual_component` |
| Suppliers | `search_supplier`, `search_any_supplier`, `add_from_supplier_and_stock_in` |

---

## Graphical interface

| Component | Responsibility |
|-----------|----------------|
| `StockTrackerWindow` | Event orchestration (SEARCH, SCAN, ADD/REMOVE, history) |
| `Ui_StockTracker` | Layout and widgets (from `.ui` export) |
| Dialog modules | History, confirm, search results, manual component, user name |
| `styles.py` | Siemens visual identity (colors, typography) |

### GUI rules

- Operator name required before stock operations
- Explicit confirmation before stock OUT
- Minimum reference length on scan (validated in GUI)
- Clear errors when Excel is locked or an API call fails

---

## SCAN flow (summary)

1. User enters barcode or supplier reference
2. Search local Excel inventory
3. If not found — query configured distributor APIs (ordered chain)
4. New part: append row to Excel, then stock IN as requested
5. History row appended on each movement

---

## Data model (Excel)

### Components sheet

ID, Supplier Reference, Manufacturer, Manufacturer Reference, Value, Description, Stock

### History sheet

Date, User, Supplier Reference, Movement, Quantity, Stock After

---

## Credentials

Loaded via `config/credentials.py` from `config/secrets.py` (local, gitignored). Optional constructor override for Mouser key in tests.

Supplier modules live under `src/core/suppliers/`.
