# Modulo de interface grafica

## Aplicacao principal

| Ficheiro | Papel |
|----------|-------|
| `stock_tracker_window.py` | Janela principal (eventos, SCAN, stock) |
| `designer/gui_stocktracker.ui` | Layout Qt Designer |
| `designer/gui_stocktracker.py` | Export `pyside6-uic` do `.ui` |
| `message_dialog.py` | Avisos / erros / perguntas (template Siemens) |
| `user_name_dialog.py` | Pedir nome de utilizador no popup |
| `confirm_dialog.py` | Confirmar remocao de stock |
| `history_dialog.py` | Historico |
| `manual_component_dialog.py` | Componente manual |
| `edit_component_dialog.py` | Editar linha do Excel |
| `search_results_dialog.py` | Varias linhas no Excel |
| `styles.py` | Estilos partilhados |
| `gui_config.py` | Caminhos de logos |

Arranque: `python -m src.main` ou `run.bat` na raiz.

**Nao** executar ficheiros de `gui/` isoladamente (imports relativos).

## Pesquisa em distribuidores

No **SCAN**, se o componente nao estiver no Excel, a app pergunta e pesquisa **todos** os APIs configurados em `config/secrets.py` (ordem: Mouser, TME, RS, DigiKey, …) ate encontrar.

## Popups

Ficheiros em `designer/popups/` — gerar com `python tools/generate_popup_uis.py`.

## Template Siemens (`siemens_template/`)

Material de referencia (icones, widgets). A janela principal usa `designer/gui_stocktracker.*`.
