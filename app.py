
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
    .comparison-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
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

def calculate_compound_interest(principal, rate, time, frequency=12):
    return principal * (1 + rate/100/frequency)**(frequency*time)

def calculate_loan_emi(principal, rate, time):
    r = rate/1200  # monthly interest rate
    n = time * 12  # number of months
    return (principal * r * (1 + r)**n) / ((1 + r)**n - 1)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful financial advisor. Provide clear, concise advice about personal finance, investing, and money management."
        }
    ]

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["💬 Chat", "🧮 Calculators", "📊 Investment Comparison"])

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
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='calculator-card'>", unsafe_allow_html=True)
        st.subheader("Investment Calculator")
        principal = st.number_input("Principal Amount ($)", min_value=0, value=10000)
        rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=8.0)
        time = st.number_input("Time Period (Years)", min_value=0, value=5)
        if st.button("Calculate Investment"):
            future_value = calculate_compound_interest(principal, rate, time)
            st.success(f"Future Value: ${future_value:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='calculator-card'>", unsafe_allow_html=True)
        st.subheader("Loan EMI Calculator")
        loan_amount = st.number_input("Loan Amount ($)", min_value=0, value=100000)
        interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=6.0, key="loan_rate")
        loan_term = st.number_input("Loan Term (Years)", min_value=0, value=20, key="loan_term")
        if st.button("Calculate EMI"):
            emi = calculate_loan_emi(loan_amount, interest_rate, loan_term)
            st.success(f"Monthly EMI: ${emi:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.title("Investment Comparison")
    
    # Sample historical returns data
    returns_data = {
        'Year': list(range(2014, 2024)),
        'Stocks': [13.7, 1.4, 12.0, 21.8, -4.4, 31.5, 18.4, 28.7, -18.1, 24.2],
        'Gold': [-1.5, -10.4, 8.5, 13.1, -2.8, 18.3, 24.6, -3.6, -0.3, 13.4],
        'Real Estate': [11.4, 10.8, 6.9, 6.2, 4.8, 5.2, 2.9, 18.4, 14.2, 3.8],
        'Fixed Deposit': [8.5, 7.5, 7.0, 6.5, 6.5, 6.0, 5.5, 5.0, 5.5, 6.0]
    }
    
    df = pd.DataFrame(returns_data)
    
    # Risk-Reward Plot
    fig_risk = px.scatter(
        df,
        x=[df[asset].std() for asset in ['Stocks', 'Gold', 'Real Estate', 'Fixed Deposit']],
        y=[df[asset].mean() for asset in ['Stocks', 'Gold', 'Real Estate', 'Fixed Deposit']],
        text=['Stocks', 'Gold', 'Real Estate', 'Fixed Deposit'],
        title="Risk vs. Return Analysis",
        labels={'x': 'Risk (Standard Deviation)', 'y': 'Average Annual Return (%)'}
    )
    st.plotly_chart(fig_risk)
    
    # Historical Returns Comparison
    fig_returns = px.line(
        df, 
        x='Year',
        y=['Stocks', 'Gold', 'Real Estate', 'Fixed Deposit'],
        title="Historical Returns Comparison",
        labels={'value': 'Annual Return (%)', 'variable': 'Asset Class'}
    )
    st.plotly_chart(fig_returns)

# Footer
st.markdown("---")
st.markdown("*Note: This is for educational purposes only. Consult a professional for financial advice.*")
