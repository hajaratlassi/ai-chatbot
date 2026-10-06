"""
config.py
---------
Centralise toute la configuration de l'application :
- chargement des variables d'environnement (.env)
- lecture des secrets Streamlit Cloud
- constantes du projet (modèle, paramètres par défaut)

Aucun autre fichier du projet ne doit lire la clé API directement :
tout passe par ce module.
"""

import os

from dotenv import load_dotenv

# ---------------------------------------------------------
# Chargement du fichier .env
# ---------------------------------------------------------
# En local, la clé API est stockée dans :
#
#     .env
#
# Exemple :
#     GROQ_API_KEY=ta_cle
#
# Le fichier .env est ignoré par Git grâce au .gitignore.
load_dotenv()


# ---------------------------------------------------------
# Récupération de la clé API Groq
# ---------------------------------------------------------
def _get_groq_api_key() -> str | None:
    """
    Récupère la clé API Groq.

    Priorité :
    1. Streamlit Secrets (utilisé sur Streamlit Cloud)
    2. Variable d'environnement / fichier .env (utilisé en local)

    Returns:
        str | None: La clé API si elle est configurée,
                    sinon None.
    """

    # -----------------------------------------------------
    # 1. Essayer Streamlit Secrets
    # -----------------------------------------------------
    try:
        import streamlit as st

        api_key = st.secrets.get("GROQ_API_KEY")

        if api_key:
            return str(api_key).strip()

    except Exception:
        # En local, Streamlit peut ne pas être disponible
        # ou les secrets peuvent ne pas être configurés.
        pass

    # -----------------------------------------------------
    # 2. Sinon, utiliser la variable d'environnement
    # -----------------------------------------------------
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        return api_key.strip()

    # Aucune clé trouvée
    return None


# Clé API Groq
GROQ_API_KEY: str | None = _get_groq_api_key()


# ---------------------------------------------------------
# Modèle utilisé
# ---------------------------------------------------------
# Modèle actuellement utilisé par le chatbot.
MODEL_NAME: str = "openai/gpt-oss-120b"


# ---------------------------------------------------------
# Paramètres de génération
# ---------------------------------------------------------

# temperature :
# - 0 = réponses plus déterministes
# - 0.7 = équilibre entre précision et créativité
# - 1+ = réponses plus créatives
DEFAULT_TEMPERATURE: float = 0.7


# Nombre maximum de tokens générés par réponse.
DEFAULT_MAX_TOKENS: int = 1024


# ---------------------------------------------------------
# Prompt système
# ---------------------------------------------------------
# Définit le comportement général de l'assistant.
SYSTEM_PROMPT: str = (
    "Tu es un assistant IA utile, clair et concis. "
    "Tu réponds en français sauf si l'utilisateur écrit dans une autre langue."
)


# ---------------------------------------------------------
# Vérification de la clé API
# ---------------------------------------------------------
def is_api_key_configured() -> bool:
    """
    Vérifie que la clé API Groq est présente et non vide.

    Returns:
        bool: True si une clé API est configurée,
              False sinon.
    """

    return bool(GROQ_API_KEY and GROQ_API_KEY.strip())