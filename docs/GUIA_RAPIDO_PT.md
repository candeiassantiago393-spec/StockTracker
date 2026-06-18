# Guia rápido — Stock Tracker (PT)

Documentação operacional em português. Especificação completa: [PROJETO_STOCKTRACKER_PT.md](PROJETO_STOCKTRACKER_PT.md).

---

## Arrancar a aplicação

```powershell
cd Downloads\StockTracker\StockTracker
.\.venv\Scripts\Activate.ps1
python -m src.main
```

Ou duplo-clique em `run.bat`.

---

## Duas páginas na GUI

| Página | Botão no header | Excel |
|--------|-----------------|-------|
| **Components** | COMPONENTS | Folha `Components` + movimentos em `History` |
| **Equipments** | EQUIPMENTS | Folha `Equipments` (equipamentos calibrados) |

Barra inferior partilhada: Last 20, histórico, ADD MANUAL, EDIT, OPEN EXCEL, CLEAR, Exit.

---

## Dados (`data/stock.xlsx`)

| Folha | Conteúdo |
|-------|----------|
| `Components` | Peças e stock |
| `Equipments` | Supplier Reference, Serial Number, Description, datas de calibração, Datasheet, Image |
| `History` | Movimentos IN/OUT |

Fechar o Excel antes de gravar. Ver [data/README.md](../data/README.md).

---

## Qt Designer (editar o aspeto)

### Pastas

| Local | Uso |
|-------|-----|
| `src/gui/designer/` | **Canónico** — a app importa daqui |
| `StockTracker-Designer/` | Pacote no repo para editar no Designer |
| `Desktop\StockTracker-Designer` | Cópia no Ambiente de Trabalho |

### Ficheiros principais

| Ficheiro | Página |
|----------|--------|
| `gui_stocktracker.ui` | Components (DESIGNER.bat opção **1**) |
| `gui_equipments.ui` | Equipments (DESIGNER.bat opção **2**) |
| `popups/components/gui_popup_*.ui` | Diálogos Components (opções **3–6**) |
| `popups/equipments/gui_popup_*.ui` | Diálogos Equipments (opções **7–9**) |
| `popups/shared/gui_popup_*.ui` | Confirm + template (opções **10–11**) |

Guia Equipments (layout Qt Designer + objectNames): `src/gui/designer/EQUIPMENTS-LEIA-ME.txt`

### Organizar tudo (repo + Desktop)

Na raiz do projeto:

```text
tools\ORGANIZAR-DESKTOP.bat
```

Regenera `.ui`, exporta `.py`, sincroniza Designer e copia o projeto para `Desktop\StockTracker-Projeto`.

### Depois de editar um `.ui`

1. Copiar o `.ui` alterado para `src\gui\designer\`
2. `tools\export-ui.bat`
3. `python -m src.main`

---

## Estrutura do código

| Camada | Pasta / ficheiro |
|--------|------------------|
| Entrada | `src/main.py` |
| Lógica | `src/core/stock.py` |
| GUI Components | `src/gui/stock_tracker_window.py` + `designer/gui_stocktracker.ui` |
| GUI Equipments | `src/gui/equipments_page.py` + `designer/gui_equipments.ui` |
| Estilos template | `src/gui/styles.py`, `tools/gui_ui_builder.py` |
| Credenciais | `config/secrets.py` (não commitar) |

Mapa da GUI: [src/gui/ESTRUTURA.md](../src/gui/ESTRUTURA.md)

---

## Documentação em inglês

Índice: [docs/README.md](README.md) — COMMANDS, ARCHITECTURE, QT_DESIGNER, WORKSPACE, etc.
