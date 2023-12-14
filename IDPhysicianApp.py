import streamlit as st
import glob
import json
import pandas as pd
import plotly.express as px
from streamlit import cache


# Dummy login page
def login_page():
    st.title("Ataxia Questionaire Physician Portal")


    # Display the logos
    col1, col2 = st.columns(2)
    col1.image("logos/JH.png", use_column_width=True, caption="Ataxia Center for Excellence")
    col2.image("logos/ID.png", use_column_width=True, caption="Insight Diagnostics")
    with st.sidebar:
        st.header("Physician Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            st.session_state["logged_in"] = True
            st.rerun()

# File search functionality
#@st.cache_data(experimental_allow_widgets=True)
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
                path = "./responses/*.json"

            st.write(f"Searching for files at: {path}")  # Debug: show the search path
            matching_files = glob.glob(path)
            st.session_state["files"] = matching_files
            return st.session_state["files"]
        except Exception as e:
            return []
    return st.session_state["files"]



# Data processing with caching
def process_data(files):
    all_data = []
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            timestamp = pd.to_datetime(data['timestamp'])

            for group, questions in data['grouped_responses'].items():
                for item in questions:
                    if isinstance(item, dict) and 'question' in item and 'response' in item:
                        all_data.append({
                            'timestamp': timestamp,
                            'question_group': group,  # Ensure this key is correctly populated
                            'question': item['question'],
                            'response': item['response']
                        })

    df = pd.DataFrame(all_data)

    # Debug: Print the first few rows of the DataFrame
    print(df.head())

    return df



# Plotting data using Plotly
#@st.cache_data(experimental_allow_widgets=True)
def plot_data(df, selected_groups):
    # Filter data based on selected question groups
    filtered_df = df[df['question_group'].isin(selected_groups)]

    # Calculate the average response score for each question group at each timestamp
    avg_df = filtered_df.groupby(['timestamp', 'question_group'])['response'].mean().reset_index()

    # Plotting line graph
    fig = px.line(
        avg_df, x='timestamp', y='response', color='question_group', markers=True,
        labels={'response': 'Average Response Score', 'timestamp': 'Date', 'question_group': 'Question Group'},
    )

    fig.update_layout(title='Average Patient Responses Over Time', xaxis_title='Date', yaxis_title='Average Response Score')

    # Set the size of the figure (width, height)
    fig.update_layout(width=2000, height=1000)  # Adjust these values as needed

    st.plotly_chart(fig, use_container_width=True)



# Display filtering options
def display_filter_options(df):
    # Debug: Print the DataFrame columns
    print("DataFrame columns:", df.columns)

    question_groups = df['question_group'].unique().tolist()
    st.session_state.filter_options = question_groups
    selected_groups = st.multiselect("Select Question Groups to Display", st.session_state.filter_options, default=question_groups)
   
    return selected_groups


def main():
    # Initialize session state variable for login status
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
    else:
        st.sidebar.empty()  # Optionally clear the sidebar
        st.title("Ataxia Questionnaire Patient Entry Dashboard")
        files = search_for_files()
        if files:
            data_df = process_data(files)
            selected_groups = display_filter_options(data_df)
            if selected_groups:
                plot_data(data_df, selected_groups)

if __name__ == "__main__":
    main()
