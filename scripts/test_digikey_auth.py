"""
Testa token DigiKey (sandbox + production). Mostra o erro real da API.

Uso:
  1. Copia config/secrets.example.py para config/secrets.py e preenche DIGIKEY_*
  2. python scripts/test_digikey_auth.py

Ou variaveis de ambiente: DIGIKEY_CLIENT_ID, DIGIKEY_CLIENT_SECRET
"""
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

HOSTS = {
    "sandbox": "https://sandbox-api.digikey.com",
    "production": "https://api.digikey.com",
}


PLACEHOLDERS = (
    "O_SEU_CLIENT_ID_DIGIKEY",
    "O_SEU_CLIENT_SECRET_DIGIKEY",
    "A_SUA_CHAVE",
)


def _is_placeholder(value: str) -> bool:
    v = value.strip()
    if not v:
        return True
    return any(p in v for p in PLACEHOLDERS)


def load_credentials():
    client_id = os.environ.get("DIGIKEY_CLIENT_ID", "").strip()
    client_secret = os.environ.get("DIGIKEY_CLIENT_SECRET", "").strip()
    if client_id and client_secret:
        return client_id, client_secret
    try:
        from config.credentials import load_secrets

        secrets = load_secrets()
        client_id = str(secrets.get("DIGIKEY_CLIENT_ID", "")).strip()
        client_secret = str(secrets.get("DIGIKEY_CLIENT_SECRET", "")).strip()
        return client_id, client_secret
    except Exception:
        return "", ""


def credentials_ready(client_id: str, client_secret: str) -> bool:
    return bool(client_id and client_secret) and not (
        _is_placeholder(client_id) or _is_placeholder(client_secret)
    )


def try_token(label: str, host: str, client_id: str, client_secret: str) -> None:
    url = f"{host}/v1/oauth2/token"
    print(f"\n--- {label} ---")
    print(f"POST {url}")
    try:
        r = requests.post(
            url,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
            timeout=15,
        )
        print(f"Status: {r.status_code}")
        if r.ok:
            token = r.json().get("access_token", "")
            print(f"OK — access_token recebido ({len(token)} chars)")
            print(f"Usa DIGIKEY_ENV = \"{label}\" em config/secrets.py")
        else:
            print(f"Falhou — corpo: {r.text[:500]}")
    except Exception as exc:
        print(f"Erro de rede: {exc}")


def main() -> None:
    client_id, client_secret = load_credentials()
    if not credentials_ready(client_id, client_secret):
        print(
            "Credenciais em falta ou ainda sao placeholders.\n"
            "Edita config/secrets.py — substitui O_SEU_CLIENT_ID_DIGIKEY e\n"
            "O_SEU_CLIENT_SECRET_DIGIKEY pelos valores da Sandbox App.\n"
            "Guia: docs/utilizador/DIGIKEY_SETUP.md"
        )
        sys.exit(1)

    print(f"Client ID (primeiros 8 chars): {client_id[:8]}...")
    for label, host in HOSTS.items():
        try_token(label, host, client_id, client_secret)

    print(
        "\nNa tua app tens 'sandbox-ProductInformation V4' — o que funcionar"
        " aqui deve ser 'sandbox'. No portal Swagger: Switch to Sandbox Mode."
    )


if __name__ == "__main__":
    main()
