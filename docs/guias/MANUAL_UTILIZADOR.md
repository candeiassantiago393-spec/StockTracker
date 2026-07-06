# Manual do utilizador — Stock Tracker

Aplicação de inventário para o laboratório. Os dados ficam no Excel (`data/stock.xlsx`). A interface segue o template Siemens (PySide6).

Especificação técnica: [PROJETO_STOCKTRACKER_PT.md](../especificacao/PROJETO_STOCKTRACKER_PT.md)

---

## Instalação (primeira vez)

1. Ter Python 3.10 ou superior instalado.
2. Na pasta do projeto, executar `INSTALAR.bat` (cria o `.venv` e instala dependências).
3. Copiar `config\secrets.example.py` para `config\secrets.py` e preencher as chaves API que forem usadas (Mouser, DigiKey, etc.). Ver `config/README.md`.
4. Garantir que existe `data\stock.xlsx` — a app cria um ficheiro vazio no primeiro arranque se não houver nenhum.
5. Arrancar com `run.bat`.

Para confirmar que está tudo instalado: `python tools\verificar_instalacao.py`

---

## Arranque diário

Duplo-clique em `run.bat`, ou:

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.main
```

**Importante:** fechar o ficheiro `stock.xlsx` no Microsoft Excel antes de gravar stock na aplicação. Se o Excel estiver aberto, a gravação falha e aparece uma mensagem de erro.

Indicar sempre o **nome de utilizador** antes de movimentos de stock — fica registado no histórico.

---

## Páginas da aplicação

No topo há três secções principais (atalhos `Ctrl+1`, `Ctrl+2`, `Ctrl+3`):

### Components

Gestão de componentes activos (ICs, conectores, etc.) na folha Excel `Components`.

- **SEARCH** — pesquisa só no Excel (referência, fabricante, descrição).
- **SCAN** — lê o código de barras ou referência; se não existir no Excel, consulta os distribuidores configurados (Mouser, TME, RS, DigiKey…) e pode importar a peça.
- **ADD STOCK / REMOVE STOCK** — entrada e saída de quantidades. A saída pede confirmação.
- **ADD MANUAL** — adicionar componente sem passar pela API.
- **EDIT** — alterar dados do componente seleccionado.
- **Last 20** — últimos registos; pode seleccionar uma linha e abrir o item.
- Imagem do catálogo à direita (zoom com a roda do rato, lupa ao passar o rato).

**Modo Passive (R/C)** — `Ctrl+Shift+M` dentro de Components. Passa a trabalhar com resistores e condensadores na folha `Generic`. O fluxo é o mesmo (scan, stock in/out, manual). Ao introduzir a referência de fornecedor, o campo Package pode preencher-se sozinho se a API tiver essa informação.

### Equipments

Equipamentos calibrados (multímetros, osciloscópios, etc.) na folha `Equipments`.

- Pesquisa por referência, número de série ou descrição.
- Datas de calibração e expiração.
- Datasheet e imagem guardados em `data\equipments\{id}\` — botões para adicionar ficheiros e abrir a pasta.
- Checkbox **Loaned** para registar empréstimo (folha `EquipmentLoans`).

### Statistics

Resumo do inventário: stock baixo, calibrações a expirar, estatísticas por localização. Botão **EXPORT PDF** grava o relatório em `data\reports\`.

### Pesquisa global

`Ctrl+G` — procura em Components, Passive e Equipments ao mesmo tempo.

---

## Ficheiro Excel (`data/stock.xlsx`)

| Folha | Uso |
|-------|-----|
| `Components` | Componentes |
| `Generic` | Resistores e condensadores (modo Passive) |
| `Equipments` | Equipamentos calibrados |
| `EquipmentLoans` | Empréstimos |
| `History` | Movimentos IN/OUT (automático) |

Backups automáticos em `data\backups\` (últimos 20). Mais detalhe em [data/README.md](../../data/README.md).

### Armário físico (Stock 1/2/3 e boxes)

A organização do armário SMD do laboratório está registada na coluna **Location** do Excel. Para ver o mapa completo (que peça está em cada gaveta ou box), abrir o **backup mais recente** em `data\backups\`. Descrição: [ARMARIO_LABORATORIO.md](ARMARIO_LABORATORIO.md).

---

## Atalhos úteis

| Atalho | Acção |
|--------|--------|
| `Ctrl+1` / `Ctrl+2` / `Ctrl+3` | Components / Equipments / Statistics |
| `Ctrl+G` | Pesquisa global |
| `Ctrl+F` | Campo de pesquisa |
| `F6` | Campo de scan / referência |
| `F5` | SCAN |
| `Ctrl+I` / `Ctrl+U` | Stock IN / OUT |
| `Ctrl+N` | ADD MANUAL |
| `Ctrl+E` | EDIT |
| `Ctrl+Shift+M` | Alternar Components / Passive |
| `Ctrl+Shift+E` | Abrir Excel |
| `Esc` | Limpar campos |

Os botões mostram o atalho no tooltip.

---

## Problemas frequentes

| Situação | O que fazer |
|----------|-------------|
| Não grava no Excel | Fechar o `stock.xlsx` no Excel |
| SCAN não encontra na API | Verificar `config\secrets.py` e ligação à rede |
| DigiKey dá erro 403 | Usar app Sandbox — ver `docs\user\DIGIKEY_SETUP.md` |
| Imagem do componente não aparece | Normal em algumas referências; URLs ficam em cache em `data\catalog_links\` |

---

## Quem mantém o código

- Lógica: `src\core\` (principalmente `stock.py`)
- Interface: `src\gui\`
- Layout visual (Qt Designer): `src\gui\designer\` — ver `docs\user\QT_DESIGNER.md`
- Mapa dos ficheiros da GUI: `src\gui\ESTRUTURA.md`

Documentação adicional: [docs/README.md](../README.md)
