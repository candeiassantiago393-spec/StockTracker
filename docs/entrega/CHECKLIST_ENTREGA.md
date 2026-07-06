# Checklist de entrega — Stock Tracker

Use esta lista nos **5 dias** antes da entrega à Siemens.

## 1. Código e repositório

- [ ] `git status` limpo (sem ficheiros sensíveis por commitar)
- [ ] `config/secrets.py` **não** está no Git (só `secrets.example.py`)
- [ ] `data/stock.xlsx` **não** está no Git (dados reais do laboratório)
- [ ] Push final para GitHub concluído
- [ ] Branch documentada (nome + link no relatório de estágio)

## 2. Instalação num PC limpo

- [ ] `INSTALAR.bat` executa sem erros
- [ ] `python tools\verificar_entrega.py` — todos os checks OK
- [ ] `run.bat` abre a aplicação
- [ ] `config\secrets.py` configurado (ou nota: “APIs opcionais”)

## 3. Demonstração (5–10 min)

Preparar roteiro:

1. **Components** — pesquisa Excel, SCAN, stock IN/OUT
2. **Passive (R/C)** — `Ctrl+Shift+M`, scan de resistor/condensador
3. **Equipments** — pesquisa, empréstimo, calibração
4. **Statistics** — gráficos + **EXPORT PDF**
5. **Ctrl+G** — pesquisa global

## 4. Documentação

- [ ] [`word/StockTracker_Documentacao_Projeto.docx`](../../word/StockTracker_Documentacao_Projeto.docx) regenerado (`python tools\build_project_docx.py`)
- [ ] Índice Word atualizado no Microsoft Word
- [ ] [`PROJETO_STOCKTRACKER_PT.md`](../especificacao/PROJETO_STOCKTRACKER_PT.md) revisto
- [ ] [`GUIA_RAPIDO_PT.md`](../guias/GUIA_RAPIDO_PT.md) revisto

## 5. Pacote físico / digital

Entregar à empresa:

| Item | Notas |
|------|-------|
| Link GitHub | Com acesso para o tutor |
| Word `.docx` | Documento formal |
| Relatório de estágio | 1–2 páginas: objetivos, resultados, limitações |
| Excel exemplo (opcional) | `stock.xlsx` anonimizado, fora do Git |
| Contacto | Email Siemens + instruções `run.bat` |

## 6. O que NÃO entregar

- `config/secrets.py` (chaves API reais)
- Cache local (`data/component_image_cache/`, `data/catalog_links/`)
- `.venv/` (o receptor cria com `INSTALAR.bat`)
- Backups Excel antigos (opcional, só se pedido)

## 7. Limitações conhecidas (mencionar no relatório)

- DigiKey sandbox pode dar 403 em produção — ver `docs/user/DIGIKEY_SETUP.md`
- Fechar Excel antes de gravar
- Modo Passive deteta R/C por texto/API — cristais ou peças atípicas podem precisar confirmação manual
- `data/stock.xlsx` é ficheiro único — sem multi-utilizador simultâneo
