import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Fonction pour insérer des données dans la table 'reponse'
def insert_reponse_data(data):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    c.executemany('''
    INSERT INTO reponse (numero_equipe, nom_zd, nom_ilot, numero_agent, nbre_UE_total, nbre_UE_partiel, nbre_UE_informel, nbre_UE_formel, nbre_UE_refus, date_aujourdhui)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)

    conn.commit()
    conn.close()

# Fonction principale de l'application
def reponse_excel():
    st.title("Importation de Réponses depuis Excel vers SQLite")

    # Téléchargement du fichier Excel
    file = st.file_uploader("Choisir un fichier Excel", type=["xlsx"],key="reponse")

    if file:
        # Lecture du fichier Excel
        xls = pd.ExcelFile(file)
        sheets = xls.sheet_names

        # Sélection de la feuille
        sheet = st.selectbox("Sélectionner la feuille", sheets)

        if sheet:
            # Lecture de la feuille sélectionnée
            df = pd.read_excel(xls, sheet_name=sheet)

            # Affichage du dataframe
            st.write("Aperçu des données importées:")
            st.write(df.head())

            # Vérification de la présence des colonnes nécessaires
            required_columns = ['numero_equipe', 'nom_zd', 'nom_ilot', 'numero_agent', 'nbre_UE_total', 'nbre_UE_partiel', 'nbre_UE_informel', 'nbre_UE_formel', 'nbre_UE_refus', 'date_aujourdhui']
            if all(column in df.columns for column in required_columns):
                if st.button("Enregistrer dans la base de données"):
                    data = df[required_columns].values.tolist()
                    insert_reponse_data(data)
                    st.success("Données insérées avec succès dans la base de données.")
            else:
                st.error(f"Le fichier Excel doit contenir les colonnes suivantes : {', '.join(required_columns)}")



def insert_departement_data(data):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    c.executemany('''
    INSERT INTO departement (nom_departement, nom_region)
    VALUES (?, ?)
    ''', data)

    conn.commit()
    conn.close()

# Fonction principale de l'application
def departement_excel():
    st.title("Importation de Départements depuis Excel vers SQLite")

    # Téléchargement du fichier Excel
    file = st.file_uploader("Choisir un fichier Excel", type=["xlsx"],key="departexcel")

    if file:
        # Lecture du fichier Excel
        xls = pd.ExcelFile(file)
        sheets = xls.sheet_names

        # Sélection de la feuille
        sheet = st.selectbox("Sélectionner la feuille", sheets)

        if sheet:
            # Lecture de la feuille sélectionnée
            df = pd.read_excel(xls, sheet_name=sheet)

            # Affichage du dataframe
            st.write("Aperçu des données importées:")
            st.write(df.head())

            # Vérification de la présence des colonnes nécessaires
            required_columns = ['nom_departement', 'nom_region']
            if all(column in df.columns for column in required_columns):
                if st.button("Enregistrer dans la base de données"):
                    data = df[required_columns].values.tolist()
                    insert_departement_data(data)
                    st.success("Données insérées avec succès dans la base de données.")
            else:
                st.error(f"Le fichier Excel doit contenir les colonnes suivantes : {', '.join(required_columns)}")

# Fonction pour insérer des données dans la table 'sous_prefecture'
def insert_sous_prefecture_data(data):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    c.executemany('''
    INSERT INTO sous_prefecture (nom_sous_prefecture, nom_departement)
    VALUES (?, ?)
    ''', data)

    conn.commit()
    conn.close()

# Fonction principale de l'application
def sous_prefecture_excel():
    st.title("Importation de Sous-préfectures depuis Excel vers SQLite")

    # Téléchargement du fichier Excel
    file = st.file_uploader("Choisir un fichier Excel", type=["xlsx"],key="sous_pref")

    if file:
        # Lecture du fichier Excel
        xls = pd.ExcelFile(file)
        sheets = xls.sheet_names

        # Sélection de la feuille
        sheet = st.selectbox("Sélectionner la feuille", sheets)

        if sheet:
            # Lecture de la feuille sélectionnée
            df = pd.read_excel(xls, sheet_name=sheet)

            # Affichage du dataframe
            st.write("Aperçu des données importées:")
            st.write(df.head())

            # Vérification de la présence des colonnes nécessaires
            required_columns = ['nom_sous_prefecture', 'nom_departement']
            if all(column in df.columns for column in required_columns):
                if st.button("Enregistrer dans la base de données"):
                    data = df[required_columns].values.tolist()
                    insert_sous_prefecture_data(data)
                    st.success("Données insérées avec succès dans la base de données.")
            else:
                st.error(f"Le fichier Excel doit contenir les colonnes suivantes : {', '.join(required_columns)}")


# Fonction pour insérer des données dans la table 'chef_equipe'
def insert_chef_equipe_data(data):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    c.executemany('''
    INSERT INTO chef_equipe (numero_equipe, matricule_ce, nom_chef_equipe, nom_sup)
    VALUES (?, ?, ?, ?)
    ''', data)

    conn.commit()
    conn.close()

# Fonction principale de l'application
def chef_equipe_excel():
    st.title("Importation de Chefs d'Équipe depuis Excel vers SQLite")

    # Téléchargement du fichier Excel
    file = st.file_uploader("Choisir un fichier Excel", type=["xlsx"],key="chefexcel")

    if file:
        # Lecture du fichier Excel
        xls = pd.ExcelFile(file)
        sheets = xls.sheet_names

        # Sélection de la feuille
        sheet = st.selectbox("Sélectionner la feuille", sheets)

        if sheet:
            # Lecture de la feuille sélectionnée
            df = pd.read_excel(xls, sheet_name=sheet)

            # Affichage du dataframe
            st.write("Aperçu des données importées:")
            st.write(df.head())

            # Vérification de la présence des colonnes nécessaires
            required_columns = ['numero_equipe', 'matricule_ce', 'nom_chef_equipe', 'nom_sup']
            if all(column in df.columns for column in required_columns):
                if st.button("Enregistrer dans la base de données"):
                    data = df[required_columns].values.tolist()
                    insert_chef_equipe_data(data)
                    st.success("Données insérées avec succès dans la base de données.")
            else:
                st.error(f"Le fichier Excel doit contenir les colonnes suivantes : {', '.join(required_columns)}")




# Fonction pour insérer des données dans la table 'agent'
def insert_agent_data(data):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    c.executemany('''
    INSERT INTO agent (numero_agent, numero_equipe)
    VALUES (?, ?)
    ''', data)

    conn.commit()
    conn.close()

# Fonction principale de l'application
def agent_excel():
    st.title("Importation des Agents depuis Excel vers SQLite")

    # Téléchargement du fichier Excel
    file = st.file_uploader("Choisir un fichier Excel", type=["xlsx"],key="agt_excel")

    if file:
        # Lecture du fichier Excel
        xls = pd.ExcelFile(file)
        sheets = xls.sheet_names

        # Sélection de la feuille
        sheet = st.selectbox("Sélectionner la feuille", sheets)

        if sheet:
            # Lecture de la feuille sélectionnée
            df = pd.read_excel(xls, sheet_name=sheet)

            # Affichage du dataframe
            st.write("Aperçu des données importées:")
            st.write(df.head())

            # Vérification de la présence des colonnes nécessaires
            required_columns = ['numero_agent', 'numero_equipe']
            if all(column in df.columns for column in required_columns):
                if st.button("Enregistrer dans la base de données"):
                    data = df[required_columns].values.tolist()
                    insert_agent_data(data)
                    st.success("Données insérées avec succès dans la base de données.")
            else:
                st.error(f"Le fichier Excel doit contenir les colonnes suivantes : {', '.join(required_columns)}")





import streamlit as st
import pandas as pd
import sqlite3

# Fonction pour insérer des données dans la table 'superviseur'
def insert_superviseur_data(data):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    c.executemany('''
    INSERT INTO superviseur (matricule, nom_sup, nom_region)
    VALUES (?, ?, ?)
    ''', data)

    conn.commit()
    conn.close()

# Fonction principale de l'application
def superviseur_excel():
    st.title("Importation de Superviseurs depuis Excel vers SQLite")

    # Téléchargement du fichier Excel
    file = st.file_uploader("Choisir un fichier Excel", type=["xlsx"])

    if file:
        # Lecture du fichier Excel
        xls = pd.ExcelFile(file)
        sheets = xls.sheet_names

        # Sélection de la feuille
        sheet = st.selectbox("Sélectionner la feuille", sheets)

        if sheet:
            # Lecture de la feuille sélectionnée
            df = pd.read_excel(xls, sheet_name=sheet)

            # Affichage du dataframe
            st.write("Aperçu des données importées:")
            st.write(df.head())

            # Vérification de la présence des colonnes nécessaires
            required_columns = ['matricule', 'nom_sup', 'nom_region']
            if all(column in df.columns for column in required_columns):
                if st.button("Enregistrer dans la base de données"):
                    data = df[required_columns].values.tolist()
                    insert_superviseur_data(data)
                    st.success("Données insérées avec succès dans la base de données.")
            else:
                st.error(f"Le fichier Excel doit contenir les colonnes suivantes : {', '.join(required_columns)}")






