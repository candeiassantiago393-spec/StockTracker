# Fluxograma — Página Equipments

## Pesquisa e seleção

```mermaid
flowchart TD
    S[search_entry + SEARCH] --> V{validate_user?}
    V --> E[search_equipments_all]
    E --> M{vários?}
    M -->|sim| R[EquipmentSearchDialog]
    M -->|não| D[display_equipment row]
    R --> D
    D --> SEL[_selected_row definido]
```

## SCAN supplier reference

```mermaid
flowchart TD
    SC[supplier_ref_entry + SCAN] --> F[find_equipment_by_supplier_ref]
    F --> H{encontrado?}
    H -->|sim| D[display_equipment]
    H -->|não| W[Aviso não encontrado]
```

## Imagem do equipamento

```mermaid
flowchart TD
    subgraph Entrada
        DR[Drag & drop ficheiro]
        AD[Botão Add]
    end
    DR --> V{is_image_file?}
    AD --> FP[QFileDialog]
    FP --> V
    V -->|sim| L[link_equipment_image]
    L --> FS[data/equipments/id/image.*]
    L --> XLS[Coluna Image no Excel]
    V -->|não| E[Erro formato]
```

Caixa de imagem (`.ui`): **300×320 px** mínimo (`EQUIPMENT_IMAGE_PREVIEW_HEIGHT` em `styles.py`).

## Documentação de suporte

```mermaid
flowchart TD
    DS[doc_search_entry + SEARCH] --> L[list_documents em data/equipments/id/]
    L --> LIST[doc_results_list visível]
    OP[OPEN] --> OS[Abrir ficheiro selecionado]
    LK[LINK] --> XL[Coluna Datasheet Excel]
    OF[OPEN FOLDER] --> DIR[Abrir pasta data/equipments/id/]
    ADOC[ADD DOC] --> INS[install_datasheet na pasta]
```

| Campo detalhe vazio + clique | ADD Equipment |
|------------------------------|---------------|
| Campo preenchido + clique | Sem ação (usar EDIT) |
