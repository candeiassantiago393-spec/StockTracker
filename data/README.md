# Data — Stock Tracker

Place your inventory file here: **`stock.xlsx`**

## Required sheets

| Sheet | Purpose |
|-------|---------|
| `Components` | Parts and stock levels |
| `History` | Stock movements (IN/OUT) |
| `Equipments` | Calibrated equipments (supplier ref, serial, description, dates, **Datasheet** filename) |

The app creates headers automatically if the file is missing or empty.

## Support documentation

Folder: **`support_documentation/`** (inside `data/`)

Store datasheets, manuals and other support files here. From the **Equipments** page:

- **SEARCH** — lists matching files in `doc_results_list`
- **LINK** — associates the selected file with the current equipment (saved in Excel)
- When you **search equipment**, its linked datasheet loads in the list and opens automatically
- **ADD DOC** — copies a file; if an equipment is selected, it is linked automatically

### Example data (demo)

Sample datasheets live in `support_documentation/DS_*.pdf`.  
To load **5 example equipments** (oscilloscope, multimeters, power analyzer, generator):

```powershell
python tools/seed_example_equipments.py
```

Close `stock.xlsx` in Excel before running. Re-run skips equipments already in the workbook.

## Before running the app

- **Close** `stock.xlsx` in Microsoft Excel before save operations
- Keep regular backups of your inventory

## After cloning from GitHub

`stock.xlsx` is **not** in the repository (see root `.gitignore`). Either:

1. Copy your existing file into this folder, or  
2. Run the app once — it will create a new workbook with empty sheets.

Example (adjust paths):

```powershell
copy "path\to\your\stock.xlsx" "data\stock.xlsx"
```
