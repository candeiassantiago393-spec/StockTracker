"""
Modelo de credenciais — copiar para secrets.py e preencher.

  copy config\\secrets.example.py config\\secrets.py

Substitui cada "A_SUA_..." pela chave real. Nunca commits secrets.py.
Deixa "" nos fornecedores que ainda nao usas.
"""

# =============================================================================
# MOUSER — https://www.mouser.com/api-search/
# =============================================================================
MOUSER_API_KEY = "A_SUA_CHAVE_MOUSER"

# =============================================================================
# DIGIKEY — https://developer.digikey.com/
# Usa app SANDBOX (Create Sandbox App), nao Production App.
# =============================================================================
DIGIKEY_CLIENT_ID = "O_SEU_CLIENT_ID_DIGIKEY"
DIGIKEY_CLIENT_SECRET = "O_SEU_CLIENT_SECRET_DIGIKEY"
# "sandbox" com Sandbox App | "production" so com Production App + API producao
DIGIKEY_ENV = "sandbox"

# =============================================================================
# TME — https://developers.tme.eu
# =============================================================================
TME_API_TOKEN = "O_SEU_TOKEN_TME"
TME_APP_SECRET = "O_SEU_APP_SECRET_TME"

# =============================================================================
# ROBERT MAUSER — sem API publica (reservado)
# =============================================================================
ROBERT_MAUSER_API_KEY = ""

# =============================================================================
# RS COMPONENTS — chave no portal RS; URL em src/core/suppliers/rs.py
# =============================================================================
RS_API_KEY = "A_SUA_CHAVE_RS"
