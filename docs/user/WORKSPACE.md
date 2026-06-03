# Workspace and optional project copies

## Canonical repository

Develop, run tests, and use Git in **one** primary clone of the repository (the folder you open in your IDE).

That folder must contain:

- `src/`, `config/`, `data/`, `docs/`, `tools/`
- `run.bat`, `requirements.txt`, `.venv/` (local)

---

## Optional mirror (backup or USB)

Script: `tools/sincronizar-desktop.ps1`

Copies the project to a destination folder (configured in the script). It **excludes**:

- `config/secrets.py`
- `.venv/`
- `.git/` (depending on script options)

Run after meaningful changes if you keep an offline copy.

---

## Qt Designer–only folder (optional)

Some teams keep a slim folder with:

- `gui_stocktracker.ui`
- `src/gui/siemens_template/` resources

for layout review on a machine without the full dev environment. The full application still builds from the main repository.

---

## Do not mix legacy trees

Older folders named `stock-tracker` or duplicate templates on the desktop are not maintained. Use only the current repository as the source of truth.
