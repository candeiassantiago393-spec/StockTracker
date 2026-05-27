# Organizar o teu trabalho — Stock Tracker

## Uma regra simples

| O quê | Onde (pasta oficial) |
|-------|------------------------|
| **Programar, Git, correr a app** | `Downloads\StockTracker\StockTracker` |
| **Abrir no Qt Designer** | `Downloads\...\src\gui\designer\gui_stocktracker.ui` |
| **Mostrar UI ao tutor (opcional)** | `Ambiente de Trabalho\StockTracker-Designer` |

Abre o **Cursor** nesta pasta:

```
C:\Users\z005027j\Downloads\StockTracker\StockTracker
```

---

## O que tens no Ambiente de Trabalho

| Pasta | Serve para quê? | O que fazer |
|-------|-----------------|-------------|
| **StockTracker-Projeto** | Cópia do projeto (backup / USB) | Sincronizar com `tools\sincronizar-desktop.ps1` quando mudares PC |
| **StockTracker-Designer** | Só o `.ui` + logo para o tutor | Manter; abrir `gui_stocktracker.ui` |
| **StockTracker** | Template antigo do tutor | **Ignorar** (legado) |
| **siemens_template** (solta no Desktop) | Cópia extra para o Designer | Podes apagar se usares a pasta **Designer** ou o projeto em Downloads |

---

## Estrutura do projeto (oficial)

```
StockTracker/
├── config/          → secrets.py (API keys — NÃO partilhar)
├── data/            → stock.xlsx (inventário)
├── docs/            → documentação (estágio, APIs, Qt Designer)
├── src/
│   ├── main.py      → arrancar a app
│   ├── core/        → Excel, fornecedores (Mouser, TME, …)
│   └── gui/
│       ├── designer/           → gui_stocktracker.ui  ★ Qt Designer
│       └── siemens_template/   → template Siemens + resources.qrc
├── tools/           → export UI, sincronizar Desktop, gerar .ui
├── run.bat          → duplo clique para abrir a app
└── requirements.txt
```

---

## Fluxo de trabalho diário

### 1. Trabalhar no código

```powershell
cd C:\Users\z005027j\Downloads\StockTracker\StockTracker
.\.venv\Scripts\activate
python -m src.main
```

### 2. Editar a interface no Qt Designer

```powershell
.\tools\abrir-qt-designer.ps1
```

Ou: **File → Open** → `src\gui\designer\gui_stocktracker.ui`

Depois de guardar no Designer:

```powershell
.\tools\export_stocktracker_ui.ps1
python -m src.main
```

### 3. Sincronizar cópia para o Ambiente de Trabalho

```powershell
.\tools\sincronizar-desktop.ps1
```

(Não copia `secrets.py` nem `.venv` — as chaves ficam só no PC principal.)

---

## Documentação útil

| Ficheiro | Conteúdo |
|----------|----------|
| [COMANDOS.md](COMANDOS.md) | Instalar, correr, resolver erros |
| [QT_DESIGNER.md](QT_DESIGNER.md) | .ui, export, template Siemens |
| [FORNECEDORES.md](FORNECEDORES.md) | Mouser, TME, DigiKey |
| [ORGANIZACAO.md](ORGANIZACAO.md) | Mapa técnico do repositório |
| [CONTINUAR_AGENTE.md](CONTINUAR_AGENTE.md) | Notas para continuar o desenvolvimento |

---

## Checklist antes de entregar ao tutor

- [ ] `gui_stocktracker.ui` abre no Qt Designer sem erro de `.qrc`
- [ ] `python -m src.main` funciona
- [ ] `config/secrets.py` **não** vai no ZIP/Git (só `secrets.example.py`)
- [ ] `data/stock.xlsx` incluído se o tutor precisar de dados de teste
- [ ] Interface em **inglês**, estilo Siemens

---

## Limpar confusão (opcional)

Depois de confirmares que tudo funciona em **Downloads**:

1. Apagar `Desktop\StockTracker` (template velho) — só se não precisares.
2. Apagar `Desktop\siemens_template` (cópia solta) — a pasta **StockTracker-Designer** já tem recursos.
3. Manter **StockTracker-Projeto** como cópia de segurança sincronizada.

**Não apagues** `Downloads\StockTracker\StockTracker` — é o projeto principal com Git.
