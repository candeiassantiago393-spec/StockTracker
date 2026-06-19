# Fluxograma — Qt Designer (workflow)

```mermaid
flowchart TD
    GEN[generate_*_ui.py / gui_ui_builder.py] --> UI[src/gui/designer/*.ui]
    SYNC[sync_designer_package.ps1] --> PKG[StockTracker-Designer/]
    PKG --> DES[DESIGNER.bat opções 1-11]
    DES --> EDIT[Editar no Qt Designer]
    EDIT --> COPY[Copiar .ui para src/gui/designer/]
    COPY --> EXP[export-ui.bat / pyside6-uic]
    EXP --> PY[gui_*.py gerados]
    PY --> RUN[python -m src.main]
```

## Páginas principais

| Opção | Ficheiro | Gerador |
|-------|----------|---------|
| 1 | `gui_stocktracker.ui` | `generate_stocktracker_ui.py` |
| 2 | `gui_equipments.ui` | `generate_equipments_ui.py` |

## Regras importantes

- **Não editar** `gui_*.py` à mão — sempre exportar a partir do `.ui`.
- Métricas partilhadas: `src/gui/styles.py`, `tools/gui_ui_builder.py`.
- Após export Components: script corrige import `resources_rc`.
- Sincronizar pacote: `powershell -File tools\sync_designer_package.ps1 -Target Repo`

Documentação completa: [../user/QT_DESIGNER.md](../user/QT_DESIGNER.md)
