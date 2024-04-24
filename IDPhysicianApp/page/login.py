import streamlit as st
from utils.db_utils import get_mongo_db
from utils.debug_logging import debug_log

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
            query = {
                'username':username,
                'password':password
            }
            db = get_mongo_db()
            user_collection = db['users']
            user = user_collection.find_one(query)
            debug_log(user)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.sidebar.empty()
                
                st.rerun()
