# Commands and operations

Run all commands from the **repository root** (folder containing `src/`, `config/`, `run.bat`).

```powershell
cd path\to\StockTracker
```

---

## Virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Run the application

| Action | Command |
|--------|---------|
| Graphical UI | `python -m src.main` or double-click `run.bat` |
| Terminal test menu | `python -m src.test_terminal` |

---

## Configure API keys

```powershell
copy config\secrets.example.py config\secrets.py
```

Edit `config/secrets.py` with your keys. See [SUPPLIERS.md](SUPPLIERS.md) and [DIGIKEY_SETUP.md](DIGIKEY_SETUP.md).

---

## Verify working directory

```powershell
dir src
dir config
```

If `src` is missing, change to the repository root (not a parent or child folder by mistake).

---

## Terminal test menu (summary)

| Option | Function |
|--------|----------|
| 1 | Search Excel |
| 2 | Lookup by code / scan |
| 3 | Stock IN |
| 4 | Stock OUT (with confirmation) |
| 5 | Distributor catalog lookup (no save) |
| 6 | Catalog → Excel → IN |
| 7 | List components |
| 8 | Last 20 history rows |
| 9 | Change user name |
| 10 | Add manual component |
| 0 | Exit |

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `No module named 'src'` | Wrong directory | `cd` to repo root |
| `ImportError: relative import` | GUI file run directly | `python -m src.main` |
| Excel not saved | `stock.xlsx` open in Excel | Close the file |
| API no response | Keys / network / part number | Check `config/secrets.py` |
| Insufficient stock | OUT quantity too high | Check current stock |

---

## Git (optional)

```powershell
git status
git add .
git commit -m "Describe your change"
git push
```

Never commit `config/secrets.py` or real API keys.
