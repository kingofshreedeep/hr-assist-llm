import streamlit as st
import requests
import json
import uuid
from datetime import datetime

# Professional App Configuration
st.set_page_config(
    page_title="TalentScout AI - Professional Hiring Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Professional CSS Variables System */
    :root {
        /* Design Tokens - Colors */
        --color-primary-50: #eff6ff;
        --color-primary-100: #dbeafe;
        --color-primary-500: #3b82f6;
        --color-primary-600: #2563eb;
        --color-primary-700: #1d4ed8;
        --color-primary-900: #1e3a8a;
        
        --color-neutral-50: #f8fafc;
        --color-neutral-100: #f1f5f9;
        --color-neutral-200: #e2e8f0;
        --color-neutral-300: #cbd5e1;
        --color-neutral-400: #94a3b8;
        --color-neutral-500: #64748b;
        --color-neutral-600: #475569;
        --color-neutral-700: #334155;
        --color-neutral-800: #1e293b;
        --color-neutral-900: #0f172a;
        
        --color-success: #10b981;
        --color-warning: #f59e0b;
        --color-error: #ef4444;
        
        /* Theme Variables */
        --bg-primary: var(--color-neutral-50);
        --bg-secondary: #ffffff;
        --bg-tertiary: var(--color-neutral-100);
        --text-primary: var(--color-neutral-900);
        --text-secondary: var(--color-neutral-600);
        --text-muted: var(--color-neutral-400);
        --border-color: var(--color-neutral-200);
        --accent-color: var(--color-primary-600);
        --gradient-primary: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-primary-700) 100%);
        
        /* Shadows */
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        
        /* Spacing */
        --space-1: 0.25rem;
        --space-2: 0.5rem;
        --space-3: 0.75rem;
        --space-4: 1rem;
        --space-6: 1.5rem;
        --space-8: 2rem;
        
        /* Border Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
    }

    /* Dark Theme */
    [data-theme="dark"] {
        --bg-primary: var(--color-neutral-900);
        --bg-secondary: var(--color-neutral-800);
        --bg-tertiary: var(--color-neutral-700);
        --text-primary: var(--color-neutral-50);
        --text-secondary: var(--color-neutral-300);
        --text-muted: var(--color-neutral-400);
        --border-color: var(--color-neutral-600);
        --gradient-primary: linear-gradient(135deg, var(--color-primary-500) 0%, var(--color-primary-600) 100%);
        
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.4), 0 1px 2px 0 rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3);
    }

    /* Base Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        font-size: 14px;
        line-height: 1.5;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Streamlit App Styling */
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .main .block-container {
        padding: var(--space-6);
        max-width: 1400px;
        background: var(--bg-primary);
    }

    /* Professional Header */
    .main-header {
        background: var(--gradient-primary);
        color: white;
        padding: var(--space-6);
        border-radius: var(--radius-xl);
        margin-bottom: var(--space-6);
        box-shadow: var(--shadow-lg);
        text-align: center;
    }

    .header-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
    }

    .header-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        margin: var(--space-2) 0 0 0;
    }

    /* Sidebar Professional Styling */
    .css-1d391kg {
        background: var(--bg-tertiary) !important;
        border-right: 1px solid var(--border-color);
    }

    .sidebar-content {
        background: var(--bg-secondary);
        border-radius: var(--radius-xl);
        border: 1px solid var(--border-color);
        padding: var(--space-6);
        box-shadow: var(--shadow-sm);
        margin-bottom: var(--space-4);
    }

    /* Progress Section */
    .progress-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--space-6);
        display: flex;
        align-items: center;
        gap: var(--space-3);
    }

    .progress-item {
        margin-bottom: var(--space-4);
    }

    .progress-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--text-secondary);
        margin-bottom: var(--space-2);
        display: flex;
        align-items: center;
        gap: var(--space-2);
    }

    /* Chat Container */
    .chat-container {
        background: var(--bg-secondary);
        border-radius: var(--radius-xl);
        border: 1px solid var(--border-color);
        padding: var(--space-6);
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
        box-shadow: var(--shadow-md);
        margin-bottom: var(--space-6);
    }

    .message-container {
        margin-bottom: var(--space-4);
        animation: slideIn 0.3s ease-out;
    }

    .message-assistant {
        background: var(--gradient-primary);
        color: white;
        padding: var(--space-4) var(--space-6);
        border-radius: var(--radius-lg);
        border-bottom-left-radius: var(--radius-sm);
        max-width: 75%;
        margin-left: auto;
        font-size: 0.9375rem;
        line-height: 1.6;
        word-wrap: break-word;
    }

    .message-user {
        background: var(--bg-tertiary);
        color: var(--text-primary);
        padding: var(--space-4) var(--space-6);
        border-radius: var(--radius-lg);
        border-bottom-right-radius: var(--radius-sm);
        border: 1px solid var(--border-color);
        max-width: 75%;
        margin-right: auto;
        font-size: 0.9375rem;
        line-height: 1.6;
        word-wrap: break-word;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Input and Button Styling */
    .stTextInput > div > div > input {
        background: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--text-primary) !important;
        font-size: 0.9375rem !important;
        padding: var(--space-4) !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }

    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-3) var(--space-6) !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-lg) !important;
    }

    /* Theme Toggle Button */
    .theme-toggle-container {
        text-align: center;
        margin-bottom: var(--space-4);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: var(--space-4);
        }
        
        .message-assistant, .message-user {
            max-width: 90%;
        }
    }

    /* Progress Bar Custom Styling */
    .stProgress > div > div > div > div {
        background-color: var(--color-success) !important;
    }

    /* Selectbox Styling */
    .stSelectbox > div > div > div {
        background: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--text-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_dark_theme" not in st.session_state:
    st.session_state.is_dark_theme = False
if "progress" not in st.session_state:
    st.session_state.progress = {
        "name": 0,
        "experience": 0,
        "position": 0,
        "skills": 0
    }

# Theme toggle function
def toggle_theme():
    st.session_state.is_dark_theme = not st.session_state.is_dark_theme

# Apply theme
theme_attribute = 'data-theme="dark"' if st.session_state.is_dark_theme else ''
st.markdown(f'<script>document.body.setAttribute("data-theme", "{("dark" if st.session_state.is_dark_theme else "light")}")</script>', unsafe_allow_html=True)

# Professional Header
st.markdown("""
<div class="main-header">
    <h1 class="header-title">🎯 TalentScout AI</h1>
    <p class="header-subtitle">Professional Hiring Assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for Progress Tracking
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <div class="progress-title">
            📊 Interview Progress
        </div>
    """, unsafe_allow_html=True)
    
    # Theme Toggle
    st.markdown('<div class="theme-toggle-container">', unsafe_allow_html=True)
    if st.button("🌙 Dark Mode" if not st.session_state.is_dark_theme else "☀️ Light Mode", 
                 key="theme_toggle", on_click=toggle_theme):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Progress indicators
    progress_items = [
        ("👤", "Personal Information", "name"),
        ("💼", "Professional Experience", "experience"),
        ("💻", "Role & Position", "position"),
        ("⚡", "Technical Skills", "skills")
    ]
    
    for icon, label, key in progress_items:
        st.markdown(f"""
        <div class="progress-item">
            <div class="progress-label">
                {icon} {label}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.progress[key] / 100)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Session Info
    st.markdown("""
    <div class="sidebar-content">
        <div class="progress-title">
            ℹ️ Session Info
        </div>
        <p style="font-size: 0.8rem; color: var(--text-muted);">
            Session ID: """ + st.session_state.session_id[:8] + """...<br>
            Messages: """ + str(len(st.session_state.messages)) + """<br>
            Started: """ + datetime.now().strftime("%H:%M") + """
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main Chat Interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
if not st.session_state.messages:
    st.markdown("""
    <div class="message-container">
        <div class="message-assistant">
            Welcome to TalentScout AI. I'm your professional hiring assistant designed to evaluate candidates efficiently. Let's begin with your full name.
        </div>
    </div>
    """, unsafe_allow_html=True)

for message in st.session_state.messages:
    message_class = "message-assistant" if message["role"] == "assistant" else "message-user"
    st.markdown(f"""
    <div class="message-container">
        <div class="{message_class}">
            {message["content"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Progress analysis function
def analyze_progress(message):
    text = message.lower()
    
    # Name detection
    if len(message.split()) <= 4 and any(char.isalpha() for char in message):
        st.session_state.progress["name"] = 100
    
    # Experience detection
    if any(word in text for word in ["year", "experience", "exp"]) and any(char.isdigit() for char in text):
        st.session_state.progress["experience"] = 100
    
    # Position detection
    if any(word in text for word in ["developer", "engineer", "analyst", "manager", "architect", "lead", "senior", "junior"]):
        st.session_state.progress["position"] = 100
    
    # Skills detection
    if any(word in text for word in ["python", "javascript", "java", "react", "angular", "vue", "node", "sql", "aws", "azure", "docker"]):
        st.session_state.progress["skills"] = 100

# Chat input and API communication
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input("", placeholder="Enter your response...", key="user_input")

with col2:
    send_button = st.button("Send 📤", key="send_button")

if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Analyze progress
    analyze_progress(user_input)
    
    # Send to API
    try:
        with st.spinner("Processing..."):
            api_url = "http://localhost:8000/chat"
            payload = {
                "message": user_input,
                "session_id": st.session_state.session_id
            }
            
            response = requests.post(api_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                bot_response = response.json().get("response", "I apologize, but I couldn't process your response.")
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            else:
                st.session_state.messages.append({"role": "assistant", "content": "I apologize, but I encountered a technical issue. Please try again."})
                
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        st.session_state.messages.append({"role": "assistant", "content": "I'm having trouble connecting to the AI service. Please ensure the backend is running."})
    
    # Clear input and rerun to show new messages
    st.rerun()

# Auto-scroll to bottom
st.markdown("""
<script>
    var chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
</script>
""", unsafe_allow_html=True)