import streamlit as st
import connexion
import  page

import page  # Assurez-vous que la fonction authenticate_user est importée depuis le module page

def login_page():
    # Adding CSS for the colors of the Côte d'Ivoire flag (orange, white, green)
    st.markdown("""
        <style>
            .stApp {
                background-color: #FFFFFF;  /* Background color */
            }
            .css-1d391kg {
                background-color: #FFFFFF;  /* Background color of the main container */
            }
            .stTextInput > div {
                background-color: #FFFFFF;  /* Background color of the text input fields */
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #CCCCCC;
            }
            .stTextInput input {
                border: none;
                color: #000000;  /* Text color */
            }
            .stTextInput input:focus {
                outline: none;
                box-shadow: 0 0 5px 2px rgba(0, 0, 0, 0.1);
            }
            .stButton button {
                background-color: #FF8000;  /* Orange color for the button */
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                cursor: pointer;
                font-weight: bold;
            }
            .stButton button:hover {
                background-color: #FFA64D;  /* Lighter orange on hover */
            }
            .stAlert div {
                background-color: #FFFFFF;  /* Background color of alert boxes */
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #CCCCCC;
            }
            .css-1siy2j7 {
                color: #00A859;  /* Green color for success messages */
                font-weight: bold;
            }
            .css-10trblm {
                color: #FF8000;  /* Orange color for error messages */
                font-weight: bold;
            }
            .css-10trblm h1 {
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Connexion")

    matricule = st.text_input("Matricule")
    password = st.text_input("Mot de passe", type="password")
    submit_button = st.button("Se connecter")

    if submit_button:
        user_role, user_matricule = page.authenticate_user(matricule, password)

        if user_role == 'superviseur':
            st.success("Connexion réussie en tant que superviseur.")
            st.session_state['logged_in'] = True
            st.session_state['user_role'] = 'superviseur'
            st.session_state['user_matricule'] = user_matricule
            st.experimental_rerun()
        elif user_role == 'chef_equipe':
            st.success("Connexion réussie en tant que chef d'équipe.")
            st.session_state['logged_in'] = True
            st.session_state['user_role'] = 'chef_equipe'
            st.session_state['user_matricule'] = user_matricule
            st.experimental_rerun()
        else:
            st.error("Matricule ou mot de passe incorrect.")



# Page principale
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None

    if st.session_state['logged_in']:
        st.markdown(
            """
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
            """,
            unsafe_allow_html=True
        )

        st.sidebar.title("Navigation")
        if st.session_state['user_role'] == 'superviseur':
            pages = st.sidebar.selectbox("Choisir une page", ["Saisie les statistiques", "Statistique", "Configuration"])
        elif st.session_state['user_role'] == 'chef_equipe':
            pages = st.sidebar.selectbox("Choisir une page", ["Saisie les statistiques", "Statistique"])

        if pages == "Saisie les statistiques":
            page.reponse()
        elif pages == "Statistique":
            moyen, sous_p, dep, region = connexion.statistiques_par_agent_et_entite()
            st.subheader("Rendement moyen par agents")
            st.dataframe(moyen)
            st.subheader("Statistiques par Sous-prefecture")
            st.dataframe(sous_p)
            st.subheader("Statistiques par département")
            st.dataframe(dep)
            st.subheader("Statistiques par région")
            st.dataframe(region)
            st.subheader("Données globales et exportation")
            df = connexion.get_reponse_data()
            st.dataframe(df)
        elif pages == "Configuration":
            page.localite()

    else:
        login_page()

main()
