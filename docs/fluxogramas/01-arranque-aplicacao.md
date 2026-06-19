# Fluxograma — Arranque da aplicação

```mermaid
flowchart TD
    A[run.bat ou python -m src.main] --> B[src/main.py]
    B --> C[QApplication]
    C --> D[StockTrackerWindow]
    D --> E[Ui_StockTracker.setupUi]
    E --> F[apply_component_details_grid]
    F --> G[_connect_signals]
    G --> H[_setup_page_navigation]
    H --> I[EquipmentsPage embutida]
    I --> J[User Name overlay + barra ações]
    J --> K[show maximizado / fullscreen]
    K --> L{Utilizador interage}
```

| Passo | Ficheiro | Notas |
|-------|----------|-------|
| Entrada | `src/main.py` | Não executar `gui/*.py` diretamente |
| Lógica Excel | `src/core/stock.py` | `StockTracker()` no `__init__` da janela |
| Layout Components | `gui_stocktracker.ui` | Grelha 5 colunas, imagem à direita |
| Layout Equipments | `gui_equipments.ui` | Página no `QStackedWidget` |
