# Fluxograma — Popups e diálogos

## Mapa `.ui` → Python

```mermaid
flowchart LR
    subgraph components/popups
        PM[gui_popup_manual.ui] --> MD[manual_component_dialog.py]
        PE[gui_popup_edit.ui] --> ED[edit_component_dialog.py]
        PS[gui_popup_search.ui] --> SD[search_results_dialog.py]
        PH[gui_popup_history.ui] --> HD[history_dialog.py]
    end
    subgraph equipments/popups
        EE[gui_popup_equipment.ui] --> EQD[equipment_dialog.py]
        ES[gui_popup_search.ui] --> ESD[equipment_search_dialog.py]
        EH[gui_popup_history.ui] --> ETD[equipments_table_dialog.py]
    end
    subgraph shared/popups
        PC[gui_popup_confirm.ui] --> MSG[message_dialog.py]
        PC --> USR[user_name_dialog.py]
        PC --> CFM[confirm_dialog.py]
        PT[gui_popup_template.ui] --> REF[Referência Siemens]
    end
```

## DESIGNER.bat — opções 3–11

| Opção | Ficheiro |
|-------|----------|
| 3 | `popups/components/gui_popup_manual.ui` |
| 4 | `popups/components/gui_popup_edit.ui` |
| 5 | `popups/components/gui_popup_search.ui` |
| 6 | `popups/components/gui_popup_history.ui` |
| 7 | `popups/equipments/gui_popup_equipment.ui` |
| 8 | `popups/equipments/gui_popup_search.ui` |
| 9 | `popups/equipments/gui_popup_history.ui` |
| 10 | `popups/shared/gui_popup_confirm.ui` |
| 11 | `popups/shared/gui_popup_template.ui` |

Canonical: `src/gui/designer/popups/` · Pacote edição: `StockTracker-Designer/popups/`
