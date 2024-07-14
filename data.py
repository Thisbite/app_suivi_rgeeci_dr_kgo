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


import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect("rgeeci.db")
c = conn.cursor()

# Fonction de modification pour la table 'region'
def update_region(id, nom):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("""
        UPDATE region
        SET nom = ?
        WHERE id = ?
    """, (nom, id))
    conn.commit()
    conn.close()

# Fonction de modification pour la table 'departement'
def update_departement(id, nom_departement, nom_region):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("""
        UPDATE departement
        SET nom_departement = ?, nom_region = ?
        WHERE id = ?
    """, (nom_departement, nom_region, id))
    conn.commit()
    conn.close()

# Fonction de modification pour la table 'sous_prefecture'
def update_sous_prefecture(id, nom_sous_prefecture, nom_departement):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("""
        UPDATE sous_prefecture
        SET nom_sous_prefecture = ?, nom_departement = ?
        WHERE id = ?
    """, (nom_sous_prefecture, nom_departement, id))
    conn.commit()
    conn.close()

# Fonction de modification pour la table 'zone_denombrement'
def update_zone_denombrement(id, nom_zd, nom_sous_prefecture, nom_quartier):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("""
        UPDATE zone_denombrement
        SET nom_zd = ?, nom_sous_prefecture = ?, nom_quartier = ?
        WHERE id = ?
    """, (nom_zd, nom_sous_prefecture, nom_quartier, id))
    conn.commit()
    conn.close()

# Fonction de modification pour la table 'ilot'
def update_ilot(id, nom_ilot, nom_zd):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("""
        UPDATE ilot
        SET nom_ilot = ?, nom_zd = ?
        WHERE id = ?
    """, (nom_ilot, nom_zd, id))
    conn.commit()
    conn.close()

# Fonction de modification pour la table 'superviseur'
def update_superviseur(matricule, nom_sup, nom_region):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("""
        UPDATE superviseur
        SET nom_sup = ?, nom_region = ?
        WHERE matricule = ?
    """, (nom_sup, nom_region, matricule))
    conn.commit()
    conn.close()

# Fonction de modification pour la table 'chef_equipe'
def update_chef_equipe(id, numero_equipe, matricule_ce, nom_chef_equipe, nom_sup):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("""
        UPDATE chef_equipe
        SET numero_equipe = ?, matricule_ce = ?, nom_chef_equipe = ?, nom_sup = ?
        WHERE id = ?
    """, (numero_equipe, matricule_ce, nom_chef_equipe, nom_sup, id))
    conn.commit()
    conn.close()

# Fonction de modification pour la table 'reponse'
def update_reponse(id, numero_equipe, nom_zd, nom_ilot, numero_agent, nbre_UE_total, nbre_UE_partiel, nbre_UE_informel, nbre_UE_formel, nbre_UE_refus, date_aujourdhui):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("""
        UPDATE reponse
        SET numero_equipe = ?, nom_zd = ?, nom_ilot = ?, numero_agent = ?, nbre_UE_total = ?,
            nbre_UE_partiel = ?, nbre_UE_informel = ?, nbre_UE_formel = ?, nbre_UE_refus = ?, date_aujourdhui = ?
        WHERE id = ?
    """, (numero_equipe, nom_zd, nom_ilot, numero_agent, nbre_UE_total, nbre_UE_partiel, nbre_UE_informel, nbre_UE_formel, nbre_UE_refus, date_aujourdhui, id))
    conn.commit()
    conn.close()

# Fonction de modification pour la table 'agent'
def update_agent(id, numero_agent, numero_equipe):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("""
        UPDATE agent
        SET numero_agent = ?, numero_equipe = ?
        WHERE id = ?
    """, (numero_agent, numero_equipe, id))
    conn.commit()
    conn.close()



import streamlit as st
import sqlite3


# Fonction pour se connecter à la base de données SQLite



# Fonction pour récupérer les détails d'une région par ID
def get_region_by_id(region_id):
    conn = sqlite3.connect("rgeeci.db")

    c = conn.cursor()
    c.execute("SELECT * FROM region WHERE id=?", (region_id,))
    region = c.fetchone()
    conn.close()
    return region


# Page principale de l'application Streamlit pour la modification de la table 'region'
def region_update_page():
    st.title("Modification de la Table 'region'")

    # Sélectionner une région à modifier
    region_id = st.number_input("ID de la région à modifier", min_value=1, step=1)

    # Charger les détails de la région sélectionnée
    if st.button("Charger la région"):
        region = get_region_by_id(region_id)
        if region:
            st.write(f"Détails de la région avec ID {region_id}:")
            st.write(f"Nom actuel: {region[1]}")
            new_nom = st.text_input("Nouveau nom de la région", value=region[1])
            if st.button("Mettre à jour"):
                update_region(region_id, new_nom)
                st.success("Région mise à jour avec succès.")
        else:
            st.warning(f"Aucune région trouvée avec l'ID {region_id}.")


# Fonction pour récupérer les détails d'un département par ID
def get_departement_by_id(departement_id):
    conn = sqlite3.connect("rgeeci.db")

    c = conn.cursor()
    c.execute("SELECT * FROM departement WHERE id=?", (departement_id,))
    departement = c.fetchone()
    conn.close()
    return departement






def departement_update_page():


    # Option pour sélectionner une ligne à modifier
    if st.checkbox("Modifier un département", key="departement_modification"):
        # Sélectionner l'ID du département à modifier
        id_options = [1, 2, 3]  # Exemple : remplacer par une liste d'IDs disponibles dans votre base de données
        selected_id = st.selectbox("Choisir l'ID du département à modifier", id_options, key="select_departement")

        if selected_id:
            # Charger les détails du département sélectionné
            departement = get_departement_by_id(selected_id)
            if departement:
                st.write(f"Détails du département avec ID {selected_id}:")
                st.write(f"Nom actuel: {departement[1]}")
                st.write(f"Nom de région actuel: {departement[2]}")

                # Champ pour les nouvelles valeurs à mettre à jour
                new_nom_departement = st.text_input("Nouveau nom du département", value=departement[1])
                new_nom_region = st.text_input("Nouveau nom de région", value=departement[2])

                # Bouton pour soumettre les modifications
                if st.button("Modifier la ligne", key="modifier_departement"):
                    update_departement(selected_id, new_nom_departement, new_nom_region)
                    st.success("Département mis à jour avec succès.")
            else:
                st.warning(f"Aucun département trouvé avec l'ID {selected_id}.")


# Fonction pour récupérer les détails d'une sous-préfecture par ID
def get_sous_prefecture_by_id(sous_prefecture_id):
    conn = sqlite3.connect("rgeeci.db")

    c = conn.cursor()
    c.execute("SELECT * FROM sous_prefecture WHERE id=?", (sous_prefecture_id,))
    sous_prefecture = c.fetchone()
    conn.close()
    return sous_prefecture



# Page principale de l'application Streamlit pour la modification de la table 'sous_prefecture'
import streamlit as st


def sous_prefecture_update_page():


    # Option pour sélectionner une ligne à modifier
    if st.checkbox("Modifier une sous-préfecture", key="sous_prefecture_modification"):
        # Sélectionner l'ID de la sous-préfecture à modifier
        id_options = [1, 2, 3]  # Exemple : remplacer par une liste d'IDs disponibles dans votre base de données
        selected_id = st.selectbox("Choisir l'ID de la sous-préfecture à modifier", id_options,
                                   key="select_sous_prefecture")

        if selected_id:
            # Charger les détails de la sous-préfecture sélectionnée
            sous_prefecture = get_sous_prefecture_by_id(selected_id)
            if sous_prefecture:
                st.write(f"Détails de la sous-préfecture avec ID {selected_id}:")
                st.write(f"Nom actuel: {sous_prefecture[1]}")
                st.write(f"Nom du département actuel: {sous_prefecture[2]}")

                # Champ pour les nouvelles valeurs à mettre à jour
                new_nom_sous_prefecture = st.text_input("Nouveau nom de la sous-préfecture", value=sous_prefecture[1])
                new_nom_departement = st.text_input("Nouveau nom du département", value=sous_prefecture[2])

                # Bouton pour soumettre les modifications
                if st.button("Modifier la ligne", key="modifier_sous_prefecture"):
                    update_sous_prefecture(selected_id, new_nom_sous_prefecture, new_nom_departement)
                    st.success("Sous-préfecture mise à jour avec succès.")
            else:
                st.warning(f"Aucune sous-préfecture trouvée avec l'ID {selected_id}.")


# Fonction pour récupérer les détails d'un superviseur par matricule
def get_superviseur_by_matricule(matricule):
    conn = sqlite3.connect("rgeeci.db")

    c = conn.cursor()
    c.execute("SELECT * FROM superviseur WHERE matricule=?", (matricule,))
    superviseur = c.fetchone()
    conn.close()
    return superviseur


# Page principale de l'application Streamlit pour la modification de la table 'superviseur'
import streamlit as st


def superviseur_update_page():
    # Option pour sélectionner une ligne à modifier
    if st.checkbox("Modifier un superviseur", key="superviseur_modification"):
        # Saisir le matricule du superviseur à modifier
        matricule = st.text_input("Matricule du superviseur à modifier")

        # Bouton pour charger les détails du superviseur
        if st.button("Charger le superviseur", key="charger_superviseur"):
            superviseur = get_superviseur_by_matricule(matricule)
            if superviseur:
                st.write(f"Détails du superviseur avec matricule {matricule}:")
                st.write(f"Nom actuel: {superviseur[1]}")
                st.write(f"Région actuelle: {superviseur[2]}")

                # Champ pour les nouvelles valeurs à mettre à jour
                new_nom_sup = st.text_input("Nouveau nom du superviseur", value=superviseur[1])
                new_nom_region = st.text_input("Nouveau nom de région", value=superviseur[2])

                # Bouton pour soumettre les modifications
                if st.button("Mettre à jour", key="modifier_superviseur"):
                    update_superviseur(matricule, new_nom_sup, new_nom_region)
                    st.success("Superviseur mis à jour avec succès.")
            else:
                st.warning(f"Aucun superviseur trouvé avec le matricule {matricule}.")


# Fonction pour récupérer les détails d'un chef d'équipe par son ID
def get_chef_equipe_by_id(id):
    conn = sqlite3.connect("rgeeci.db")

    c = conn.cursor()
    c.execute("SELECT * FROM chef_equipe WHERE id=?", (id,))
    chef_equipe = c.fetchone()
    conn.close()
    return chef_equipe


# Page principale de l'application Streamlit pour la modification de la table 'chef_equipe'
import streamlit as st
import sqlite3

# Fonction pour se connecter à la base de données SQLite
import streamlit as st
import sqlite3

# Fonction pour se connecter à la base de données SQLite
def connect_db():
    conn = sqlite3.connect("rgeeci.db")
    return conn

# Fonction pour récupérer les détails d'un chef d'équipe par son ID
def get_chef_equipe_by_id(id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM chef_equipe WHERE id=?", (id,))
    chef_equipe = c.fetchone()
    conn.close()
    return chef_equipe

# Fonction pour mettre à jour un chef d'équipe dans la base de données
def update_chef_equipe(id, numero_equipe, matricule_ce, nom_chef_equipe, nom_sup):
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        UPDATE chef_equipe
        SET numero_equipe = ?, matricule_ce = ?, nom_chef_equipe = ?, nom_sup = ?
        WHERE id = ?
    """, (numero_equipe, matricule_ce, nom_chef_equipe, nom_sup, id))
    conn.commit()
    conn.close()

# Page principale de l'application Streamlit pour la modification de la table 'chef_equipe'
import streamlit as st


def chef_equipe_update_page():


    # Option pour sélectionner une ligne à modifier
    if st.checkbox("Modifier une equipe", key="chef_equipe_modification"):
        # Sélectionner l'ID du chef d'équipe à modifier
        id_options = [1, 2, 3]  # Exemple : remplacer par une liste d'IDs disponibles dans votre base de données
        selected_id = st.selectbox("Choisir l'ID du chef d'équipe à modifier", id_options, key="select_chef_equipe")

        if selected_id:
            # Charger les détails du chef d'équipe sélectionné
            chef_equipe = get_chef_equipe_by_id(selected_id)
            if chef_equipe:
                st.write(f"Détails du chef d'équipe avec ID {selected_id}:")
                st.write(f"Numéro d'équipe actuel: {chef_equipe[1]}")
                st.write(f"Matricule actuel: {chef_equipe[2]}")
                st.write(f"Nom actuel: {chef_equipe[3]}")
                st.write(f"Nom du superviseur actuel: {chef_equipe[4]}")

                # Champ pour les nouvelles valeurs à mettre à jour
                new_numero_equipe = st.number_input("Nouveau numéro d'équipe", value=int(chef_equipe[1]), step=1)
                new_matricule_ce = st.text_input("Nouveau matricule du chef d'équipe", value=chef_equipe[2])
                new_nom_chef_equipe = st.text_input("Nouveau nom du chef d'équipe", value=chef_equipe[3])
                new_nom_sup = st.text_input("Nouveau nom du superviseur", value=chef_equipe[4])

                # Bouton pour soumettre les modifications
                if st.button("Modifier la ligne", key="modifier_chef_equipe"):
                    update_chef_equipe(selected_id, new_numero_equipe, new_matricule_ce, new_nom_chef_equipe,
                                       new_nom_sup)
                    st.success("Chef d'équipe mis à jour avec succès.")
            else:
                st.warning(f"Aucun chef d'équipe trouvé avec l'ID {selected_id}.")


# Fonction pour récupérer les détails d'une zone de dénombrement par son ID
def get_zone_denombrement_by_id(id):
    conn = sqlite3.connect("rgeeci.db")

    c = conn.cursor()
    c.execute("SELECT * FROM zone_denombrement WHERE id=?", (id,))
    zone_denombrement = c.fetchone()
    conn.close()
    return zone_denombrement


import streamlit as st


def zone_denombrement_update_page():
    # Option pour sélectionner une ligne à modifier
    if st.checkbox("Modifier une ZD", key="zone_denombrement_modification"):
        # Sélectionner l'ID de la zone de dénombrement à modifier
        id_options = [1, 2, 3]  # Exemple : remplacer par une liste d'IDs disponibles dans votre base de données
        selected_id = st.selectbox("Choisir l'ID de la zone de dénombrement à modifier", id_options,
                                   key="select_zone_denombrement")

        if selected_id:
            # Charger les détails de la zone de dénombrement sélectionnée
            zone_denombrement = get_zone_denombrement_by_id(selected_id)
            if zone_denombrement:
                st.write(f"Détails de la zone de dénombrement avec ID {selected_id}:")
                st.write(f"Nom de la zone de dénombrement actuel: {zone_denombrement[1]}")
                st.write(f"Sous-préfecture actuelle: {zone_denombrement[2]}")
                st.write(f"Quartier actuel: {zone_denombrement[3]}")

                # Champ pour les nouvelles valeurs à mettre à jour
                new_nom_zd = st.text_input("Nouveau nom de la zone de dénombrement", value=zone_denombrement[1])
                new_nom_sous_prefecture = st.text_input("Nouveau nom de la sous-préfecture", value=zone_denombrement[2])
                new_nom_quartier = st.text_input("Nouveau nom du quartier", value=zone_denombrement[3])

                # Bouton pour soumettre les modifications
                if st.button("Modifier la ligne ZD", key="modifier_zone_denombrement"):
                    update_zone_denombrement(selected_id, new_nom_zd, new_nom_sous_prefecture, new_nom_quartier)
                    st.success("Zone de dénombrement mise à jour avec succès.")
            else:
                st.warning(f"Aucune zone de dénombrement trouvée avec l'ID {selected_id}.")


def get_ilot_by_id(id):
    conn = sqlite3.connect("rgeeci.db")

    c = conn.cursor()
    c.execute("SELECT * FROM ilot WHERE id=?", (id,))
    ilot = c.fetchone()
    conn.close()
    return ilot


# Page principale de l'application Streamlit pour la modification de la table 'ilot'
import streamlit as st


def ilot_update_page():


    # Option pour sélectionner une ligne à modifier
    if st.checkbox("Modifier un ilot", key="ilot_modification"):
        # Sélectionner l'ID de l'îlot à modifier
        id_options = [1, 2, 3]  # Exemple : remplacer par une liste d'IDs disponibles dans votre base de données
        selected_id = st.selectbox("Choisir l'ID de l'îlot à modifier", id_options, key="select_ilot")

        if selected_id:
            # Charger les détails de l'îlot sélectionné
            ilot = get_ilot_by_id(selected_id)
            if ilot:
                st.write(f"Détails de l'îlot avec ID {selected_id}:")
                st.write(f"Nom de l'îlot actuel: {ilot[1]}")
                st.write(f"Zone de dénombrement actuelle: {ilot[2]}")

                # Champ pour les nouvelles valeurs à mettre à jour
                new_nom_ilot = st.text_input("Nouveau nom de l'îlot", value=ilot[1])
                new_nom_zd = st.text_input("Nouveau nom de la zone de dénombrement", value=ilot[2])

                # Bouton pour soumettre les modifications
                if st.button("Modifier la ligne", key="modifier_ilot"):
                    update_ilot(selected_id, new_nom_ilot, new_nom_zd)
                    st.success("Îlot mis à jour avec succès.")
            else:
                st.warning(f"Aucun îlot trouvé avec l'ID {selected_id}.")
