# scripts/Inputs.py
import streamlit as st
from . import default
import json
import os

SAVE_FILE = "saved_inputs.json"

def main():
    st.subheader("Édition des données")
    st.sidebar.button("🔁 Réinitialiser les données", on_click=load_defaults)
    st.sidebar.button("💾 Sauvegarder les données", on_click=save_inputs)
    st.sidebar.button("📂 Charger les données sauvegardées", on_click=load_inputs)
    if "cours_data" not in st.session_state:
        load_defaults()
    
    # Initialiser si besoin

    Columns = {
        'CH_Prof': {'size' : 1.1, 'title' : 'Professeurs'},
        'CH_Salle': {'size' : 0.9,'title' : 'Salles'},
        'CU_Déplacement': {'size' : 0.9,'title' : 'Déplacements'},
        'cours_data': {'size' : 0.7,'title' : 'Programme'},
        'AddBudget': {'size': 0.5,'title': 'Budget Supp'}
    }

    STColumns = st.columns([icol['size'] for icol in Columns.values()])
    for ikey, icol in zip(Columns.keys(), STColumns):
        with icol:
            st.subheader(Columns[ikey]['title'])
            if ikey == 'cours_data':
                cours_data = st.session_state["cours_data"]
                cours_data = recompute_total(cours_data)
                st.session_state["cours_data"] = st.data_editor(cours_data, use_container_width=True, hide_index=True)
            else:
                st.session_state[ikey] = st.data_editor(st.session_state[ikey], use_container_width=True, hide_index=True if ikey != 'CH_Prof' else False)

def recompute_total(cours_dict):
    for cours in cours_dict['Nb']:
        nb = cours_dict['Nb'].get(cours, 0)
        duree = cours_dict['Durée'].get(cours, 0)
        cours_dict['Total'][cours] = nb * duree
    return cours_dict

def load_defaults():
    st.session_state["CH_Prof"] = default.CH_Prof.copy()
    st.session_state["CH_Salle"] = default.CH_Salle.copy()
    st.session_state["CU_Déplacement"] = default.CU_Déplacement.copy()
    st.session_state["cours_data"] = recompute_total(default.cours_data.copy())
    st.session_state["AddBudget"] = default.AddBudget.copy()
    st.sidebar.success("Données réinitialisées.", icon="✅")

def save_inputs():
    data = {
        "CH_Prof": st.session_state["CH_Prof"],
        "CH_Salle": st.session_state["CH_Salle"],
        "CU_Déplacement": st.session_state["CU_Déplacement"],
        "cours_data": st.session_state["cours_data"],
        "AddBudget": st.session_state["AddBudget"]
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    st.sidebar.success("Données sauvegardées.", icon="✅")

def load_inputs():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            st.session_state["CH_Prof"] = data["CH_Prof"]
            st.session_state["CH_Salle"] = data["CH_Salle"]
            st.session_state["CU_Déplacement"] = data["CU_Déplacement"]
            st.session_state["cours_data"] = data["cours_data"]
            st.session_state["AddBudget"] = data["AddBudget"]
        st.sidebar.success("Données chargées.", icon="✅")
    else:
        st.sidebar.warning("Aucune sauvegarde trouvée.", icon="⚠️")