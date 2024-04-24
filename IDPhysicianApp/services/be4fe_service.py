import os
import requests
from requests.auth import HTTPBasicAuth
import streamlit as st
from utils.debug_logging import debug_log

host = os.getenv('BACKEND_HOST_ADDRESS')

def login_basic_auth(username,password):
    response = requests.get(f"{host}/v1/valid_users", auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        return True
    return False

def search_for_responses(search_term):
    if st.button("Search"):
        try:
            username = st.session_state["creds"]["username"]
            password = st.session_state["creds"]["password"]
            query_params = {"search_term":search_term}
            response = requests.get(f"{host}/v1/questionnaires/responses",
                                    params=query_params,
                                    auth=HTTPBasicAuth(username, password))
            return response.json()
        except Exception as e:
            print(e)
            return []