# Fluxograma — Página Components

## Pesquisa manual (SEARCH)

```mermaid
flowchart TD
    S[search_entry + SEARCH] --> V{validate_user?}
    V -->|não| U[UserNameDialog]
    V -->|sim| E[search_in_excel_all]
    E --> M{vários resultados?}
    M -->|sim| R[SearchResultsDialog]
    M -->|não| SH[show_component]
    R --> SH
    SH --> IMG[Carregar imagem + links catálogo]
```

## SCAN / código de barras

```mermaid
flowchart TD
    SC[barcode_entry + SCAN ou Enter] --> L{len <= 4?}
    L -->|sim| IGN[Ignorar silenciosamente]
    L -->|não| V{validate_user?}
    V --> E[find_component_any Excel]
    E --> F{encontrado?}
    F -->|sim| SH[show_component]
    F -->|não| API[search_any_supplier cadeia APIs]
    API --> N{novo na API?}
    N -->|sim| ADD[add_component_row + opcional stock]
    N -->|não| ERR[Erro / não encontrado]
    ADD --> SH
```

## Stock IN / OUT

```mermaid
flowchart TD
    Q[quantity_entry] --> A{ADD ou REMOVE?}
    A --> V{validate_user + código + qty?}
    V --> U[update_stock IN/OUT]
    U --> H[add_history]
  U --> CF{OUT e stock insuficiente?}
    CF -->|sim| CD[SiemensConfirmDialog]
    CF -->|não| OK[Atualizar val_stock]
```

## Detalhes e imagem (layout atual)

```mermaid
flowchart LR
    subgraph Grelha Component Details
        L0[Col 0: etiquetas 152px]
        L1[Col 1: offset 288px]
        L2[Col 2: campos + Copy]
        L3[Col 3: flex]
        L4[Col 4: imagem 240x240]
    end
    L4 --> CP[CatalogImagePreview runtime]
    CP --> CACHE[data/component_image_cache]
    CP --> LINKS[data/catalog_links]
```

| Ação UI | Comportamento |
|---------|----------------|
| Campo detalhe **vazio** + clique | Abre ADD MANUAL |
| Campo detalhe **preenchido** + clique | Sem ação (usar EDIT) |
| WEB / Datasheet | URLs em cache; confirmação antes de abrir PDF |
| Operations ordem | Scan → Quantity → Stock Actions |
