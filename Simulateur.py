import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Données de base
Couts = {
    'CH Johanna': {'Niv1': 30, 'Niv2': 30},
    'CH Merhan': {'Bodywork': 60, 'LadyStyling': 60, 'AtChor': 60, 'Intensif': 55},
    'CH Samuel': {'Niv1': 55, 'Niv2': 55, 'AtChor': 55, 'Intensif': 55},
    'CH Orpheon': {'Niv1': 17, 'Niv2': 17},
    'CH StEtMtLc': {'Bodywork': 0, 'LadyStyling': 0, 'AtChor': 0, 'Intensif': 0},
    'Ass Orpheon': {'Niv1': 0.51, 'Niv2': 0.51, 'Bodywork': 0.51, 'LadyStyling': 0.51},
    'Dep Johanna': {'Niv1': 0, 'Niv2': 0},
    'Dep Merhan': {'Bodywork': 10, 'LadyStyling': 10, 'AtChor': 10, 'Intensif': 10},
    'Dep Samuel': {'Niv1': 0, 'Niv2': 0, 'AtChor': 0, 'Intensif': 0}
}

CF_Adhesion = {'Adhésion': 15}

Cours = {
    'Nb': {'Niv1': 33, 'Niv2': 33, 'Bodywork': 15, 'LadyStyling': 15, 'AtChor': 10, 'Intensif': 10},
    'Durée': {'Niv1': 1.5, 'Niv2': 1.5, 'Bodywork': 1, 'LadyStyling': 1.5, 'AtChor': 2, 'Intensif': 6},
    'Total': {'Niv1': 0, 'Niv2': 0, 'Bodywork': 0, 'LadyStyling': 0, 'AtChor': 0, 'Intensif': 0}
}

AddBudget = {'Niv1': 0, 'Niv2': 0, 'Bodywork': 0, 'LadyStyling': 0, 'AtChor': 0, 'Intensif': 0}

def recompute_total(cours_dict):
    """
    Recalcule Total = Nb × Durée pour chaque cours.
    """
    for cours in cours_dict['Nb']:
        nb = cours_dict['Nb'].get(cours, 0)
        duree = cours_dict['Durée'].get(cours, 0)
        cours_dict['Total'][cours] = nb * duree
    return cours_dict

# -----------------------
# 1. Chargement dans session_state
# -----------------------
if 'cours_data' not in st.session_state:
    st.session_state.cours_data = Cours
    st.session_state.cours_data = recompute_total(st.session_state.cours_data)

# 2. Layout
col11, col12, col13 = st.columns([4.6, 1.4, 0.80])

with col11:
    st.subheader("Entrées")
    edited_profs1 = st.data_editor(Couts, num_rows="dynamic", use_container_width=True)

with col12:
    st.subheader("Programme")
    edited_cours = st.data_editor(
        st.session_state.cours_data,
        num_rows="dynamic",
        use_container_width=False,
        key="editor_cours"
    )

with col13:
    st.subheader("Budget Sup")
    edited_adhesion = st.data_editor(AddBudget, num_rows="dynamic", use_container_width=False)

col21, col22 = st.columns([6, 0.8])
# 3. Onglets
Onglet = ['Budget', 'Simulation']
with col21:
    st.tabs(Onglet)

with col22:
    st.subheader("Adhésion")
    edited_adhesion = st.data_editor(CF_Adhesion, num_rows="dynamic", use_container_width=False)

    # Ajout du bouton de mise à jour
    if st.button("Mettre à jour Total"):
        # On récupère les données éditées
        st.session_state.cours_data = edited_cours
        # Puis on recalcule
        st.session_state.cours_data = recompute_total(st.session_state.cours_data)
        # Et on force un rerun de la page pour mettre à jour l'affichage
        st.experimental_rerun()