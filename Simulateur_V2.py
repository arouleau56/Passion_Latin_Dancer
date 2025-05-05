import streamlit as st
import pandas as pd

from scripts import Inputs, Budget

st.set_page_config(layout="wide")

def edit_page(page_name):
    if page_name!='Budget page':
        st.markdown(f"# {page_name}")
    st.sidebar.markdown(f"# {page_name}")
    match page_name:
        case "Main Page":
            pass
        case "Inputs page":
            Inputs.main()
        case "Budget page":
            Budget.main()
        case "Définition couts":
            None

page_names = ["Main Page", "Inputs page", "Budget page", "Définition couts"]

st.sidebar.image("Logo.png", width=300)
selected_page = st.sidebar.selectbox("Select a page", page_names)

edit_page(selected_page)