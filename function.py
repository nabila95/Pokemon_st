import time
import json
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import sqlalchemy as db
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
class DataBase():
    def __init__(self, name_database='pokemon'):
        self.name = name_database
        self.url = f"sqlite:///{name_database}.db"
        self.engine = db.create_engine(self.url)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.table = self.engine.table_names()

    def create_table(self, name_table, **kwargs):
        columns = [db.Column(k, v, primary_key=True) if 'id_' in k else db.Column(k, v) for k, v in kwargs.items()]
        db.Table(name_table, self.metadata, *columns)
        self.metadata.create_all(self.engine)
        print(f"Table '{name_table}' créée avec succès.")

    def add_row(self, name_table, **kwargs):
        name_table = self.read_table(name_table)
        stmt = db.insert(name_table).values(kwargs)
        self.connection.execute(stmt)
        print('Ligne ajoutée avec succès.')

    def read_table(self, name_table, return_keys=False):
        table = db.Table(name_table, self.metadata, autoload=True, autoload_with=self.engine)
        if return_keys:
            table.columns.keys()
        else:
            return table

def scraping_pokemon_card():
# 1  Connexion à la base de données
    database = DataBase('pokémon')
# 2 Création d'une table
    database.create_table('pokedex', 
                      id_national=db.Integer, 
                      name=db.String, 
                      types=db.String,
                      image=db.String,
                      link=db.String,
                      Species=db.String,
                      height=db.String,
                      weight=db.String,
                     generation=db.String  # Ajout de la colonne de génération

)
    
    # Instancier le navigateur Chrome
    driver = Chrome('')

    # Ouvrir l'URL contenant les cartes Pokémon
    driver.get("https://pokemondb.net/pokedex/national")

    # Attendre que la page se charge complètement
    time.sleep(5)  # Attendre un peu plus longtemps pour assurer le chargement complet

    # Créer une liste pour stocker les informations des cartes
    cards_info = {}
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "list-nav")))

    # Rechercher les liens de navigation pour chaque génération
    generation_links = driver.find_elements(By.CLASS_NAME, "list-nav")[0].find_elements(By.TAG_NAME, "a")

    # Parcourir chaque génération pour collecter les informations
    for generation_link in generation_links:
        # Récupérer le lien et le nom de la génération
        gen_link = generation_link.get_attribute("href")
        gen_name = generation_link.text

        # Cliquer sur le lien de la génération
        generation_link.click()

        # Attendre que la page se charge complètement
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, gen_link.split('#')[1])))
        time.sleep(2)
        # Collecter les cartes Pokémon de cette génération
        cards = driver.find_elements(By.CLASS_NAME, "infocard")
    # Rechercher les cartes Pokémon
        cards = driver.find_elements(By.CLASS_NAME, "infocard")
        print(len(cards))

        # Limiter le nombre de cartes à extraire si nécessaire
        # n_cards = min(len(cards), n_cards)

        # Parcourir chaque carte Pokémon pour collecter les informations
        for card in range(len(cards)):
            print(card)
            try:
                name=cards[card].find_element(By.CLASS_NAME, "ent-name").text
                # cards[0].find_element(By.CLASS_NAME, "ent-name").text
            except:
                None
            try:
                types_elements = cards[card].find_elements(By.CLASS_NAME,'itype')
                types = [element.text for element in types_elements]

            except:
                None
            # Récupérer le lien de l'image
            try:
                image= cards[card].find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                image = None
            try:
                link=cards[card].find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                None
            
            driver.get(link)
            time.sleep(2)
            
            # Ajouter les informations de la carte à la liste
            # cards_info.append({"image_link": image_link})
            try:
                national=cards.find_element(By.TAG_NAME,'strong').text
            except:
                None
            #les données de section 
            details_section = driver.find_element(By.TAG_NAME, 'tbody')

            try:national=details_section.find_elements(By.TAG_NAME,'tr')[0].find_element(By.TAG_NAME,'strong').text
            except:None
            try:Species=details_section.find_elements(By.TAG_NAME,'tr')[2].find_element(By.TAG_NAME,'td').text
            except:None
            try:height=details_section.find_elements(By.TAG_NAME,'tr')[3].find_element(By.TAG_NAME,'td').text
            except:None
            try:weight=details_section.find_elements(By.TAG_NAME,'tr')[4].find_element(By.TAG_NAME,'td').text
            except:None
            driver.back()
            time.sleep(2)
            cards = driver.find_elements(By.CLASS_NAME, "infocard")
            # cards_info[national]={
            #     'national':national,
            #     'name':name,
            #     'types':types,
            #     'image':image,
            #     'link':link,
            #     'Species':Species,
import time
import random
import json
from selenium.webdriver import Chrome
from function import *



import time
import random
import json
from selenium.webdriver import Chrome
from function import *


def scraping_pokemon_cards():
# 1  Connexion à la base de données
    database = DataBase('pokemon')
# 2 Création d'une table
    database.create_table('pokedox', 
                      id_national=db.Integer, 
                      name=db.String, 
                      types=db.String,
                      image=db.String,
                      link=db.String,
                      Species=db.String,
                      height=db.String,
                      weight=db.String,
)
    
    # Instancier le navigateur Chrome
    driver = Chrome('')

    # Ouvrir l'URL contenant les cartes Pokémon
    driver.get("https://pokemondb.net/pokedex/national")

    # Attendre que la page se charge complètement
    time.sleep(5)  # Attendre un peu plus longtemps pour assurer le chargement complet

    # Créer une liste pour stocker les informations des cartes
    cards_info = {}

    # Rechercher les cartes Pokémon
    cards = driver.find_elements(By.CLASS_NAME, "infocard")
    print(len(cards))

    # Limiter le nombre de cartes à extraire si nécessaire
    # n_cards = min(len(cards), n_cards)

    # Parcourir chaque carte Pokémon pour collecter les informations
    for card in range(len(cards)):
        print(card)
        try:
            name=cards[card].find_element(By.CLASS_NAME, "ent-name").text
            # cards[0].find_element(By.CLASS_NAME, "ent-name").text
        except:
            None
        try:
            types_elements = cards[card].find_elements(By.CLASS_NAME,'itype')
            types = [element.text for element in types_elements]

        except:
            None
        # Récupérer le lien de l'image
        try:
            image= cards[card].find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            image = None
        try:
            link=cards[card].find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            None
        
        driver.get(link)
        time.sleep(2)
        
        # Ajouter les informations de la carte à la liste
        # cards_info.append({"image_link": image_link})
        try:
            national=cards.find_element(By.TAG_NAME,'strong').text
        except:
            None
        #les données de section 
        details_section = driver.find_element(By.TAG_NAME, 'tbody')

        try:national=details_section.find_elements(By.TAG_NAME,'tr')[0].find_element(By.TAG_NAME,'strong').text
        except:None
        try:Species=details_section.find_elements(By.TAG_NAME,'tr')[2].find_element(By.TAG_NAME,'td').text
        except:None
        try:height=details_section.find_elements(By.TAG_NAME,'tr')[3].find_element(By.TAG_NAME,'td').text
        except:None
        try:weight=details_section.find_elements(By.TAG_NAME,'tr')[4].find_element(By.TAG_NAME,'td').text
        except:None
        driver.back()
        time.sleep(2)
        cards = driver.find_elements(By.CLASS_NAME, "infocard")
        # cards_info[national]={
        #     'national':national,
        #     'name':name,
        #     'types':types,
        #     'image':image,
        #     'link':link,
        #     'Species':Species,
        #     'height':height,
        #     'weight':weight




        # }
        try : 
            database.add_row('pokedox', 
                      id_national=national, 
                      name=name, 
                      types=json.dumps(types) if types else None,
                      image=image,
                      link=link,
                      Species=Species,
                      height=height,
                      weight=weight,
                    )
        except:
            pass
    driver.quit()   
    return cards_info 