import streamlit as st
from openai import OpenAI

# Page configuration for a premium feel
st.set_page_config(
    page_title="Simple AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for rich aesthetics (sleek dark gradients and beautiful typography)
st.markdown("""
    <style>
    /* Gradient headers */
    h1 {
        background: linear-gradient(90deg, #FF4B4B, #FF8F8F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
    }
    
    /* Clean sidebar styling */
    .css-1d391kg {
        background-color: #11151c;
    }
    
    /* Hover effects on buttons */
    .stButton>button:hover {
        border-color: #FF4B4B;
        color: #FF4B4B;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Simple AI Chatbot")
st.write("Welcome! This is a simple, real-time chatbot built using Streamlit and OpenAI.")

# Sidebar for configuration and API key
st.sidebar.title("Configuration")

# Try loading API Key from Streamlit secrets or session state
api_key = ""
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
elif "OPENAI_API_KEY" in st.session_state:
    api_key = st.session_state["OPENAI_API_KEY"]

# Check if OpenAI API Key is in secrets or environment, otherwise prompt user
api_key_input = st.sidebar.text_input(
    "OpenAI API Key", 
    value=api_key,
    type="password", 
    placeholder="sk-...", 
    help="Provide your OpenAI API key to start chatting."
)

if api_key_input:
    api_key = api_key_input
    st.session_state["OPENAI_API_KEY"] = api_key_input

if not api_key:
    st.info("👈 Please enter your OpenAI API key in the sidebar to begin chatting.")
    st.stop()

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add a button to clear the chat conversation
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Stream the response from OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    # Add a blinking cursor effect during streaming
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error communicating with OpenAI: {e}")
            full_response = "Sorry, I encountered an error. Please verify your API key and try again."
            message_placeholder.markdown(full_response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
