import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI
from models.mon_mondel import User, session
import os 
from configs.config import OPENAI_API_KEY


"""
Ce fichier contient les fonctions pour lancer et principale de cette API
"""
API_KEY = os.getenv('OPENAI_API_KEY')

def handle_login():
    """
    Gère le processus de connexion de l'utilisateur.
    Cette fonction affiche un formulaire de connexion, vérifie les informations de l'utilisateur,
    et permet à l'utilisateur de se connecter à l'application.
    Args:
        Aucun.
    Returns:
        Aucun retour explicite.
    Exemple:
        >>> handle_login()
        # L'interface utilisateur pour la connexion est affichée.
    Remarques:
        - Cette fonction suppose que la session utilisateur est initialisée et que la base de données
          contient les informations d'identification (nom d'utilisateur et mot de passe).
        - En cas de succès, cette fonction définira `st.session_state.user_id` pour indiquer que
          l'utilisateur est connecté.
        - Si l'utilisateur est connecté, cette fonction appelle la fonction `main()` pour afficher l'interface
          principale du Chatbot.
    """

    st.title("Connexion")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            st.success("Connexion réussie. Bienvenue, {}!".format(username))
            st.session_state.user_id = user.id
        else:
            st.error("Identifiants incorrects")

    session.close()

    if "user_id" in st.session_state:
        main()

programming_languages = ["Python", "JavaScript", "HTML"] 

API_KEY = OPENAI_API_KEY 
st.set_page_config(page_title='🤖', layout='centered')

if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""

def main():
    """
    Fonction principale pour l'application Streamlit de Chatbot.

    Cette fonction configure et affiche l'interface utilisateur pour l'application Chatbot.
    Elle gère l'initialisation, la connexion à l'API OpenAI, l'interaction avec l'utilisateur,
    et l'affichage des réponses du Chatbot.

    Args:
        Aucun.

    Returns:
        Aucun retour explicite.

    Exemple:
         main()
        # L'interface utilisateur de l'application Chatbot est affichée.

    Remarques:
        Cette fonction suppose que la variable `API_KEY` contient une clé valide pour accéder
        à l'API OpenAI. Elle utilise également d'autres variables globales telles que
        `MODEL`, `ENTITY_MEMORY_CONVERSATION_TEMPLATE`, et `programming_languages`.
    """

    st.title(":globe_with_meridians: scoboy 🤖")
    st.markdown('''> :black[**Un ChatBot basé sur ChatGPT qui se souvient du contexte de la conversation.**]''')

    if API_KEY:
        st.write("API :white_check_mark:")

        MODEL = 'gpt-3.5-turbo'
        llmObj = ChatOpenAI(openai_api_key=API_KEY, model_name=MODEL)

        K = 3
        if 'entity_memory' not in st.session_state:
            st.session_state.entity_memory = ConversationEntityMemory(llm=llmObj, k=K)
        
        programming_language = st.selectbox("Langage de programmation de la réponse", programming_languages)
        

        comments = "avec des commentaires et une description"

        prompt = ENTITY_MEMORY_CONVERSATION_TEMPLATE + f"en {programming_language}{comments}"

        Conversation = ConversationChain(llm=llmObj, prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE, memory=st.session_state.entity_memory)

        user_input = st.text_input("Vous: ", st.session_state["input"],
                                   key="input",
                                   placeholder="Votre ami Chatbot ! Posez vos questions...",
                                   label_visibility='hidden')
        
        execute_button = st.button("Exécuter") 

        if execute_button and user_input:
            output = Conversation.run(input=user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(output)

        with st.expander("Conversation", expanded=True):
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                st.info(st.session_state["past"][i], icon="🧐")
                st.success(st.session_state["generated"][i], icon="🤖")

    else:
        st.warning('API :x:')
