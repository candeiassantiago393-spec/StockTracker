# Suppliers — Mouser, DigiKey, TME, RS, Robert Mauser

## Credentials (`config/secrets.py`)

Copy from `config/secrets.example.py`. Use empty `""` for suppliers you are not using yet.

| Supplier | Keys in `secrets.py` |
|----------|----------------------|
| **Mouser** | `MOUSER_API_KEY` |
| **DigiKey** | `DIGIKEY_CLIENT_ID`, `DIGIKEY_CLIENT_SECRET`, `DIGIKEY_ENV` (`sandbox` / `production`) |
| **TME** | `TME_API_TOKEN`, `TME_APP_SECRET` (both required) |
| **Robert Mauser** | `ROBERT_MAUSER_API_KEY` (reserved — no public API yet) |
| **RS** | `RS_API_KEY` only (base URL in `src/core/suppliers/rs.py`) |

Example (RS only):

```python
RS_API_KEY = "your-rs-key-here"
```

## Status in code

| Supplier | API | In project |
|----------|-----|------------|
| **Mouser** | Yes | **Working** (GUI SCAN + terminal 5/6) |
| **DigiKey** | Yes (OAuth) | Implemented — may get 403 on sandbox until portal is configured |
| **RS** | Partner-specific | Key in secrets; URL hardcoded in `rs.py` (adjust if RS docs differ) |
| **TME** | Yes | **Working** (terminal option 10) |
| **Robert Mauser** | No public REST | Manual / Excel |

## Code layout

```
src/core/suppliers/
├── credentials.py   # which keys each supplier needs
├── base.py
├── mouser.py
├── digikey.py
├── rs.py
├── tme.py
└── robert_mauser.py
```

## Test from Python

```python
from src.core.stock import StockTracker
t = StockTracker()
print("Configured:", t.configured_suppliers())
print(t.search_rs("123-456"))   # after RS_API_KEY (+ URL if needed)
print(t.search_digikey("MCP2221A-I/SL-ND"))
```

Terminal menu still uses Mouser for options 5 and 6; other suppliers can be tested with the snippet above or we can extend the menu later.

## Registration links

- Mouser: https://www.mouser.com/api-search/
- DigiKey: https://developer.digikey.com/
- TME: https://developers.tme.eu
- RS: partner / api-store portal (endpoint varies by account)
