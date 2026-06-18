# Data — Stock Tracker

Place your inventory file here: **`stock.xlsx`**

## Required sheets

| Sheet | Purpose |
|-------|---------|
| `Components` | Parts and stock levels |
| `History` | Stock movements (IN/OUT) |
| `Equipments` | Calibrated equipments (supplier ref, serial, description, dates, **Datasheet**, **Image**) |

The app creates headers automatically if the file is missing or empty.

## Support documentation

Folder: **`support_documentation/`** (inside `data/`)

Store datasheets, manuals and other support files here. From the **Equipments** page:

- **SEARCH** — shows matching files in `doc_results_list` (list is hidden until you search)
- **OPEN** — opens the selected file from the list, or the linked datasheet if the list is hidden
- **LINK** — associates the selected file with the current equipment (saved in Excel column **Datasheet**)
- When you **search equipment**, its linked datasheet opens automatically (if the file exists)
- **ADD DOC** — copies a file; if an equipment is selected, it is linked automatically

## Equipment images

Folder: **`equipment_images/`** (inside `data/`)

From the **Equipments** page: drag & drop an image onto the preview area, or use **Add**.  
Linked filename is stored in Excel column **Image**. Use **Delete** to remove.

## Component catalog image cache

Folder: **`component_image_cache/`** (inside `data/`)

When you open a component on the **Components** page, its distributor image may be saved here for faster reload.  
**Only viewed components are cached** — the app never scans the whole Excel file to download images.

Automatic limits: **800 images**, **150 MB** total, **90 days** per entry (oldest removed first).

### Example data (demo)

Sample datasheets live in `support_documentation/DS_*.pdf`.  
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

## After cloning from GitHub

`stock.xlsx` is **not** in the repository (see root `.gitignore`). Either:

1. Copy your existing file into this folder, or  
2. Run the app once — it will create a new workbook with empty sheets.

Example (adjust paths):

```powershell
copy "path\to\your\stock.xlsx" "data\stock.xlsx"
```
