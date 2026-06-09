# Stock Tracker

Aplicação desktop para gestão de inventário de componentes eletrónicos.

 [PROJETO_STOCKTRACKER.md](PROJETO_STOCKTRACKER.md)

# Especificações

- Inventário local em Excel (`data/stock.xlsx`);
- Interface gráfica PySide6 com templates de UI corporativa Siemens;
- Pesquisa de componentes no Excel (referência do distribuidor, fabricante, MPN, descrição);
- Leitura de código de barras / etiqueta (padrões tipo Mouser `P…Q`);
- Movimentos de stock **IN** / **OUT** com registo na folha **History**;
- Pesquisa multi-distribuidor no SCAN (apenas APIs configuradas);
- Adição/edição manual de componentes sem API;
- Nome de utilizador obrigatório para movimentos e histórico;
- Separação clara: lógica de negócio em `src/core/`, UI em `src/gui/`;
- Credenciais em `config/secrets.py` (nao commitar).

# Protocolo de comunicação

A comunicação externa usa **APIs REST HTTPS** nos módulos de distribuidores em `src/core/suppliers/`.

## Arranque em runtime

| Característica | Valor |
|:---------------|:------|
| Comando de entrada | `python -m src.main` ou `run.bat` |
| Python         | 3.10+ |
| Plataforma     | Windows 10/11 |
| Ficheiro de dados | `data/stock.xlsx` (fechar o Excel antes de gravar novas informações) |

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

## Folha: Materials

| Coluna | Índice | Tipo | Permissão | Descrição |
|:-------|:------:|:-----|:----------|:----------|
| ID | A (0) | int | w | Identificador auto-incrementado |
| Description | B (1) | string | rw | Descrição do material |
| Calibration Date | C (2) | string | rw | Data de calibração (`YYYY-MM-DD`) |
| Calibration Expiration Date | D (3) | string | rw | Data de expiração da calibração |

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

| Operação           | Gatilho | Método(s) core |
|:-------------------|:--------|:----------------|
| Pesquisa (Excel)   | SEARCH  | `search_in_excel_all`, diálogos |
| Scan / código de barras | SCAN | `extract_part_number`, `add_from_supplier_and_stock_in` |
| Entrada de stock   | ADD     | `update_stock("IN")` ou fluxo scan |
| Saída de stock     | REMOVE  | `update_stock("OUT")` + diálogo de confirmação |
| Histórico          | Botões History | `get_history_rows` |
| Componente manual  | Popup manual | `add_manual_component` |
| Editar componente  | Edit / clique em detalhes vazios | `update_component` |
| Abrir Excel        | OPEN EXCEL | `startfile` do SO em `stock.xlsx` |

## Regras de utilizador (GUI)

- Nome de utilizador obrigatório antes de alterar stock;
- OUT exige confirmação;
- Comprimento mínimo da referência no scan validado na GUI;
- Se o Excel estiver aberto, `save_workbook` falha com mensagem clara.

# Arquitetura

```
src/main.py
    └── src/gui/stock_tracker_window.py  (PySide6)
            └── src/core/stock.py        (StockTracker)
                    ├── openpyxl → data/stock.xlsx
                    └── src/core/suppliers/* → APIs REST
```

A documentação ao nível de módulo segue o template Siemens (secções numeradas em `stock.py`, `main.py`, `suppliers/base.py`).

# Versões

Versionamento do projeto (aplicação, não por componente):

| Versão | Notas |
|:-------|:------|
| 2.x    | GUI única; SCAN multi-fornecedor; UI Siemens Designer |
| 1.x    | Excel + GUI focada em Mouser |
| 0.x    | Consola / protótipo (`src/test_terminal.py`) |

Entregável formal: `word/StockTracker_Documentacao_Projeto.docx` (regenerar com `python tools/build_project_docx.py`).

## Alterações atuais

- Pesquisa multi-distribuidor sem combo de fornecedor na janela principal;
- Diagnósticos DigiKey sandbox e mensagens 403;
- Diálogo de nome de utilizador, OPEN EXCEL, componente manual a partir de detalhes vazios.

# TODO

- Chaves DigiKey produção / resolução 403 sandbox com suporte DigiKey;
- Integração Robert Mauser quando houver detalhes da API;
- Temperatura / alertas opcionais N/A (não aplicável a esta app).
