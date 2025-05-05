import streamlit as st
import pandas as pd
from plotly import express as px

from .Inputs import recompute_total
#from .Budget import compute_budgets  # utile si Budget.py est séparé en compute et main

ColToShow = ['Professeurs', 'Salles', 'Assurance', 'Déplacements', 'Budget Sup']

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
            cout = (taux or 0) * (heures or 0)

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
                budget_salle[matiere] = budget_salle.get(matiere, 0) + (taux or 0) * (heures or 0)
    df_salles = pd.DataFrame.from_dict(budget_salle, orient='index', columns=['Salles'])

    # Calcul Budget Assurance
    budget_assurance = {}
    for matiere, taux in CH_Salle.get('Assurance', {}).items():
        heures = cours_data['Total'].get(matiere, 0)
        budget_assurance[matiere] = (taux or 0) * (heures or 0)
    df_assurance = pd.DataFrame.from_dict(budget_assurance, orient='index', columns=['Assurance'])

    # Calcul Budget Déplacements
    budget_deplacement = {}
    for prof, matieres in CU_Déplacement.items():
        for matiere, montant in matieres.items():
            nb_cours = cours_data['Nb'].get(matiere, 0)
            budget_deplacement[matiere] = budget_deplacement.get(matiere, 0) + (montant or 0) * (nb_cours or 0)
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

def actualize_budget(ColToShow=ColToShow):
    st.session_state["cours_data"] = recompute_total(st.session_state["cours_data"])
    budget_final, budget_resume = compute_budgets(
        st.session_state["CH_Prof"],
        st.session_state["CH_Salle"],
        st.session_state["CU_Déplacement"],
        st.session_state["cours_data"],
        st.session_state["AddBudget"]
    )
    budget_final, budget_parcours = budget_final[ColToShow], budget_final[['Global']]
    budget_global = budget_parcours.sum()

    st.session_state["budget_final"] = budget_final
    st.session_state["budget_resume"] = budget_resume
    st.session_state["budget_parcours"] = budget_parcours
    #st.session_state["budget_global"] = budget_global
    st.success("Budget mis à jour.")

    BudgetCol, ChartCol = st.columns([2, 1])

    with BudgetCol:
        if "budget_final" in st.session_state:
            st.dataframe(st.session_state["budget_final"][ColToShow].style.format("{:.2f} €"), use_container_width=True)
        
        CoursCol, CatCol, CatGlobal = st.columns([1, 1, 1])
        with CoursCol:
            if "budget_parcours" in st.session_state:
                st.subheader("Budget par parcours")
                st.dataframe(st.session_state["budget_parcours"].style.format("{:.2f} €"), use_container_width=False)
        with CatCol:
            if "budget_resume" in st.session_state:
                st.subheader("Budget par catégorie")
                st.dataframe(st.session_state["budget_resume"][ColToShow].T.style.format("{:.2f} €"), use_container_width=False)

        with CatGlobal:
            if "budget_global" in st.session_state:
                st.subheader("Budget global")
                #st.dataframe(st.session_state["budget_global"].T.style.format("{:.2f} €"), use_container_width=False)
                st.subheader(f"Total : {budget_global.loc['Global'].round(2)}€")
    
    with ChartCol:
        fig = px.bar(
            st.session_state["budget_resume"],
            x=st.session_state["budget_resume"].index,
            y=ColToShow,
            title=None,
            labels={"value": "Montant (€)", "index": "Catégorie"},
            text_auto=True,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

def main():
    if not all(k in st.session_state for k in ["CH_Prof", "CH_Salle", "CU_Déplacement", "cours_data", "AddBudget"]):
        st.warning("Veuillez d'abord remplir les données dans l'onglet Inputs.")
        return
    st.sidebar.button("🔁 Actualiser le budget", on_click=actualize_budget)