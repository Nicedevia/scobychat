import streamlit as st
from components.common import handle_login
from dotenv import load_dotenv
import os
from streamlit_option_menu import option_menu
from  models.mon_mondel import User, Country, Language, session
import streamlit as st
import re


st.image('asset/SCOBOY.png')


load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

access_granted = False
if "input" not in st.session_state:
    st.session_state.input = ""

if st.session_state.get('switch_button', False):
     st.session_state['menu_option'] = (st.session_state.get('menu_option',0)+1) % 4
     manual_select = st.session_state['menu_option']
else:
     manual_select = None

selected = option_menu(None, ["Sing up", "Log in",  "History", 'Setting'], 
     icons=['house', 'cloud-upload', "list-task", 'gear'], 
     menu_icon="cast", default_index=0, orientation="horizontal",
    
     styles={
         "container": {"padding": "0!important", "background-color": "linear-gradient(to right, #D4FAD4, #D4FAD4)"},
         "icon": {"color": "linear-gradient(to right, #D4FAD4, #D4FAD4)", "font-size": "25px"}, 
         "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
         "nav-link-selected": {"background-color": "orange"},
     }
 )



if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False


if selected == 'Sing up':
    st.title("Formulaire d'inscription")

    st.header("Utilisateur")
    username = st.text_input("Nom d'utilisateur (@email)")
    password = st.text_input("Mot de passe 7 caractères, une MAJ et un caractère spécial", type="password")
    country_name = st.text_input("Pays")
    language_name = st.text_input("Langue")

    if st.button("S'inscrire"):
        if len(password) < 7:
            st.error("Le mot de passe doit contenir au moins 7 caractères.")
        elif not re.search(r'[A-Z]', password):
            st.error("Le mot de passe doit contenir au moins une lettre majuscule.")
        elif not re.search(r'\d', password):
            st.error("Le mot de passe doit contenir au moins un caractère numérique.")
        else:
            new_user = User(username=username, password=password)
            new_country = Country(name=country_name)
            new_language = Language(name=language_name)
            session.add(new_user)
            session.add(new_country)
            session.add(new_language)
            session.commit()
            st.success("Inscription réussie !")



    session.close()
 
        

if selected == 'Log in':
    if not st.session_state.access_granted:
        handle_login()
