# AI Chatbot — Streamlit + Groq

Un chatbot IA moderne construit avec Python, Streamlit et l'API Groq, avec mémoire de conversation complète.

## Fonctionnalités

- Interface de chat moderne (composants natifs Streamlit)
- Mémoire complète de la conversation (questions de suivi cohérentes)
- Bouton **New Conversation** pour repartir à zéro
- Indicateur de chargement pendant la génération
- Gestion propre des erreurs (clé API absente/invalide, rate limit, réseau, réponse vide)
- Clé API gérée de façon sécurisée via `.env` (jamais commitée sur GitHub)
- Code organisé en modules séparés (config / logique métier / interface)

## Architecture

```
Utilisateur → Interface Streamlit → st.session_state (mémoire)
            → src/chatbot.py → API Groq → LLM → réponse
            → st.session_state → réaffichage de la conversation
```

- `app.py` : point d'entrée, interface Streamlit uniquement.
- `src/config.py` : lecture du `.env` et constantes (modèle, paramètres).
- `src/chatbot.py` : appels à l'API Groq et gestion des erreurs.
- `src/utils.py` : fonctions utilitaires réutilisables.

## Technologies utilisées

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [Groq API](https://console.groq.com/) (modèle `llama-3.3-70b-versatile`)
- python-dotenv

## Installation

```bash
git clone <url-du-repo>
cd ai-chatbot
python -m venv venv
```

Activation de l'environnement virtuel :

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Installation des dépendances :

```bash
pip install -r requirements.txt
```

## Configuration

1. Copie `.env.example` vers `.env` :
   ```bash
   cp .env.example .env
   ```
2. Récupère une clé API sur [console.groq.com/keys](https://console.groq.com/keys).
3. Renseigne-la dans `.env` :
   ```
   GROQ_API_KEY=ta_cle_ici
   ```

⚠️ Le fichier `.env` est ignoré par Git (`.gitignore`) : il ne doit **jamais** être poussé sur GitHub.

## Lancement local

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans le navigateur, en général sur `http://localhost:8501`.

## Utilisation

1. Écris ton message dans le champ en bas de l'écran.
2. Le chatbot répond en tenant compte de tout l'historique.
3. Clique sur **New Conversation** (sidebar) pour effacer la conversation en cours.

## Structure du projet

```
ai-chatbot/
├── app.py
├── requirements.txt
├── .env            (non versionné)
├── .env.example
├── .gitignore
├── README.md
└── src/
    ├── __init__.py
    ├── chatbot.py
    ├── config.py
    └── utils.py
```

## Sécurité

- La clé API n'est jamais écrite en dur dans le code.
- Elle est lue uniquement depuis `.env` via `python-dotenv`.
- Les messages d'erreur affichés à l'utilisateur ne contiennent jamais la clé API ni de détails techniques sensibles.

## Gestion des erreurs

L'application gère explicitement :
- l'absence de clé API,
- une clé API invalide,
- les erreurs réseau,
- les limites de taux (rate limit) de Groq,
- les réponses vides du modèle,
- toute exception inattendue (message générique, sans détail technique exposé).

## Pistes d'amélioration

- Export de la conversation (PDF, texte)
- Choix du modèle depuis l'interface
- Streaming de la réponse token par token
- Authentification multi-utilisateurs
- Historique persistant entre sessions (base de données)

## Déploiement

Voir la section déploiement partagée séparément pour configurer les secrets sur une plateforme d'hébergement Streamlit.
