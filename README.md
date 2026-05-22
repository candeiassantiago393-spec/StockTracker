# Stock Tracker

**Electronic component inventory — Siemens internship project.**

Desktop app for stock management with an Excel database, PySide6 GUI (Siemens-style UI), and distributor API integration (Mouser active; DigiKey, TME, RS prepared).

> **Documentation in Portuguese:** see [`docs/`](docs/README.md) (architecture, commands, suppliers, internship report draft).

---

## Features

- Excel inventory (`Components` + `History` sheets)
- GUI: search, barcode/scan, stock IN/OUT, history viewer
- **Multi-match search** in Excel with selection dialog
- **Autocomplete** from Excel (search field + barcode/Mouser reference field)
- Mouser API: lookup and import new parts
- Modular suppliers: `src/core/suppliers/` (Mouser, DigiKey, TME, RS, Robert Mauser stub)
- Terminal test menu: `python -m src.test_terminal`
- Clear split: business logic in `core/`, UI in `gui/`

---

## Requirements

- Windows 10/11
- Python 3.10+
- Internet (Mouser API)
- Close `data/stock.xlsx` in Excel before saving from the app

---

## Quick start

```powershell
git clone https://github.com/YOUR_USER/StockTracker.git
cd StockTracker
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy config\secrets.example.py config\secrets.py
```

1. Edit `config/secrets.py` — set `MOUSER_API_KEY` (and other keys if needed).
2. Add your inventory file: `data/stock.xlsx` (see [`data/README.md`](data/README.md)).
3. Run:

```powershell
python -m src.main
```

Or double-click `run.bat`.

---

## Configuration

| File | Purpose |
|------|---------|
| `config/secrets.py` | API keys (**local only**, not in Git) |
| `config/secrets.example.py` | Template for secrets |
| `data/stock.xlsx` | Inventory database (**not in Git** by default) |

Never commit `config/secrets.py` or real API keys.

---

## Project structure

```
StockTracker/
├── config/          # credentials loader + secrets.example.py
├── data/            # stock.xlsx (local, gitignored)
├── docs/            # user & architecture docs (PT)
├── src/
│   ├── main.py      # GUI entry point
│   ├── test_terminal.py
│   ├── core/        # StockTracker + suppliers
│   └── gui/         # PySide6 UI
├── tools/           # maintenance scripts
├── requirements.txt
└── run.bat
```

| Layer | Location | Role |
|-------|----------|------|
| Entry | `src/main.py` | Starts GUI |
| Business | `src/core/stock.py` | Excel, stock, history, APIs |
| UI | `src/gui/` | Events, dialogs, styles |
| Suppliers | `src/core/suppliers/` | Mouser, DigiKey, TME, RS, … |

---

## Documentation

| Document | Content |
|----------|---------|
| [docs/README.md](docs/README.md) | Documentation index |
| [docs/utilizador/COMANDOS.md](docs/utilizador/COMANDOS.md) | Install, run, troubleshooting |
| [docs/utilizador/ARQUITETURA.md](docs/utilizador/ARQUITETURA.md) | Architecture & flows |
| [docs/utilizador/FORNECEDORES.md](docs/utilizador/FORNECEDORES.md) | API suppliers |
| [docs/utilizador/CONTINUAR_AGENTE.md](docs/utilizador/CONTINUAR_AGENTE.md) | Handover notes for development |

---

## Publish to GitHub

Repository is already a Git repo. After creating an empty repo on GitHub:

```powershell
git remote add origin https://github.com/YOUR_USER/StockTracker.git
git branch -M main
git push -u origin main
```

**GitHub repository description (short):**

```
Desktop electronic component inventory (Excel + PySide6 + Mouser API). Siemens internship project.
```

---

## Development notes

- Run as module: `python -m src.main` (do not run `gui/*.py` directly).
- Legacy project path (do not mix): `Documents\stock-tracker`.

---

## Resumo (PT)

Aplicação de inventário de componentes eletrónicos: Excel, interface Siemens (PySide6), API Mouser, pesquisa com lista de resultados e sugestões ao escrever. Projeto de estágio — uso interno.
