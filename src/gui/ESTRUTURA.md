# Modulo de interface grafica

## Aplicacao principal

| Ficheiro | Papel |
|----------|-------|
| `stock_tracker_window.py` | Janela principal (Components + navegacao Equipments) |
| `equipments_page.py` | Pagina Equipments (logica; layout em `designer/gui_equipments.ui`; imagem, lista `doc_results_list` oculta ate SEARCH) |
| `designer/gui_stocktracker.ui` | Layout Components (Qt Designer) |
| `designer/gui_equipments.ui` | Layout Equipments (Qt Designer) |
| `designer/gui_stocktracker.py` | Export `pyside6-uic` — nao editar a mao |
| `designer/gui_equipments.py` | Export `pyside6-uic` — nao editar a mao |
| `styles.py` | Metricas e estilos Siemens (template) |
| `gui_config.py` | Caminhos de logos |

### Dialogos

| Ficheiro | Template |
|----------|----------|
| `message_dialog.py` | `popups/shared/gui_popup_confirm.ui` |
| `user_name_dialog.py` | `popups/shared/gui_popup_confirm.ui` |
| `confirm_dialog.py` | confirm |
| `history_dialog.py` | `popups/components/gui_popup_history.ui` |
| `manual_component_dialog.py` | `popups/components/gui_popup_manual.ui` |
| `edit_component_dialog.py` | `popups/components/gui_popup_edit.ui` |
| `search_results_dialog.py` | `popups/components/gui_popup_search.ui` |
| `equipment_search_dialog.py` | `popups/equipments/gui_popup_search.ui` |
| `equipments_table_dialog.py` | `popups/equipments/gui_popup_history.ui` |
| `equipment_dialog.py` | `popups/equipments/gui_popup_equipment.ui` |

Arranque: `python -m src.main` ou `run.bat` na raiz.

**Nao** executar ficheiros de `gui/` isoladamente (imports relativos).

## Pasta `designer/`

Ver [designer/README.md](designer/README.md) — gerar, exportar e sincronizar com Qt Designer.

Pacote de edicao: `StockTracker-Designer/` na raiz do repo (espelho para o Qt Designer).

## Template Siemens (`siemens_template/`)

Icones, fontes e widgets de referencia. A janela usa `designer/*.ui`; metricas em `styles.py` alinhadas com `siemens_template/gui_template.ui`.

## Ferramentas

| Comando / script | Funcao |
|------------------|--------|
| `tools/ORGANIZAR-DESKTOP.bat` | Regenera `.ui`, exporta `.py`, sincroniza Designer + Desktop |
| `tools/generate_all_designer_uis.py` | Regenera todos os `.ui` |
| `tools/gui_ui_builder.py` | Builders partilhados (template) |
| `tools/export-ui.bat` | Exporta `.ui` → `.py` |
| `tools/sync_designer_package.ps1` | Atualiza `StockTracker-Designer/` (repo e/ou Desktop) |
| `tools/ABRIR-DESIGNER.bat` | Abre Components ou Equipments no Designer |

Documentacao: [docs/GUIA_RAPIDO_PT.md](../../docs/GUIA_RAPIDO_PT.md) · [designer/EQUIPMENTS-LEIA-ME.txt](designer/EQUIPMENTS-LEIA-ME.txt)
