# Ambiente de desenvolvimento (VS Code)

## Abrir o projeto

**File → Open Folder** → selecionar a pasta que contem `src/`, `data/`, `requirements.txt` e `run.bat`.

---

## Interpretador Python

1. Terminal: `.\.venv\Scripts\activate`
2. Canto inferior direito: selecionar `.venv\Scripts\python.exe`

---

## Executar e depurar

| Metodo | Procedimento |
|--------|--------------|
| Terminal | `python -m src.main` |
| Atalho | Duplo clique em `run.bat` |
| Depuracao | Abrir `src/main.py` → F5 |

**Importante:** nao executar ficheiros individuais em `src/gui/` com o botao Run; utilizar sempre `python -m src.main`.

---

## Organizacao no Explorer

- **Expandir:** `src/core`, ficheiros em `src/gui/` (raiz da pasta gui)
- **Colapsar:** `src/gui/siemens_template/`, `.venv/`

---

## Ficheiros de trabalho frequentes

| Ficheiro | Quando editar |
|----------|----------------|
| `src/core/stock.py` | Regras de negocio |
| `src/gui/stock_tracker_window.py` | Comportamento da interface |
| `config/secrets.py` | Chave Mouser (local) |
| `data/stock.xlsx` | Dados de inventario |

---

## Documentacao relacionada

- [COMANDOS.md](COMANDOS.md)
- [ORGANIZACAO.md](ORGANIZACAO.md)
- [ARQUITETURA.md](ARQUITETURA.md)
