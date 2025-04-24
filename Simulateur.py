
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
#st.title("Simulateur de Coût Horaire")

# Données de base
Raw_Input = {
    'P_Johanna':{
        'Niv1': 30,
        'Niv2': 30
    },
    'P_Merhan':{
        'Bodywork': 60,
        'LadyStyling': 60,
        'AtChor': 60,
        'Intensif': 55
    },
    'P_Samuel':{
        'Niv1': 55,
        'Niv2': 55,
        'AtChor': 55,
        'Intensif': 55
    },
    'S_Orpheon':{
        'Niv1': 17,
        'Niv2': 17
    },
    'S_StEtMtLc':{
        'Bodywork': 0,
        'LadyStyling': 0,
        'AtChor': 0,
        'Intensif': 0
    },
    'A_Orpheon':{
        'Niv1': 0.51,
        'Niv2': 0.51,
        'Bodywork': 0.51,
        'LadyStyling': 0.51,
    },
    'D_Johanna': {
        'Niv1': 0,
        'Niv2': 0
    },
    'D_Merhan': {
        'Bodywork': 10,
        'LadyStyling': 10,
        'AtChor': 10,
        'Intensif': 10
    },
    'D_Samuel': {
        'Niv1': 0,
        'Niv2': 0,
        'AtChor': 0,
        'Intensif': 0
    }
}

CF_Adhesion = {
    'Adhésion': 15
}

Cours = {
    'NbSeances':
    {
        'Niv1': 33,
        'Niv2': 33,
        'Bodywork': 15,
        'LadyStyling': 15,
        'AtChor': 10,
        'Intensif': 10
    },
    'DureeSeance':
    {
        'Niv1': 1.5,
        'Niv2': 1.5,
        'Bodywork': 1,
        'LadyStyling': 1.5,
        'AtChor': 2,
        'Intensif': 6
    }
}

DF_CH_Prof = pd.DataFrame(Raw_Input)
DF_Cours = pd.DataFrame(Cours)

# Édition du tableau
#edited_profs = st.data_editor(profs, num_rows="dynamic", use_container_width=True)

col1, col2 = st.columns([2,1])

with col1:
    st.header("Entrées")
    edited_profs1 = st.data_editor(Raw_Input, num_rows="dynamic", use_container_width=True)

with col2:
    st.header("Adhésion")
    edited_adhesion = st.data_editor(CF_Adhesion, num_rows="dynamic", use_container_width=False)

st.data_editor(DF_CH_Prof.T)