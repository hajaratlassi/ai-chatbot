"""
app.py
------
Point d'entrée de l'application Streamlit.
Ce fichier orchestre l'interface : il ne contient aucune logique d'appel
à Groq (déléguée à src/chatbot.py) ni de configuration (déléguée à src/config.py).
"""

import streamlit as st

from src import config
from src.chatbot import generer_reponse, ChatbotError
from src.utils import nouveau_message, historique_est_vide, tronquer_historique

# --- Configuration générale de la page Streamlit ---
# Doit être le premier appel Streamlit du script.
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="centered",
)


def initialiser_session() -> None:
    """
    Initialise st.session_state["messages"] une seule fois, au tout premier
    chargement de la page. Streamlit réexécute ce script à chaque interaction
    (message envoyé, clic sur un bouton...), mais st.session_state persiste
    entre ces réexécutions -- c'est ce qui constitue la mémoire de la conversation.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []  # liste de {"role": ..., "content": ...}


def afficher_sidebar() -> None:
    """Affiche la barre latérale : titre, infos, bouton New Conversation."""
    with st.sidebar:
        st.header("⚙️ Paramètres")
        st.markdown(f"**Modèle :** `{config.MODEL_NAME}`")
        st.markdown(f"**Messages en mémoire :** {len(st.session_state.messages)}")

        st.divider()

        if st.button("🆕 New Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.divider()
        st.caption(
            "Cette application utilise l'API Groq pour générer des réponses. "
            "Aucune donnée n'est stockée au-delà de cette session."
        )


def afficher_historique() -> None:
    """Affiche tous les messages déjà présents dans st.session_state.messages."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def gerer_nouveau_message(texte_utilisateur: str) -> None:
    """
    Traite l'envoi d'un nouveau message utilisateur :
    1. l'ajoute à l'historique et l'affiche
    2. appelle le modèle avec tout l'historique
    3. affiche la réponse (ou un message d'erreur propre)
    4. ajoute la réponse à l'historique

    Args:
        texte_utilisateur: le texte saisi par l'utilisateur dans le champ de chat.
    """
    # 1. Ajout + affichage immédiat du message utilisateur
    st.session_state.messages.append(nouveau_message("user", texte_utilisateur))
    with st.chat_message("user"):
        st.markdown(texte_utilisateur)

    # 2. Appel au modèle, avec indicateur de chargement
    with st.chat_message("assistant"):
        with st.spinner("Le modèle réfléchit..."):
            try:
                historique_envoye = tronquer_historique(st.session_state.messages)
                reponse = generer_reponse(historique_envoye)
                st.markdown(reponse)
            except ChatbotError as e:
                # Erreur prévisible et déjà traduite en message clair par chatbot.py
                reponse = None
                st.error(f"⚠️ {e}")

    # 3. On n'ajoute à l'historique que si on a bien reçu une réponse.
    # Si on ajoutait aussi les erreurs, le modèle les "verrait" comme faisant
    # partie de la conversation lors du prochain message, ce qu'on veut éviter.
    if reponse:
        st.session_state.messages.append(nouveau_message("assistant", reponse))


def main() -> None:
    st.title("💬 AI Chatbot")
    st.caption("Un chatbot alimenté par Groq, avec mémoire de conversation.")

    initialiser_session()
    afficher_sidebar()

    # Vérification précoce : si la clé API manque, on prévient tout de suite
    # plutôt que de laisser l'utilisateur taper un message pour rien.
    if not config.is_api_key_configured():
        st.warning(
            "⚠️ Aucune clé API Groq détectée. "
            "Crée un fichier `.env` à la racine du projet avec la ligne "
            "`GROQ_API_KEY=ta_cle` (voir `.env.example`)."
        )

    afficher_historique()

    if historique_est_vide(st.session_state.messages):
        st.info("👋 Pose-moi une question pour démarrer la conversation.")

    texte_utilisateur = st.chat_input("Écris ton message ici...")
    if texte_utilisateur:
        gerer_nouveau_message(texte_utilisateur)


if __name__ == "__main__":
    main()
