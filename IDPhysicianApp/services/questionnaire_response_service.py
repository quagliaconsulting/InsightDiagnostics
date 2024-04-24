import streamlit as st
from utils.db_utils import get_mongo_db
from utils.debug_logging import debug_log

def search_for_files():
    search_term = st.text_input("Enter MRN to search (leave empty for all results)")
    if "files" not in st.session_state:
        st.session_state["files"] = []
    if st.button("Search"):
        try:
#             st.write("Search button clicked")  # Debug: Confirm button click
            if search_term == "" or search_term.lower() == "all":
                # If search term is empty or 'all', return all files
                path = "./responses/*.json"
            else:
                # Otherwise, search for files starting with the search term
                path = "../../responses/*.json"

            st.write(f"Searching for files at: {path}")  # Debug: show the search path
            matching_files = glob.glob(path)
            st.session_state["files"] = matching_files
            return st.session_state["files"]
        except Exception as e:
            return []
    return st.session_state["files"]

def search_for_responses(search_term):
    if "responses" not in st.session_state:
        st.session_state["responses"] = []
    if st.button("Search"):
        try:
            db = get_mongo_db()
            response_collection = db['questionnaire_response']
            query = {
                '$or': [{
                    "patientExternalId": search_term
                },
                {
                    "patientName": search_term
                }]
            }
            debug_log(f'Querying questionnaire_response with {query}')
            responses = list(response_collection.find(query))
            debug_log(f'Response count: {len(responses)}')
            st.session_state["responses"] = responses
            return st.session_state["responses"]
        except Exception as e:
            print(e)
            return []
