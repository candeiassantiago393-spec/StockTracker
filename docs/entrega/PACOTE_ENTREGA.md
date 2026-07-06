# Pacote de entrega — Stock Tracker

## Resumo do projeto

**Stock Tracker** — aplicação desktop Windows (Python + PySide6) para inventário de componentes eletrónicos, passivos (R/C), equipamentos calibrados e relatórios. Dados em Excel local; integração opcional com APIs de distribuidores (Mouser, DigiKey, TME, RS).

**Autor:** estágio Siemens  
**Repositório:** https://github.com/candeiassantiago393-spec/StockTracker  
**Versão documentada:** 2.1

---

## Estrutura do repositório (entrega)

```
StockTracker/
├── INSTALAR.bat              ← primeira instalação
├── run.bat                   ← arrancar a app
├── README.md                 ← visão geral (EN)
├── requirements.txt
├── config/
│   ├── secrets.example.py    ← template de credenciais
│   └── credentials.py
├── data/
│   ├── README.md             ← stock.xlsx, caches, backups
│   └── stock.xlsx            ← criado localmente (não no Git)
├── docs/
│   ├── entrega/              ← este pacote
│   ├── especificacao/        ← PROJETO_STOCKTRACKER_PT.md
│   ├── guias/                ← GUIA_RAPIDO_PT.md
│   ├── fluxogramas/          ← diagramas Mermaid
│   └── user/                 ← arquitetura, APIs, GitHub
├── src/
│   ├── main.py
│   ├── core/                 ← stock.py, suppliers, relatórios
│   └── gui/                  ← interface Siemens
├── tools/                    ← Designer, export, verificação
├── word/                     ← documento Word formal
└── StockTracker-Designer/    ← pacote Qt Designer
```

---

## Funcionalidades entregues (v2.1)

| Módulo | Descrição |
|--------|-----------|
| **Components** | Pesquisa Excel, SCAN multi-distribuidor, stock IN/OUT, imagem catálogo |
| **Passive (R/C)** | Folha `Generic`, resistores/condensadores, scan, localização |
| **Equipments** | Calibração, datasheet/imagem por pasta, empréstimos |
| **Statistics** | Stock baixo, calibrações, por localização, export PDF |
| **Pesquisa global** | `Ctrl+G` — Components + Passive + Equipments |
| **Histórico** | Folha `History` + Last 20 com abertura do item |
| **Alertas** | Email opcional de calibração a expirar |

---

## Folhas Excel (`data/stock.xlsx`)

| Folha | Uso |
|-------|-----|
| `Components` | Componentes activos |
| `Generic` | Passivos R/C (alto volume) |
| `Equipments` | Equipamentos calibrados |
| `EquipmentLoans` | Registo de empréstimos |
| `History` | Movimentos de stock |

---

## Instalação (receptor)

```powershell
git clone https://github.com/candeiassantiago393-spec/StockTracker.git
cd StockTracker
.\INSTALAR.bat
copy config\secrets.example.py config\secrets.py
# Editar secrets.py
.\run.bat
```

---

## Documentação por perfil

| Perfil | Começar aqui |
|--------|----------------|
| Tutor / gestão | `word/StockTracker_Documentacao_Projeto.docx` |
| Técnico / manutenção | `docs/especificacao/PROJETO_STOCKTRACKER_PT.md` |
| Utilizador laboratório | `docs/guias/GUIA_RAPIDO_PT.md` |
| Desenvolvedor UI | `docs/user/QT_DESIGNER.md` |

---

## Continuidade após o estágio

1. Manter `config/secrets.py` no PC do laboratório (backup seguro).
2. Backups automáticos em `data/backups/` (últimos 20).
3. Evoluções sugeridas: `docs/roadmap/MELHORIAS_SUGERIDAS.md`.
4. Regenerar Word após alterações: `python tools/build_project_docx.py`.
