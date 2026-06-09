# Data — Stock Tracker

Place your inventory file here: **`stock.xlsx`**

## Required sheets

| Sheet | Purpose |
|-------|---------|
| `Components` | Parts and stock levels |
| `History` | Stock movements (IN/OUT) |
| `Materials` | Calibrated materials (supplier ref, serial number, description, dates) |

The app creates headers automatically if the file is missing or empty.

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
