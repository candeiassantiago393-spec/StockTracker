# Modulo de interface grafica

## Aplicacao principal

| Ficheiro | Papel |
|----------|-------|
| `stock_tracker_window.py` | Janela principal (Components + navegacao Materials) |
| `materials_page.py` | Pagina Materials (logica; layout em `designer/gui_materials.ui`) |
| `designer/gui_stocktracker.ui` | Layout Components (Qt Designer) |
| `designer/gui_materials.ui` | Layout Materials (Qt Designer) |
| `designer/gui_stocktracker.py` | Export `pyside6-uic` — nao editar a mao |
| `designer/gui_materials.py` | Export `pyside6-uic` — nao editar a mao |
| `styles.py` | Metricas e estilos Siemens (template) |
| `gui_config.py` | Caminhos de logos |

### Dialogos

| Ficheiro | Template |
|----------|----------|
| `message_dialog.py` | `popups/gui_popup_confirm.ui` |
| `user_name_dialog.py` | `popups/gui_popup_confirm.ui` |
| `confirm_dialog.py` | confirm |
| `history_dialog.py` | `popups/gui_popup_history.ui` |
| `manual_component_dialog.py` | `popups/gui_popup_manual.ui` |
| `edit_component_dialog.py` | `popups/gui_popup_edit.ui` |
| `search_results_dialog.py` | `popups/gui_popup_search.ui` |
| `material_search_dialog.py` | `popups/gui_popup_search.ui` |
| `materials_table_dialog.py` | `popups/gui_popup_history.ui` |
| `material_dialog.py` | Estilos popup Siemens (Python) |

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
| `ORGANIZAR-DESKTOP.bat` | Regenera `.ui`, exporta `.py`, sincroniza Designer + Desktop |
| `tools/generate_all_designer_uis.py` | Regenera todos os `.ui` |
| `tools/gui_ui_builder.py` | Builders partilhados (template) |
| `tools/export-ui.bat` | Exporta `.ui` → `.py` |
| `tools/sync_designer_package.ps1` | Atualiza `StockTracker-Designer/` (repo e/ou Desktop) |
| `tools/ABRIR-DESIGNER.bat` | Abre Components ou Materials no Designer |

Documentacao: [docs/GUIA_RAPIDO_PT.md](../../docs/GUIA_RAPIDO_PT.md) · [designer/MATERIALS-LEIA-ME.txt](designer/MATERIALS-LEIA-ME.txt)
