"""Carregamento de credenciais locais (config/secrets.py)."""
import importlib.util
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent
SECRETS_FILE = CONFIG_DIR / "secrets.py"


def load_secrets() -> dict:
    """Devolve atributos de secrets.py como dicionario."""
    if not SECRETS_FILE.is_file():
        return {}
    spec = importlib.util.spec_from_file_location("secrets", SECRETS_FILE)
    if not spec or not spec.loader:
        return {}
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {
        key: getattr(module, key)
        for key in dir(module)
        if key.isupper() and not key.startswith("_")
    }
