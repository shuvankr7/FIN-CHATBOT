import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px
import numpy as np

# Load environment variables
load_dotenv()
GROQ_API_KEY = "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"

# Page config
st.set_page_config(page_title="FinChat Pro", layout="wide")

# Basic styling
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .calculator-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
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

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful financial advisor. Provide clear, concise advice about personal finance, investing, and money management."
        }
    ]

# Tabs for different sections
tab1, tab2 = st.tabs(["💬 Chat", "🧮 Financial Calculators"])

with tab1:
    st.title("💰 FinChat Pro")
    
    # Display chat messages
    for message in st.session_state.messages[1:]:
        with st.container():
            st.markdown(f"""<div class="chat-message {message['role']}">
                {message['content']}
            </div>""", unsafe_allow_html=True)

    # Chat input
    user_input = st.text_input("Your question:")
    if st.button("Send") and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = call_groq_api(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with tab2:
    st.title("Financial Calculators")
    
    # Add calculators
    calculators = {
        "Inflation Impact Calculator": lambda principal, rate, time: principal * (1 + rate / 100) ** time,
        "Child Education Planning Calculator": lambda current_cost, inflation_rate, years: current_cost * (1 + inflation_rate / 100) ** years,
        "Compound Interest Calculator": lambda principal, rate, time, frequency: principal * (1 + rate / 100 / frequency) ** (frequency * time),
        "ULIP Calculator": lambda premium, term, rate: premium * (1 + rate / 100) ** term,
        "Recurring Deposit (RD) Calculator": lambda monthly_deposit, rate, time: monthly_deposit * (1 + rate / 100) ** time,
        "Fixed Deposit (FD) Calculator": lambda principal, rate, time: principal * (1 + rate / 100) ** time,
        "NPS Calculator": lambda contribution, years: contribution * (1 + 0.1) ** years,
        "EPF Calculator": lambda contribution, years: contribution * (1 + 0.08) ** years,
        "PPF Calculator": lambda contribution, years: contribution * (1 + 0.07) ** years,
        "Goal-Based Investment Calculator": lambda goal, rate, years: goal / ((1 + rate / 100) ** years),
        "SWP (Systematic Withdrawal Plan) Calculator": lambda total_amount, withdrawal: total_amount - withdrawal,
        "Lumpsum Mutual Fund Calculator": lambda investment, rate, years: investment * (1 + rate / 100) ** years,
        "SIP Calculator": lambda monthly_investment, rate, time: monthly_investment * ((1 + rate / 100) ** time),
        "EMI Calculator": lambda principal, rate, time: (principal * (rate / 12 / 100) * (1 + rate / 12 / 100) ** (time * 12)) / ((1 + rate / 12 / 100) ** (time * 12) - 1),
        "Loan Prepayment Calculator": lambda principal, prepayment: principal - prepayment,
        "Loan Tenure Calculator": lambda emi, principal, rate: (principal * (rate / 12 / 100) / emi) / (1 - (1 + rate / 12 / 100) ** -12),
    }

    for name, calculation_function in calculators.items():
        with st.container():
            st.markdown("<div class='calculator-card'>", unsafe_allow_html=True)
            st.subheader(name)
            if name == "Inflation Impact Calculator":
                principal = st.number_input("Principal Amount ($)", min_value=0, value=10000)
                rate = st.number_input("Inflation Rate (%)", min_value=0.0, value=2.0)
                time = st.number_input("Time Period (Years)", min_value=0, value=5)
                if st.button("Calculate Impact"):
                    result = calculation_function(principal, rate, time)
                    st.success(f"Adjusted Value: ${result:,.2f}")
            # (Repeat similar input and button logic for other calculators)
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("*Note: This is for educational purposes only. Consult a professional for financial advice.*")
