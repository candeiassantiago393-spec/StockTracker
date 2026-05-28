# Modulo de interface grafica

## Aplicacao Stock Tracker

| Ficheiro | Papel |
|----------|-------|
| `stock_tracker_window.py` | Controlador da janela principal |
| `ui_stock_tracker.py` | Layout PySide6 |
| `history_dialog.py` | Historico (shell `gui_popup.ui`) |
| `manual_component_dialog.py` | Adicionar componente manual |
| `search_results_dialog.py` | Escolher linha do Excel |
| `styles.py` | Estilos Siemens |
| `siemens_template/popup_shell.py` | Base Siemens para todos os popups |
| `gui_config.py` | Caminhos de recursos (logos) |

Arranque: `python -m src.main` (nao executar estes ficheiros isoladamente).

---

## Templates Siemens (`siemens_template/`)

Material de referencia fornecido no ambito do estagio (Qt Designer, widgets, icones).

Popups da aplicacao reutilizam `siemens_template/gui_popup.ui` via `popup_shell.py`
(mesmo padrao que `gui_popup_setup.py`).

Ficheiros `.ui` de referencia para o Qt Designer: `designer/popups/` (gerados com
`python tools/generate_popup_uis.py`).

O resto do template nao e obrigatorio para correr a app de inventario.

Manutencao da estrutura de pastas (se necessario): `tools/REORGANIZAR_GUI.bat`
