import streamlit as st
from services import be4fe_service

def login_page():
    st.title("Ataxia Questionaire Physician Portal")


    # Display the logos
    col1, col2 = st.columns(2)
    col1.image("../logos/JH.png", use_column_width=True, caption="Ataxia Center for Excellence")
    col2.image("../logos/ID.png", use_column_width=True, caption="Insight Diagnostics")
    with st.sidebar:
        st.header("Physician Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            valid_user = be4fe_service.login_basic_auth(username,password)
            if valid_user:
                st.session_state["logged_in"] = True
                st.session_state["creds"] = {
                    "username":username,
                    "password":password
                }
                st.sidebar.empty()
                
                st.rerun()
