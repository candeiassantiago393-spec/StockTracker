# Publishing to GitHub

## Before pushing

- [ ] `config/secrets.py` is **not** tracked (listed in `.gitignore`)
- [ ] Only placeholders in `config/secrets.example.py`
- [ ] `data/stock.xlsx` is not committed (local inventory by default)
- [ ] `.venv/` is not committed

Verify:

```powershell
cd path\to\StockTracker
git status
git check-ignore -v config/secrets.py
```

---

## 1. Create a GitHub repository

1. Open https://github.com/new
2. Name: `StockTracker` (or your choice)
3. Choose **Private** if the codebase is internal
4. Do **not** add a README if this repository already has one locally
5. Copy the remote URL, e.g. `https://github.com/YOUR_ORG/StockTracker.git`

---

## 2. Initial push

From the repository root:

```powershell
git add .
git status
```

Confirm that `config/secrets.py` and `data/stock.xlsx` do **not** appear as staged files.

```powershell
git commit -m "Initial commit: Stock Tracker desktop application"
git remote add origin https://github.com/YOUR_ORG/StockTracker.git
git branch -M main
git push -u origin main
```

If `origin` already exists:

```powershell
git remote set-url origin https://github.com/YOUR_ORG/StockTracker.git
git push -u origin main
```

---

## 3. Authentication

- **Browser:** follow the prompt from Git Credential Manager
- **Personal access token:** GitHub → Settings → Developer settings → Tokens
- **GitHub CLI:** `gh auth login`

---

## 4. Clone on another machine

```powershell
git clone https://github.com/YOUR_ORG/StockTracker.git
cd StockTracker
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy config\secrets.example.py config\secrets.py
# Edit secrets.py with your API keys
python -m src.main
```

---

## Useful commands

| Action | Command |
|--------|---------|
| View status | `git status` |
| View diff | `git diff` |
| New commit | `git add .` → `git commit -m "message"` → `git push` |
| View remotes | `git remote -v` |

---

## What belongs in the repository

| Included | Excluded (`.gitignore`) |
|----------|-------------------------|
| `src/`, `docs/`, `tools/`, `scripts/` | `config/secrets.py` |
| `config/secrets.example.py` | `.venv/`, `__pycache__/` |
| `gui_stocktracker.ui` and generated UI | `data/stock.xlsx` (default) |
| Siemens template assets | Real API keys |
