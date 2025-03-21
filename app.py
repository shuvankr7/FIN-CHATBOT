# import streamlit as st
# import requests
# import json
# import uuid
# import os
# import sys
# import time
# from datetime import datetime
# from dotenv import load_dotenv
# import pandas as pd
# import altair as alt
# # Page configuration
# st.set_page_config(
#     page_title="FinChat - AI Financial Assistant",
#     page_icon="💰",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items={
#         'Get Help': 'https://github.com/yourusername/finchat',
#         'Report a bug': 'https://github.com/yourusername/finchat/issues',
#         'About': "# FinChat\nYour personal AI financial assistant powered by GROQ."
#     }
# )
# # Load API keys from Streamlit secrets or .env file
# try:
#     # First try to load from Streamlit secrets (for cloud deployment)
#     GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
#     print("Loaded API key from Streamlit secrets")
# except Exception:
#     # Fall back to .env file (for local development)
#     load_dotenv()
#     GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
#     print("Loaded API key from .env file")

# GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# # Debug info
# print(f"Python version: {sys.version}", flush=True)
# print(f"GROQ API KEY status: {'Available' if GROQ_API_KEY else 'Missing'}", flush=True)
# print(f"Current working directory: {os.getcwd()}", flush=True)



# # Custom CSS for better styling
# st.markdown("""
# <style>
#     /* Main layout */
#     .main {
#         background-color: #f8fafc;
#     }
    
#     [data-testid="stSidebar"] {
#         background-color: #1E293B;
#         color: white;
#         border-right: 1px solid #334155;
#     }
    
#     [data-testid="stSidebar"] .sidebar-content {
#         padding: 1rem;
#     }
    
#     /* Containers and blocks */
#     .main .block-container {
#         padding: 1rem;
#         max-width: 1200px;
#         margin: 0 auto;
#     }
    
#     /* Chat interface */
#     .chat-container {
#         background-color: white;
#         border-radius: 1rem;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
#         padding: 1rem;
#         margin-bottom: 1rem;
#         height: 70vh;
#         overflow-y: auto;
#         scrollbar-width: thin;
#     }
    
#     .chat-message {
#         padding: 1rem;
#         border-radius: 0.75rem;
#         margin-bottom: 1rem;
#         display: flex;
#         align-items: flex-start;
#         animation: fadeIn 0.5s;
#     }
    
#     @keyframes fadeIn {
#         0% { opacity: 0; transform: translateY(10px); }
#         100% { opacity: 1; transform: translateY(0); }
#     }
    
#     .chat-message.user {
#         background-color: #f1f5f9;
#         border-bottom-right-radius: 0.25rem;
#         margin-left: 2rem;
#     }
    
#     .chat-message.assistant {
#         background-color: #f0f9ff;
#         border: 1px solid #e0f2fe;
#         border-bottom-left-radius: 0.25rem;
#         margin-right: 2rem;
#     }
    
#     .chat-message .avatar {
#         width: 40px;
#         height: 40px;
#         border-radius: 50%;
#         object-fit: cover;
#         margin-right: 1rem;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 1.5rem;
#     }
    
#     .chat-message .message {
#         flex-grow: 1;
#     }
    
#     /* Input area */
#     .input-area {
#         background-color: white;
#         border-radius: 0.75rem;
#         padding: 1rem;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
#     }
    
#     .stTextInput>div>div>input {
#         border-radius: 0.5rem;
#         border: 1px solid #cbd5e1;
#         padding: 0.75rem;
#         font-size: 1rem;
#     }
    
#     .stButton>button {
#         border-radius: 0.5rem;
#         background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
#         color: white;
#         font-weight: bold;
#         padding: 0.5rem 1.5rem;
#         transition: all 0.3s ease;
#         border: none;
#         box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.5);
#     }
    
#     .stButton>button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.6);
#     }
    
#     /* Text styling */
#     h1 {
#         color: #0f172a;
#         font-size: 2.5rem;
#         font-weight: 800;
#         margin-bottom: 0.5rem;
#         background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }
    
#     h2 {
#         color: #334155;
#         font-size: 1.5rem;
#         font-weight: 600;
#         margin-top: 1.5rem;
#         margin-bottom: 1rem;
#     }
    
#     .subtitle {
#         color: #64748b;
#         font-size: 1.25rem;
#         margin-bottom: 2rem;
#     }
    
#     .header-container {
#         display: flex;
#         align-items: center;
#         margin-bottom: 0.5rem;
#     }
    
#     .header-container .logo {
#         font-size: 3rem;
#         margin-right: 1rem;
#         background: linear-gradient(135deg, #fbbf24 0%, #ea580c 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }
    
#     .disclaimer {
#         font-size: 0.8rem;
#         color: #64748b;
#         margin-top: 1.5rem;
#         padding: 1rem;
#         border-left: 4px solid #cbd5e1;
#         background-color: #f8fafc;
#     }
    
#     /* Feature boxes */
#     .feature-box {
#         background-color: white;
#         border-radius: 0.75rem;
#         padding: 1.5rem;
#         margin-bottom: 1rem;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
#         transition: transform 0.3s ease, box-shadow 0.3s ease;
#     }
    
#     .feature-box:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
#     }
    
#     .feature-icon {
#         font-size: 2rem;
#         margin-bottom: 1rem;
#         background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }
    
#     /* Sidebar custom styles */
#     .sidebar-title {
#         color: white;
#         font-size: 1.25rem;
#         font-weight: 600;
#         margin-bottom: 1rem;
#     }
    
#     .sidebar-subtitle {
#         color: #94a3b8;
#         font-size: 0.9rem;
#         margin-bottom: 1.5rem;
#     }
    
#     /* Tabs and metrics */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 1rem;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         background-color: transparent;
#         border-radius: 0.5rem 0.5rem 0 0;
#         padding: 0.5rem 1rem;
#         color: #64748b;
#     }
    
#     .stTabs [aria-selected="true"] {
#         background-color: white !important;
#         color: #3b82f6 !important;
#         font-weight: 600;
#     }
    
#     /* Loading spinner */
#     .stSpinner > div > div {
#         border-color: #3b82f6 !important;
#     }
    
#     /* Tooltip */
#     .stTooltip {
#         border-color: #cbd5e1;
#     }
# </style>
# """, unsafe_allow_html=True)

# def call_groq_api(messages):
#     """Call the GROQ API with the chat history."""
#     try:
#         response = requests.post(
#             GROQ_API_URL,
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {GROQ_API_KEY}"
#             },
#             json={
#                 "model": "llama3-70b-8192",
#                 "messages": messages,
#                 "temperature": 0.7,
#                 "max_tokens": 1024,
#             },
#             timeout=30  # 30 second timeout
#         )
#         response.raise_for_status()
#         return response.json()["choices"][0]["message"]["content"]
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error calling GROQ API: {str(e)}")
#         return "I'm sorry, I couldn't process your request at the moment. Please try again later."

# def get_avatar(role):
#     """Return the appropriate avatar based on the message role."""
#     if role == "assistant":
#         return "💰"  # Finance icon for assistant
#     else:
#         return "👤"  # User icon for user messages

# def display_message(message, role):
#     """Display a chat message with appropriate styling."""
#     with st.container():
#         st.markdown(f"""
#         <div class="chat-message {role}">
#             <div class="avatar">{get_avatar(role)}</div>
#             <div class="message">{message}</div>
#         </div>
#         """, unsafe_allow_html=True)

# def initialize_session_state():
#     """Initialize the session state variables if they don't exist."""
#     if "session_id" not in st.session_state:
#         st.session_state.session_id = str(uuid.uuid4())
    
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {
#                 "role": "system",
#                 "content": """You are FinChat, a specialized AI assistant focused exclusively on personal finance topics.
# Your expertise includes:
# - Money management and budgeting
# - Investment strategies and financial planning
# - Tax information and advice
# - Finance news and market trends
# - Credit, debt management, and loans
# - Retirement planning
# - Insurance

# Guidelines:
# 1. Provide accurate, helpful information on financial topics.
# 2. If asked about non-financial topics, politely redirect the conversation to finance.
# 3. Use clear, concise language that is easy to understand.
# 4. When appropriate, structure your responses with bullet points for readability.
# 5. Always disclose that your advice is informational only and not professional financial advice.
# 6. Stay current with general financial concepts.
# 7. For very specific tax or investment questions, recommend consulting with a certified professional."""
#             }
#         ]
    
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

# def sample_financial_questions():
#     """Provides sample financial questions users can ask."""
#     return [
#         "How can I start investing with little money?",
#         "What's the difference between a Roth IRA and Traditional IRA?",
#         "How do I create a basic budget?",
#         "Should I pay off debt or invest first?",
#         "What's the 50/30/20 budgeting rule?",
#         "How can I improve my credit score?",
#         "What's the best way to save for retirement?",
#         "How do taxes work on investment gains?"
#     ]

# def get_financial_metrics():
#     """Generate sample financial metrics for demonstration."""
#     # This is demo data - in a real app you would fetch this from an API
#     return {
#         "savings_rate": 25,
#         "debt_to_income": 28,
#         "emergency_fund": 4.5,  # months
#         "investment_return": 7.2  # percent
#     }

# def draw_financial_metrics(metrics):
#     """Draw financial metrics in an attractive way."""
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Savings rate gauge
#         savings_rate = metrics["savings_rate"]
#         savings_color = "#10B981" if savings_rate >= 20 else "#FBBF24" if savings_rate >= 10 else "#EF4444"
#         st.markdown(f"""
#             <div class="feature-box">
#                 <div class="feature-icon">💰</div>
#                 <h3>Savings Rate</h3>
#                 <div style="font-size: 2rem; font-weight: bold; color: {savings_color};">{savings_rate}%</div>
#                 <div>of income saved</div>
#             </div>
#         """, unsafe_allow_html=True)
        
#         # Emergency fund gauge
#         emergency_months = metrics["emergency_fund"]
#         emergency_color = "#10B981" if emergency_months >= 6 else "#FBBF24" if emergency_months >= 3 else "#EF4444"
#         st.markdown(f"""
#             <div class="feature-box">
#                 <div class="feature-icon">🛟</div>
#                 <h3>Emergency Fund</h3>
#                 <div style="font-size: 2rem; font-weight: bold; color: {emergency_color};">{emergency_months}</div>
#                 <div>months of expenses</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         # Debt to income ratio
#         dti = metrics["debt_to_income"]
#         dti_color = "#10B981" if dti < 30 else "#FBBF24" if dti < 40 else "#EF4444"
#         st.markdown(f"""
#             <div class="feature-box">
#                 <div class="feature-icon">⚖️</div>
#                 <h3>Debt-to-Income</h3>
#                 <div style="font-size: 2rem; font-weight: bold; color: {dti_color};">{dti}%</div>
#                 <div>ratio</div>
#             </div>
#         """, unsafe_allow_html=True)
        
#         # Investment return
#         inv_return = metrics["investment_return"]
#         st.markdown(f"""
#             <div class="feature-box">
#                 <div class="feature-icon">📈</div>
#                 <h3>Investment Return</h3>
#                 <div style="font-size: 2rem; font-weight: bold; color: #3B82F6;">{inv_return}%</div>
#                 <div>annualized</div>
#             </div>
#         """, unsafe_allow_html=True)

# def create_sidebar():
#     """Create attractive sidebar with resources."""
#     st.sidebar.markdown('<div class="sidebar-title">💰 FinChat Resources</div>', unsafe_allow_html=True)
#     st.sidebar.markdown('<div class="sidebar-subtitle">Useful tools and information</div>', unsafe_allow_html=True)
    
#     # Sample questions
#     st.sidebar.markdown("### 💬 Sample Questions")
#     for question in sample_financial_questions():
#         if st.sidebar.button(question, key=f"btn_{question[:20]}"):
#             # If user clicks a sample question, use it as input
#             st.session_state.user_input = question
#             st.experimental_rerun()
    
#     # Financial Resources links
#     st.sidebar.markdown("### 🔗 Helpful Resources")
#     resources = [
#         {"name": "Investopedia", "url": "https://www.investopedia.com/", "desc": "Financial education website"},
#         {"name": "NerdWallet", "url": "https://www.nerdwallet.com/", "desc": "Personal finance tools & reviews"},
#         {"name": "Bogleheads", "url": "https://www.bogleheads.org/", "desc": "Investment philosophy forum"},
#         {"name": "IRS.gov", "url": "https://www.irs.gov/", "desc": "Official tax information"}
#     ]
    
#     for resource in resources:
#         st.sidebar.markdown(f"[{resource['name']}]({resource['url']}) - {resource['desc']}")
    
#     # Add info about the app
#     st.sidebar.markdown("---")
#     st.sidebar.markdown("### 🤖 About FinChat")
#     st.sidebar.info("""
#     FinChat is your AI financial assistant powered by GROQ LLM technology. 
#     Ask questions about budgeting, investing, taxes, and more.
    
#     **Note:** This is for informational purposes only.
#     """)

# def create_chart():
#     """Create a simple financial chart for visualizing sample data."""
#     # Sample investment growth data
#     years = list(range(2024, 2044))
#     conservative = [10000 * (1.05 ** (year - 2024)) for year in years]
#     balanced = [10000 * (1.07 ** (year - 2024)) for year in years]
#     aggressive = [10000 * (1.09 ** (year - 2024)) for year in years]
    
#     # Create DataFrame
#     data = pd.DataFrame({
#         'Year': years,
#         'Conservative (5%)': conservative,
#         'Balanced (7%)': balanced,
#         'Aggressive (9%)': aggressive
#     })
    
#     # Melt the DataFrame for easier plotting
#     melted_data = pd.melt(data, id_vars=['Year'], var_name='Portfolio', value_name='Value')
    
#     # Create Altair chart
#     chart = alt.Chart(melted_data).mark_line().encode(
#         x=alt.X('Year:O', title='Year'),
#         y=alt.Y('Value:Q', title='Portfolio Value ($)'),
#         color=alt.Color('Portfolio:N', scale=alt.Scale(
#             domain=['Conservative (5%)', 'Balanced (7%)', 'Aggressive (9%)'],
#             range=['#10B981', '#3B82F6', '#8B5CF6']
#         )),
#         tooltip=['Year', 'Portfolio', 'Value']
#     ).interactive().properties(
#         title='$10,000 Investment Growth Over 20 Years'
#     )
    
#     return chart

# def main():
#     # Initialize session state
#     initialize_session_state()
    
#     # Create the sidebar
#     create_sidebar()
    
#     # Main layout
#     st.markdown("""
#     <div class="header-container">
#         <div class="logo">💰</div>
#         <h1>FinChat: Your AI Financial Assistant</h1>
#     </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown('<p class="subtitle">Your personal guide to smart money decisions. Ask me anything about finance!</p>', unsafe_allow_html=True)
    
#     # Create tabs for different sections
#     tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Financial Dashboard", "ℹ️ How It Works"])
    
#     with tab1:  # Chat Tab
#         # Chat container
#         with st.container():
#             st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)
            
#             # Display chat history
#             for message in st.session_state.chat_history:
#                 display_message(message["content"], message["role"])
            
#             # Display welcome message if no chat history
#             if not st.session_state.chat_history:
#                 display_message(
#                     "Hello! I'm your FinChat assistant. I can help with personal finance questions, money management, taxes, and finance news. What would you like to know about today?", 
#                     "assistant"
#                 )
            
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         # User input area
#         with st.container():
#             st.markdown('<div class="input-area">', unsafe_allow_html=True)
#             col1, col2 = st.columns([5, 1])
#             with col1:
#                 user_input = st.text_input("", key="user_input", placeholder="Ask about finance, taxes, or money management...")
#             with col2:
#                 send_button = st.button("Send")
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         if send_button and user_input:
#             # Display user message
#             display_message(user_input, "user")
            
#             # Add user message to session state
#             st.session_state.chat_history.append({"role": "user", "content": user_input})
#             st.session_state.messages.append({"role": "user", "content": user_input})
            
#             # Show a spinner while waiting for the API response
#             with st.spinner("Thinking..."):
#                 # Call GROQ API to get response
#                 assistant_response = call_groq_api(st.session_state.messages)
                
#                 # Add assistant response to session state
#                 st.session_state.messages.append({"role": "assistant", "content": assistant_response})
#                 st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
            
#             # Display assistant response
#             display_message(assistant_response, "assistant")
            
#             # Clear the input box
#             st.session_state.user_input = ""
    
#     with tab2:  # Financial Dashboard Tab
#         st.markdown("## Your Financial Dashboard")
#         st.markdown("This interactive dashboard helps you visualize key financial metrics.")
        
#         # Display sample metrics
#         metrics = get_financial_metrics()
#         draw_financial_metrics(metrics)
        
#         # Display investment growth chart
#         st.markdown("### Investment Growth Projection")
#         chart = create_chart()
#         st.altair_chart(chart, use_container_width=True)
        
#         # Add disclaimer for sample data
#         st.info("Note: This dashboard shows sample data for demonstration purposes only.")
    
#     with tab3:  # How It Works Tab
#         st.markdown("## How FinChat Works")
        
#         # Create three columns for features
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             st.markdown("""
#             <div class="feature-box">
#                 <div class="feature-icon">🧠</div>
#                 <h3>AI-Powered Advice</h3>
#                 <p>FinChat uses the powerful GROQ LLM to provide personalized financial guidance based on your specific questions.</p>
#             </div>
#             """, unsafe_allow_html=True)
            
#         with col2:
#             st.markdown("""
#             <div class="feature-box">
#                 <div class="feature-icon">🔒</div>
#                 <h3>Private & Secure</h3>
#                 <p>Your conversations are not stored permanently, and we prioritize your data privacy and security.</p>
#             </div>
#             """, unsafe_allow_html=True)
            
#         with col3:
#             st.markdown("""
#             <div class="feature-box">
#                 <div class="feature-icon">📚</div>
#                 <h3>Educational Focus</h3>
#                 <p>FinChat aims to improve your financial literacy with clear, comprehensive explanations of complex topics.</p>
#             </div>
#             """, unsafe_allow_html=True)
        
#         # How to use section with numbered steps
#         st.markdown("### How to Use FinChat")
        
#         st.markdown("""
#         1. **Ask a Question** - Type your financial question in the chat input box
#         2. **Get Answers** - Receive clear, informative responses about personal finance
#         3. **Explore Topics** - Use the sample questions in the sidebar for inspiration
#         4. **Track Metrics** - View the dashboard to visualize key financial concepts
#         """)
        
#         # Add a progress meter for a visual element
#         progress_value = 0.87
#         st.markdown("### User Satisfaction Rating")
#         st.progress(progress_value)
#         st.text(f"{int(progress_value * 100)}% of users found FinChat helpful")
    
#     # Disclaimer at the bottom
#     st.markdown("""
#     <div class="disclaimer">
#         <strong>Disclaimer:</strong> FinChat provides general information for educational purposes only. 
#         Always consult with a qualified financial professional before making important financial decisions.
#         The sample metrics and charts are for illustrative purposes only and do not represent actual financial data.
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Auto-scroll to bottom of chat (JavaScript)
#     st.markdown("""
#     <script>
#         // Scroll chat container to bottom
#         const chatContainer = document.getElementById('chat-container');
#         if (chatContainer) {
#             chatContainer.scrollTop = chatContainer.scrollHeight;
#         }
#     </script>
#     """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()







import streamlit as st
import requests
import json
import uuid
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import altair as alt

# Load API keys from Streamlit secrets or .env file
try:
    # First try to load from Streamlit secrets (for cloud deployment)
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    print("Loaded API key from Streamlit secrets")
except Exception:
    # Fall back to .env file (for local development)
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
    print("Loaded API key from .env file")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Debug info
print(f"Python version: {sys.version}", flush=True)
print(f"GROQ API KEY status: {'Available' if GROQ_API_KEY else 'Missing'}", flush=True)
print(f"Current working directory: {os.getcwd()}", flush=True)

# Page configuration
st.set_page_config(
    page_title="FinChat - AI Financial Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/finchat',
        'Report a bug': 'https://github.com/yourusername/finchat/issues',
        'About': "# FinChat\nYour personal AI financial assistant powered by GROQ."
    }
)

# Custom CSS for better styling (merged with edited CSS)
st.markdown("""
<style>
    /* Main layout */
    .main {
        background-color: #f8fafc;
    }

    [data-testid="stSidebar"] {
        background-color: #1E293B;
        color: white;
        border-right: 1px solid #334155;
    }

    [data-testid="stSidebar"] .sidebar-content {
        padding: 1rem;
    }

    /* Containers and blocks */
    .main .block-container {
        padding: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Chat interface */
    .chat-container {
        background-color: white;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        padding: 1rem;
        margin-bottom: 1rem;
        height: 70vh;
        overflow-y: auto;
        scrollbar-width: thin;
    }

    .chat-message {
        padding: 1rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        animation: fadeIn 0.5s;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .chat-message.user {
        background-color: #f1f5f9;
        border-bottom-right-radius: 0.25rem;
        margin-left: 2rem;
    }

    .chat-message.assistant {
        background-color: #f0f9ff;
        border: 1px solid #e0f2fe;
        border-bottom-left-radius: 0.25rem;
        margin-right: 2rem;
    }

    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }

    .chat-message .message {
        flex-grow: 1;
    }

    /* Input area */
    .input-area {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    .stTextInput>div>div>input {
        border-radius: 0.5rem;
        border: 1px solid #cbd5e1;
        padding: 0.75rem;
        font-size: 1rem;
    }

    .stButton>button {
        border-radius: 0.5rem;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        font-weight: bold;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.5);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.6);
    }

    /* Text styling */
    h1 {
        color: #0f172a;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2 {
        color: #334155;
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    .subtitle {
        color: #64748b;
        font-size: 1.25rem;
        margin-bottom: 2rem;
    }

    .header-container {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .header-container .logo {
        font-size: 3rem;
        margin-right: 1rem;
        background: linear-gradient(135deg, #fbbf24 0%, #ea580c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .disclaimer {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 1.5rem;
        padding: 1rem;
        border-left: 4px solid #cbd5e1;
        background-color: #f8fafc;
    }

    /* Feature boxes */
    .feature-box {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Sidebar custom styles */
    .sidebar-title {
        color: white;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }

    /* Tabs and metrics */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 0.5rem 0.5rem 0 0;
        padding: 0.5rem 1rem;
        color: #64748b;
    }

    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #3b82f6 !important;
        font-weight: 600;
    }

    /* Loading spinner */
    .stSpinner > div > div {
        border-color: #3b82f6 !important;
    }

    /* Tooltip */
    .stTooltip {
        border-color: #cbd5e1;
    }

    /* Edited Styles */
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .calculator-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .result-container {
        background-color: #e9ecef;
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
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

def sample_financial_questions():
    """Provides sample financial questions users can ask."""
    return [
        "How can I start investing with little money?",
        "What's the difference between a Roth IRA and Traditional IRA?",
        "How do I create a basic budget?",
        "Should I pay off debt or invest first?",
        "What's the 50/30/20 budgeting rule?",
        "How can I improve my credit score?",
        "What's the best way to save for retirement?",
        "How do taxes work on investment gains?"
    ]

def get_financial_metrics():
    """Generate sample financial metrics for demonstration."""
    # This is demo data - in a real app you would fetch this from an API
    return {
        "savings_rate": 25,
        "debt_to_income": 28,
        "emergency_fund": 4.5,  # months
        "investment_return": 7.2  # percent
    }

def draw_financial_metrics(metrics):
    """Draw financial metrics in an attractive way."""
    col1, col2 = st.columns(2)

    with col1:
        # Savings rate gauge
        savings_rate = metrics["savings_rate"]
        savings_color = "#10B981" if savings_rate >= 20 else "#FBBF24" if savings_rate >= 10 else "#EF4444"
        st.markdown(f"""
            <div class="feature-box">
                <div class="feature-icon">💰</div>
                <h3>Savings Rate</h3>
                <div style="font-size: 2rem; font-weight: bold; color: {savings_color};">{savings_rate}%</div>
                <div>of income saved</div>
            </div>
        """, unsafe_allow_html=True)

        # Emergency fund gauge
        emergency_months = metrics["emergency_fund"]
        emergency_color = "#10B981" if emergency_months >= 6 else "#FBBF24" if emergency_months >= 3 else "#EF4444"
        st.markdown(f"""
            <div class="feature-box">
                <div class="feature-icon">🛟</div>
                <h3>Emergency Fund</h3>
                <div style="font-size: 2rem; font-weight: bold; color: {emergency_color};">{emergency_months}</div>
                <div>months of expenses</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Debt to income ratio
        dti = metrics["debt_to_income"]
        dti_color = "#10B981" if dti < 30 else "#FBBF24" if dti < 40 else "#EF4444"
        st.markdown(f"""
            <div class="feature-box">
                <div class="feature-icon">⚖️</div>
                <h3>Debt-to-Income</h3>
                <div style="font-size: 2rem; font-weight: bold; color: {dti_color};">{dti}%</div>
                <div>ratio</div>
            </div>
        """, unsafe_allow_html=True)

        # Investment return
        inv_return = metrics["investment_return"]
        st.markdown(f"""
            <div class="feature-box">
                <div class="feature-icon">📈</div>
                <h3>Investment Return</h3>
                <div style="font-size: 2rem; font-weight: bold; color: #3B82F6;">{inv_return}%</div>
                <div>annualized</div>
            </div>
        """, unsafe_allow_html=True)

def create_sidebar():
    """Create attractive sidebar with resources."""
    st.sidebar.markdown('<div class="sidebar-title">💰 FinChat Resources</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-subtitle">Useful tools and information</div>', unsafe_allow_html=True)

    # Sample questions
    st.sidebar.markdown("### 💬 Sample Questions")
    for question in sample_financial_questions():
        if st.sidebar.button(question, key=f"btn_{question[:20]}"):
            # If user clicks a sample question, use it as input
            st.session_state.user_input = question
            st.experimental_rerun()

    # Financial Resources links
    st.sidebar.markdown("### 🔗 Helpful Resources")
    resources = [
        {"name": "Investopedia", "url": "https://www.investopedia.com/", "desc": "Financial education website"},
        {"name": "NerdWallet", "url": "https://www.nerdwallet.com/", "desc": "Personal finance tools & reviews"},
        {"name": "Bogleheads", "url": "https://www.bogleheads.org/", "desc": "Investment philosophy forum"},
        {"name": "IRS.gov", "url": "https://www.irs.gov/", "desc": "Official tax information"}
    ]

    for resource in resources:
        st.sidebar.markdown(f"[{resource['name']}]({resource['url']}) - {resource['desc']}")

    # Add info about the app
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 About FinChat")
    st.sidebar.info("""
    FinChat is your AI financial assistant powered by GROQ LLM technology. 
    Ask questions about budgeting, investing, taxes, and more.

    **Note:** This is for informational purposes only.
    """)

def create_chart():
    """Create a simple financial chart for visualizing sample data."""
    # Sample investment growth data
    years = list(range(2024, 2044))
    conservative = [10000 * (1.05 ** (year - 2024)) for year in years]
    balanced = [10000 * (1.07 ** (year - 2024)) for year in years]
    aggressive = [10000 * (1.09 ** (year - 2024)) for year in years]

    # Create DataFrame
    data = pd.DataFrame({
        'Year': years,
        'Conservative (5%)': conservative,
        'Balanced (7%)': balanced,
        'Aggressive (9%)': aggressive
    })

    # Melt the DataFrame for easier plotting
    melted_data = pd.melt(data, id_vars=['Year'], var_name='Portfolio', value_name='Value')

    # Create Altair chart
    chart = alt.Chart(melted_data).mark_line().encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Value:Q', title='Portfolio Value ($)'),
        color=alt.Color('Portfolio:N', scale=alt.Scale(
            domain=['Conservative (5%)', 'Balanced (7%)', 'Aggressive (9%)'],
            range=['#10B981', '#3B82F6', '#8B5CF6']
        )),
        tooltip=['Year', 'Portfolio', 'Value']
    ).interactive().properties(
        title='$10,000 Investment Growth Over 20 Years'
    )

    return chart

def format_currency(amount):
    return f"₹{amount:,.2f}"

def main():
    # Initialize session state
    initialize_session_state()

    # Create the sidebar
    create_sidebar()

    # Main layout
    st.markdown("""
    <div class="header-container">
        <div class="logo">💰</div>
        <h1>FinChat: Your AI Financial Assistant</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="subtitle">Your personal guide to smart money decisions. Ask me anything about finance!</p>', unsafe_allow_html=True)

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Financial Dashboard", "ℹ️ How It Works"])

    with tab1:  # Chat Tab
        # Chat container
        with st.container():
            st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)

            # Display chat history
            for message in st.session_state.chat_history:
                display_message(message["content"], message["role"])

            # Display welcome message if no chat history
            if not st.session_state.chat_history:
                display_message(
                    "Hello! I'm your FinChat assistant. I can help with personal finance questions, money management, taxes, and finance news. What would you like to know about today?",
                    "assistant"
                )

            st.markdown('</div>', unsafe_allow_html=True)

        # User input area
        with st.container():
            st.markdown('<div class="input-area">', unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])
            with col1:
                user_input = st.text_input("", key="user_input", placeholder="Ask about finance, taxes, or money management...")
            with col2:
                send_button = st.button("Send")
            st.markdown('</div>', unsafe_allow_html=True)

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

    with tab2:  # Financial Dashboard Tab
        # Main title
        st.title("💰 Financial Calculator Dashboard")

        # Create tabs for different calculators
        tabs = st.tabs(["Fixed Deposit", "SIP Calculator", "Loan EMI", "Income Tax", "Investment Projections"])

        # Fixed Deposit Calculator
        with tabs[0]:
            st.header("Fixed Deposit Calculator")
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    fd_principal = st.number_input("Principal Amount (₹)", min_value=1000, value=100000, step=1000, key="fd_principal")
                    fd_rate = st.number_input("Interest Rate (%)", min_value=1.0, max_value=15.0, value=6.0, step=0.1, key="fd_rate")
                with col2:
                    fd_years = st.number_input("Time Period (Years)", min_value=1, max_value=30, value=5, step=1, key="fd_years")
                    fd_compound = st.selectbox("Compounding Frequency", ["Annually", "Semi-annually", "Quarterly", "Monthly"])

                if st.button("Calculate FD Returns"):
                    compounds_per_year = {"Annually": 1, "Semi-annually": 2, "Quarterly": 4, "Monthly": 12}[fd_compound]
                    fd_amount = fd_principal * (1 + (fd_rate/100)/compounds_per_year) ** (fd_years * compounds_per_year)
                    fd_interest = fd_amount - fd_principal

                    st.markdown("### Results")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Principal Amount", format_currency(fd_principal))
                    col2.metric("Total Interest", format_currency(fd_interest))
                    col3.metric("Maturity Amount", format_currency(fd_amount))

        # SIP Calculator
        with tabs[1]:
            st.header("SIP Calculator")
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    sip_amount = st.number_input("Monthly Investment (₹)", min_value=500, value=10000, step=500, key="sip_amount")
                    sip_rate = st.number_input("Expected Return Rate (%)", min_value=1.0, max_value=30.0, value=12.0, step=0.1, key="sip_rate")
                with col2:
                    sip_years = st.number_input("Investment Period (Years)", min_value=1, max_value=40, value=10, step=1, key="sip_years")

                if st.button("Calculate SIP Returns"):
                    monthly_rate = sip_rate/(12 * 100)
                    months = sip_years * 12
                    sip_maturity = sip_amount * ((1 + monthly_rate) ** months - 1) * (1 + monthly_rate) / monthly_rate
                    total_investment = sip_amount * months
                    total_interest = sip_maturity - total_investment

                    st.markdown("### Results")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Investment", format_currency(total_investment))
                    col2.metric("Total Interest", format_currency(total_interest))
                    col3.metric("Maturity Amount", format_currency(sip_maturity))

                    # Investment growth chart
                    years = list(range(1, sip_years + 1))
                    invested = [sip_amount * 12 * y for y in years]
                    wealth = [sip_amount * 12 * ((1 + monthly_rate) ** (y * 12) - 1) * (1 + monthly_rate) / monthly_rate for y in years]

                    df = pd.DataFrame({
                        'Year': years,
                        'Invested Amount': invested,
                        'Wealth Gained': wealth
                    })

                    chart = alt.Chart(df).transform_fold(
                        ['Invested Amount', 'Wealth Gained'],
                        as_=['Category', 'Amount']
                    ).mark_line().encode(
                        x='Year:Q',
                        y='Amount:Q',
                        color='Category:N'
                    ).properties(
                        title='Investment Growth Over Time',
                        width=600,
                        height=400
                    )

                    st.altair_chart(chart, use_container_width=True)

        # Loan EMI Calculator
        with tabs[2]:
            st.header("Loan EMI Calculator")
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    loan_amount = st.number_input("Loan Amount (₹)", min_value=10000, value=1000000, step=10000, key="loan_amount")
                    loan_rate = st.number_input("Interest Rate (%)", min_value=1.0, max_value=30.0, value=8.0, step=0.1, key="loan_rate")
                with col2:
                    loan_years = st.number_input("Loan Period (Years)", min_value=1, max_value=30, value=20, step=1, key="loan_years")

                if st.button("Calculate Loan EMI"):
                    monthly_rate = loan_rate/(12 * 100)
                    months = loan_years * 12
                    emi = loan_amount * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
                    total_payment = emi * months
                    total_interest = total_payment - loan_amount

                    st.markdown("### Results")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Loan Amount", format_currency(loan_amount))
                    col2.metric("Monthly EMI", format_currency(emi))
                    col3.metric("Total Interest", format_currency(total_interest))
                    col4.metric("Total Payment", format_currency(total_payment))

        # Income Tax Calculator
        with tabs[3]:
            st.header("Income Tax Calculator (India)")
            with st.container():
                tax_regime = st.radio("Select Tax Regime", ["Old", "New"])
                income = st.number_input("Annual Income (₹)", min_value=0, value=500000, step=10000, key="income")

                def calculate_old_tax(income):
                    tax = 0
                    if income > 1000000: tax += (income - 1000000) * 0.30
                    if income > 500000: tax += min(income - 500000, 500000) * 0.20
                    if income > 250000: tax += min(income - 250000, 250000) * 0.05
                    return tax

                def calculate_new_tax(income):
                    tax = 0
                    if income > 1500000: tax += (income - 1500000) * 0.30
                    if income > 1250000: tax += min(income - 1250000, 250000) * 0.25
                    if income > 1000000: tax += min(income - 1000000, 250000) * 0.20
                    if income > 750000: tax += min(income - 750000, 250000) * 0.15
                    if income > 500000: tax += min(income - 500000, 250000) * 0.10
                    if income > 300000: tax += min(income - 300000, 200000) * 0.05
                    return tax

                if st.button("Calculate Tax"):
                    tax = calculate_old_tax(income) if tax_regime == "Old" else calculate_new_tax(income)
                    cess = tax * 0.04
                    total_tax = tax + cess

                    st.markdown("### Tax Calculation Results")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Income", format_currency(income))
                    col2.metric("Tax Amount", format_currency(tax))
                    col3.metric("Total Tax (inc. 4% Cess)", format_currency(total_tax))

        # Investment Projections
        with tabs[4]:
            st.header("Investment Growth Projections")
            with st.container():
                initial_investment = st.number_input("Initial Investment (₹)", min_value=0, value=100000, step=10000)
                monthly_contribution = st.number_input("Monthly Contribution (₹)", min_value=0, value=10000, step=1000)
                projection_years = st.number_input("Projection Years", min_value=1, max_value=40, value=20)
                return_rates = st.slider("Expected Annual Return (%)", min_value=1, max_value=20, value=(8, 12))

                if st.button("Show Projections"):
                    years = list(range(projection_years + 1))
                    conservative = []
                    aggressive = []

                    for year in years:
                        monthly = monthly_contribution * 12
                        conservative_amount = (initial_investment + monthly * year) * (1 + return_rates[0]/100) ** year
                        aggressive_amount = (initial_investment + monthly * year) * (1 + return_rates[1]/100) ** year
                        conservative.append(conservative_amount)
                        aggressive.append(aggressive_amount)

                    df = pd.DataFrame({
                        'Year': years,
                        f'Conservative ({return_rates[0]}%)': conservative,
                        f'Aggressive ({return_rates[1]}%)': aggressive
                    })

                    chart = alt.Chart(df).transform_fold(
                        [f'Conservative ({return_rates[0]}%)', f'Aggressive ({return_rates[1]}%)'],
                        as_=['Scenario', 'Amount']
                    ).mark_line().encode(
                        x='Year:Q',
                        y='Amount:Q',
                        color='Scenario:N',
                        tooltip=['Year:Q', 'Amount:Q', 'Scenario:N']
                    ).properties(
                        title='Investment Growth Projection',
                        width=700,
                        height=400
                    )

                    st.altair_chart(chart, use_container_width=True)

                    st.markdown("### Final Values")
                    col1, col2 = st.columns(2)
                    col1.metric(f"Conservative Scenario ({return_rates[0]}%)", format_currency(conservative[-1]))
                    col2.metric(f"Aggressive Scenario ({return_rates[1]}%)", format_currency(aggressive[-1]))

    with tab3:  # How It Works Tab
        st.markdown("## How FinChat Works")

        # Create three columns for features
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="feature-box">
                <div class="feature-icon">🧠</div>
                <h3>AI-Powered Advice</h3>
                <p>FinChat uses the powerful GROQ LLM to provide personalized financial guidance based on your specific questions.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-box">
                <div class="feature-icon">🔒</div>
                <h3>Private & Secure</h3>
                <p>Your conversations are not stored permanently, and we prioritize your data privacy and security.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="feature-box">
                <div class="feature-icon">📚</div>
                <h3>Educational Focus</h3>
                <p>FinChat aims to improve your financial literacy with clear, comprehensive explanations of complex topics.</p>
            </div>
            """, unsafe_allow_html=True)

        # How to use section with numbered steps
        st.markdown("### How to Use FinChat")

        st.markdown("""
        1. **Ask a Question** - Type your financial question in the chat input box
        2. **Get Answers** - Receive clear, informative responses about personal finance
        3. **Explore Topics** - Use the sample questions in the sidebar for inspiration
        4. **Track Metrics** - View the dashboard to visualize key financial concepts
        """)

        # Add a progress meter for a visual element
        progress_value = 0.87
        st.markdown("### User Satisfaction Rating")
        st.progress(progress_value)
        st.text(f"{int(progress_value * 100)}% of users found FinChat helpful")

    # Disclaimer at the bottom
    st.markdown("""
    <div class="disclaimer">
        <strong>Disclaimer:</strong> FinChat provides general information for educational purposes only. 
        Always consult with a qualified financial professional before making important financial decisions.
        The sample metrics and charts are for illustrative purposes only and do not represent actual financial data.
    </div>
    """, unsafe_allow_html=True)

    # Auto-scroll to bottom of chat (JavaScript)
    st.markdown("""
    <script>
        // Scroll chat container to bottom
        const chatContainer = document.getElementById('chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
