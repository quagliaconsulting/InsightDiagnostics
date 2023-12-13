import streamlit as st
import time
from openai import OpenAI

client = OpenAI(api_key='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')
assistantid = 'asst_2W47RoXSEQhyk2jc4mDq7Wqg'

# Streamlit UI
st.title('Perfect Patient Pathway Bot')
# Display the logos
col1, col2 = st.columns(2)
col1.image("logos/JH.png", use_column_width=True, caption="Ataxia Center for Excellence")
col2.image("logos/ID.png", use_column_width=True, caption="Insight Diagnostics")

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Function to interact with OpenAI
def ask_gpt(question):
    try:
        if "thread" not in st.session_state: 
            # Create a new thread with initial message
            thread = client.beta.threads.create(
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            st.session_state["thread"]=thread
        else:
            thread=st.session_state["thread"]
        
        thread_id = thread.id

        # Run the thread with your assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistantid
            
        )

        # Polling for Run status updates
        while True:
            run_update = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_update.status not in ["queued", "in_progress"]:
                break
            time.sleep(0.5)  # Adding a short delay to reduce API calls

        # Retrieve and return the messages after run completion
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        
        return messages

    except Exception as e:
        st.error(f"An error occurred: {e}")


# User input with conditional prompt
if not st.session_state.submitted:
    user_input = st.text_input("Chat with us to get your medical path perfected! What brings you in today?")
else:
    # Display conversation history using st.markdown
    st.header("Conversation History:")
    for msg in st.session_state.history:
        st.markdown(msg)

    user_input = st.text_input(" ")

    

# Invoke the function and handle submission
if st.button("Submit"):
    st.session_state.submitted = True  # Update the submitted state
    response = ask_gpt(user_input)
    if response:
        for message in response.data:
            if message.role == "assistant":
                # Update conversation history
                st.session_state.history.append("You: " + user_input)
                st.session_state.history.append("Perfect Patient Pathway Bot: " + message.content[0].text.value)

                # Clear input box by resetting the session state variable
                st.session_state.user_input = " "
                st.rerun()