# Arquitetura — Stock Tracker

## Principio de separacao

O projeto segue a estrutura exigida no estagio:

```
Interface (gui/)  --->  Logica (core/stock.py)  --->  Dados (Excel / Mouser)
```

A interface **nao** implementa regras de stock; limita-se a recolher input, validar utilizador e invocar metodos da classe `StockTracker`.

---

## Classe `StockTracker`

| Area | Metodos principais |
|------|-------------------|
| Excel | `get_workbook`, `get_components_sheet`, `save_workbook` |
| Pesquisa | `search_in_excel`, `find_component_any`, `extract_part_number` |
| Stock | `update_stock` (IN/OUT), `add_history` |
| Mouser | `search_mouser`, `add_from_mouser_and_stock_in` |

---

## Interface grafica

| Componente | Responsabilidade |
|------------|------------------|
| `StockTrackerWindow` | Orquestracao de eventos (SEARCH, SCAN, ADD/REMOVE) |
| `Ui_StockTracker` | Layout e widgets |
| `HistoryDialog` | Visualizacao do historico |
| `styles.py` | Identidade visual Siemens (cores, tipografia) |

### Regras na camada GUI

- Nome de utilizador obrigatorio antes de operacoes
- Confirmacao explicita antes de remocao de stock (OUT)
- Referencia minima de 5 caracteres em operacoes de scan
- Mensagens de erro quando o Excel esta aberto ou a API falha

---

## Fluxo SCAN (resumo)

1. Utilizador introduz codigo / scan
2. Procura no Excel
3. Se nao existir — opcao de consulta Mouser
4. Novo componente: linha no Excel com stock 0
5. Utilizador indica quantidade e confirma ADD STOCK

---

## Dados

### Folha Components

ID, Mouser Reference, Manufacturer, Manufacturer Reference, Value, Description, Stock

### Folha History

Date, User, Mouser Reference, Movement, Quantity, Stock After

---

## Credenciais

Carregamento por ordem:

1. Variavel de ambiente `MOUSER_API_KEY`
2. Ficheiro `config/secrets.py` (local, nao versionado)
