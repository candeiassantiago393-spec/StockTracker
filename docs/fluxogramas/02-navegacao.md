# Fluxograma — Navegação e barra partilhada

```mermaid
flowchart TD
    subgraph Header
        H1[COMPONENTS]
        H2[EQUIPMENTS]
    end
    H1 -->|page 0| P0[container_main_body / Components]
    H2 -->|page 1| P1[EquipmentsPage]
    subgraph Barra inferior partilhada
        B1[Last 20]
        B2[Comp. hist. / Eq. hist.]
        B3[ADD MANUAL]
        B4[EDIT]
        B5[OPEN EXCEL]
        B6[CLEAR]
        B7[Exit]
    end
    P0 --> Barra inferior partilhada
    P1 --> Barra inferior partilhada
    B1 --> D1[HistoryDialog / EquipmentsTableDialog]
    B3 --> D2[Manual / Equipment dialog]
    B4 --> D3[Edit component / equipment]
```

| Botão | Components | Equipments |
|-------|------------|------------|
| Last 20 | Histórico movimentos | Últimas 20 linhas Equipments |
| Comp./Eq. hist. | Histórico filtrado componente | Tabela equipamentos |
| ADD MANUAL | `ManualComponentDialog` | `EquipmentDialog` (novo) |
| EDIT | `EditComponentDialog` | `EquipmentDialog` (editar) |

Título da página: `Inventory — Components` / `Inventory — Equipments` (runtime).
