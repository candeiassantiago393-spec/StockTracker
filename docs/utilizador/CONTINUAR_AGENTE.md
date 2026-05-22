# Continuar conversa com o Agent (Cursor)

Cola isto num chat novo no Cursor (pasta do projeto aberta) ou usa:

```
@docs/utilizador/CONTINUAR_AGENTE.md continua o Stock Tracker a partir daqui
```

---

## Projeto correto (nao e o legado)

| Usar | Nao usar |
|------|----------|
| `C:\Users\z005027j\Downloads\StockTracker\StockTracker` | `Documents\stock-tracker` (legado) |

Abrir no Cursor: **File → Open Folder** → pasta que contem `src`, `config`, `run.bat`.

---

## Estado atual (resumo)

- **Stack:** Python, PySide6, openpyxl, requests, Excel `data/stock.xlsx`
- **API ativa:** **Mouser** apenas (`MOUSER_API_KEY` em `config/secrets.py`)
- **DigiKey:** removido do codigo (tentativa anterior: token OK, pesquisa 403 no portal sandbox)
- **TME / Robert Mauser:** stubs em `src/core/suppliers/` (sem API real ainda)

---

## Arquitetura (regras do tutor)

| Camada | Onde | Papel |
|--------|------|--------|
| Entrada GUI | `src/main.py` | Arranca PySide6 → `StockTrackerWindow` |
| Testes terminal | `src/test_terminal.py` | Menu 1–9, 0 (Mouser: 5 e 6) |
| Logica | `src/core/stock.py` | Classe `StockTracker` — Excel, stock IN/OUT, historico, Mouser |
| API Mouser | `src/core/suppliers/mouser.py` | HTTP Mouser |
| Formato resultados | `src/core/suppliers/base.py` | `normalize_part()` |
| GUI layout | `src/gui/ui_stock_tracker.py` | Widgets |
| GUI eventos | `src/gui/stock_tracker_window.py` | Botoes → chama `self.tracker` |
| Historico | `src/gui/history_dialog.py` | Popup historico |
| Credenciais | `config/secrets.py` | Chave real (gitignore) |
| Loader | `config/credentials.py` | `load_secrets()` → dict para `stock.py` |
| Template exemplo | `config/secrets.example.py` | Modelo sem chaves reais |

**Regras:** sem logica de negocio na GUI; nao executar ficheiros em `gui/` isoladamente.

---

## Credenciais

```python
# config/secrets.py (editar aqui)
MOUSER_API_KEY = "..."
```

Fluxo: `secrets.py` → `credentials.load_secrets()` → `StockTracker._secrets` / `api_key` → `mouser.search()`.

---

## Comandos

```powershell
cd C:\Users\z005027j\Downloads\StockTracker\StockTracker
.\.venv\Scripts\activate
python -m src.main           # GUI (ou duplo clique run.bat)
python -m src.test_terminal  # consola de testes
```

Erro `No module named 'src'`: pasta errada (falta um nivel `StockTracker` no caminho).

---

## Pastas na raiz

| Pasta | Funcao |
|-------|--------|
| `src/` | Codigo da aplicacao |
| `config/` | secrets + loader |
| `data/` | `stock.xlsx` (fechar Excel antes de gravar) |
| `docs/` | Documentacao humana |
| `tools/` | Scripts pontuais (nao e o arranque da app) |
| `.cursor/rules/` | Regras automaticas para o Agent |
| `.venv/` | Ambiente Python |

---

## Ficheiros para @ no Cursor (demo ao tutor)

1. `src/core/stock.py`
2. `src/gui/stock_tracker_window.py`
3. `src/main.py`
4. `config/secrets.py` (nao partilhar chave em gravacao)
5. `src/core/suppliers/mouser.py` (se falar da API)

---

## Fornecedores (`src/core/suppliers/`)

| Ficheiro | Estado |
|----------|--------|
| `mouser.py` | Implementado |
| `base.py` | Formato comum PartInfo |
| `tme.py` | Stub futuro |
| `robert_mauser.py` | Sem API publica — so mensagem |
| `__init__.py` | Encaminha `search_part()` |

---

## GUI (`src/gui/`)

- `ui_stock_tracker.py` = desenho da janela
- `stock_tracker_window.py` = cliques e chamadas a `StockTracker`
- `siemens_template/` = exemplos Siemens (referencia, nao e o fluxo principal)

---

## O que ja foi feito na conversa anterior

- Projeto reorganizado (core / gui / config / docs)
- Chaves em `config/secrets.py` (nao no codigo)
- Documentacao em `docs/utilizador/`
- Integracao DigiKey testada e depois **removida** a pedido do utilizador
- Utilizador aprendeu estrutura: config, src, suppliers, gui, main.py

---

## Possiveis proximos passos

- Relatorio de estagio — rascunho em [RELATORIO_ESTAGIO.md](RELATORIO_ESTAGIO.md)
- Melhorias GUI ou validacoes (ex.: mensagens em portugues)
- TME se o tutor pedir
- GitHub: `git init` na raiz (ainda sem repositorio); nao commitar `secrets.py` nem `data/stock.xlsx`

---

## Mensagem curta para colar no Agent

```
Stock Tracker — pasta Downloads\StockTracker\StockTracker.
Mouser only. Logic in src/core/stock.py, GUI in src/gui/, entry src/main.py.
Read @docs/utilizador/CONTINUAR_AGENTE.md and help me continue.
Responde em portugues quando fizer sentido.
```

---

## Documentacao relacionada

- [ORGANIZACAO.md](ORGANIZACAO.md) — pastas
- [ARQUITETURA.md](ARQUITETURA.md) — fluxos
- [COMANDOS.md](COMANDOS.md) — instalacao e erros
- [FORNECEDORES.md](FORNECEDORES.md) — Mouser / futuros
