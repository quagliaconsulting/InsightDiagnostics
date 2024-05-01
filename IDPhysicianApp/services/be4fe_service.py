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
    # moving the st.button up to the calling method makes the button appear twice
    # this work should be done but we need to resolve that issue. keeping hear for
    # sake of time
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
        
def get_note_templates():
    try:
        username = st.session_state["creds"]["username"]
        password = st.session_state["creds"]["password"]
        response = requests.get(f"{host}/v1/notes/templates",
                                auth=HTTPBasicAuth(username,password))
        return response.json()
    except Exception as e:
        print(e)
        return []
        
def create_note(note):
    try:
        username = st.session_state["creds"]["username"]
        password = st.session_state["creds"]["password"]
        debug_log(f"Creating note {note}")
        response = requests.post(f"{host}/v1/notes",
                                 headers={"Content-Type":"application/json"},
                                 json=note,
                                 auth=HTTPBasicAuth(username,password))
        return response.json()
    except Exception as e:
        print(e)
        return None