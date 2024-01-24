import streamlit as st
import numpy as np
import plotly.graph_objects as go
import json
import os
import pdb
from datetime import datetime as dt
import requests
from common.service.questionnaire_service import QuestionnaireService

# pdb.set_trace()  # Debugger will activate here

write_to_cloud = False
#questionnaire_host = 'https://patientsort.azurewebsites.net'
questionnaire_host = 'http://localhost:5000'
questionnaireService = QuestionnaireService(questionnaire_host)

# Define the grouped questions

def main():
    # Initialize session state variables if they don't exist
    if 'responses' not in st.session_state:
        st.session_state.responses = []

    if 'page' not in st.session_state:
        st.session_state.page = "questions"

    if st.session_state.page == "questions":
        display_questions()
    elif st.session_state.page == "user_details":
        display_user_details()
    elif st.session_state.page == "summary":
        display_summary()

def display_questions():
    st.title("Ataxia Questionaire")

    # Display the logos
    col1, col2 = st.columns(2)
    col1.image("logos/JH.png", use_column_width=True, caption="Ataxia Center for Excellence")
    col2.image("logos/ID.png", use_column_width=True, caption="Insight Diagnostics")

    query_params = st.experimental_get_query_params()
    questionnaire_id = query_params.get("questionnaire_id")[0]
    version = query_params.get("version")[0]

    try:
        grouped_questions = questionnaireService.get_grouped_questions(questionnaire_id,version)
    except requests.RequestException as e:
        st.error(f'Error getting questions - {e}')
        return
    
    # Collect responses
    for group, questions in grouped_questions.items():
        st.subheader(group)
        for q in questions:
            question_prompt = q['prompt']
            st.session_state.responses.append( {
                'response': str(getResponse(q)),
                'responseType': q['responseType'],
                'prompt': question_prompt
            } )

    st.session_state.mrn = st.text_input("JH MRN:")

    # Display plots and recommendations
    #display_plots_and_recommendations()

    # Check if user has clicked the "Submit" button
    if st.button("Submit Responses",disabled=(st.session_state.mrn == "")):
        questionnaireService.submit_response(st.session_state.responses,st.session_state.mrn,questionnaire_id,version)
        st.session_state.page = "user_details"
        st.rerun()

def getResponse(question):
    if question['responseType'] == 'range':
        return st.slider(question['prompt'], question['detail']['min'], question['detail']['max'], 0)
    else:
        raise Exception(f"No valid response type for {question}")

def display_user_details():
    # Collect additional user details
    st.title("Please enter your details")
    st.session_state.name = st.text_input("Name:")
    st.session_state.birthday = st.text_input("Birthday:")
    st.session_state.mrn = st.text_input("JH MRN:")

    if st.button("Submit Details"):
        st.session_state.page = "summary"
        st.rerun()

def display_summary():
    st.subheader("Summary")
    st.write(f"Name: {st.session_state.name}")
    st.write(f"Birthday: {st.session_state.birthday}")
    st.write(f"JH MRN: {st.session_state.mrn}")

    # Display the stored recommendation
    st.subheader("Recommendation")
    st.write(f"Based on your responses, we recommend consulting an expert in **{st.session_state.recommended_group}**.")

    st.subheader("Responses")
    for question, response in st.session_state.responses.items():
        st.write(f"{question}: {response}")

    st.subheader("Database Upload") 

# ... [your main function]        
   
# def display_plots_and_recommendations():
#     # Calculate group scores for recommendation
#     group_scores = {}
#     for group, questions in grouped_questions.items():
#         valid_responses = [st.session_state.responses[q] for q in questions]
#         group_scores[group] = np.mean(valid_responses)

#     # Define distinct colors for each group
#     colors = [
#         '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
#         '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
#     ]

#     color_map = {group: colors[i] for i, group in enumerate(grouped_questions)}

#     # Prepare data for Plotly clustered bar chart
#     bars_data = []
#     x_labels = []

#     for group, questions in grouped_questions.items():
#         # Flag to show legend only for the first question of each group
#         show_legend = True
#         for q in questions:
#             x_labels.append(q)
#             bars_data.append(
#                 go.Bar(
#                     name=group,
#                     x=[q],
#                     y=[st.session_state.responses[q]],
#                     width=[0.15],  # this controls the width of each bar
#                     marker_color=color_map[group],  # set color based on group
#                     legendgroup=group,  # group bars by their group in the legend
#                     showlegend=show_legend  # show legend only for the first question of each group
#                 )
#             )
#             show_legend = False

#     # Create the Plotly figure
#     fig = go.Figure(data=bars_data)

#     # Update layout for better visualization
#     fig.update_layout(
#         barmode='group',
#         title="Survey Results",
#         xaxis_title="Questions",
#         xaxis={'tickvals': list(range(len(x_labels))), 'ticktext': x_labels, 'tickangle': -45},
#         yaxis_title="Score",
#         yaxis=dict(tickvals=list(range(6)), ticktext=[str(i) for i in range(6)]),
#         legend_title="Groups",
#         width=1200,  # Set the width of the graph
#         height=1000,   # Set the height of the graph
#         margin=dict(l=0, r=50, b=150, t=50)  # Adjust left, right, bottom, and top margins as needed
#     )

#     # Provide recommendation
#     st.session_state.recommended_group = max(group_scores, key=group_scores.get)
#     st.subheader("Recommendation")
#     st.write(f"Based on your responses, we recommend consulting an expert in **{st.session_state.recommended_group}**.")

#     # Display the Plotly chart in Streamlit
#     st.plotly_chart(fig)

if __name__ == "__main__":
    main()
