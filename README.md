# Stock Tracker

**Sistema de inventario de componentes eletronicos** — estagio Siemens.

Gestao de stock em Excel, integracao com a API Mouser e interface desktop PySide6 alinhada com o design system Siemens.

---

## Funcionalidades

- Pesquisa e consulta de componentes no inventario (Excel)
- Leitura de codigos de barras / referencias Mouser
- Entrada e saida de stock com registo em historico
- Importacao de novos componentes via API Mouser
- Interface grafica com validacao de utilizador e confirmacao de remocoes

---

## Requisitos

- Windows 10/11
- Python 3.10 ou superior
- Microsoft Excel (ficheiro `data/stock.xlsx` deve estar **fechado** durante operacoes de gravacao)
- Ligacao a Internet (consultas Mouser)

---

## Instalacao

```powershell
cd C:\Users\z005027j\Downloads\StockTracker\StockTracker
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Chave API Mouser

```powershell
copy config\secrets.example.py config\secrets.py
```

Editar `config/secrets.py` e definir `MOUSER_API_KEY`. O ficheiro `secrets.py` nao e versionado (`.gitignore`).

---

## Utilizacao

| Metodo | Acao |
|--------|------|
| **Duplo clique** | `run.bat` |
| **Terminal** | `python -m src.main` |
| **Testes CLI** | `python -m src.test_terminal` |

---

## Arquitetura

```
src/
├── main.py                 # Entrada da aplicacao
├── test_terminal.py        # Consola de testes (desenvolvimento)
├── core/
│   └── stock.py            # Logica de negocio (StockTracker)
└── gui/
    ├── stock_tracker_window.py
    ├── ui_stock_tracker.py
    ├── history_dialog.py
    ├── styles.py
    └── siemens_template/   # Templates oficiais Siemens (referencia)
```

| Camada | Responsabilidade |
|--------|------------------|
| `core/stock.py` | Excel, API Mouser, movimentos de stock, historico |
| `gui/` | Interacao, validacoes de utilizador, confirmacoes |
| `data/stock.xlsx` | Base de dados (folhas Components e History) |

---

## Documentacao

| Documento | Conteudo |
|-----------|----------|
| [docs/README.md](docs/README.md) | Indice da documentacao |
| [docs/utilizador/COMANDOS.md](docs/utilizador/COMANDOS.md) | Comandos e resolucao de problemas |
| [docs/utilizador/ORGANIZACAO.md](docs/utilizador/ORGANIZACAO.md) | Estrutura do repositorio |
| [docs/utilizador/ARQUITETURA.md](docs/utilizador/ARQUITETURA.md) | Decisoes tecnicas e fluxos |
| [src/gui/ESTRUTURA.md](src/gui/ESTRUTURA.md) | Modulo de interface grafica |

---

## Estrutura do repositorio

```
StockTracker/
├── config/           # Credenciais (secrets.py local)
├── data/             # stock.xlsx
├── docs/             # Documentacao
├── src/              # Codigo fonte
├── tools/            # Scripts de manutencao
├── requirements.txt
└── run.bat
```

---

## Notas de desenvolvimento

- Nao executar ficheiros em `src/gui/` diretamente (ex.: `history_dialog.py`); usar `python -m src.main`.
- Separacao obrigatoria: logica em `core/`, interface em `gui/`.
- Projeto de referencia antigo: `Documents\stock-tracker` (nao misturar com este repositorio).

---

*Stock Tracker — projeto de estagio. Uso interno.*
