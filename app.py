import streamlit as st
import sqlalchemy as db
import pandas as pd
from IPython.display import YouTubeVideo
import requests, openai, os
# Connexion à la base de données SQLite
engine = db.create_engine('sqlite:///pokemon.db')

# Fonction pour lire les données depuis la base de données
def fetch_data(start_index, end_index):
    connection = engine.connect()
    query = f"SELECT * FROM pokedox LIMIT {start_index}, {end_index}"  # Remplacez "votre_table" par le nom de votre table dans la base de données
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# Configuration de la page Streamlit
st.set_page_config(
    page_title='Scraping Pokémon carte',
    page_icon='https://cdn-icons-png.flaticon.com/512/1169/1169608.png',
    layout='wide'
)
import streamlit as st

# Titre et message de bienvenue
st.title('Collecte de cartes Pokémon')
st.write('Bienvenue sur cette application de collecte de cartes Pokémon.')

# Explication sur l'utilisation de Selenium
st.write("J'ai choisi le framework Selenium pour son aptitude à interagir directement avec des sites web, permettant de simuler des actions utilisateur réelles. Il est idéal pour extraire des données à partir de pages web dynamiques ou nécessitant des interactions spécifiques telles que l'authentification, la pagination dynamique et la navigation entre différentes pages. Sa flexibilité et sa capacité à répondre à des exigences spécifiques du site en font un choix optimal pour collecter des données complexes sur des sites web variés.")

def homepage():
    # Changer la couleur de fond
    bg_color = '#f0f0f0'  # Couleur de fond souhaitée (par exemple)
    st.markdown(
        f"""
        <style>
        body {{
            background-color: {bg_color};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

   

    # Ajout de la vidéo
    
    # st.video("https://www.youtube.com/watch?v=0VLPfiX5VJU&t=6s")
    

    st.sidebar.markdown("<h1 style='color: YelLow;'>EL ABDALI NABILA</h1>", unsafe_allow_html=True)
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/fr/7/75/Pok%C3%A9mon_Go_Logo.png")
    st.sidebar.subheader("Description de l'application")
    st.sidebar.markdown("Cette application permet de collecter des données du site pokémon et  de discuter avec un bot expert du jeu.")
    st.sidebar.link_button("Lien vers le site", "https://pokemondb.net/pokedex/national")

    st.write('Utilisez le bouton ci-dessous pour afficher les données stockées dans la base de données.')

    # Variables de session
    if 'start_index' not in st.session_state:
        st.session_state.start_index = 0
    if 'end_index' not in st.session_state:
        st.session_state.end_index = 100

    # Affichage des données


show_pokemon = st.checkbox("Afficher les Pokémon")
pokemon_count = st.slider("Nombre de Pokémon à afficher :", 1, 100, 10)

if show_pokemon:
    # Lecture des données depuis la base de données dans un DataFrame
    df = fetch_data(st.session_state.start_index, st.session_state.end_index)  # Appel de la fonction fetch_data pour obtenir les données

    # Affichage des données par groupe de six
    cols = st.columns(5)
    
    for index, row in df.head(pokemon_count).iterrows():  # Utilisation de la fonction head() pour limiter le nombre de Pokémon affichés
        # Affichage des informations de la carte Pokémon
        col = cols[index % 5]

        # Affichage de l'image en tant que lien
        col.markdown(
            f'<a href="{row["link"]}" target="_blank"><img src="{row["image"]}" width="100"></a>',
            unsafe_allow_html=True
        )
        # Affichage du nom en bleu et avec une taille de police réduite
        col.markdown(
            f"<span style='color: blue; font-size: small;'>{row['name']}</span>",
            unsafe_allow_html=True
        )
        # Affichage du type avec une taille de police réduite
        col.markdown(
            f"<span style='font-size: small;'>{row['types']}</span>",
            unsafe_allow_html=True
        )
        col.write('---')  

    # Mettre à jour les index de début et de fin pour afficher la prochaine tranche de données
    st.session_state.start_index += pokemon_count
    st.session_state.end_index += pokemon_count

import openai

# Remplacez 'VOTRE_CLE_API_OPENAI' par votre clé API OpenAI




# Configuration de la clé API OpenAI
openai.api_key = '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'

# Fonction pour interagir avec le chatbot
def chat_with_bot(prompt_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Vous êtes connecté au service client. Posez votre question."},
            {"role": "user", "content": prompt_text}
        ]
    )
    return response['choices'][0]['message']['content']

# Titre de la page d'accueil
st.title('Chatbot OpenAI GPT-3')

# Zone de saisie pour interagir avec le chatbot
user_input = st.text_input('Entrez votre question :')

# Bouton pour soumettre la question
if st.button('Envoyer'):
    if user_input:
        # Affichage de la réponse du chatbot
        bot_response = chat_with_bot(user_input)
        st.text_area('Réponse du Chatbot :', value=bot_response, height=200)
    else:
        st.warning('Veuillez saisir une question pour obtenir une réponse du chatbot.')


if __name__ == "__main__":
    homepage()
