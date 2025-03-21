import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load environment variables
load_dotenv()
GROQ_API_KEY = "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"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful financial advisor. Provide clear, concise advice about personal finance, investing, and money management."
        }
    ]

# Page config
st.set_page_config(page_title="FinChat Pro", layout="wide")

# Custom CSS for attractive UI
st.markdown("""
<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f9;
        color: #333;
    }
    .stApp {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 8px;
        background: white;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #4CAF50;
        text-align: center;
    }
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 5px solid #4CAF50;
    }
    .reply-area {
        margin-top: 20px;
        display: flex;
        justify-content: space-between;
    }
    .reply-area input {
        flex: 1;
        padding: 10px;
        border: 1px solid #cccccc;
        border-radius: 5px;
    }
    .reply-area button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 15px;
        cursor: pointer;
        margin-left: 10px;
    }
    .reply-area button:hover {
        background-color: #45a049;
    }
    .suggestion-button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        margin: 5px 0;
    }
    .suggestion-button:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

def call_groq_api(messages):
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

# Main UI
st.title("Kshirsa AI")

# Chat Interface
st.markdown("### Personal assistant")

# Display chat messages
for message in st.session_state.messages[1:]:
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input area
col1, col2 = st.columns([4, 1])
with col1:
    prompt = st.text_input("Ask me anything about finance...", key='input_prompt')
with col2:
    if st.button("Send"):
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Thinking..."):
                response = call_groq_api(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.expander("Replay Area").empty()  # Clear the text input area
                st.experimental_rerun()

# Chat suggestions
st.markdown("### Suggestions")
suggestions = [
    "How to start investing?",
    "Explain mutual funds",
    "Best tax-saving options?",
    "Create emergency fund",
    "what is 50-30-20- rule"
    "Retirement planning tips",
    "Compare PPF and FD",
]

# Suggestion buttons
for suggestion in suggestions:
    if st.button(suggestion, key=suggestion):
        st.session_state.messages.append({"role": "user", "content": suggestion})
        with st.spinner("Thinking..."):
            response = call_groq_api(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("*Note: Trying to make your persoonal finance journey smooth*")
