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

# Custom CSS
st.markdown("""
<style>
    .calculator-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
st.title("💰 FinChat Pro")

# Chat Interface
st.markdown("### AI Financial Assistant")

# Display chat messages
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input - must be outside any container elements
if prompt := st.chat_input("Ask me anything about finance..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        response = call_groq_api(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Chat suggestions
suggestions = [
    "How to start investing?",
    "Explain mutual funds",
    "Best tax-saving options?",
    "Create emergency fund",
    "Retirement planning tips",
    "Compare PPF and FD",
]

# Suggestion buttons in columns
cols = st.columns(3)
for i, suggestion in enumerate(suggestions):
    with cols[i % 3]:
        if st.button(suggestion, key=f"sug_{i}"):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            with st.spinner("Thinking..."):
                response = call_groq_api(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

# Footer
st.markdown("---")
st.markdown("*Note: All calculations are approximate. Please consult a financial advisor for personalized advice.*")
