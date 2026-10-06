"""
config.py
---------
Centralise toute la configuration de l'application :
- chargement des variables d'environnement (.env)
- constantes du projet (modèle, paramètres par défaut)

Aucun autre fichier du projet ne doit lire le .env directement :
tout passe par ce module.
"""

import os
from dotenv import load_dotenv

# Charge le contenu du fichier .env dans les variables d'environnement
# du processus Python en cours d'exécution.
load_dotenv()

# Récupère la clé API Groq. Si la variable n'existe pas dans le .env,
# os.getenv renvoie None (plutôt que de lever une exception) -- c'est
# volontaire : on veut pouvoir détecter l'absence de clé proprement
# dans le code appelant, avec un message clair, plutôt qu'un crash brut.
GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")

# Nom du modèle utilisé pour les réponses du chatbot.
# llama-3.3-70b-versatile est, au moment de l'écriture de ce projet,
# le modèle généraliste recommandé par Groq pour ce type d'usage.
MODEL_NAME: str = "openai/gpt-oss-120b"# Paramètres de génération par défaut.
# temperature : contrôle la créativité/aléatoire des réponses (0 = déterministe, 1+ = plus créatif).
DEFAULT_TEMPERATURE: float = 0.7

# max_tokens : nombre maximum de tokens (fragments de mots) que le modèle peut générer en réponse.
DEFAULT_MAX_TOKENS: int = 1024

# Message système qui définit le comportement général de l'assistant.
# Il est envoyé à chaque requête, avant l'historique de conversation.
SYSTEM_PROMPT: str = (
    "Tu es un assistant IA utile, clair et concis. "
    "Tu réponds en français sauf si l'utilisateur écrit dans une autre langue."
)


def is_api_key_configured() -> bool:
    """
    Vérifie que la clé API est présente et non vide.

    Returns:
        bool: True si une clé API semble configurée, False sinon.
    """
    return bool(GROQ_API_KEY and GROQ_API_KEY.strip())
