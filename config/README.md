# Configuration

| File | In Git? | Description |
|------|---------|-------------|
| `secrets.example.py` | Yes | Template with placeholders (`A_SUA_CHAVE_...`) |
| `secrets.py` | **No** | Your real keys (gitignored) |
| `credentials.py` | Yes | Loads `secrets.py` at runtime |

## Setup

```powershell
copy config\secrets.example.py config\secrets.py
```

Edit `secrets.py` — replace every placeholder with your real key.

| Placeholder | Where to get it |
|-------------|-----------------|
| `A_SUA_CHAVE_MOUSER` | [mouser.com/api-search](https://www.mouser.com/api-search/) |
| `O_SEU_CLIENT_ID_DIGIKEY` | [developer.digikey.com](https://developer.digikey.com/) → **Sandbox App** |
| `O_SEU_CLIENT_SECRET_DIGIKEY` | Same Sandbox App (Credentials) |
| `A_SUA_CHAVE_RS` | RS partner portal |

**DigiKey:** use a **Sandbox App** only for development. Step-by-step: [docs/utilizador/DIGIKEY_SETUP.md](../docs/utilizador/DIGIKEY_SETUP.md)

## Test DigiKey

```powershell
python scripts/test_digikey_auth.py
```

Never commit `secrets.py`.
