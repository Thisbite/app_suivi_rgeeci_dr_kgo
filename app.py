import streamlit as st


# CSS personnalisé pour le style de la page avec les couleurs du drapeau de la Côte d'Ivoire
st.markdown("""
    <style>
        .stApp {
            background-color: #FFFFFF;  /* Couleur de fond */
        }
        .css-1d391kg {
            background-color: #FFFFFF;  /* Couleur de fond du conteneur principal */
        }
        .stTextInput > div {
            background-color: #FFFFFF;  /* Couleur de fond des champs de saisie de texte */
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #CCCCCC;
        }
        .stTextInput input {
            border: none;
            color: #000000;  /* Couleur du texte */
        }
        .stTextInput input:focus {
            outline: none;
            box-shadow: 0 0 5px 2px rgba(0, 0, 0, 0.1);
        }
        .stButton button {
            background-color: #FF8000;  /* Couleur orange pour le bouton */
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            cursor: pointer;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #FFA64D;  /* Orange plus clair au survol */
        }
        .stAlert div {
            background-color: #FFFFFF;  /* Couleur de fond des alertes */
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #CCCCCC;
        }
        .css-1siy2j7 {
            color: #00A859;  /* Couleur verte pour les messages de succès */
            font-weight: bold;
        }
        .css-10trblm {
            color: #FF8000;  /* Couleur orange pour les messages d'erreur */
            font-weight: bold;
        }
        .css-10trblm h1 {
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


import streamlit as st
import connexion
import data
import page

def login_page():
    st.title("Système de Suivi de Collecte RGEECI")

    # Matricule et mot de passe pour la connexion
    matricule = st.text_input("Matricule")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        role, user_matricule = page.authenticate_user(matricule, password)
        if role:
            st.session_state['logged_in'] = True
            st.session_state['user_matricule'] = user_matricule
            st.session_state['user_role'] = role
            st.success(f"Bienvenue, {role} {user_matricule}")
            st.experimental_rerun()  # Rafraîchit l'application pour afficher la page principale
        else:
            st.error("Matricule ou mot de passe incorrect.")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None

    if not st.session_state['logged_in']:
        login_page()
    else:
        st.markdown("""
            <style>
                .sidebar .sidebar-content {
                    background-color: #f0f0f0;
                    padding: 20px;
                    border-radius: 10px;
                }
                .main {
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                }
                .footer {
                    text-align: center;
                    margin-top: 20px;
                }
            </style>
        """, unsafe_allow_html=True)

        st.sidebar.title("Menu")
        if st.session_state['user_role'] == 'superviseur':
            pages = st.sidebar.selectbox("Choisir menu", [ "Statistiques","Configuration"])
        elif st.session_state['user_role'] == 'chef_equipe':
            pages = st.sidebar.selectbox("Choisir menu", ["Saisie les statistiques"])

        if pages == "Saisie les statistiques":
            page.reponse()
        elif pages == "Statistiques":
            moyen, sous_p, dep, region = connexion.statistiques_par_agent_et_entite()
            st.write("_________________________________________________")
            st.subheader("Rendement moyen par agents")
            st.write("_________________________________________________")
            st.dataframe(moyen)
            st.write("_________________________________________________")
            st.subheader("Statistiques par équipe et  Sous-prefecture")
            st.write("_________________________________________________")
            st.dataframe(sous_p)
            st.write("_________________________________________________")
            st.subheader("Statistiques par département")
            st.write("_________________________________________________")
            st.dataframe(dep)
            st.write("_________________________________________________")
            st.subheader("Statistiques par région")
            st.write("_________________________________________________")
            st.dataframe(region)
            st.write("_________________________________________________")
            st.subheader("Données globales et exportation")
            st.write("_________________________________________________")
            df = connexion.get_reponse_data()
            st.write("_________________________________________________")
            st.dataframe(df)
            st.write("_________________________________________________")
        elif pages == "Configuration":
            page.localite()
            st.write("_________________________________________________")
            data.chef_equipe_update_page()
            st.write("_________________________________________________")
            data.superviseur_update_page()
            st.write("_________________________________________________")
            data.departement_update_page()
            st.write("_________________________________________________")
            data.sous_prefecture_update_page()
            st.write("_________________________________________________")
            data.zone_denombrement_update_page()
            st.write("_________________________________________________")
            data.ilot_update_page()
            st.write("_________________________________________________")
            if st.checkbox("Vue sur table", key="vue12"):
                d1, d2, d3, d4 = data.vue()
                st.write(d1)
                st.write("_________________________________________________")
                st.write(d2)
                st.write("_________________________________________________")
                st.write(d3)
                st.write("_________________________________________________")
                st.write(d4)
                st.write("_________________________________________________")

        # Ajout du bouton de déconnexion dans le menu latéral
        if st.sidebar.button("Déconnexion"):
            st.session_state['logged_in'] = False
            st.session_state['user_role'] = None
            st.session_state['user_matricule'] = None
            st.experimental_rerun()  # Rafraîchit l'application pour afficher la page de connexion

# Lancer la fonction principale
main()
