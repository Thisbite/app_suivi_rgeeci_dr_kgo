import sqlite3
import streamlit as st
import data
def insert_data(table, data):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    if table == 'region':
        c.execute("INSERT INTO region ( nom) VALUES ( ?)", data)
    elif table == 'departement':
        c.execute("INSERT INTO departement ( nom_departement, nom_region) VALUES ( ?, ?)", data)
    elif table == 'sous_prefecture':
        c.execute("INSERT INTO sous_prefecture ( nom_sous_prefecture, nom_departement) VALUES ( ?, ?)", data)
    elif table == 'zone_denombrement':
        c.execute("INSERT INTO zone_denombrement (nom_zd, nom_sous_prefecture, nom_quartier) VALUES ( ?, ?, ?)", data)
    elif table == 'ilot':
        c.execute("INSERT INTO ilot ( nom_ilot, nom_zd) VALUES ( ?, ?)", data)
    elif table == 'superviseur':
        c.execute("INSERT INTO superviseur (matricule, nom_sup, nom_region) VALUES (?, ?, ?)", data)
    elif table == 'chef_equipe':
        c.execute("INSERT INTO chef_equipe (numero_equipe,matricule_ce,nom_chef_equipe, nom_sup) VALUES ( ?,?,?, ?)", data)
    elif table == 'agent':
        c.execute("INSERT INTO agent ( numero_agent, numero_equipe) VALUES ( ?, ?)", data)

    conn.commit()
    conn.close()

# Créer les tables si elles n'existent pas
data.create_tables()

import streamlit as st
import connexion

# Fonction pour la page de configuration
def localite():
    st.title("Paramètre de suivi de collecte RGEECI")

    table = st.selectbox('Sélectionnez la table', ['region', 'departement', 'sous_prefecture', 'zone_denombrement', 'ilot', 'superviseur', 'chef_equipe', 'agent'])

    if table == 'region':
        with st.form(key='region_form'):
            nom = st.text_input("Nom")
            submit_button = st.form_submit_button(label='Enregistrer')
            if submit_button:
                if nom:
                    insert_data('region', (nom,))
                    st.success("Enregistrement réussi pour la table région.")
                else:
                    st.error("Tous les champs sont obligatoires.")

    elif table == 'departement':
        with st.form(key='departement_form'):
            nom_departement = st.text_input("Nom Département")
            regions = data.get_region()  # Assurez-vous que cette fonction renvoie les régions disponibles
            nom_region = st.selectbox("Nom Région", [region[1] for region in regions])
            submit_button = st.form_submit_button(label='Enregistrer')
            if submit_button:
                if nom_departement and nom_region:
                    insert_data('departement', (nom_departement, nom_region))
                    st.success("Enregistrement réussi pour la table département.")
                else:
                    st.error("Tous les champs sont obligatoires.")

    elif table == 'sous_prefecture':
        with st.form(key='sous_prefecture_form'):
            nom_sous_prefecture = st.text_input("Nom Sous-Prefecture")
            departements = data.get_departement()  # Assurez-vous que cette fonction renvoie les départements disponibles
            nom_departement = st.selectbox("Nom du Département", [departement[1] for departement in departements])
            submit_button = st.form_submit_button(label='Enregistrer')
            if submit_button:
                if nom_sous_prefecture and nom_departement:
                    insert_data('sous_prefecture', (nom_sous_prefecture, nom_departement))
                    st.success("Enregistrement réussi pour la table sous-prefecture.")
                else:
                    st.error("Tous les champs sont obligatoires.")

    elif table == 'zone_denombrement':
        with st.form(key='zone_denombrement_form'):
            st.write("Exemple nom ZD:ZD4006")
            nom_zd = st.text_input("Nom Zone de Denombrement")
            sous_pref = data.get_sous_prefecture()  # Assurez-vous que cette fonction renvoie les sous-préfectures disponibles
            nom_sous_prefecture = st.selectbox("Nom Sous-Préfecture", [sous_prefecture[1] for sous_prefecture in sous_pref])
            nom_quartier = st.text_input("Nom Quartier")
            submit_button = st.form_submit_button(label='Enregistrer')
            if submit_button:
                if nom_zd and nom_sous_prefecture and nom_quartier:
                    insert_data('zone_denombrement', (nom_zd, nom_sous_prefecture, nom_quartier))
                    st.success("Enregistrement réussi pour la table zone de denombrement.")
                else:
                    st.error("Tous les champs sont obligatoires.")

    elif table == 'ilot':
        with st.form(key='ilot_form'):
            st.write("Exemple nom ilot:001")
            nom_ilot = st.text_input("Nom Ilot")
            zd = data.get_zone_denombrement()  # Assurez-vous que cette fonction renvoie les zones de dénombrement disponibles
            nom_zd = st.selectbox("Nom Zone de Dénombrement", [zds[1] for zds in zd])
            submit_button = st.form_submit_button(label='Enregistrer')
            if submit_button:
                if nom_ilot and nom_zd:
                    insert_data('ilot', (nom_ilot, nom_zd))
                    st.success("Enregistrement réussi pour la table ilot.")
                else:
                    st.error("Tous les champs sont obligatoires.")

    elif table == 'superviseur':
        with st.form(key='superviseur_form'):
            matricule = st.text_input("Matricule")
            nom_sup = st.text_input("Nom Superviseur")
            regions = data.get_region()  # Assurez-vous que cette fonction renvoie les régions disponibles
            nom_region = st.selectbox("Nom Région", [region[1] for region in regions])
            submit_button = st.form_submit_button(label='Enregistrer')
            if submit_button:
                if matricule and nom_sup and nom_region:
                    insert_data('superviseur', (matricule, nom_sup, nom_region))
                    st.success("Enregistrement réussi pour la table superviseur.")
                else:
                    st.error("Tous les champs sont obligatoires.")

    elif table == 'chef_equipe':
        with st.form(key='chef_equipe_form'):
            numero_equipe = st.text_input("Numéro Équipe")
            matricule_ce = st.text_input("Matricule du CE")
            nom_chef_equipe = st.text_input("Nom du chef équipe")
            sup = data.get_superviseurs()
            nom_sup = st.selectbox("Nom Superviseur", [sups[1] for sups in sup])
            submit_button = st.form_submit_button(label='Enregistrer')
            if submit_button:
                if numero_equipe and nom_sup and matricule_ce and nom_chef_equipe:
                    insert_data('chef_equipe', (numero_equipe, matricule_ce, nom_chef_equipe, nom_sup))
                    st.success("Enregistrement réussi pour la table chef_equipe.")
                else:
                    st.error("Tous les champs sont obligatoires.")

    elif table == 'agent':
        with st.form(key='agent_form'):
            numero_agent = st.text_input("Numéro Agent")
            numero_equipe = st.text_input("Numéro Équipe")
            submit_button = st.form_submit_button(label='Enregistrer')
            if submit_button:
                if numero_agent and numero_equipe:
                    insert_data('agent', (numero_agent, numero_equipe))
                    st.success("Enregistrement réussi pour la table agent.")
                else:
                    st.error("Tous les champs sont obligatoires.")


def authenticate_user(matricule, password):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()

    # Vérifier si l'utilisateur est un superviseur
    c.execute('SELECT * FROM superviseur WHERE matricule = ? AND matricule = ?', (matricule, password))
    superviseur = c.fetchone()

    if superviseur:
        conn.close()
        return 'superviseur', matricule

    # Vérifier si l'utilisateur est un chef d'équipe
    c.execute('SELECT * FROM chef_equipe WHERE matricule_ce = ? AND matricule_ce = ?', (matricule, password))
    chef_equipe = c.fetchone()

    if chef_equipe:
        conn.close()
        return 'chef_equipe', matricule

    conn.close()
    return None, None


def get_numero_equipe(matricule):
    conn = sqlite3.connect("rgeeci.db")
    c = conn.cursor()
    c.execute('SELECT numero_equipe FROM chef_equipe WHERE matricule_ce = ?', (matricule,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None


# Fonction pour la page des réponses
def reponse():
    st.title("Enregistrement des Réponses")

    if 'user_matricule' in st.session_state:
        matricule = st.session_state['user_matricule']
        numero_equipe = get_numero_equipe(matricule)

        if numero_equipe:
            st.write(f"Numéro d'équipe détecté : {numero_equipe}")

            with st.form(key='reponse_form'):
                zd = data.get_zone_denombrement()
                nom_zd = st.selectbox("Nom Zone de Dénombrement", [zds[1] for zds in zd])

                ilots = data.get_ilot()
                nom_ilot = st.selectbox("Nom Ilot", [ilot[1] for ilot in ilots])

                numero_agent = st.number_input("Numéro Agent", min_value=0)
                nbre_UE_total = st.number_input("Nombre d'UE Total", min_value=0)
                nbre_UE_partiel = st.number_input("Nombre d'UE Partiel", min_value=0)
                nbre_UE_informel = st.number_input("Nombre d'UE Informel", min_value=0)
                nbre_UE_formel = st.number_input("Nombre d'UE Formel", min_value=0)
                nbre_UE_refus = st.number_input("Nombre d'UE Refus", min_value=0)

                submit_button = st.form_submit_button(label='Enregistrer')
                if submit_button:
                    if (nom_zd and nom_ilot and numero_agent and nbre_UE_total and nbre_UE_partiel
                            and nbre_UE_informel and nbre_UE_formel and nbre_UE_refus):
                        # Récupération de la date actuelle
                        import datetime
                        date_aujourdhui=datetime.datetime.now().strftime("%Y-%m-%d")

                        # Insertion des données dans la table 'reponse'
                        data.insert_reponse_data(numero_equipe, nom_zd, nom_ilot, numero_agent, nbre_UE_total,
                                                 nbre_UE_partiel, nbre_UE_informel, nbre_UE_formel, nbre_UE_refus,
                                                 date_aujourdhui)
                        st.success("Enregistrement réussi pour la table reponse.")
                    else:
                        st.error("Tous les champs sont obligatoires.")
        else:
            st.error("Numéro d'équipe non trouvé pour ce chef d'équipe.")
    else:
        st.error("Utilisateur non authentifié.")


# Ajout de CSS pour styliser la page
st.markdown(
    """
    <style>
        .st-eb {
            background-color: #f0f0f0; /* Couleur de fond */
            padding: 20px; /* Espacement intérieur */
            border-radius: 10px; /* Coins arrondis */
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Ombre légère */
        }
        .st-eb-header {
            background-color: #ffffff; /* Couleur d'arrière-plan de l'en-tête */
            padding: 10px; /* Espacement intérieur de l'en-tête */
            border-bottom: 1px solid #e6e6e6; /* Bordure inférieure */
            border-radius: 10px 10px 0 0; /* Coins arrondis, seulement en haut */
        }
        .st-eb-content {
            padding: 20px; /* Espacement intérieur du contenu */
        }
        .st-eb-footer {
            text-align: center; /* Alignement du texte au centre */
            margin-top: 20px; /* Marge en haut */
        }
    </style>
    """,
    unsafe_allow_html=True
)