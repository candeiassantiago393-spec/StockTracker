"""
Test DigiKey OAuth token (sandbox + production). Prints the API response.

Usage:
  1. Copy config/secrets.example.py to config/secrets.py and set DIGIKEY_*
  2. python scripts/test_digikey_auth.py

Or environment variables: DIGIKEY_CLIENT_ID, DIGIKEY_CLIENT_SECRET
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
    "YOUR_DIGIKEY_CLIENT_ID",
    "YOUR_DIGIKEY_CLIENT_SECRET",
    "YOUR_MOUSER_API_KEY",
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


def try_keyword_search(host: str, client_id: str, client_secret: str) -> None:
    """Testa pesquisa v4 (mesmo fluxo que a app)."""
    keyword = "MCP2221A-I/SL-ND"
    print(f"\n--- keyword search (sandbox) ---")
    print(f"POST {host}/products/v4/search/keyword  Keywords={keyword!r}")
    try:
        tr = requests.post(
            f"{host}/v1/oauth2/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
            timeout=15,
        )
        if not tr.ok:
            print(f"Token falhou: {tr.status_code} {tr.text[:300]}")
            return
        token = tr.json().get("access_token", "")
        sr = requests.post(
            f"{host}/products/v4/search/keyword",
            headers={
                "X-DIGIKEY-Client-Id": client_id,
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={"Keywords": keyword, "Limit": 5, "Offset": 0},
            timeout=15,
        )
        print(f"Status: {sr.status_code}")
        if sr.ok:
            products = sr.json().get("Products") or []
            print(f"OK — {len(products)} produto(s) na resposta")
        else:
            print(f"Corpo: {sr.text[:500]}")
            if sr.status_code == 403:
                try:
                    cid = sr.json().get("correlationId", "")
                    if cid:
                        print(f"correlationId: {cid}")
                except Exception:
                    pass
                print(
                    "\n403 com portal Approved+Enabled: as chaves estao OK (token 200).\n"
                    "  A pesquisa e bloqueada pelo servidor DigiKey (sandbox), nao pelo Stock Tracker.\n"
                    "  Confirma no Swagger (Sandbox Mode) KeywordSearch; se 403 igual,\n"
                    "  contacta suporte DigiKey com o correlationId acima.\n"
                    "  Para inventario real: Production App + DIGIKEY_ENV=production (apos aprovacao)."
                )
    except Exception as exc:
        print(f"Erro: {exc}")


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
            "Missing credentials or placeholders still set.\n"
            "Edit config/secrets.py — set DIGIKEY_CLIENT_ID and\n"
            "DIGIKEY_CLIENT_SECRET from your DigiKey Sandbox App.\n"
            "Guide: docs/user/DIGIKEY_SETUP.md"
        )
        sys.exit(1)

    print(f"Client ID (primeiros 8 chars): {client_id[:8]}...")
    for label, host in HOSTS.items():
        try_token(label, host, client_id, client_secret)

    try_keyword_search(HOSTS["sandbox"], client_id, client_secret)

    print(
        "\nNa tua app tens 'sandbox-ProductInformation V4' — o que funcionar"
        " aqui deve ser 'sandbox'. No portal Swagger: Switch to Sandbox Mode."
    )
    print(
        "Compara os primeiros caracteres do Client ID acima com o portal"
        " (Show key) — tem de ser a MESMA app."
    )


if __name__ == "__main__":
    main()
