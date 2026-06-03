# Configuration

| File | In Git? | Description |
|------|---------|-------------|
| `secrets.example.py` | Yes | Template with placeholders |
| `secrets.py` | **No** | Your real keys (gitignored) |
| `credentials.py` | Yes | Loads `secrets.py` at runtime |

## Setup

```powershell
copy config\secrets.example.py config\secrets.py
```

Edit `secrets.py` — replace every placeholder with your real key.

| Placeholder | Where to obtain it |
|-------------|-------------------|
| `YOUR_MOUSER_API_KEY` | [mouser.com/api-search](https://www.mouser.com/api-search/) |
| `YOUR_DIGIKEY_CLIENT_ID` | [developer.digikey.com](https://developer.digikey.com/) → **Sandbox App** |
| `YOUR_DIGIKEY_CLIENT_SECRET` | Same Sandbox App (Credentials) |
| `YOUR_RS_API_KEY` | RS partner / API portal |

**DigiKey:** use a **Sandbox App** for development. Step-by-step: [docs/user/DIGIKEY_SETUP.md](../docs/user/DIGIKEY_SETUP.md)

## Test DigiKey

```powershell
python scripts/test_digikey_auth.py
```

Never commit `secrets.py`.
