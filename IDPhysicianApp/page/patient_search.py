import streamlit as st
from services import be4fe_service
from datetime import datetime
import page.components.notes as notes
import page.components.patient_surveys as patient_surveys

def patient_search():
    st.title("Ataxia Questionnaire Patient Entry Dashboard")
    search_term = st.text_input("Enter MRN to search")
    if search_term:
        
        # Save the search term to session state
        print(f"Search term {search_term}")
        if st.button("Search") and ( 'search_term' not in st.session_state or st.session_state.search_term != search_term):
            st.session_state.search_term = search_term
            responses = be4fe_service.search_for_responses(search_term)
            st.session_state.responses = responses

        if 'responses' in st.session_state:
            ################
            notes.create_note()
            #################
            st.write("Patient Surveys")
            patient_surveys.display_serveys()

        else:
            st.write("No responses found.")
    else:
        st.write("Please enter a search term.")