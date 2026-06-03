# Development environment (VS Code / Cursor)

## Open the project

**File → Open Folder** → select the directory that contains `src/`, `data/`, `requirements.txt`, and `run.bat`.

---

## Python interpreter

1. Terminal: `.\.venv\Scripts\Activate.ps1`
2. Status bar: select `.venv\Scripts\python.exe`

---

## Run and debug

| Method | Steps |
|--------|--------|
| Terminal | `python -m src.main` |
| Shortcut | Double-click `run.bat` |
| Debugger | Open `src/main.py` → F5 (with Python extension) |

**Important:** do not run individual files under `src/gui/` with the Run button; use `python -m src.main` so package imports resolve.

---

## Explorer layout

- **Expand:** `src/core`, top-level files in `src/gui/`
- **Collapse:** `src/gui/siemens_template/`, `.venv/`

---

## Files you will edit often

| File | When |
|------|------|
| `src/core/stock.py` | Business rules, Excel, supplier integration |
| `src/gui/stock_tracker_window.py` | UI behaviour and events |
| `config/secrets.py` | API keys (local only) |
| `data/stock.xlsx` | Inventory data |

---

## Related documentation

- [COMMANDS.md](COMMANDS.md)
- [REPOSITORY_LAYOUT.md](REPOSITORY_LAYOUT.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
