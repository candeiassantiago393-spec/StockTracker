# Modulo de interface grafica

## Aplicacao principal

| Ficheiro | Papel |
|----------|-------|
| `stock_tracker_window.py` | Janela principal (Components, Equipments, Statistics) |
| `keyboard_shortcuts.py` | Atalhos globais (Ctrl+1/2/3, Ctrl+G, …) |
| `components_massive_mode.py` | Modo Passive (R/C) embarcado em Components |
| `statistics_page.py` | Pagina Statistics + export PDF |
| `catalog_image_preview.py` | Preview interativo da imagem de catalogo |
| `equipments_page.py` | Pagina Equipments (emprestimos, calibracao) |
| `global_search_dialog.py` | Pesquisa global Ctrl+G |
| `optional_location_dialog.py` | Localizacao opcional no stock IN |
| `inventory_report_pdf.py` | Exportacao PDF de inventario |
| `designer/gui_stocktracker.ui` | Layout Components (Qt Designer) |
| `designer/gui_equipments.ui` | Layout Equipments (Qt Designer) |
| `styles.py` | Metricas e estilos Siemens |

### Dialogos

| Ficheiro | Uso |
|----------|-----|
| `massive_dialog.py` | Adicionar/editar passivo R/C |
| `massive_table_dialog.py` | Tabela Passive (Last 20) |
| `components_table_dialog.py` | Tabela Components (Last 20) |
| `equipments_table_dialog.py` | Tabela Equipments (Last 20) |
| `equipment_loan_dialog.py` | Registo de emprestimo |
| `history_dialog.py` | Historico (selecionavel) |
| `manual_component_dialog.py` / `edit_component_dialog.py` | Components manual/edit |
| `search_results_dialog.py` / `equipment_search_dialog.py` | Resultados de pesquisa |

Arranque: `INSTALAR.bat` (primeira vez) · `run.bat` · `python -m src.main`

**Nao** executar ficheiros de `gui/` isoladamente (imports relativos).

## Core relacionado

| Ficheiro | Papel |
|----------|-------|
| `src/core/stock.py` | Excel, stock, equipamentos, passivos |
| `src/core/passive_transfer.py` | Detecao R/C e autofill Package |
| `src/core/inventory_report.py` | Dados para relatorio PDF |

## Ferramentas

| Script | Funcao |
|--------|--------|
| `tools/ORGANIZAR-DESKTOP.bat` | Regenera UI + sync Designer |
| `tools/verificar_entrega.py` | Verificacao pre-entrega |
| `tools/build_project_docx.py` | Documento Word formal |

Documentacao: [docs/entrega/](../../docs/entrega/README.md) · [GUIA_RAPIDO_PT.md](../../docs/guias/GUIA_RAPIDO_PT.md)
