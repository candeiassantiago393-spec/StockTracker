# Stock Tracker

Inventário de componentes e equipamentos de laboratório. Excel local, interface Siemens (PySide6), consulta opcional a distribuidores (Mouser, DigiKey, TME, RS).

**Manual do utilizador (PT):** [`docs/guias/MANUAL_UTILIZADOR.md`](docs/guias/MANUAL_UTILIZADOR.md)  
**Documentação:** [`docs/README.md`](docs/README.md)

---

## Funcionalidades

- Folhas Excel: `Components`, `Generic` (R/C), `Equipments`, `EquipmentLoans`, `History`
- Páginas: **Components**, **Passive (R/C)**, **Equipments**, **Statistics**
- Scan multi-distribuidor, pesquisa global (`Ctrl+G`), exportação PDF
- Imagens de catálogo, equipamentos com pasta por ID, empréstimos e alertas de calibração

---

## Instalação

```powershell
.\INSTALAR.bat
copy config\secrets.example.py config\secrets.py
```

Editar `config\secrets.py`. Arrancar com `run.bat`.

Verificar: `python tools\verificar_instalacao.py`

---

## Estrutura

```
StockTracker/
├── run.bat, INSTALAR.bat
├── config/          secrets.example.py, credentials.py
├── data/            stock.xlsx, backups/, equipments/
├── docs/            manual, especificação, fluxogramas
├── src/
│   ├── main.py
│   ├── core/        stock.py, suppliers/
│   └── gui/
├── tools/           Designer, export UI, manutenção
└── word/            documentação Word do projeto
```

---

## Requisitos

- Windows 10/11, Python 3.10+
- Fechar `data/stock.xlsx` no Excel antes de gravar
- `config/secrets.py` não vai para o Git
