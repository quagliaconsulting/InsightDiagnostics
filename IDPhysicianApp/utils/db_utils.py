from pymongo import MongoClient
import streamlit as st
import os

def get_mongo_db():
    if 'mongo_db' not in st.session_state:
        connStr = os.getenv('MONGO_CONNECTION_URL')
        client = MongoClient(connStr)
        db = client['patientsort']
        st.session_state['mongo_db'] = db
    return st.session_state['mongo_db']
