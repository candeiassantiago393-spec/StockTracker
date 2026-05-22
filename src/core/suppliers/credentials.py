"""Read supplier API keys from environment or config/secrets.py."""
import os
from typing import Iterable

# Secret names per supplier (fill matching keys in config/secrets.py)
SUPPLIER_KEYS: dict[str, tuple[str, ...]] = {
    "mouser": ("MOUSER_API_KEY",),
    "digikey": ("DIGIKEY_CLIENT_ID", "DIGIKEY_CLIENT_SECRET"),
    "tme": ("TME_API_TOKEN", "TME_APP_SECRET"),
    "robert_mauser": ("ROBERT_MAUSER_API_KEY",),
    "rs": ("RS_API_KEY",),
}


def get_secret(secrets: dict, name: str, env_name: str | None = None) -> str:
    env = env_name or name
    return os.environ.get(env, "").strip() or str(secrets.get(name, "")).strip()


def is_configured(supplier: str, secrets: dict) -> bool:
    keys = SUPPLIER_KEYS.get(supplier, ())
    if not keys:
        return False
    return all(get_secret(secrets, key) for key in keys)


def configured_suppliers(secrets: dict) -> list[str]:
    return [sid for sid in SUPPLIER_KEYS if is_configured(sid, secrets)]
