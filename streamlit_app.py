import streamlit as st
from openai import OpenAI

# Get OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

if not openai_api_key:
    st.error("OpenAI API key not found. Please ensure it's set in Streamlit secrets.")
else:
    # Use the key
    client = OpenAI(api_key=openai_api_key)
    st.write("API Key loaded successfully!")

    # Show title and description.
    st.title("💬 Chatbot")
    st.write(
        "This is a simple chatbot that uses OpenAI's GPT-3.5-turbo model to generate responses. "
        "To use this app, the OpenAI API key is automatically loaded by the developer. "
    )

    # Initialize session state variables
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "prompt_count" not in st.session_state:
        st.session_state.prompt_count = 0  # Initialize prompt count

    # Display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Check if user has reached the limit
    if st.session_state.prompt_count >= 5:
        st.warning("You have reached the limit of 5 prompts for this session.")
    else:
        # Allow user to input prompts if limit is not reached
        if prompt := st.chat_input("What is up?"):
            # Increment prompt count
            st.session_state.prompt_count += 1

            # Store and display the current prompt
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate a response using the OpenAI API
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            # Stream the response to the chat
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})