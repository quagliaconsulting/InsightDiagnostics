import streamlit as st
from services import questionnaire_response_service
from datetime import datetime

def patient_search():
    st.title("Ataxia Questionnaire Patient Entry Dashboard")
    search_term = st.text_input("Enter MRN to search")
    if search_term:
        responses = questionnaire_response_service.search_for_responses(search_term)

        if responses:
            for response in responses:
                created_at = response.get("createdAt")
                if created_at:
                    created_at = datetime.fromisoformat(created_at).strftime("%Y-%m-%d %H:%M:%S")
                
                # Questionnaire name and version
                questionnaire_name = response.get("questionnaireName", "Unknown")
                questionnaire_version = str(response.get("questionnaireVersion"))

                # Create the expander tile
                with st.expander(f"{questionnaire_name} - Version: {questionnaire_version} (Submitted: {created_at})"):
                    # Display the patient details
                    st.write(f"Patient Name: {response.get('patientName', 'Unknown')}")
                    st.write(f"Patient External ID: {response.get('patientExternalId', 'Unknown')}")

                    # Display the grouped responses
                    grouped_responses = response.get("grouped_responses", {})
                    for group_name, questions in grouped_responses.items():
                        st.write(f"### {group_name}")
                        for question in questions:
                            st.write(f"- {question['question']}: {question['response']}")

        else:
            st.write("No responses found.")
    else:
        st.write("Please enter a search term.")