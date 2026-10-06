"""
utils.py
--------
Petites fonctions utilitaires réutilisables, sans dépendance à Streamlit
ni à Groq. Elles ne font qu'une chose chacune et sont faciles à tester.
"""


def nouveau_message(role: str, content: str) -> dict:
    """
    Construit un message au format attendu par l'historique de conversation.

    Args:
        role: "user" ou "assistant".
        content: le texte du message.

    Returns:
        dict: {"role": role, "content": content}
    """
    return {"role": role, "content": content}


def historique_est_vide(historique: list[dict]) -> bool:
    """Retourne True si l'historique de conversation ne contient aucun message."""
    return len(historique) == 0


def tronquer_historique(historique: list[dict], max_messages: int = 30) -> list[dict]:
    """
    Garde seulement les N derniers messages de l'historique.

    Utile pour éviter d'envoyer un historique trop long au modèle
    (coût plus élevé, risque de dépasser la fenêtre de contexte).
    On garde toujours les messages les plus récents, qui sont les plus
    pertinents pour la conversation en cours.

    Args:
        historique: la liste complète des messages.
        max_messages: nombre maximum de messages à conserver.

    Returns:
        list[dict]: l'historique tronqué (ou inchangé s'il est déjà assez court).
    """
    if len(historique) <= max_messages:
        return historique
    return historique[-max_messages:]
