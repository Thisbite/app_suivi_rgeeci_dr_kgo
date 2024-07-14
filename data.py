import sqlite3

conn = sqlite3.connect("rgeeci.db")
c = conn.cursor()

#c.execute(" DROP TABLE reponse")

def create_tables():
    # Connexion à la base de données SQLite
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    # Création des tables
    c.execute('''
    CREATE TABLE IF NOT EXISTS region (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS departement (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_departement TEXT,
        nom_region TEXT,
        FOREIGN KEY (nom_region) REFERENCES region(nom)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS sous_prefecture (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_sous_prefecture TEXT,
        nom_departement TEXT,
        FOREIGN KEY (nom_departement) REFERENCES departement(nom_departement)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS zone_denombrement (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_zd TEXT,
        nom_sous_prefecture TEXT,
        nom_quartier TEXT,
        FOREIGN KEY (nom_sous_prefecture) REFERENCES sous_prefecture(nom_sous_prefecture)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS ilot (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_ilot TEXT,
        nom_zd TEXT,
        FOREIGN KEY (nom_zd) REFERENCES zone_denombrement(nom_zd)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS superviseur (
        matricule TEXT PRIMARY KEY,
        nom_sup TEXT,
        nom_region TEXT,
        FOREIGN KEY (nom_region) REFERENCES region(nom)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS chef_equipe (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_equipe INTEGER,
        matricule_ce TEXT,
        nom_chef_equipe TEXT,
        nom_sup TEXT,
        FOREIGN KEY (nom_sup) REFERENCES superviseur(nom_sup)
    )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS reponse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_equipe INTEGER,
            nom_zd TEXT,
            nom_ilot TEXT,
            numero_agent INTEGER,
            nbre_UE_total INTEGER,
            nbre_UE_partiel INTEGER,
            nbre_UE_informel INTEGER,
            nbre_UE_formel INTEGER,
            nbre_UE_refus INTEGER,
            date_aujourdhui TEXT,
            FOREIGN KEY (numero_equipe) REFERENCES chef_equipe(numero_equipe),
            FOREIGN KEY (nom_zd) REFERENCES zone_denombrement(nom_zd),
            FOREIGN KEY (nom_ilot) REFERENCES ilot(nom_ilot),
            FOREIGN KEY (numero_agent) REFERENCES agent(numero_agent)
        )
        ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS agent (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_agent INTEGER,
        numero_equipe INTEGER,
        FOREIGN KEY (numero_equipe) REFERENCES chef_equipe(numero_equipe)
    )
    ''')

    # Validation des changements et fermeture de la connexion
    conn.commit()
    conn.close()

# Exécution de la fonction pour créer les tables
create_tables()


def insert_region( nom):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("INSERT INTO region ( nom) VALUES ( ?)", ( nom))
    conn.commit()
    conn.close()

def insert_departement( nom_departement, nom_region):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("INSERT INTO departement (nom_departement, nom_region) VALUES ( ?, ?)", (id, nom_departement, nom_region))
    conn.commit()
    conn.close()

def insert_sous_prefecture(nom_sous_prefecture, nom_departement):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("INSERT INTO sous_prefecture ( nom_sous_prefecture, nom_departement) VALUES ( ?, ?)", (id, nom_sous_prefecture, nom_departement))
    conn.commit()
    conn.close()

def insert_zone_denombrement(nom_zd, nom_sous_prefecture, nom_quartier):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("INSERT INTO zone_denombrement ( nom_zd, nom_sous_prefecture, nom_quartier) VALUES ( ?, ?, ?)", (id, nom_zd, nom_sous_prefecture, nom_quartier))
    conn.commit()
    conn.close()

def insert_ilot( nom_ilot, nom_zd):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("INSERT INTO ilot (id, nom_ilot, nom_zd) VALUES ( ?, ?)", ( nom_ilot, nom_zd))
    conn.commit()
    conn.close()

def insert_superviseur(matricule, nom_sup, nom_region):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("INSERT INTO superviseur (matricule, nom_sup, nom_region) VALUES (?, ?, ?)", (matricule, nom_sup, nom_region))
    conn.commit()
    conn.close()

def insert_chef_equipe( numero_equipe,matricule_ce,nom_chef_equipe, nom_sup):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("INSERT INTO chef_equipe (numero_equipe,matricule_ce,nom_chef_equipe, nom_sup) VALUES ( ?,?,?, ?)", ( numero_equipe,matricule_ce,nom_chef_equipe, nom_sup))
    conn.commit()
    conn.close()

def insert_agent( numero_agent, numero_equipe):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("INSERT INTO agent ( numero_agent, numero_equipe) VALUES ( ?, ?)", ( numero_agent, numero_equipe))
    conn.commit()
    conn.close()

def get_region():
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT id,nom
        FROM region     
    ''')
    regions = c.fetchall()
    conn.close()
    return regions




def get_departement():
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT id, nom_departement 
        FROM departement
    ''')
    departements = c.fetchall()
    conn.close()
    return departements


def get_sous_prefecture():
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT id, nom_sous_prefecture 
        FROM sous_prefecture
    ''')
    sous_prefectures = c.fetchall()
    conn.close()
    return sous_prefectures

def get_zone_denombrement():
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT id, nom_zd 
        FROM zone_denombrement
    ''')
    zones_denombrement = c.fetchall()
    conn.close()
    return zones_denombrement

def get_ilot():
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT id, nom_ilot 
        FROM ilot
    ''')
    ilots = c.fetchall()
    conn.close()
    return ilots

def get_superviseurs():
    # Connexion à la base de données SQLite
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    # Exécution de la requête pour récupérer les superviseurs
    c.execute('''
        SELECT DISTINCT matricule, nom_sup 
        FROM superviseur
    ''')

    # Récupération des résultats
    superviseurs = c.fetchall()

    # Fermeture de la connexion
    conn.close()

    return superviseurs

def get_agents():
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT id, numero_agent 
        FROM agent
    ''')
    agents = c.fetchall()
    conn.close()
    return agents

def get_chefs_equipe():
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute('''
        SELECT id, numero_equipe, nom_chef_equipe 
        FROM chef_equipe
    ''')
    chefs_equipe = c.fetchall()
    conn.close()
    return chefs_equipe

def insert_reponse_data(numero_equipe, nom_zd, nom_ilot, numero_agent, nbre_UE_total, nbre_UE_partiel, nbre_UE_informel, nbre_UE_formel, nbre_UE_refus,date_aujourdhui):
    # Connexion à la base de données SQLite
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    # Insertion des données dans la table 'reponse'
    c.execute('''
    INSERT INTO reponse (numero_equipe, nom_zd, nom_ilot, numero_agent, nbre_UE_total, nbre_UE_partiel, nbre_UE_informel, nbre_UE_formel, nbre_UE_refus,date_aujourdhui)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    ''', (numero_equipe, nom_zd, nom_ilot, numero_agent, nbre_UE_total, nbre_UE_partiel, nbre_UE_informel, nbre_UE_formel, nbre_UE_refus,date_aujourdhui))

    # Validation des changements et fermeture de la connexion
    conn.commit()
    conn.close()
