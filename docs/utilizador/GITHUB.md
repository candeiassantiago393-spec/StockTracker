# Publicar no GitHub (Cursor terminal)

## Antes de fazer push

- [ ] `config/secrets.py` **não** vai para o Git (está no `.gitignore`)
- [ ] Só placeholders em `config/secrets.example.py`
- [ ] `data/stock.xlsx` não vai (dados locais)
- [ ] `.venv/` não vai

Verificar:

```powershell
cd C:\Users\z005027j\Downloads\StockTracker\StockTracker
git status
git check-ignore -v config/secrets.py
```

---

## 1. Criar repositório no GitHub

1. Abre https://github.com/new
2. Nome: `StockTracker` (ou outro)
3. **Private** (recomendado — estágio Siemens)
4. **Não** marques "Add README" (já tens um local)
5. Cria o repositório e copia a URL, ex.:  
   `https://github.com/TEU_USER/StockTracker.git`

---

## 2. No terminal do Cursor (PowerShell)

```powershell
cd C:\Users\z005027j\Downloads\StockTracker\StockTracker
```

### Adicionar ficheiros e commit

```powershell
git add .
git status
```

Confirma que **não** aparece `config/secrets.py` nem `data/stock.xlsx`.

```powershell
git commit -m "$(cat <<'EOF'
Add Siemens UI, Qt Designer workflow, multi-supplier APIs and demo mode.

EOF
)"
```

### Ligar ao GitHub e enviar

Substitui `TEU_USER` pelo teu utilizador GitHub:

```powershell
git remote add origin https://github.com/TEU_USER/StockTracker.git
git branch -M main
git push -u origin main
```

Se o remote `origin` já existir:

```powershell
git remote set-url origin https://github.com/TEU_USER/StockTracker.git
git push -u origin main
```

---

## 3. Login GitHub (se pedir)

- **Browser:** segue o link que o Git pede
- **Token:** Settings → Developer settings → Personal access tokens
- **gh CLI:** `gh auth login` (se tiveres GitHub CLI instalado)

---

## 4. Depois do primeiro push

Clonar noutro PC:

```powershell
git clone https://github.com/TEU_USER/StockTracker.git
cd StockTracker
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy config\secrets.example.py config\secrets.py
# editar secrets.py com as tuas chaves
python -m src.main
```

---

## Comandos úteis

| Ação | Comando |
|------|---------|
| Ver alterações | `git status` |
| Ver diff | `git diff` |
| Commit seguinte | `git add .` → `git commit -m "mensagem"` → `git push` |
| Ver remote | `git remote -v` |

---

## O que vai no repositório

| Incluído | Excluído (.gitignore) |
|----------|------------------------|
| Código `src/`, `config/*.example.py` | `config/secrets.py` |
| `docs/`, `tools/`, `scripts/` | `.venv/` |
| `gui_stocktracker.ui` + export `.py` | `data/stock.xlsx` |
| Template Siemens | Chaves API reais |
