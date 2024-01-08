import streamlit as st
import pandas as pd
import sqlalchemy as db
import os

# Fonction pour convertir un DataFrame en CSV
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# Fonction pour sauvegarder les données dans un fichier CSV
def save_data_to_csv(df, file_path):
    df.to_csv(file_path, index=False)

# Connexion à la base de données SQLite
engine = db.create_engine('sqlite:///pokemon.db')  # Remplacez 'votre_base_de_donnees.db' par le nom de votre base de données

# Lecture des types de Pokémon depuis la base de données
# Charger les types de Pokémon depuis la base de données
def load_types_from_db():
    connection = engine.connect()
    query = "SELECT types FROM pokedox"  # Récupérer tous les types de la table
    df = pd.read_sql(query, connection)
    types_list = df['types'].str.split(',').explode().str.strip().unique().tolist()
    types_list_cleaned = [type_.replace('[', '').replace(']', '').replace('"', '') for type_ in types_list]
    connection.close()
    return types_list_cleaned

# Charger les types de Pokémon depuis la base de données
pokemon_types = load_types_from_db()

# Interface Streamlit
key_article = st.selectbox('Choisissez un type de Pokémon : ', pokemon_types)
nb_pokemon = st.slider("Nombre de Pokémon à afficher et télécharger en format CSV :", 1, 1024, value=10)  # Slider pour choisir le nombre de Pokémon

# Lecture des données depuis la base de données
def load_data_from_db():
    connection = engine.connect()
    query = "SELECT * FROM pokedox WHERE types LIKE :type_name"
    df = pd.read_sql(query, connection, params={"type_name": f"%{key_article}%"})
    connection.close()
    return df

# Charger les données depuis la base de données
df = load_data_from_db()

# Bouton pour sauvegarder les données dans un fichier CSV
if st.button('Télécharger les données en format CSV'):
    # Chemin vers le dossier 'utiles' dans le répertoire de votre application
    folder_path = 'utiles'
    # Créer le dossier 'utiles' s'il n'existe pas déjà
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_list = os.listdir(folder_path)
    st.sidebar.markdown('**Liste des fichiers CSV disponibles :**')
    for file_name in file_list:
        st.sidebar.write(file_name)
    # Chemin vers le fichier CSV à sauvegarder avec le nom du type sélectionné
    file_name = f"{key_article}_pokemons.csv"
    file_path = os.path.join(folder_path, file_name)

    save_data_to_csv(df[:nb_pokemon], file_path)
    st.success(f'Les données ont été sauvegardées dans {file_name}')
