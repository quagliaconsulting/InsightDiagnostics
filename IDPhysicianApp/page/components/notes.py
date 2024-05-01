import streamlit as st
import services.be4fe_service as be4fe_service

def create_note():
    if 'note_templates' not in st.session_state:
        st.session_state.note_templates = be4fe_service.get_note_templates()

    note_templates = st.session_state.note_templates
    template_dict = {template['_id']: template['name'] for template in note_templates}

    # Create a dropdown menu where the display values are template names, but we work with IDs
    selected_template_id = st.selectbox('Select a Template:', list(template_dict.keys()), format_func=lambda x: template_dict[x])
    note = st.text_input("Paste note here")
    if note:
        create_note_request = {
            "note":note,
            "templateId":selected_template_id
        }
        be4fe_service.create_note(create_note_request)