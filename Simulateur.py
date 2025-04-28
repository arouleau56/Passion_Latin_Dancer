import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Données de base
CH_Prof = {
    'Johanna': {'Niv1': 30, 'Niv2': 30},
    'Merhan': {'Bodywork': 60, 'LadyStyling': 60, 'AtChor': 60, 'Intensif': 55},
    'Samuel': {'Niv1': 55, 'Niv2': 55, 'AtChor': 55, 'Intensif': 55}
}

CH_Salle = {
    'Orpheon': {'Niv1': 17, 'Niv2': 17},
    'StEtMtLc': {'Bodywork': 0, 'LadyStyling': 0, 'AtChor': 0, 'Intensif': 0},
    'Assurance': {'Niv1': 0.51, 'Niv2': 0.51, 'Bodywork': 0.51, 'LadyStyling': 0.51},
}

CU_Déplacement = {
    'Johanna': {'Niv1': 0, 'Niv2': 0},
    'Merhan': {'Bodywork': 10, 'LadyStyling': 10, 'AtChor': 10, 'Intensif': 10},
    'Samuel': {'Niv1': 0, 'Niv2': 0, 'AtChor': 0, 'Intensif': 0}
}

CF_Adhesion = {'Inscription': 15}

Cours = {
    'Nb': {'Niv1': 33, 'Niv2': 33, 'Bodywork': 15, 'LadyStyling': 15, 'AtChor': 10, 'Intensif': 10},
    'Durée': {'Niv1': 1.5, 'Niv2': 1.5, 'Bodywork': 1, 'LadyStyling': 1.5, 'AtChor': 2, 'Intensif': 6},
    'Total': {'Niv1': 0, 'Niv2': 0, 'Bodywork': 0, 'LadyStyling': 0, 'AtChor': 0, 'Intensif': 0}
}

AddBudget = {'Niv1': 0, 'Niv2': 0, 'Bodywork': 0, 'LadyStyling': 0, 'AtChor': 0, 'Intensif': 0}

Couts_Adhesion = {'Niv1': 235, 'Niv2': 235, 'Bodywork': 110, 'LadyStyling': 165, 'AtChor': 290, 'Intensif': 435}

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
col11, col12, col13, col14, col15, col16 = st.columns([1.2,0.9,0.8,0.7,0.5,0.7])

with col11:
    st.subheader("Professeurs")
    edited_profs = st.data_editor(CH_Prof, num_rows="fixed", use_container_width=True)

with col12:
    st.subheader("Salles")
    edited_salles = st.data_editor(CH_Salle, num_rows="fixed", use_container_width=True, hide_index=True)

with col13:
    st.subheader("Déplacements")
    edited_dep = st.data_editor(CU_Déplacement, num_rows="fixed", use_container_width=True, hide_index=True)

with col14:
    st.subheader("Programmes")
    edited_cours = st.data_editor(
        st.session_state.cours_data,
        num_rows="fixed",
        use_container_width=True,
        key="editor_cours",
        hide_index=True
    )

with col15:
    st.subheader("Budget Sup")
    edited_budget_sup = st.data_editor(AddBudget, num_rows="fixed", use_container_width=True, hide_index=True)

with col16:
    st.image("Logo.png", width=300)

    st.subheader("Autres frais")
    edited_adhesion = st.data_editor(CF_Adhesion, num_rows="fixed", use_container_width=True)

col21, col22 = st.columns([4.1, 0.7])

def compute_budgets(CH_Prof, CH_Salle, CU_Déplacement, cours_data, add_budget):
    budgets = {}
    
    # Coût individuel par prof
    budget_johanna = {}
    budget_merhan = {}
    budget_samuel = {}

    # Calcul Budget Professeurs
    budget_prof = {}
    for prof, matieres in CH_Prof.items():
        for matiere, taux in matieres.items():
            heures = cours_data['Total'].get(matiere, 0)
            cout = taux * heures

            if prof == 'Johanna':
                budget_johanna[matiere] = cout
            elif prof == 'Merhan':
                budget_merhan[matiere] = cout
            elif prof == 'Samuel':
                budget_samuel[matiere] = cout

            budget_prof[matiere] = budget_prof.get(matiere, 0) + cout

    # DataFrames individuels
    df_johanna = pd.DataFrame.from_dict(budget_johanna, orient='index', columns=['Johanna'])
    df_merhan = pd.DataFrame.from_dict(budget_merhan, orient='index', columns=['Merhan'])
    df_samuel = pd.DataFrame.from_dict(budget_samuel, orient='index', columns=['Samuel'])
    df_professeurs = pd.DataFrame.from_dict(budget_prof, orient='index', columns=['Professeurs'])

    # Calcul Budget Salles
    budget_salle = {}
    for salle, matieres in CH_Salle.items():
        if salle != "Assurance":
            for matiere, taux in matieres.items():
                heures = cours_data['Total'].get(matiere, 0)
                budget_salle[matiere] = budget_salle.get(matiere, 0) + taux * heures
    df_salles = pd.DataFrame.from_dict(budget_salle, orient='index', columns=['Salles'])

    # Calcul Budget Assurance
    budget_assurance = {}
    for matiere, taux in CH_Salle.get('Assurance', {}).items():
        heures = cours_data['Total'].get(matiere, 0)
        budget_assurance[matiere] = taux * heures
    df_assurance = pd.DataFrame.from_dict(budget_assurance, orient='index', columns=['Assurance'])

    # Calcul Budget Déplacements
    budget_deplacement = {}
    for prof, matieres in CU_Déplacement.items():
        for matiere, montant in matieres.items():
            nb_cours = cours_data['Nb'].get(matiere, 0)
            budget_deplacement[matiere] = budget_deplacement.get(matiere, 0) + montant * nb_cours
    df_deplacement = pd.DataFrame.from_dict(budget_deplacement, orient='index', columns=['Déplacements'])

    # Calcul Budget Supplémentaire
    budget_sup = {}
    for matiere in cours_data['Nb']:
        budget_sup[matiere] = add_budget.get(matiere, 0)
    df_budget_sup = pd.DataFrame.from_dict(budget_sup, orient='index', columns=['Budget Sup'])

    # Concaténation dans le bon ordre
    budget_final = pd.concat(
        [df_johanna, df_merhan, df_samuel, df_professeurs, df_salles, df_assurance, df_deplacement, df_budget_sup],
        axis=1
    ).fillna(0)

    # Calcul Global : uniquement sur Professeurs + Salles + Assurance + Déplacements + Budget Supplémentaire
    budget_final['Global'] = budget_final[['Professeurs', 'Salles', 'Assurance', 'Déplacements', 'Budget Sup']].sum(axis=1)

    # Résumé
    budget_resume = pd.DataFrame(budget_final[['Professeurs', 'Salles', 'Assurance', 'Déplacements', 'Budget Sup', 'Global']].sum(axis=0)).transpose()
    budget_resume.index = ['Total par catégorie']

    return budget_final, budget_resume

# 3. Onglets
with col21:
    tab1, tab2 = st.tabs(['Budget', 'Simulation'])

    with tab1:
        subcol1, subcol2 = st.columns([1.25, 1])
        with subcol1:
            if 'budget_final' in st.session_state:
                st.subheader("Budget Consolidé")
                st.dataframe(st.session_state.budget_final.style.format("{:.2f} €"))
        with subcol2:
            if 'budget_resume' in st.session_state:
                st.subheader("Résumé des Budgets par Catégorie")
                st.dataframe(st.session_state.budget_resume.style.format("{:.2f} €"))
            pass

    with tab2:
        pass

with col22:
    st.subheader("Coûts d'adhésion")
    edited_adhesion = st.data_editor(Couts_Adhesion, num_rows="fixed", use_container_width=True)

    if st.button("Update program", type="primary", use_container_width=True):
        st.session_state.cours_data = edited_cours
        st.session_state.cours_data = recompute_total(st.session_state.cours_data)
        st.session_state.budget_final, st.session_state.budget_resume = compute_budgets(
            edited_profs,
            edited_salles,
            edited_dep,
            st.session_state.cours_data,
            edited_budget_sup
        )
        st.experimental_rerun()
    pass