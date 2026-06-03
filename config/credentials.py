"""Carregamento de credenciais locais vindas de (config/secrets.py)."""
import importlib.util #usado para ler o secrets.py sem fazer import
from pathlib import Path #trata do caminho

CONFIG_DIR = Path(__file__).resolve().parent#Descobre a pasta onde está este credentials.py
SECRETS_FILE = CONFIG_DIR / "secrets.py"#constrói caminho 


def load_secrets() -> dict:
    """Devolve atributos de secrets.py como dicionario."""
    if not SECRETS_FILE.is_file():#verifica ficheiro se nao existir return
        return {}#devolve dicionario vazio,evita crash
    spec = importlib.util.spec_from_file_location("secrets", SECRETS_FILE)
    if not spec or not spec.loader:#(verifica)se nao conseguir preparar a spec nao tenta executar
        return {} # se nao verificar da return
    module = importlib.util.module_from_spec(spec)#criação do objeto module
    spec.loader.exec_module(module)#aqui vai ao secrets buscar o valor do module API MOUSER DIGIKEY
    return { #Devolve o dicionario
        key: getattr(module, key)#Para cada nome key escolhido, vai buscar o valor real ao módulo (getattr).
        for key in dir(module)#lista todos os nomes disponiveis no modulo
        if key.isupper() and not key.startswith("_")
        # Mantem apenas constantes publicas em MAIUSCULAS (chaves/configuracoes) e ignora atributos internos.
    }
