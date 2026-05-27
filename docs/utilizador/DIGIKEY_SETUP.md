# DigiKey — configurar do zero (uma so app)

## 1. Apagar apps antigas no portal

1. [developer.digikey.com](https://developer.digikey.com/) — login
2. Menu do teu nome → **Apps**

**Sandbox Apps**

- Para cada app: seta ao lado de **Edit** → **Delete** (ou abre a app → separador **Delete**)
- Apaga todas (incluindo "Stock Tracker" antigas)

**Production Apps** (se existirem)

- **Organizations** → **Production Apps**
- Apaga as duplicadas "Stock Tracker" da mesma forma

## 2. Criar uma unica app nova

1. **Sandbox Apps** → botao vermelho **+ Create Sandbox App**
2. Nome: `Stock Tracker`
3. Callback URL: `https://localhost`
4. Descricao: inventario / pesquisa de pecas
5. Adiciona API: **ProductInformation V4** (sandbox)
6. **Add sandbox app** → espera estado **Approved**

## 3. Copiar credenciais

1. Clica no nome **Stock Tracker** (link azul)
2. **Credentials** → revela e copia:
   - **Client ID**
   - **Client Secret** (par da mesma app)

## 4. Colar no projeto

Edita `config/secrets.py`:

```python
DIGIKEY_CLIENT_ID = "colar Client ID aqui"
DIGIKEY_CLIENT_SECRET = "colar Client Secret aqui"
DIGIKEY_ENV = "sandbox"
```

Guarda o ficheiro. Tambem preenche `MOUSER_API_KEY` se usas Mouser.

## 5. Testar

```powershell
cd c:\Users\z005027j\Downloads\StockTracker\StockTracker
python scripts/test_digikey_auth.py
```

Esperado: `OK — access_token recebido` em **sandbox**.

Depois:

```powershell
python -c "from src.core.stock import StockTracker; t=StockTracker(); print(t.search_digikey('MCP2221A-I/SL-ND'))"
```

## Erros comuns

| Erro | Causa | Solucao |
|------|-------|---------|
| Invalid clientId | Chaves de Production App em sandbox | Usar **Sandbox App** + `DIGIKEY_ENV = "sandbox"` |
| Sem credenciais | Placeholders ainda em secrets.py | Substituir `O_SEU_CLIENT_ID_...` pelos valores reais |
| 403 na pesquisa | API nao subscrita na app | Ativar ProductInformation V4 na Sandbox App |

## Swagger (opcional)

Documentacao → **Switch to Sandbox Mode** → KeywordSearch → Authorize (Client ID + OAuth2 ID/Secret da **mesma** Sandbox App).

Nao e obrigatorio se `test_digikey_auth.py` ja der OK.
