import sqlite3
import pandas as pd
import base64
import streamlit as st


def get_reponse_data():
    conn = sqlite3.connect("rgeeci.db")
    conn.execute('PRAGMA encoding="UTF-8";')

    query = '''
        SELECT 
            r.numero_equipe,
            r.numero_agent,
            rg.nom,
            d.nom_departement,
            sp.nom_sous_prefecture,
            zd.nom_zd,
            il.nom_ilot,
            r.nbre_UE_total,
            r.nbre_UE_partiel,
            r.nbre_UE_informel,
            r.nbre_UE_formel,
            r.nbre_UE_refus,
            r.date_aujourdhui,
            s.nom_sup
        FROM reponse r
        INNER JOIN chef_equipe ce ON r.numero_equipe = ce.numero_equipe
        INNER JOIN superviseur s ON ce.nom_sup = s.nom_sup
        LEFT JOIN ilot il ON r.nom_ilot = il.nom_ilot
        LEFT JOIN zone_denombrement zd ON il.nom_zd = zd.nom_zd
        LEFT JOIN sous_prefecture sp ON zd.nom_sous_prefecture = sp.nom_sous_prefecture
        LEFT JOIN departement d ON sp.nom_departement = d.nom_departement
        LEFT JOIN region rg ON d.nom_region = rg.nom
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()

    df.columns = ["Numero equipe", "Numero agent", "Region", "Departement",
                  "Sous-prefecture", "ZD", "Ilot", "Nombre UE total",
                  "Nombre UE partiel", "Nombre UE informel", "Nombre UE formel",
                  "Nombre UE refus", "Date", "Nom Superviseur"]

    # Convertir DataFrame en CSV avec encodage UTF-8
    csv = df.to_csv(index=False, encoding='utf-8-sig')

    # Encodage en base64
    b64 = base64.b64encode(csv.encode('utf-8')).decode()

    # Générer lien de téléchargement
    href = f'<a href="data:file/csv;base64,{b64}" download="reponse_data.csv">Télécharger CSV</a>'

    # Afficher lien dans Streamlit
    st.markdown(href, unsafe_allow_html=True)

    return df


def statistiques_par_agent_et_entite():
    conn = sqlite3.connect("rgeeci.db")

    query = '''
        SELECT 
            r.numero_equipe,
            r.numero_agent,
            rg.nom AS nom_region,
            d.nom_departement,
            sp.nom_sous_prefecture,
            zd.nom_zd,
            il.nom_ilot,
            r.nbre_UE_total,
            r.nbre_UE_partiel,
            r.nbre_UE_informel,
            r.nbre_UE_formel,
            r.nbre_UE_refus,
            r.date_aujourdhui,
            s.nom_sup AS nom_superviseur
        FROM reponse r
        INNER JOIN chef_equipe ce ON r.numero_equipe = ce.numero_equipe
        INNER JOIN superviseur s ON ce.nom_sup = s.nom_sup
        LEFT JOIN ilot il ON r.nom_ilot = il.nom_ilot
        LEFT JOIN zone_denombrement zd ON il.nom_zd = zd.nom_zd
        LEFT JOIN sous_prefecture sp ON zd.nom_sous_prefecture = sp.nom_sous_prefecture
        LEFT JOIN departement d ON sp.nom_departement = d.nom_departement
        LEFT JOIN region rg ON d.nom_region = rg.nom
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Calcul du nombre moyen d'UE total par agent
    moyen_agt = df.groupby(['nom_region', 'numero_equipe', 'numero_agent'])['nbre_UE_total'].mean().reset_index()
    moyen_agt = moyen_agt.sort_values(by='nbre_UE_total', ascending=False)

    # Calcul des statistiques par sous-préfecture
    stats_sous_prefecture = df.groupby(['numero_equipe', 'nom_region', 'nom_departement', 'nom_sous_prefecture']) \
        .agg({
        'nbre_UE_total': 'sum',
        'nbre_UE_partiel': 'sum',
        'nbre_UE_informel': 'sum',
        'nbre_UE_formel': 'sum',
        'nbre_UE_refus': 'sum'
    }).reset_index().sort_values(by='nbre_UE_total', ascending=False)

    # Calcul des statistiques par département
    stats_depart = df.groupby(['numero_equipe', 'nom_region', 'nom_departement']) \
        .agg({
        'nbre_UE_total': 'sum',
        'nbre_UE_partiel': 'sum',
        'nbre_UE_informel': 'sum',
        'nbre_UE_formel': 'sum',
        'nbre_UE_refus': 'sum'
    }).reset_index().sort_values(by='nbre_UE_total', ascending=False)

    # Calcul des statistiques par région
    stats_region = df.groupby(['nom_region']) \
        .agg({
        'nbre_UE_total': 'sum',
        'nbre_UE_partiel': 'sum',
        'nbre_UE_informel': 'sum',
        'nbre_UE_formel': 'sum',
        'nbre_UE_refus': 'sum'
    }).reset_index().sort_values(by='nbre_UE_total', ascending=False)

    return moyen_agt, stats_sous_prefecture, stats_depart, stats_region


# Utilisation des fonctions dans Streamlit
def main():
    st.title("Statistiques RGEECI")

    st.subheader("Données de réponse")
    df = get_reponse_data()
    st.dataframe(df)

    st.subheader("Statistiques par Agent et Entité")
    moyen_agt, stats_sous_prefecture, stats_depart, stats_region = statistiques_par_agent_et_entite()

    st.write("**Rendement moyen par agents**")
    st.dataframe(moyen_agt)

    st.write("**Statistiques par Sous-prefecture**")
    st.dataframe(stats_sous_prefecture)

    st.write("**Statistiques par Département**")
    st.dataframe(stats_depart)

    st.write("**Statistiques par Région**")
    st.dataframe(stats_region)


if __name__ == "__main__":
    main()
