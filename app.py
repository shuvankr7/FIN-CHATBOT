import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GROQ_API_KEY = "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"

# Page config
st.set_page_config(page_title="Simple FinChat", layout="centered")

# Basic styling
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        background-color: #f0f2f6;
    }
    .chat-message.assistant {
        background-color: #e0f0ff;
    }
</style>
""", unsafe_allow_html=True)

def call_groq_api(messages):
    """Call the GROQ API with the chat history."""
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
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
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful financial advisor. Provide clear, concise advice about personal finance, investing, and money management."
        }
    ]

# Main interface
st.title("💰 Simple FinChat")
st.markdown("Ask me anything about personal finance!")

# Display chat messages
for message in st.session_state.messages[1:]:  # Skip system message
    with st.container():
        st.markdown(f"""<div class="chat-message {message['role']}">
            {message['content']}
        </div>""", unsafe_allow_html=True)

# Chat input
user_input = st.text_input("Your question:", key="user_input")

if st.button("Send") and user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    with st.spinner("Thinking..."):
        response = call_groq_api(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Rerun to update chat display
    st.rerun()

# Simple footer
st.markdown("---")
st.markdown("*Note: This is for educational purposes only. Consult a professional for financial advice.*")
