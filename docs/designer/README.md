# Qt Designer — índice

Documentação centralizada para editar layouts `.ui` do Stock Tracker.

## Onde estão os ficheiros

| Pasta | Função |
|-------|--------|
| [`src/gui/designer/`](../../src/gui/designer/) | **Canónico** — `.ui` + `.py` exportados usados pela app |
| [`StockTracker-Designer/`](../../StockTracker-Designer/) | Pacote para abrir no Qt Designer (`DESIGNER.bat`) |
| `Desktop\StockTracker-Designer` | Cópia local (opcional) — ver [WORKSPACE.md](../user/WORKSPACE.md) |

## Guias

| Documento | Conteúdo |
|-----------|----------|
| [user/QT_DESIGNER.md](../user/QT_DESIGNER.md) | Workflow completo (EN) |
| [../../src/gui/designer/README.md](../../src/gui/designer/README.md) | Ficheiros `.ui`, métricas, regenerar/exportar |
| [../../src/gui/designer/EQUIPMENTS-LEIA-ME.txt](../../src/gui/designer/EQUIPMENTS-LEIA-ME.txt) | Página Equipments (PT) |
| [../../StockTracker-Designer/LEIA-ME.txt](../../StockTracker-Designer/LEIA-ME.txt) | Pacote Designer (PT) |
| [../../src/gui/designer/popups/README.md](../../src/gui/designer/popups/README.md) | Popups Components / Equipments / shared |
| [fluxogramas/08-qt-designer.md](../fluxogramas/08-qt-designer.md) | Fluxograma Mermaid |

## Comandos rápidos

```text
tools\ABRIR-DESIGNER.bat              # abrir .ui no repo
StockTracker-Designer\DESIGNER.bat    # pacote Designer (opções 1–11)
tools\ORGANIZAR-DESKTOP.bat           # sincronizar repo + Desktop
tools\export-ui.bat                   # .ui → .py após editar
python tools/generate_all_designer_uis.py   # regenerar a partir de Python
```

## Estrutura do pacote Designer

```
StockTracker-Designer/
├── DESIGNER.bat
├── LEIA-ME.txt
├── EQUIPMENTS-LEIA-ME.txt
├── gui_stocktracker.ui          # Components
├── gui_equipments.ui            # Equipments
├── popups/
│   ├── components/              # manual, edit, search, history
│   ├── equipments/              # equipment, search, history
│   └── shared/                  # confirm, template
└── siemens_template/            # ícones, fontes, template base
```

Após editar `.ui` no pacote Designer, copie para `src/gui/designer/` e execute `tools\export-ui.bat`.
