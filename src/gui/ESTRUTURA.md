# Modulo de interface grafica

## Aplicacao principal

| Ficheiro | Papel |
|----------|-------|
| `stock_tracker_window.py` | Janela principal |
| `keyboard_shortcuts.py` | Atalhos de teclado |
| `components_massive_mode.py` | Modo Passive (R/C) |
| `statistics_page.py` | Pagina Statistics |
| `equipments_page.py` | Pagina Equipments |
| `global_search_dialog.py` | Pesquisa global (Ctrl+G) |
| `massive_dialog.py` | Adicionar/editar passivo |
| `catalog_image_preview.py` | Imagem de catalogo com zoom |

Arranque: `run.bat` ou `python -m src.main`

## Core

| Ficheiro | Papel |
|----------|-------|
| `src/core/stock.py` | Excel, stock, APIs |
| `src/core/passive_transfer.py` | Detecao R/C |
| `src/core/inventory_report.py` | Dados para PDF |

Manual: [docs/guias/MANUAL_UTILIZADOR.md](../../docs/guias/MANUAL_UTILIZADOR.md)
