import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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

# Calculator Functions
def calculate_sip(monthly_investment, rate, time):
    monthly_rate = rate/(12*100)
    months = time * 12
    future_value = monthly_investment * ((1 + monthly_rate) * ((1 + monthly_rate)**months - 1)/monthly_rate)
    return future_value

def calculate_emi(principal, rate, time):
    r = rate/1200
    n = time * 12
    return (principal * r * (1 + r)**n) / ((1 + r)**n - 1)

def calculate_ppf(yearly_investment, rate=7.1, time=15):
    total_amount = 0
    for i in range(time):
        total_amount += yearly_investment
        total_amount *= (1 + rate/100)
    return total_amount

def calculate_fd(principal, rate, time, frequency=4):
    return principal * (1 + rate/100/frequency)**(frequency*time)

def calculate_rd(monthly_deposit, rate, time):
    quarters = time * 4
    quarterly_rate = rate/400
    amount = monthly_deposit * 3 * (((1 + quarterly_rate)**quarters - 1)/quarterly_rate)
    return amount

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful financial advisor. Provide clear, concise advice about personal finance, investing, and money management."
        }
    ]

# Main UI
st.title("💰 FinChat Pro")
tabs = st.tabs(["💬 Chat", "🧮 Financial Calculators"])

with tabs[0]:
    # Chat Interface
    st.markdown("### AI Financial Assistant")
    
    # Chat suggestions
    suggestions = [
        "How to start investing?",
        "Explain mutual funds",
        "Best tax-saving options?",
        "Create emergency fund",
        "Retirement planning tips",
        "Compare PPF and FD",
    ]
    
    cols = st.columns(3)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(suggestion, key=f"sug_{i}"):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                with st.spinner("Thinking..."):
                    response = call_groq_api(st.session_state.messages)
                    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display chat messages
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask me anything about finance...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = call_groq_api(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

with tabs[1]:
    st.markdown("### Financial Calculators")
    
    calculator = st.selectbox("Choose Calculator", [
        "SIP Calculator",
        "EMI Calculator",
        "PPF Calculator",
        "Fixed Deposit Calculator",
        "Recurring Deposit Calculator",
        "Education Planning Calculator"
    ])
    
    if calculator == "SIP Calculator":
        with st.container():
            st.markdown("#### Systematic Investment Plan (SIP) Calculator")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                monthly_inv = st.number_input("Monthly Investment (₹)", min_value=500, value=5000)
            with col2:
                roi = st.number_input("Expected Return Rate (%)", min_value=1.0, value=12.0)
            with col3:
                years = st.number_input("Investment Period (Years)", min_value=1, value=10)
            
            if st.button("Calculate SIP Returns"):
                future_value = calculate_sip(monthly_inv, roi, years)
                total_investment = monthly_inv * years * 12
                wealth_gained = future_value - total_investment
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Investment", f"₹{total_investment:,.0f}")
                with col2:
                    st.metric("Wealth Gained", f"₹{wealth_gained:,.0f}")
                with col3:
                    st.metric("Future Value", f"₹{future_value:,.0f}")
                
                # Visualization
                years_list = list(range(years + 1))
                investment_value = [monthly_inv * 12 * year for year in years_list]
                future_values = [calculate_sip(monthly_inv, roi, year) for year in years_list]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=years_list, y=investment_value, name="Investment"))
                fig.add_trace(go.Scatter(x=years_list, y=future_values, name="Future Value"))
                fig.update_layout(title="Investment Growth Over Time",
                                xaxis_title="Years",
                                yaxis_title="Value (₹)")
                st.plotly_chart(fig)
    
    elif calculator == "EMI Calculator":
        st.markdown("#### EMI Calculator")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            loan_amount = st.number_input("Loan Amount (₹)", min_value=10000, value=1000000)
        with col2:
            interest_rate = st.number_input("Interest Rate (%)", min_value=1.0, value=8.5)
        with col3:
            tenure = st.number_input("Loan Tenure (Years)", min_value=1, value=20)
        
        if st.button("Calculate EMI"):
            emi = calculate_emi(loan_amount, interest_rate, tenure)
            total_payment = emi * tenure * 12
            total_interest = total_payment - loan_amount
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Monthly EMI", f"₹{emi:,.0f}")
            with col2:
                st.metric("Total Interest", f"₹{total_interest:,.0f}")
            with col3:
                st.metric("Total Payment", f"₹{total_payment:,.0f}")
            
            # Pie chart for loan breakup
            fig = go.Figure(data=[go.Pie(labels=['Principal', 'Interest'],
                                       values=[loan_amount, total_interest])])
            fig.update_layout(title="Loan Amount Breakup")
            st.plotly_chart(fig)
    
    elif calculator == "PPF Calculator":
        st.markdown("#### Public Provident Fund (PPF) Calculator")
        yearly_investment = st.number_input("Yearly Investment (₹)", min_value=500, max_value=150000, value=150000)
        
        if st.button("Calculate PPF Returns"):
            maturity_amount = calculate_ppf(yearly_investment)
            total_investment = yearly_investment * 15
            interest_earned = maturity_amount - total_investment
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Investment", f"₹{total_investment:,.0f}")
            with col2:
                st.metric("Interest Earned", f"₹{interest_earned:,.0f}")
            with col3:
                st.metric("Maturity Amount", f"₹{maturity_amount:,.0f}")
    
    elif calculator == "Fixed Deposit Calculator":
        st.markdown("#### Fixed Deposit Calculator")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            principal = st.number_input("Principal Amount (₹)", min_value=1000, value=100000)
        with col2:
            rate = st.number_input("Interest Rate (%)", min_value=1.0, value=6.0)
        with col3:
            time = st.number_input("Time Period (Years)", min_value=1, value=5)
        
        if st.button("Calculate FD Returns"):
            maturity_amount = calculate_fd(principal, rate, time)
            interest_earned = maturity_amount - principal
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Interest Earned", f"₹{interest_earned:,.2f}")
            with col2:
                st.metric("Maturity Amount", f"₹{maturity_amount:,.2f}")
    
    elif calculator == "Recurring Deposit Calculator":
        st.markdown("#### Recurring Deposit Calculator")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            monthly_deposit = st.number_input("Monthly Deposit (₹)", min_value=500, value=5000)
        with col2:
            rate = st.number_input("Interest Rate (%)", min_value=1.0, value=5.5)
        with col3:
            time = st.number_input("Time Period (Years)", min_value=1, value=3)
        
        if st.button("Calculate RD Returns"):
            maturity_amount = calculate_rd(monthly_deposit, rate, time)
            total_deposit = monthly_deposit * time * 12
            interest_earned = maturity_amount - total_deposit
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Deposit", f"₹{total_deposit:,.2f}")
            with col2:
                st.metric("Interest Earned", f"₹{interest_earned:,.2f}")
            with col3:
                st.metric("Maturity Amount", f"₹{maturity_amount:,.2f}")
    
    elif calculator == "Education Planning Calculator":
        st.markdown("#### Education Planning Calculator")
        col1, col2 = st.columns(2)
        
        with col1:
            current_cost = st.number_input("Current Education Cost (₹)", min_value=100000, value=1000000)
            years_to_goal = st.number_input("Years until Education", min_value=1, value=10)
        with col2:
            inflation_rate = st.number_input("Education Inflation Rate (%)", min_value=1.0, value=10.0)
            expected_return = st.number_input("Expected Return Rate (%)", min_value=1.0, value=12.0)
        
        if st.button("Calculate Education Plan"):
            future_cost = current_cost * (1 + inflation_rate/100)**years_to_goal
            monthly_investment = (future_cost * (expected_return/1200)) / (((1 + expected_return/1200)**(years_to_goal*12)) - 1)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Future Education Cost", f"₹{future_cost:,.0f}")
            with col2:
                st.metric("Required Monthly Investment", f"₹{monthly_investment:,.0f}")

# Footer
st.markdown("---")
st.markdown("*Note: All calculations are approximate. Please consult a financial advisor for personalized advice.*")
