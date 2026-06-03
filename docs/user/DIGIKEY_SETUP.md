# DigiKey API setup (sandbox)

Use this guide to configure DigiKey credentials in `config/secrets.py` for development.

---

## 1. Developer account

1. Register at https://developer.digikey.com/
2. Sign in to the developer portal

---

## 2. Create a Sandbox application

1. **My Apps** → **Create Sandbox App** (not Production for initial development)
2. Note the **Client ID** and **Client Secret**
3. Enable the product search / keyword search APIs required by your app (per portal options)

---

## 3. Configure `secrets.py`

```python
DIGIKEY_CLIENT_ID = "your-client-id"
DIGIKEY_CLIENT_SECRET = "your-client-secret"
DIGIKEY_ENV = "sandbox"
DIGIKEY_LOCALE_SITE = "PT"
DIGIKEY_LOCALE_LANGUAGE = "pt"
DIGIKEY_LOCALE_CURRENCY = "EUR"
```

Use `DIGIKEY_ENV = "production"` only with a **Production** app and production API access.

---

## 4. Test authentication

From repository root:

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/test_digikey_auth.py
```

A successful run prints token information or a successful API response. HTTP **403** often means sandbox app mismatch, wrong environment, or missing API product on the app.

---

## 5. Use in Stock Tracker

When keys are set, DigiKey is included in the multi-supplier SCAN order (see project specification). Empty `DIGIKEY_CLIENT_ID` / `SECRET` skips DigiKey.

---

## Troubleshooting

| Issue | Check |
|-------|--------|
| 403 Forbidden | Sandbox app vs `DIGIKEY_ENV`, API products enabled on app |
| Invalid client | Client ID/secret copied correctly, no extra spaces |
| No results | Part number format, locale settings |

See also: [SUPPLIERS.md](SUPPLIERS.md), [COMMANDS.md](COMMANDS.md).
