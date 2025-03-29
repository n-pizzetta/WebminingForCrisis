import streamlit as st


def add_title(title, level=1, centered=True):
    """
    Ajoute un titre formaté avec un niveau HTML.
    """
    css_class = "centered-title" if centered else ""
    st.markdown(f'<h{level} class="{css_class}">{title}</h{level}>', unsafe_allow_html=True)

def add_paragraph(content):
    """
    Ajoute un paragraphe formaté en Markdown.
    """
    st.markdown(content)
    
def add_image(image_name, width=None):
    """
    Ajoute une image centrée avec une largeur facultative.
    """
    cols = st.columns([1, 6, 1])  
    with cols[1]:  
        st.image(f'assets/{image_name}', width=width)
    
def show_page():
    add_title("Web Mining Project 2024–2025")
    add_title("Project Overview", level=3, centered=False)

    add_paragraph("""
    This project focuses on exploring and analyzing social media data—specifically from Twitter—during crisis events such as 
    floods, fires, earthquakes, and more.  
    The project has two main goals:  
    1) Describe and analyze the social web graph based on content, usage, and structure;  
    2) Mine relevant knowledge to support decision-making during emergencies.
    """)

    add_title("Data Description", level=3, centered=False)
    add_paragraph("""
    The dataset is provided by the TREC Incident Stream initiative and consists of real tweets posted during various past crisis events.  
    It includes structured information such as:  
    - Events (e.g., “2012 Guatemala Earthquake”),  
    - Event Types (e.g., flood, earthquake, typhoon),  
    - Users who posted during the events,  
    - Tweets containing text, hashtags, mentions, and metadata,  
    - Human-annotated tweet priorities (Low, Medium, High, Critical),  
    - High-level information categories (e.g., Advice, News, Search & Rescue).
    """)

    add_title("Try It Now!", level=3, centered=False)
    add_paragraph("""
    You can, explore timelines, and visualize keyword distributions by navigating to the left tabs.
    """)

