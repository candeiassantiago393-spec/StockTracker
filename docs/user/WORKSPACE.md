# Workspace and optional project copies

## Canonical repository

Develop, run tests, and use Git in **one** primary clone:

`Downloads\StockTracker\StockTracker`

That folder must contain:

- `src/`, `config/`, `data/`, `docs/`, `tools/`
- `run.bat`, `requirements.txt`, `.venv/` (local)
- `StockTracker-Designer/` — Qt Designer package (mirror for editing `.ui`)

---

## Desktop folders (optional)

| Folder | Purpose |
|--------|---------|
| `Desktop\StockTracker-Projeto` | Full project copy (no `.git`, no `secrets.py`, no `.venv`) |
| `Desktop\StockTracker-Designer` | Qt Designer only — edit `.ui` files |

Refresh both from the canonical repo:

```text
tools\ORGANIZAR-DESKTOP.bat
```

or:

```powershell
powershell -File tools\organizar-ambiente.ps1
```

---

## Qt Designer — Components and Materials

| File | Page |
|------|------|
| `gui_stocktracker.ui` | Components (`DESIGNER.bat` option **1**) |
| `gui_materials.ui` | Materials (`DESIGNER.bat` option **2**) |
| `popups\components\` | Components dialogs (options **3–6**) |
| `popups\materials\` | Materials dialogs (options **7–9**) |
| `popups\shared\` | Confirm + Siemens template |

Quick guides (Portuguese): `StockTracker-Designer\LEIA-ME.txt` · `MATERIALS-LEIA-ME.txt`

**Workflow after editing `.ui` on Desktop:**

1. Copy changed `.ui` to `src\gui\designer\` in the main repo
2. Run `tools\export-ui.bat`
3. Run `python -m src.main`

---

## Do not mix legacy trees

Older folders named `stock-tracker` or duplicate templates on the desktop are not maintained. Use only the current repository as the source of truth.
