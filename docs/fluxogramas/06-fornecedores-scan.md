# Fluxograma — Fornecedores (SCAN Components)

```mermaid
flowchart TD
    START[SCAN Components] --> EX[Procurar no Excel]
    EX -->|hit| DONE[show_component]
    EX -->|miss| CHAIN[search_any_supplier]
    CHAIN --> M[Mouser]
    M -->|miss| T[TME]
    T -->|miss| RS[RS]
    RS -->|miss| DK[DigiKey]
    DK -->|miss| RM[Robert Mauser]
    RM -->|hit| MAP[Mapear para linha Excel]
    MAP --> DONE
    RM -->|miss| FAIL[Não encontrado]
```

| Módulo | Pasta |
|--------|-------|
| Orquestração | `src/core/stock.py` |
| Implementações | `src/core/suppliers/*.py` |
| Credenciais | `config/secrets.py` |

Configuração e testes: [../user/SUPPLIERS.md](../user/SUPPLIERS.md)

**Nota:** A página Equipments **não** usa SCAN de fornecedores — apenas Excel local.
