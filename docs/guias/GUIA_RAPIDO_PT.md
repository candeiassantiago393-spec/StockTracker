# Guia rápido — Stock Tracker (PT)

Documentação operacional em português.

| Documento | Conteúdo |
|-----------|----------|
| Especificação | [PROJETO_STOCKTRACKER_PT.md](../especificacao/PROJETO_STOCKTRACKER_PT.md) |
| Entrega Siemens | [docs/entrega/](../entrega/README.md) |

---

## Primeira instalação

```powershell
cd Downloads\StockTracker\StockTracker
.\INSTALAR.bat
copy config\secrets.example.py config\secrets.py
# Editar config\secrets.py com as chaves API
.\run.bat
```

Verificar: `python tools\verificar_entrega.py`

---

## Arrancar a aplicação

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.main
```

Ou duplo-clique em `run.bat`.

---

## Páginas na GUI

| Página | Atalho | Excel |
|--------|--------|-------|
| **Components** | `Ctrl+1` | Folha `Components` |
| **Passive (R/C)** | `Ctrl+Shift+M` (dentro de Components) | Folha `Generic` |
| **Equipments** | `Ctrl+2` | Folha `Equipments` |
| **Statistics** | `Ctrl+3` | Relatórios (export PDF) |

Barra inferior: Last 20, histórico, ADD MANUAL, EDIT, OPEN EXCEL, CLEAR, Exit.

**Pesquisa global** (`Ctrl+G`): procura em Components, Passive e Equipments.

---

## Dados (`data/stock.xlsx`)

| Folha | Conteúdo |
|-------|----------|
| `Components` | Componentes activos |
| `Generic` | Passivos R/C (resistores, condensadores) |
| `Equipments` | Equipamentos calibrados |
| `EquipmentLoans` | Empréstimos de equipamentos |
| `History` | Movimentos IN/OUT |

Fechar o Excel antes de gravar. Ver [data/README.md](../../data/README.md).

Relatórios PDF: `data/reports/` (Statistics → EXPORT PDF).

---

## Modo Passive (R/C)

1. Na página Components, pressione `Ctrl+Shift+M` ou use o botão de modo.
2. Scan ou pesquisa por referência de fornecedor / valor (`10k`, `100nF`, …).
3. Ao adicionar passivo, o campo **Package** pode preencher-se automaticamente pela **Supplier Ref** (catálogo ou Excel).
4. Localização opcional após ADD STOCK.

---

## Qt Designer (editar o aspeto)

### Pastas

| Local | Uso |
|-------|-----|
| `src/gui/designer/` | **Canónico** — a app importa daqui |
| `StockTracker-Designer/` | Pacote no repo para editar no Designer |
| `Desktop\StockTracker-Designer` | Cópia no Ambiente de Trabalho |

### Organizar tudo (repo + Desktop)

```text
tools\ORGANIZAR-DESKTOP.bat
```

### Depois de editar um `.ui`

1. Copiar o `.ui` alterado para `src\gui\designer\`
2. `tools\export-ui.bat`
3. `python -m src.main`

---

## Components — imagem de catálogo

Preview interativo com lupa, zoom (roda do rato) e cache local.

Lógica: `src/core/component_images.py` + `src/gui/catalog_image_preview.py`

---

## Estrutura do código

| Camada | Pasta / ficheiro |
|--------|------------------|
| Entrada | `src/main.py` |
| Lógica | `src/core/stock.py` |
| Passivos R/C | `src/core/passive_transfer.py` |
| GUI principal | `src/gui/stock_tracker_window.py` |
| Equipments | `src/gui/equipments_page.py` |
| Statistics | `src/gui/statistics_page.py` |
| Credenciais | `config/secrets.py` (não commitar) |

Mapa da GUI: [src/gui/ESTRUTURA.md](../../src/gui/ESTRUTURA.md)

---

## Atalhos de teclado

| Atalho | Ação |
|--------|------|
| `Ctrl+1` / `Ctrl+2` / `Ctrl+3` | COMPONENTS / EQUIPMENTS / STATISTICS |
| `Ctrl+G` | Pesquisa global |
| `Ctrl+F` | Foco na pesquisa |
| `F6` | Foco no código de barras / ref. fornecedor |
| `F2` | Foco na quantidade |
| `F4` | Foco no utilizador |
| `Enter` | Scan ou pesquisa (conforme o campo) |
| `Ctrl+Enter` | Pesquisar |
| `F5` | SCAN |
| `Ctrl+I` / `Ctrl+U` | Stock IN / OUT |
| `Ctrl+N` | ADD MANUAL |
| `Ctrl+E` | EDIT |
| `Ctrl+H` | Histórico do item |
| `Ctrl+Shift+H` | Last 20 |
| `Ctrl+Shift+E` | OPEN EXCEL |
| `Ctrl+Shift+M` | Alternar Components / Passive (R/C) |
| `Esc` | CLEAR (fora de campos de texto) |

Os botões mostram o atalho no tooltip.

---

## Documentação completa

Índice: [docs/README.md](../README.md)
