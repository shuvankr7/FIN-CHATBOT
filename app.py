import streamlit as st
import requests
import json
import uuid
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Debug info
print(f"Python version: {sys.version}", flush=True)
print(f"GROQ API KEY status: {'Available' if GROQ_API_KEY else 'Missing'}", flush=True)
print(f"Current working directory: {os.getcwd()}", flush=True)

# Page configuration
st.set_page_config(
    page_title="FinChat - AI Financial Assistant",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .reportview-container {
        background-color: #f5f7f9;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #f0f2f5;
    }
    .chat-message.assistant {
        background-color: #ffffff;
        border: 1px solid #e0e3e8;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        flex-grow: 1;
    }
    .stTextInput>div>div>input {
        border-radius: 0.5rem;
    }
    .stButton>button {
        border-radius: 0.5rem;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    h1 {
        color: #1E3A8A;
        font-size: 2rem;
        margin-bottom: 2rem;
    }
    .header-container {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .header-container .logo {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
    .disclaimer {
        font-size: 0.8rem;
        color: #6c757d;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def call_groq_api(messages):
    """Call the GROQ API with the chat history."""
    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}"
            },
            json={
                "model": "llama3-70b-8192",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024,
            },
            timeout=30  # 30 second timeout
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling GROQ API: {str(e)}")
        return "I'm sorry, I couldn't process your request at the moment. Please try again later."

def get_avatar(role):
    """Return the appropriate avatar based on the message role."""
    if role == "assistant":
        return "💰"  # Finance icon for assistant
    else:
        return "👤"  # User icon for user messages

def display_message(message, role):
    """Display a chat message with appropriate styling."""
    with st.container():
        st.markdown(f"""
        <div class="chat-message {role}">
            <div class="avatar">{get_avatar(role)}</div>
            <div class="message">{message}</div>
        </div>
        """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize the session state variables if they don't exist."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """You are FinChat, a specialized AI assistant focused exclusively on personal finance topics.
Your expertise includes:
- Money management and budgeting
- Investment strategies and financial planning
- Tax information and advice
- Finance news and market trends
- Credit, debt management, and loans
- Retirement planning
- Insurance

Guidelines:
1. Provide accurate, helpful information on financial topics.
2. If asked about non-financial topics, politely redirect the conversation to finance.
3. Use clear, concise language that is easy to understand.
4. When appropriate, structure your responses with bullet points for readability.
5. Always disclose that your advice is informational only and not professional financial advice.
6. Stay current with general financial concepts.
7. For very specific tax or investment questions, recommend consulting with a certified professional."""
            }
        ]
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def main():
    # Initialize session state
    initialize_session_state()
    
    # Display header
    st.markdown("""
    <div class="header-container">
        <div class="logo">💰</div>
        <h1>FinChat: Your AI Financial Assistant</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Display a brief description
    st.markdown("""
    Ask me anything about personal finance, investing, budgeting, taxes, or financial news!
    """)
    
    # Display chat history
    for message in st.session_state.chat_history:
        display_message(message["content"], message["role"])
    
    # Display welcome message if no chat history
    if not st.session_state.chat_history:
        display_message(
            "Hello! I'm your FinChat assistant. I can help with personal finance questions, money management, taxes, and finance news. What would you like to know about today?", 
            "assistant"
        )
    
    # User input area
    with st.container():
        user_input = st.text_input("Your question:", key="user_input", placeholder="Ask about finance, taxes, or money management...")
        send_button = st.button("Send")
    
    if send_button and user_input:
        # Display user message
        display_message(user_input, "user")
        
        # Add user message to session state
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show a spinner while waiting for the API response
        with st.spinner("Thinking..."):
            # Call GROQ API to get response
            assistant_response = call_groq_api(st.session_state.messages)
            
            # Add assistant response to session state
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
        
        # Display assistant response
        display_message(assistant_response, "assistant")
        
        # Clear the input box
        st.session_state.user_input = ""
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        <strong>Disclaimer:</strong> FinChat provides general information for educational purposes only. 
        Always consult with a qualified financial professional before making important financial decisions.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
