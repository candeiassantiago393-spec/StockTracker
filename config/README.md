# Configuration

| File | In Git? | Description |
|------|---------|-------------|
| `secrets.example.py` | Yes | Template — copy to `secrets.py` |
| `secrets.py` | **No** | Your API keys (gitignored) |
| `credentials.py` | Yes | Loads `secrets.py` at runtime |

```powershell
copy secrets.example.py secrets.py
```

Then edit `secrets.py` with your keys (Mouser, TME, RS, DigiKey, etc.).
