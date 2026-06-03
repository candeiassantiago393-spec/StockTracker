# Supplier APIs — Mouser, DigiKey, TME, RS, Robert Mauser

## Credentials (`config/secrets.py`)

Copy from `config/secrets.example.py` and replace placeholders. Use empty `""` for suppliers you do not use yet.

**DigiKey setup:** [DIGIKEY_SETUP.md](DIGIKEY_SETUP.md)

| Supplier | Keys in `secrets.py` |
|----------|----------------------|
| **Mouser** | `MOUSER_API_KEY` |
| **DigiKey** | `DIGIKEY_CLIENT_ID`, `DIGIKEY_CLIENT_SECRET`, `DIGIKEY_ENV` (`sandbox` / `production`) |
| **TME** | `TME_API_TOKEN`, `TME_APP_SECRET` (both required) |
| **Robert Mauser** | `ROBERT_MAUSER_API_KEY` (reserved — no public API yet) |
| **RS** | `RS_API_KEY` (base URL in `src/core/suppliers/rs.py`) |

Example (RS only):

```python
RS_API_KEY = "your-rs-key-here"
```

## Implementation status

| Supplier | API | In project |
|----------|-----|------------|
| **Mouser** | Yes | Active (GUI SCAN + terminal) |
| **DigiKey** | Yes (OAuth) | Implemented — sandbox may return 403 until portal is configured |
| **RS** | Partner-specific | Key in secrets; URL in `rs.py` (adjust per account docs) |
| **TME** | Yes | Implemented |
| **Robert Mauser** | No public REST | Manual / Excel only |

## Code layout

```
src/core/suppliers/
├── credentials.py
├── base.py
├── mouser.py
├── digikey.py
├── rs.py
├── tme.py
└── robert_mauser.py
```

## Quick test

```python
from src.core.stock import StockTracker
t = StockTracker()
print("Configured:", t.configured_suppliers())
```

```powershell
python scripts/test_digikey_auth.py
```

## Registration

- Mouser: https://www.mouser.com/api-search/
- DigiKey: https://developer.digikey.com/
- TME: https://developers.tme.eu
- RS: partner / API portal (endpoint varies by account)
