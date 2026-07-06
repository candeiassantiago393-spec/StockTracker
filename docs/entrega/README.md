# Entrega — Stock Tracker (Siemens)

Pacote de documentação para entrega do estágio.

| Documento | Descrição |
|-----------|-----------|
| [CHECKLIST_ENTREGA.md](CHECKLIST_ENTREGA.md) | Lista de verificação antes de entregar |
| [PACOTE_ENTREGA.md](PACOTE_ENTREGA.md) | O que incluir na entrega à empresa |

## Documentos principais (já no repositório)

| Audiência | Ficheiro |
|-----------|----------|
| **Empresa / tutor** | [`word/StockTracker_Documentacao_Projeto.docx`](../../word/StockTracker_Documentacao_Projeto.docx) |
| **Especificação PT** | [`especificacao/PROJETO_STOCKTRACKER_PT.md`](../especificacao/PROJETO_STOCKTRACKER_PT.md) |
| **Operadores** | [`guias/GUIA_RAPIDO_PT.md`](../guias/GUIA_RAPIDO_PT.md) |
| **Índice geral** | [`README.md`](../README.md) |

## Arranque rápido

```powershell
.\INSTALAR.bat          # primeira vez (venv + dependências)
copy config\secrets.example.py config\secrets.py
# editar config\secrets.py com as chaves API
.\run.bat
```

Verificar instalação:

```powershell
python tools\verificar_entrega.py
```

## Repositório GitHub

https://github.com/candeiassantiago393-spec/StockTracker

Branch de entrega: `backup/before-equipment-loan` (ou `main` após merge).
