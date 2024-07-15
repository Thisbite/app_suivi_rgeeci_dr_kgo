import sqlite3
import streamlit as st
from datetime import datetime
import data


# Fonction pour insérer des données dans différentes tables
def insert_data(table, data):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    queries = {
        'region': "INSERT INTO region (nom) VALUES (?)",
        'departement': "INSERT INTO departement (nom_departement, nom_region) VALUES (?, ?)",
        'sous_prefecture': "INSERT INTO sous_prefecture (nom_sous_prefecture, nom_departement) VALUES (?, ?)",
        'zone_denombrement': "INSERT INTO zone_denombrement (nom_zd, nom_sous_prefecture, nom_quartier) VALUES (?, ?, ?)",
        'ilot': "INSERT INTO ilot (nom_ilot, nom_zd) VALUES (?, ?)",
        'superviseur': "INSERT INTO superviseur (matricule, nom_sup, nom_region) VALUES (?, ?, ?)",
        'chef_equipe': "INSERT INTO chef_equipe (numero_equipe, matricule_ce, nom_chef_equipe, nom_sup) VALUES (?, ?, ?, ?)",
        'agent': "INSERT INTO agent (numero_agent, numero_equipe) VALUES (?, ?)"
    }

    if table in queries:
        c.execute(queries[table], data)
        conn.commit()
    conn.close()


# Créer les tables si elles n'existent pas
data.create_tables()


# Fonction pour la page de configuration
def localite():
    st.subheader("Paramètre de suivi de collecte RGEECI")

    tables = {
        'region': {'form_key': 'region_form', 'fields': [('Nom', 'text_input')]},
        'departement': {'form_key': 'departement_form',
                        'fields': [('Nom Département', 'text_input'), ('Nom Région', 'selectbox', data.get_region())]},
        'sous_prefecture': {'form_key': 'sous_prefecture_form', 'fields': [('Nom Sous-Prefecture', 'text_input'), (
        'Nom Département', 'selectbox', data.get_departement())]},
        'zone_denombrement': {'form_key': 'zone_denombrement_form',
                              'fields': [('Nom Zone de Dénombrement', 'text_input'),
                                         ('Nom Sous-Préfecture', 'selectbox', data.get_sous_prefecture()),
                                         ('Nom Quartier', 'text_input')]},
        'ilot': {'form_key': 'ilot_form', 'fields': [('Nom Ilot', 'text_input'), (
        'Nom Zone de Dénombrement', 'selectbox', data.get_zone_denombrement())]},
        'superviseur': {'form_key': 'superviseur_form',
                        'fields': [('Matricule', 'text_input'), ('Nom Superviseur', 'text_input'),
                                   ('Nom Région', 'selectbox', data.get_region())]},
        'chef_equipe': {'form_key': 'chef_equipe_form',
                        'fields': [('Numéro Équipe', 'text_input'), ('Matricule du CE', 'text_input'),
                                   ('Nom du chef équipe', 'text_input'),
                                   ('Nom Superviseur', 'selectbox', data.get_superviseurs())]},
        'agent': {'form_key': 'agent_form', 'fields': [('Numéro Agent', 'text_input'), ('Numéro Équipe', 'text_input')]}
    }

    table = st.selectbox('Sélectionnez le formulaire', list(tables.keys()))

    with st.form(key=tables[table]['form_key']):
        inputs = {}
        for field in tables[table]['fields']:
            label, input_type = field[0], field[1]
            if input_type == 'text_input':
                inputs[label] = st.text_input(label)
            elif input_type == 'selectbox':
                options = field[2]
                inputs[label] = st.selectbox(label, [opt[1] for opt in options])

        submit_button = st.form_submit_button(label='Enregistrer')
        if submit_button:
            if all(inputs.values()):
                insert_data(table, tuple(inputs.values()))
                st.success(f"Enregistrement réussi pour la table {table}.")
            else:
                st.error("Tous les champs sont obligatoires.")


# Fonction pour authentifier l'utilisateur
def authenticate_user(matricule, password):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    queries = {
        'superviseur': 'SELECT * FROM superviseur WHERE matricule = ? AND matricule = ?',
        'chef_equipe': 'SELECT * FROM chef_equipe WHERE matricule_ce = ? AND matricule_ce = ?'
    }

    for role, query in queries.items():
        c.execute(query, (matricule, password))
        user = c.fetchone()
        if user:
            conn.close()
            return role, matricule

    conn.close()
    return None, None


# Fonction pour récupérer le numéro d'équipe d'un chef d'équipe basé sur son matricule
import sqlite3
import streamlit as st
from datetime import datetime

# Fonction pour récupérer le numéro d'équipe
def get_numero_equipe(matricule_ce):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("SELECT numero_equipe FROM chef_equipe WHERE matricule_ce = ?", (matricule_ce,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Fonction pour récupérer les ZD par numéro d'équipe
def get_zone_denombrement_par_equipe(numero_equipe):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("""
    SELECT DISTINCT zd.nom_zd
    FROM zone_denombrement zd
    JOIN sous_prefecture sp ON zd.nom_sous_prefecture = sp.nom_sous_prefecture
    JOIN departement d ON sp.nom_departement = d.nom_departement
    JOIN region r ON d.nom_region = r.nom
    JOIN superviseur s ON r.nom=s.nom_region
    JOIN chef_equipe ce ON s.nom_sup = ce.nom_sup 
    WHERE ce.numero_equipe = ?
    """, (numero_equipe,))
    result = c.fetchall()
    conn.close()
    return result

# Fonction pour récupérer les ilots par ZD
def get_ilots_par_zd(nom_zd):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute("SELECT nom_ilot FROM ilot WHERE nom_zd = ?", (nom_zd,))
    result = c.fetchall()
    conn.close()
    return result

# Fonction pour insérer des réponses
def insert_reponse_data(numero_equipe, nom_zd, nom_ilot, numero_agent, nbre_UE_total, nbre_UE_partiel, nbre_UE_informel,
                        nbre_UE_formel, nbre_UE_refus, date_aujourdhui):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute('''
    INSERT INTO reponse (numero_equipe, nom_zd, nom_ilot, numero_agent, nbre_UE_total, nbre_UE_partiel, nbre_UE_informel, nbre_UE_formel, nbre_UE_refus, date_aujourdhui)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
    numero_equipe, nom_zd, nom_ilot, numero_agent, nbre_UE_total, nbre_UE_partiel, nbre_UE_informel, nbre_UE_formel,
    nbre_UE_refus, date_aujourdhui))
    conn.commit()
    conn.close()

# Fonction principale pour l'enregistrement des réponses
def reponse():
    st.title("Enregistrement des Réponses")

    if 'user_matricule' in st.session_state:
        matricule = st.session_state['user_matricule']
        numero_equipe = get_numero_equipe(matricule)

        if numero_equipe:
            st.write(f"Numéro d'équipe détecté : {numero_equipe}")

            with st.form(key='reponse_form'):
                # Récupérer les ZD et les afficher dans le sélecteur
                zds = get_zone_denombrement_par_equipe(numero_equipe)
                if zds:
                    nom_zd = st.selectbox("Nom Zone de Dénombrement", [zd[0] for zd in zds])

                    # Récupérer les ilots par ZD et les afficher dans le sélecteur
                    ilots = get_ilots_par_zd(nom_zd)
                    if ilots:
                        nom_ilot = st.selectbox("Nom Ilot", [ilot[0] for ilot in ilots])

                        numero_agent = st.number_input("Numéro Agent", min_value=0)
                        nbre_UE_total = st.number_input("Nombre d'UE Total", min_value=0)
                        nbre_UE_partiel = st.number_input("Nombre d'UE Partiel", min_value=0)
                        nbre_UE_informel = st.number_input("Nombre d'UE Informel", min_value=0)
                        nbre_UE_formel = st.number_input("Nombre d'UE Formel", min_value=0)
                        nbre_UE_refus = st.number_input("Nombre d'UE Refus", min_value=0)

                        # Bouton de soumission du formulaire
                        submitted = st.form_submit_button(label='Enregistrer')
                        if submitted:
                            date_aujourdhui = datetime.now().date()
                            insert_reponse_data(numero_equipe, nom_zd, nom_ilot, numero_agent, nbre_UE_total,
                                                nbre_UE_partiel, nbre_UE_informel, nbre_UE_formel, nbre_UE_refus,
                                                date_aujourdhui)
                            st.success("Enregistrement réussi.")
                    else:
                        st.warning("Aucun ilot trouvé pour cette ZD.")
                else:
                    st.warning("Aucune ZD trouvée pour cette équipe.")
        else:
            st.error("Numéro d'équipe non détecté.")
    else:
        st.error("Utilisateur non authentifié.")

# Appel de la fonction principale



# CSS personnalisé pour le style de la page
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stSidebar {
        background-color: #343a40;
        color: white;
    }
    .stButton>button {
        background-color: #FF8C00;
        color: white;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Interface de connexion utilisateur

