# Configuration — Stock Tracker

| File | Description |
|------|-------------|
| `secrets.example.py` | Template com placeholders |
| `secrets.py` | Chaves API reais (Mouser, DigiKey, TME, RS, …) |
| `credentials.py` | Carrega `secrets.py` em runtime |

## Setup num PC novo

Se clonares o **repositório privado** do lab, `secrets.py` já vem incluído — só precisas de `INSTALAR.bat` e `run.bat`.

Se clonares só o repo sem credenciais:

```powershell
copy config\secrets.example.py config\secrets.py
```

e preencher as chaves.

| Placeholder | Onde obter |
|-------------|------------|
| `YOUR_MOUSER_API_KEY` | [mouser.com/api-search](https://www.mouser.com/api-search/) |
| `YOUR_DIGIKEY_CLIENT_ID` / `SECRET` | [developer.digikey.com](https://developer.digikey.com/) (Sandbox) |
| `YOUR_RS_API_KEY` | Portal RS |

DigiKey: ver [docs/user/DIGIKEY_SETUP.md](../docs/user/DIGIKEY_SETUP.md)

## Repositório privado vs público

- **Repo privado (lab):** inclui `config/secrets.py` e `data/stock.xlsx` — cópia completa para a equipa.
- **Repo público:** não commitar `secrets.py`; manter só `secrets.example.py`.

Nunca tornar público um repo que contenha `secrets.py`.
