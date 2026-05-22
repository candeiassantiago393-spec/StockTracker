# Comandos e operacao

**Raiz do projeto:** `C:\Users\z005027j\Downloads\StockTracker\StockTracker`

---

## Ambiente virtual

```powershell
cd C:\Users\z005027j\Downloads\StockTracker\StockTracker
.\.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Executar a aplicacao

| Acao | Comando |
|------|---------|
| Interface grafica | `python -m src.main` ou `run.bat` |
| Consola de testes | `python -m src.test_terminal` |

---

## Configurar API Mouser

```powershell
copy config\secrets.example.py config\secrets.py
```

Editar `config\secrets.py` com a chave valida.

---

## Verificar diretorio de trabalho

```powershell
dir src
dir data
```

Se `src` nao existir: `cd StockTracker` (subpasta adicional).

---

## Sincronizar Excel (projeto legado)

```powershell
copy "C:\Users\z005027j\Documents\stock-tracker\data\stock.xlsx" "data\stock.xlsx"
```

---

## Consola de testes — opcoes

| Opcao | Funcao |
|-------|--------|
| 1 | Pesquisa no Excel |
| 2 | Consulta por codigo / scan |
| 3 | Entrada de stock (IN) |
| 4 | Saida de stock (OUT) — confirmacao `SIM` |
| 5 | Consulta Mouser (sem gravar) |
| 6 | Mouser + Excel + IN |
| 7 | Listar componentes |
| 8 | Historico (ultimos 20) |
| 9 | Alterar utilizador |
| 0 | Sair |

---

## Resolucao de problemas

| Sintoma | Causa provavel | Solucao |
|---------|----------------|---------|
| `No module named 'src'` | Diretorio incorreto | `cd` para raiz com `src/` e `run.bat` |
| `ImportError: relative import` | Ficheiro GUI executado isoladamente | `python -m src.main` |
| Nao grava no Excel | Ficheiro aberto no Excel | Fechar `stock.xlsx` |
| Mouser sem resposta | Chave / rede / referencia | Verificar `config/secrets.py` |
| Stock insuficiente | Quantidade invalida | Verificar stock atual |

---

## Git (opcional)

```powershell
git status
git add .
git commit -m "Descricao da alteracao"
git push
```

Nao commitar `config/secrets.py` nem dados sensiveis.
