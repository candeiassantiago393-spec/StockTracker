"""
Credential template — copy to secrets.py and fill in.

  copy config\\secrets.example.py config\\secrets.py

Replace each placeholder with your real key. Never commit secrets.py.
Leave "" for suppliers you do not use yet.
"""

# =============================================================================
# MOUSER — https://www.mouser.com/api-search/
# =============================================================================
MOUSER_API_KEY = "YOUR_MOUSER_API_KEY"

# =============================================================================
# DIGIKEY — https://developer.digikey.com/
# Use a SANDBOX app for development (see docs/user/DIGIKEY_SETUP.md).
# =============================================================================
DIGIKEY_CLIENT_ID = "YOUR_DIGIKEY_CLIENT_ID"
DIGIKEY_CLIENT_SECRET = "YOUR_DIGIKEY_CLIENT_SECRET"
DIGIKEY_ENV = "sandbox"
DIGIKEY_LOCALE_SITE = "PT"
DIGIKEY_LOCALE_LANGUAGE = "pt"
DIGIKEY_LOCALE_CURRENCY = "EUR"

# =============================================================================
# TME — https://developers.tme.eu
# =============================================================================
TME_API_TOKEN = "YOUR_TME_API_TOKEN"
TME_APP_SECRET = "YOUR_TME_APP_SECRET"

# =============================================================================
# ROBERT MAUSER — reserved (no public API)
# =============================================================================
ROBERT_MAUSER_API_KEY = ""

# =============================================================================
# RS COMPONENTS — key from RS portal; URL in src/core/suppliers/rs.py
# =============================================================================
RS_API_KEY = "YOUR_RS_API_KEY"
