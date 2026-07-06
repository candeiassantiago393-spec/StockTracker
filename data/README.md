# Data — Stock Tracker

Place your inventory file here: **`stock.xlsx`**

## Required sheets

| Sheet | Purpose |
|-------|---------|
| `Components` | Active parts and stock levels |
| `Generic` | Passive R/C inventory (resistors, capacitors) |
| `History` | Stock movements (IN/OUT) |
| `Equipments` | Calibrated equipments (supplier ref, serial, **Name**, description, dates, **Datasheet**, **Image**) |
| `EquipmentLoans` | Equipment loan records |

The app creates headers automatically if the file is missing or empty.

## Generated reports

Folder: **`reports/`** (inside `data/`)

PDF inventory exports from the **Statistics** page are saved here. Not versioned in Git — see `reports/README.txt`.

## Equipment files (per equipment)

Folder: **`equipments/{id}/`** (inside `data/`)

Each equipment has its own subfolder (name = Excel **ID**). Store the **datasheet** and **image** there so you can browse or open files directly in Explorer.

Example:

```
data/equipments/
  3/
    DS_Fluke_87V.pdf
    image.jpg
```

From the **Equipments** page:

- **LINK** / **ADD DOC** — copies the file into the selected equipment folder
- **OPEN FOLDER** — opens that equipment folder (or all equipment folders if none selected)
- Excel columns **Datasheet** and **Image** store the **filename** inside that folder

## Component catalog image cache

Folder: **`component_image_cache/`** (inside `data/`)

When you open a component on the **Components** page, its distributor image may be saved here for faster reload.  
**Only viewed components are cached** — the app never scans the whole Excel file to download images.

Automatic limits: **800 images**, **150 MB** total, **90 days** per entry (oldest removed first).

## Catalog link cache (Components)

Folder: **`catalog_links/`** (inside `data/`)

Caches distributor **WEB** and **datasheet URLs** (`_links.json`) for components you have viewed. Refreshed from the API when the cache expires (~30 days).

### Example data (demo)

To load **5 example equipments** (oscilloscope, multimeters, power analyzer, generator):

```powershell
python tools/seed_example_equipments.py
```

Close `stock.xlsx` in Excel before running. Re-run skips equipments already in the workbook.

## Before running the app

- **Close** `stock.xlsx` in Microsoft Excel before save operations
- Keep regular backups of your inventory (the app also saves automatic copies in `data/backups/` — last **20** files)

## Automatic Excel backups

Folder: **`backups/`** (inside `data/`)

Before each save, the app copies `stock.xlsx` to  
`backups/stock_YYYYMMDD_HHMMSS.xlsx` and keeps only the **20 most recent** files.

To restore: close Excel, then copy a backup file over `data/stock.xlsx`.

### Lab cabinet (Stock 1 / 2 / 3 and boxes)

Physical drawer and box labels are stored in the Excel **Location** column (`Components` and `Generic`).  
For the full mapping, open the **newest file** in `data/backups/` (sorted by date in the filename).

See [docs/guias/ARMARIO_LABORATORIO.md](../docs/guias/ARMARIO_LABORATORIO.md) (Portuguese).

## After cloning from GitHub

`stock.xlsx` is **not** in the repository (see root `.gitignore`). Either:

1. Copy your existing file into this folder, or  
2. Run the app once — it will create a new workbook with empty sheets.

Example (adjust paths):

```powershell
copy "path\to\your\stock.xlsx" "data\stock.xlsx"
```
