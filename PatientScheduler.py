import streamlit as st
import time
from openai import OpenAI


def main():
    # Initialize OpenAI client
    client = OpenAI(api_key='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')
    assistant_id = 'asst_2W47RoXSEQhyk2jc4mDq7Wqg'

    # Streamlit UI setup
    st.title('Perfect Patient Pathway Bot')

    # Display the logos
    col1, col2 = st.columns(2)
    col1.image("logos/JH.png", use_column_width=True, caption="Ataxia Center for Excellence")
    col2.image("logos/ID.png", use_column_width=True, caption="Insight Diagnostics")

    # Initialize session state for conversation history and thread
    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = None

    # Call the function to handle GPT interactions
    ask_gpt(client, assistant_id)

# Define the function to process messages with citations
def process_message(message):
    message_content = message.content[0].text

    # Add footnotes to the end of the message content
    full_response = message_content.value
    return full_response    

# Function to interact with OpenAI
def ask_gpt(client, assistant_id):
    # Initialize the model and messages list if not already in session state
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4-1106-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # Check if thread_id is None or not in the session state
    if st.session_state.thread_id is None:
        # Create a new thread and store its ID in the session state
        thread = client.beta.threads.create()
        #print(thread)
        st.session_state.thread_id = thread.id    

    # Display existing messages in the chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for the user
    if prompt := st.chat_input("What brings you in today?"):

        # Add user message to the state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        #print('Sending to openai')
        # Add the user's message to the existing thread
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )
        #print('created openai thread')
        # Create a run with additional instructions
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id
        )
        #print('ran prompt with openai')
        # Poll for the run to complete and retrieve the assistant's messages
        while run.status != 'completed':
            #print(run.status)
            #print(run.last_error)
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        #print('got message from openai')
        # Retrieve messages added by the assistant
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            full_response = process_message(message)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            with st.chat_message("assistant"):
                st.markdown(full_response, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
