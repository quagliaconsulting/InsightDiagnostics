import streamlit as st
import numpy as np
import plotly.graph_objects as go
import json
import os
from pymongo import MongoClient
import pdb
from datetime import datetime as dt
# pdb.set_trace()  # Debugger will activate here

write_to_cloud = True

connStr = os.getenv('MONGO_CONNECTION_URL')
# Define the grouped questions

questions = [
    {
        "prompt": "Over the last two weeks how often have you been bothered by the following problems?",
        "instruction": "0- Not at all, 1 -Several days, 2- More than half the days, 3 - Nearly every day, 4 - Frequently, 5 - Very Frequently",
        "group": "Psychiatric Symptoms",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "Feeling nervous, anxious, or on edge?",
        "instruction": "0- Not at all, 1 -Several days, 2- More than half the days, 3 - Nearly every day, 4 - Frequently, 5 - Very Frequently",
        "group": "Psychiatric Symptoms",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "Little interest or pleasure in doing things?",
        "instruction": "0- Not at all, 1 -Several days, 2- More than half the days, 3 - Nearly every day, 4 - Frequently, 5 - Very Frequently",
        "group": "Psychiatric Symptoms",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "Feeling down, depressed or hopeless?",
        "instruction": "0- Not at all, 1 -Several days, 2- More than half the days, 3 - Nearly every day, 4 - Frequently, 5 - Very Frequently",
        "group": "Psychiatric Symptoms",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "I have quick changes in my emotions",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Psychiatric Symptoms",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "I have trouble with my thinking or memory that does not include difficulty finding names of people or places.",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Cognition",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "I have double vision (seeing 2 of things or an object and its shadow).",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Vision",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "I see the room/world shake sometimes (like the shaking of a camera on film).",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Vision",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "Other people ask me to repeat myself when I am talking because my speech is slurred or soft.",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Speech/Swallow",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "I have trouble swallowing or frequently choke or cough when eating or drinking.",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Speech/Swallow",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "I get lightheaded or feel like I will pass out if I stand up quickly from laying or sitting or bending over to standing",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Autonomic",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "I have erectile dysfunction. (0 for not applicable)",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Autonomic",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "My hands are clumsy sometimes.",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Fine Motor",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "Typing, texting, or other fine motor tasks are more difficult than they used to be. ",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Fine Motor",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "I have constipation, act out my dreams, or my sense of smell or taste has decreased or gone away.  ",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Additional neurologic signs",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "I have muscle stiffness or muscle cramps",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Additional neurologic signs",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "I have trouble walking.",
        "instruction": "For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true. ",
        "group": "Balance",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "When I go down a long hall, I most commonly use this for extra support",
        "instruction": "0 - Nothing, 1 - Wall Occasionally, 2 - Cane, 3 - Walker, 4 - Wheelchair, 5 - I do not go anywhere without people helping me",
        "group": "Balance",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "I have fallen this many times over the last 3 months",
        "instruction": "0 - None, 1 - One to Two, 2 - Three to Six, 3 - Six to Ten, 4 - Ten to Fifteen, 5 - Fifteen+",
        "group": "Balance",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "Over the last 4 weeks, how difficult have these problems made it for you to do your work, take care of things at home, or interact with other people?",
        "instruction": " 0 - no difficulty to 5 - extremely difficult",
        "group": "General Question",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "What is the most difficult symptom?",
        "instruction": "0 - Gait/walking, 1 - Controlling Hands, 2 - Speech, 3 - Vision, 4 - Dizziness, 5 - Other",
        "group": "General Question",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
    {
        "prompt": "How satisfied are you with your clinical care at the JHU Ataxia Center?",
        "instruction": "0 - not satisfied 5 - extremely satisfied",
        "group": "General Question",
        "type":"slider",
        "config": {
            "min":0,
            "max":5,
            "value": 2
        }
    },
]

questionnare = {
    "questions":questions,
    "name": "Ataxia Questionnaire",
    "version": 1
}


client = MongoClient(connStr)

# Access database named 'mydatabase'
db = client['patientsort']
# Access collection named 'mycollection' in the database
collection = db['questionnaire']

collection.insert_one(questionnare)


grouped_questions = {
    'Psychiatric Symptoms': [
        'Over the last two weeks how often have you been bothered by the following problems?',
        'Feeling nervous, anxious, or on edge?',
        'Not being able to stop or control worrying?',
        'Do you find yourself feeling down, depressed, or hopeless?',
        'I have frequent and quick changes in my emotions.',
        "I have thoughts of suicide."
    ],
    'Cognition': [
        'I have difficulty findings words, more than other people my age.',
        'I have trouble with my memory.',
        'I am forgetful.',
        'I have trouble multitasking or doing many things at once.'
    ],
    'Vision': [
        'I have changes in my vision.',
        'I have double vision (seeing 2 of things or an object and its shadow).',
        'I see the room/world shake sometimes (like the shaking of a camera on film).',
        'I have trouble focusing on near objects (blur or a feeling your eyes do not focus)?',
        'I have trouble focusing on far objects (blur or a feeling your eyes do not focus)?'
    ],
    'Speech/Swallow': [
        'I have slurred speech (drunk speech).',
        'Other people ask me to repeat myself.',
        'I have trouble swallowing or frequently choke or cough when eating or drinking.',
        'I have quiet speech (hypophonia).'
    ],
    'Balance': [
        'I get lightheaded when I go from lying, sitting, or bending over to standing.',
        'I feel like the world is moving or spinning around me (vertigo).',
        'I have trouble walking or have changed the way I walk.',
        'When I go down a long hall, I most commonly use this for extra support: 0 - Nothing, 1 - Wall Occasionally, 2 - Cane, 3 - Walker, 4 - Wheelchair, 5 - Cannot Perform Autonomously ',
        'I have fallen this many times over the last 3 months: 0 - None, 1 - One to Two, 2 - Three to Six, 3 - Six to Ten, 4 - Ten to Fifteen, 5 - Fifteen+'
    ],
    'Autonomics': [
        'I get lightheaded or feel like I will pass out if I stand up quickly from laying or sitting.',
        'I have erectile dysfunction. (0 for not applicable)'
    ],
    'Fine Motor': [
        'My handwriting has changed.',
        'My hands are clumsy sometimes.',
        'I have difficulty with typing or texting.'
    ],
    'General Neurology': [
        'I have lost my sense of smell or taste or they have changed.',
        'I have constipation.',
        'I act out my dreams.',
        'I have muscle stiffness.',
        'I have painful muscle cramps.'
    ]    
}

def main():
    # Initialize session state variables if they don't exist
    if 'responses' not in st.session_state:
        st.session_state.responses = {}

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

    # Collect responses
    for group, questions in grouped_questions.items():
        #st.subheader("For each statement below, please rate it 0-5 with 0 being never and 5 being almost always true.")
        st.subheader(group)
        for q in questions:
            st.session_state.responses[q] = st.slider(q, 0, 5, 2)  # Default value set to 2 (Middle value)

    # Display plots and recommendations
    display_plots_and_recommendations()

    # Check if user has clicked the "Submit" button
    if st.button("Submit Responses"):
        st.session_state.page = "user_details"
        st.rerun()

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
    jsonData = getJsonData()
    # save_data_to_json(jsonData)  # Save data to a JSON file
    upload_to_azure(jsonData)    # Placeholder for Azure upload    

def getJsonData():
    grouped_responses = {group: [] for group in grouped_questions}
    for question, response in st.session_state.responses.items():
        for group, questions in grouped_questions.items():
            if question in questions:
                question_response_object = {
                   'question': question,
                   'response': response
                }
                if group in grouped_responses:
                    grouped_responses[group].append(question_response_object)
                else:
                    grouped_responses[group] = [question_response_object]

    # Organize data into a dictionary with grouped responses
    timestamp = dt.now()
    data = {
        'name': st.session_state.name,
        'birthday': st.session_state.birthday,
        'mrn': st.session_state.mrn,
        'grouped_responses': grouped_responses,  # Updated part
        'recommended_group': st.session_state.recommended_group,
        'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%S')
    }


    # Convert the dictionary to a JSON string
    # return json.dumps(data, indent=4)
    return data

def save_data_to_json():
    # Organize data into a dictionary

    # Reorganize responses by their group
    

    # Define the path where the JSON file will be saved
    save_path = os.getcwd() + f"/responses/{st.session_state.mrn}_{timestamp.strftime('%Y%m%d%H%M%S')}.json"
    # Write the JSON string to a file
    with open(save_path, 'w') as json_file:
        json_file.write(json_str)

    st.write(f"Data has been saved to a JSON file at {save_path}.")        

def upload_to_azure(data):
    # Placeholder for Azure upload
    st.write("Uploading to Azure... (not placeholder)")

    if write_to_cloud:

        # Connect to MongoDB running on the default host and port
        client = MongoClient(connStr)

        # Access database named 'mydatabase'
        db = client['patientsort']
        # Access collection named 'mycollection' in the database
        collection = db['questionnaire_response']

        collection.insert_one(data)
    

# ... [your main function]        
   
def display_plots_and_recommendations():
    # Calculate group scores for recommendation
    group_scores = {}
    for group, questions in grouped_questions.items():
        valid_responses = [st.session_state.responses[q] for q in questions]
        group_scores[group] = np.mean(valid_responses)

    # Define distinct colors for each group
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]

    color_map = {group: colors[i] for i, group in enumerate(grouped_questions)}

    # Prepare data for Plotly clustered bar chart
    bars_data = []
    x_labels = []

    for group, questions in grouped_questions.items():
        # Flag to show legend only for the first question of each group
        show_legend = True
        for q in questions:
            x_labels.append(q)
            bars_data.append(
                go.Bar(
                    name=group,
                    x=[q],
                    y=[st.session_state.responses[q]],
                    width=[0.15],  # this controls the width of each bar
                    marker_color=color_map[group],  # set color based on group
                    legendgroup=group,  # group bars by their group in the legend
                    showlegend=show_legend  # show legend only for the first question of each group
                )
            )
            show_legend = False

    # Create the Plotly figure
    fig = go.Figure(data=bars_data)

    # Update layout for better visualization
    fig.update_layout(
        barmode='group',
        title="Survey Results",
        xaxis_title="Questions",
        xaxis={'tickvals': list(range(len(x_labels))), 'ticktext': x_labels, 'tickangle': -45},
        yaxis_title="Score",
        yaxis=dict(tickvals=list(range(6)), ticktext=[str(i) for i in range(6)]),
        legend_title="Groups",
        width=1200,  # Set the width of the graph
        height=1000,   # Set the height of the graph
        margin=dict(l=0, r=50, b=150, t=50)  # Adjust left, right, bottom, and top margins as needed
    )

    # Provide recommendation
    st.session_state.recommended_group = max(group_scores, key=group_scores.get)
    st.subheader("Recommendation")
    st.write(f"Based on your responses, we recommend consulting an expert in **{st.session_state.recommended_group}**.")

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()