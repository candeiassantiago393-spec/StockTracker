# Organizacao do repositorio

## Visao geral

| Pasta | Proposito |
|-------|-----------|
| `src/core/` | Logica de negocio (`StockTracker`) |
| `src/gui/` | Interface PySide6 da aplicacao |
| `src/gui/siemens_template/` | Templates oficiais Siemens (referencia) |
| `data/` | Base de dados Excel (`stock.xlsx`) |
| `config/` | Configuracao local (`secrets.py`) |
| `docs/` | Documentacao do projeto |
| `tools/` | Scripts de manutencao pontual |

---

## Codigo fonte (`src/`)

| Ficheiro | Funcao |
|----------|--------|
| `main.py` | Ponto de entrada — inicia a GUI |
| `test_terminal.py` | Consola de testes (desenvolvimento) |
| `core/stock.py` | Classe `StockTracker` — Excel, Mouser, stock |
| `gui/stock_tracker_window.py` | Janela principal e eventos |
| `gui/ui_stock_tracker.py` | Definicao visual da janela |
| `gui/history_dialog.py` | Dialogo de historico |
| `gui/styles.py` | Folhas de estilo Siemens |

---

## Configuracao

1. Copiar `config/secrets.example.py` para `config/secrets.py`
2. Inserir `MOUSER_API_KEY`
3. Colocar ou atualizar `data/stock.xlsx`
4. Fechar o Excel antes de gravar alteracoes

---

## Execucao correta

| Correto | Incorreto |
|---------|-----------|
| `python -m src.main` | `python src/gui/history_dialog.py` |
| `run.bat` | Executar modulos com imports relativos (`from .`) |

---

## Projeto legado

`Documents\stock-tracker` — implementacao anterior. Utilizar apenas como referencia; o projeto de estagio e este repositorio em `Downloads\StockTracker\StockTracker`.
