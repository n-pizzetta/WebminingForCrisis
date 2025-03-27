import streamlit as st
from streamlit_option_menu import option_menu

from pages import visualization, home, topics, sentiments, wordclouds

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        .centered-title {
            text-align: center;
            font-size: 5rem; 
        }
        .lil_space {
            margin-top: 60px;  /* Ajustez cette valeur pour contrôler l'espacement */
        }

        .sidebar-title {
            font-size: 1.3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 15px;
        }
        
        /* Masque la barre de recherche et autres éléments par défaut dans la sidebar */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    page = option_menu(
        menu_title = "Menu",
        options = ['Home', 'Visualize Timeline','Topics', 'Sentiments', 'WordClouds'],
        icons = ['house-door','graph-up','file-earmark-text','bookmark-heart','clouds'], # bootstrap icons
        menu_icon = "heart-eyes-fill",
        default_index=0,
    )

        
menu_items = {
        "Home": home.show_page,
        "Visualize Timeline": visualization.show_page,
        "Topics": topics.show_page,
        "Sentiments" : sentiments.show_page,
        "WordClouds" : wordclouds.show_page,
    }


menu_items[page]() 
