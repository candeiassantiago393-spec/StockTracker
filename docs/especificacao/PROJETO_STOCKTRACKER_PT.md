# Stock Tracker

Aplicação desktop para gestão de inventário de componentes eletrónicos.

Versão documentada: **2.1** (entrega estágio Siemens, 2026)

[PROJETO_STOCKTRACKER.md](PROJETO_STOCKTRACKER.md) (inglês) · [Pacote de entrega](../entrega/PACOTE_ENTREGA.md)

# Especificações

- Inventário local em Excel (`data/stock.xlsx`) — folhas **Components**, **Generic**, **Equipments**, **EquipmentLoans** e **History**;
- Interface gráfica PySide6 com templates Siemens — páginas **Components**, **Passive (R/C)**, **Equipments** e **Statistics**;
- Pesquisa de componentes no Excel (referência do distribuidor, fabricante, MPN, descrição);
- Modo **Passive** para resistores e condensadores (folha `Generic`, scan, localização);
- Leitura de código de barras / etiqueta (padrões tipo Mouser `P…Q`);
- Movimentos de stock **IN** / **OUT** com registo na folha **History**;
- Pesquisa multi-distribuidor no SCAN (apenas APIs configuradas);
- **Pesquisa global** (`Ctrl+G`) em Components, Passive e Equipments;
- Relatórios de inventário e exportação **PDF** (página Statistics);
- Empréstimos de equipamentos e alertas de calibração por email;
- Adição/edição manual de componentes sem API;
- Nome de utilizador obrigatório para movimentos e histórico;
- Separação clara: lógica de negócio em `src/core/`, UI em `src/gui/`;
- Credenciais em `config/secrets.py` (não commitar).

# Protocolo de comunicação

A comunicação externa usa **APIs REST HTTPS** nos módulos de distribuidores em `src/core/suppliers/`.

## Arranque em runtime

| Característica | Valor |
|:---------------|:------|
| Comando de entrada | `python -m src.main` ou `run.bat` |
| Primeira instalação | `INSTALAR.bat` |
| Python         | 3.10+ |
| Plataforma     | Windows 10/11 |
| Ficheiro de dados | `data/stock.xlsx` (fechar o Excel antes de gravar) |
| Verificação entrega | `python tools\verificar_entrega.py` |

## Ordem SCAN multi-fornecedor

Quando o SCAN não encontra a peça no Excel, a camada core consulta cada fornecedor **configurado** por esta ordem até ao primeiro resultado:

| Ordem | ID fornecedor   | Módulo                    |
|:-----:|:----------------|:--------------------------|
| 1     | `mouser`        | `src/core/suppliers/mouser.py` |
| 2     | `tme`           | `src/core/suppliers/tme.py` |
| 3     | `rs`            | `src/core/suppliers/rs.py` |
| 4     | `digikey`       | `src/core/suppliers/digikey.py` |
| 5     | `robert_mauser` | `src/core/suppliers/robert_mauser.py` |

Credenciais e ativação: `config/secrets.py` (ver `config/secrets.example.py`).

## Estrutura normalizada da peça (`PartInfo`)

Todos os módulos de fornecedor devolvem os mesmos campos lógicos (ver `src/core/suppliers/base.py`):

| Campo                      | Descrição |
|:---------------------------|:----------|
| `supplier`                 | ID interno (`mouser`, `digikey`, …) |
| `supplier_part_number`     | SKU / código de encomenda do distribuidor |
| `manufacturer`             | Nome do fabricante |
| `manufacturer_part_number` | MPN |
| `description`              | Descrição curta |

Chaves legadas (`MouserPartNumber`, `Manufacturer`, …) mantêm-se por compatibilidade com o Excel.

# Modelo de dados (Excel)

Permissões (lógicas):

- **r**: leitura pela aplicação
- **w**: escrita por ação do utilizador
- **h**: histórico apenas append

## Folha: Components

| Coluna | Índice | Tipo   | Permissão | Descrição |
|:-------|:------:|:-------|:----------|:----------|
| ID     | A (0) | int    | w         | Identificador de linha auto-incrementado |
| Supplier Reference | B (1) | string | rw | Referência do distribuidor (ex. Mouser `581-…`) |
| Manufacturer | C (2) | string | rw | Nome do fabricante |
| Manufacturer Reference | D (3) | string | rw | MPN |
| Value  | E (4) | string | rw | Reservado / opcional |
| Description | F (5) | string | rw | Descrição da peça |
| Stock  | G (6) | int    | rw        | Quantidade atual |
| Location | H+ | string | rw | Localização física (opcional, multi-valor) |

## Folha: Generic (Passive R/C)

| Coluna | Campo | Descrição |
|:-------|:------|:----------|
| ID | int | Auto-incrementado |
| Type | R / C | Resistor ou condensador |
| Value | string | Ex.: `10k`, `100nF`, `1uF 25V` |
| Tolerance | string | Ex.: `1%`, `5%` |
| Package | string | Ex.: `0603`, `0805` |
| Name | string | Nome auto-gerado ou manual |
| Stock | int | Quantidade |
| Supplier Ref | string | Referência distribuidor |
| Dielectric | string | Ex.: `X7R`, `C0G` |
| Voltage | string | Ex.: `50V`, `16V` |
| Notes | string | Notas |
| Location | string | Localização no laboratório |

## Folha: Equipments

| Coluna | Índice | Tipo | Permissão | Descrição |
|:-------|:------:|:-----|:----------|:----------|
| ID | A (0) | int | w | Identificador auto-incrementado |
| Supplier Reference | B (1) | string | rw | Referência do fornecedor / código |
| Serial Number | C (2) | string | rw | Número de série |
| Description | D (3) | string | rw | Descrição do equipamento |
| Name | — | string | rw | Nome curto |
| Calibration Date | E (4) | string | rw | Data de calibração (`YYYY-MM-DD`) |
| Calibration Expiration Date | F (5) | string | rw | Data de expiração da calibração |
| Location | — | string | rw | Localização |
| Datasheet / Image | — | string | rw | Ficheiros em `data/equipments/{id}/` |

## Folha: EquipmentLoans

Registo de empréstimos de equipamentos (quem emprestou, data, devolução).

## Folha: History

| Coluna | Índice | Tipo   | Permissão | Descrição |
|:-------|:------:|:-------|:----------|:----------|
| Date   | A     | string datetime | h | Timestamp `YYYY-MM-DD HH:MM:SS` |
| User   | B     | string | h         | Nome do operador na GUI |
| Supplier Reference | C | string | h | Referência no momento do movimento |
| Movement | D   | string | h         | `IN` ou `OUT` |
| Quantity | E     | int    | h         | Quantidade movimentada |
| Stock After | F  | int    | h         | Saldo após o movimento |

# Operações da GUI

## Página Components

| Operação           | Gatilho | Método(s) core |
|:-------------------|:--------|:----------------|
| Pesquisa (Excel)   | SEARCH  | `search_in_excel_all`, diálogos |
| Scan / código de barras | SCAN | `extract_part_number`, `add_from_supplier_and_stock_in` |
| Entrada de stock   | ADD     | `update_stock("IN")` ou fluxo scan |
| Saída de stock     | REMOVE  | `update_stock("OUT")` + diálogo de confirmação |
| Histórico          | Botões History | `get_history_rows` |
| Componente manual  | Popup manual | `add_manual_component` |
| Editar componente  | Edit / clique em detalhes | `update_component` |
| Abrir Excel        | OPEN EXCEL | `ensure_workbook_sheets` + `startfile` |
| Pesquisa global    | `Ctrl+G` | `collect_global_search_hits` |

## Modo Passive (R/C)

| Operação | Gatilho | Notas |
|:---------|:--------|:------|
| Alternar modo | `Ctrl+Shift+M` | Components ↔ Passive na mesma página |
| Scan passivo | SCAN / Enter no barcode | `find_massive_by_supplier_ref` |
| Adicionar passivo | ADD MANUAL / deteção automática no scan | `add_massive_item` |
| Package automático | Supplier Ref + catálogo | `enrich_passive_from_reference` |
| Localização opcional | Após stock IN | `optional_location_dialog` |

Peças R/C detetadas no SCAN de Components podem ser encaminhadas para a folha `Generic` (`passive_transfer.py`).

## Página Equipments

| Operação | Gatilho | Método(s) core |
|:---------|:--------|:---------------|
| Pesquisar equipamentos | SEARCH | `search_equipments_all`, `EquipmentSearchDialog` |
| Referência fornecedor | Enter no campo scan | `find_equipment_by_supplier_ref` |
| Adicionar equipamento | ADD MANUAL | `add_equipment` |
| Editar equipamento | EDIT | `update_equipment` |
| Empréstimo | Checkbox Loaned | `return_equipment_loan`, folha `EquipmentLoans` |
| Tabelas histórico | Last 20 | `get_equipment_recent_rows`, seleção + Open |

## Página Statistics

| Operação | Descrição |
|:---------|:----------|
| Dashboard | Stock baixo, calibrações a expirar, estatísticas por localização |
| EXPORT PDF | Relatório em `data/reports/` (`inventory_report_pdf.py`) |
| Itens sem localização | Lista de stock > 0 sem Location |

## Regras de utilizador (GUI)

- Nome de utilizador obrigatório antes de alterar stock;
- OUT exige confirmação;
- Comprimento mínimo da referência no scan validado na GUI;
- Se o Excel estiver aberto, `save_workbook` falha com mensagem clara;
- Last 20 permite selecionar linha e abrir o item (Components, Passive, Equipments).

# Arquitetura

```
src/main.py
    └── src/gui/stock_tracker_window.py  (PySide6, QStackedWidget)
            ├── Components (+ Passive mode)  ← designer/gui_stocktracker.ui
            ├── Equipments                   ← equipments_page.py
            ├── Statistics                   ← statistics_page.py
            └── src/core/stock.py            (StockTracker)
                    ├── openpyxl → data/stock.xlsx
                    ├── passive_transfer.py  (R/C detection)
                    ├── inventory_report.py  (PDF data)
                    └── src/core/suppliers/* → APIs REST
```

A documentação ao nível de módulo segue o template Siemens (secções numeradas em `stock.py`, `main.py`, `suppliers/base.py`).

# Versões

| Versão | Notas |
|:-------|:------|
| **2.1** | Passive, Statistics, PDF, pesquisa global, empréstimos, alertas calibração, multi-location |
| 2.0    | GUI única; SCAN multi-fornecedor; Equipments; UI Siemens Designer |
| 1.x    | Excel + GUI focada em Mouser |
| 0.x    | Consola / protótipo (`src/test_terminal.py`) |

Entregável formal: `word/StockTracker_Documentacao_Projeto.docx` (regenerar com `python tools/build_project_docx.py`).

## Documentação de entrega

| Documento | Conteúdo |
|:----------|:---------|
| [docs/entrega/](../entrega/README.md) | Índice do pacote de entrega |
| [CHECKLIST_ENTREGA.md](../entrega/CHECKLIST_ENTREGA.md) | Verificação antes de entregar |
| [GUIA_RAPIDO_PT.md](../guias/GUIA_RAPIDO_PT.md) | Guia operacional |

# TODO / continuidade

- Chaves DigiKey produção / resolução 403 sandbox — ver `docs/user/DIGIKEY_SETUP.md`;
- Integração Robert Mauser quando houver detalhes da API;
- Ideias futuras: `docs/roadmap/MELHORIAS_SUGERIDAS.md`.
