"""
chatbot.py
----------
Toute la logique d'appel à l'API Groq vit ici :
- création du client Groq
- envoi de l'historique de conversation
- gestion des erreurs (clé invalide, réseau, rate limit, réponse vide, etc.)

Ce module ne touche jamais à Streamlit : il reçoit des données simples
(listes de dictionnaires) et retourne des données simples (texte ou erreur).
Ça le rend testable indépendamment de l'interface.
"""

from groq import Groq, APIConnectionError, RateLimitError, AuthenticationError, APIStatusError

from src import config


class ChatbotError(Exception):
    """
    Exception "maison" levée par ce module pour tout problème lié au chatbot.
    On la distingue des exceptions brutes de la librairie groq pour que
    app.py n'ait qu'un seul type d'erreur à intercepter, avec un message
    déjà traduit en français et compréhensible pour l'utilisateur final.
    """
    pass


def _get_client() -> Groq:
    """
    Crée et retourne un client Groq authentifié avec la clé API du .env.

    Raises:
        ChatbotError: si aucune clé API n'est configurée.
    """
    if not config.is_api_key_configured():
        raise ChatbotError(
            "Aucune clé API Groq n'est configurée. "
            "Ajoute GROQ_API_KEY=ta_cle dans le fichier .env à la racine du projet."
        )
    return Groq(api_key=config.GROQ_API_KEY)


def generer_reponse(historique: list[dict]) -> str:
    """
    Envoie l'historique de conversation à Groq et retourne la réponse du modèle.

    Args:
        historique: liste de messages au format
            [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
            (sans le message système, qui est ajouté ici automatiquement).

    Returns:
        str: le texte généré par le modèle.

    Raises:
        ChatbotError: pour toute erreur prévisible (clé absente/invalide,
            réseau, rate limit, réponse vide, erreur Groq générique).
    """
    client = _get_client()

    # On préfixe toujours l'historique avec le message système : il définit
    # le comportement général de l'assistant et n'est jamais affiché à l'utilisateur.
    messages = [{"role": "system", "content": config.SYSTEM_PROMPT}] + historique

    try:
        completion = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=messages,
            temperature=config.DEFAULT_TEMPERATURE,
            max_tokens=config.DEFAULT_MAX_TOKENS,
        )
    except AuthenticationError:
        raise ChatbotError(
            "La clé API Groq est invalide ou a été refusée. "
            "Vérifie sa valeur dans le fichier .env."
        )
    except RateLimitError:
        raise ChatbotError(
            "Limite de requêtes atteinte (rate limit) sur l'API Groq. "
            "Attends quelques instants avant de réessayer."
        )
    except APIConnectionError:
        raise ChatbotError(
            "Impossible de contacter l'API Groq. Vérifie ta connexion internet."
        )
    except APIStatusError as e:
        raise ChatbotError(
            f"L'API Groq a renvoyé une erreur (code {e.status_code}). "
            "Réessaie dans quelques instants."
        )
    except Exception:
        # Filet de sécurité : toute exception non prévue est transformée
        # en erreur générique propre, sans jamais exposer de détails techniques
        # ou de secrets à l'utilisateur.
        raise ChatbotError("Une erreur inattendue est survenue lors de l'appel au modèle.")

    # On vérifie qu'on a bien reçu au moins un choix de réponse et du texte.
    if not completion.choices or not completion.choices[0].message.content:
        raise ChatbotError("Le modèle a renvoyé une réponse vide. Réessaie ta question.")

    return completion.choices[0].message.content.strip()
