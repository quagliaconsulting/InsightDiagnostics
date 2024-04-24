import streamlit as st
import glob
import json
import os
import pandas as pd
import plotly.express as px
from page.login import login_page
from page.patient_search import patient_search


def main():
    # Initialize session state variable for login status
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
    else:
        st.sidebar.empty()  # Optionally clear the sidebar
        patient_search()


if __name__ == "__main__":
    main()