"""
HAVEN Crowdfunding Platform - Streamlined Frontend
Features: OAuth login, automatic term simplification, post-login navigation, campaign creation
"""

import streamlit as st
import requests
import json
import base64
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import time

# ========================================
# CONFIGURATION
# ========================================

# Backend configuration
BACKEND_URL = os.getenv("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")

# Feature flags
TRANSLATION_ENABLED = os.getenv("FEATURES_TRANSLATION_ENABLED", "true").lower() == "true"
SIMPLIFICATION_ENABLED = os.getenv("FEATURES_SIMPLIFICATION_ENABLED", "true").lower() == "true"
OAUTH_ENABLED = os.getenv("FEATURES_OAUTH_ENABLED", "true").lower() == "true"

# OAuth configuration
GOOGLE_CLIENT_ID = os.getenv("OAUTH_GOOGLE_CLIENT_ID", "")
FACEBOOK_APP_ID = os.getenv("OAUTH_FACEBOOK_APP_ID", "")

# ========================================
# TERM DEFINITIONS FOR AUTOMATIC TOOLTIPS
# ========================================

TERM_DEFINITIONS = {
    # Financial Terms
    "crowdfunding": "A way to raise money by asking many people to contribute small amounts online",
    "investment": "Money put into a project or business to make more money later",
    "equity": "Ownership share in a company",
    "revenue": "Total money earned from sales",
    "profit": "Money left after paying all costs",
    "roi": "Return on Investment - how much money you make compared to what you invested",
    "valuation": "How much a company is worth",
    "venture capital": "Money invested in new businesses with high growth potential",
    "angel investor": "Wealthy person who invests in startups",
    "seed funding": "Early money given to start a business",
    "series a": "First major round of investment funding",
    "ipo": "Initial Public Offering - when a company first sells shares to the public",
    "dividend": "Money paid to shareholders from company profits",
    "market cap": "Total value of all company shares",
    "cash flow": "Money coming in and going out of a business",
    
    # Technology Terms
    "api": "Application Programming Interface - a way for different software to communicate",
    "platform": "A system that allows people to build or use services",
    "algorithm": "A set of rules or instructions for solving a problem",
    "blockchain": "A secure digital ledger that records transactions",
    "cryptocurrency": "Digital money secured by cryptography",
    "saas": "Software as a Service - software delivered over the internet",
    "cloud computing": "Using internet-based computing services instead of local servers",
    "ai": "Artificial Intelligence - computer systems that can perform tasks requiring human intelligence",
    "machine learning": "Type of AI where computers learn from data without being explicitly programmed",
    "big data": "Extremely large datasets that require special tools to analyze",
    "iot": "Internet of Things - everyday objects connected to the internet",
    "cybersecurity": "Protection of computer systems and data from digital attacks",
    
    # Business Terms
    "startup": "A new company trying to grow quickly",
    "entrepreneur": "Person who starts and runs a business",
    "scalability": "Ability to grow and handle more customers or work",
    "market research": "Studying customers and competitors to understand demand",
    "business model": "How a company makes money",
    "prototype": "Early version of a product used for testing",
    "milestone": "Important goal or achievement in a project",
    "pivot": "Changing business direction based on what you learn",
    "mvp": "Minimum Viable Product - simplest version that customers will use",
    "b2b": "Business to Business - companies selling to other companies",
    "b2c": "Business to Consumer - companies selling directly to customers",
    "kpi": "Key Performance Indicator - important metric to measure success",
    "burn rate": "How fast a company spends money",
    "runway": "How long money will last at current spending rate",
    "exit strategy": "Plan for how investors will get their money back",
    
    # Medical Terms
    "medical treatment": "Healthcare services provided to treat illness or injury",
    "surgery": "Medical procedure involving cutting into the body to treat disease",
    "therapy": "Treatment designed to help with physical or mental health problems",
    "diagnosis": "Identifying what disease or condition a patient has",
    "prescription": "Written order from a doctor for specific medicine",
    "rehabilitation": "Process of helping someone recover from illness or injury",
    
    # NGO/Charity Terms
    "ngo": "Non-Governmental Organization - group working for social causes",
    "charity": "Organization that helps people in need without making profit",
    "donation": "Money or goods given to help others",
    "volunteer": "Person who helps without being paid",
    "fundraising": "Activities to collect money for a cause",
    "grant": "Money given by organizations to support specific projects",
    "nonprofit": "Organization that uses money to help others, not make profit"
}

# ========================================
# UTILITY FUNCTIONS
# ========================================

def get_logo_base64():
    """Convert logo image to base64 with error handling"""
    try:
        logo_paths = [
            "/home/ubuntu/haven_logo.png",
            "/home/ubuntu/assets/haven_logo.png",
            "./assets/haven_logo.png",
            "./haven_logo.png"
        ]
        
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        
        return None
    except Exception as e:
        return None

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API request with comprehensive error handling"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://haven-streamlit-frontend.onrender.com"
        }
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to backend server"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def get_supported_languages() -> List[Dict[str, str]]:
    """Get supported languages from backend or return default"""
    try:
        result = make_api_request("/api/supported-languages")
        if "error" not in result and "languages" in result:
            return result["languages"]
    except Exception:
        pass
    
    return [
        {"code": "en", "name": "English", "native": "English"},
        {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
        {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
        {"code": "te", "name": "Telugu", "native": "తెలుగు"}
    ]

def add_tooltips_to_text(text: str) -> str:
    """Add automatic tooltips to complex terms in text"""
    if not text:
        return text
    
    modified_text = text
    sorted_terms = sorted(TERM_DEFINITIONS.keys(), key=len, reverse=True)
    
    for term in sorted_terms:
        pattern = r'\b' + re.escape(term) + r'\b'
        matches = list(re.finditer(pattern, modified_text, re.IGNORECASE))
        
        for match in reversed(matches):
            start, end = match.span()
            original_term = modified_text[start:end]
            definition = TERM_DEFINITIONS[term]
            
            tooltip_html = f'''
            <span class="tooltip-term" title="{definition}">
                {original_term}
                <span class="tooltip-icon">ℹ️</span>
                <span class="tooltip-text">{definition}</span>
            </span>
            '''
            
            modified_text = modified_text[:start] + tooltip_html + modified_text[end:]
    
    return modified_text

# ========================================
# CSS STYLING
# ========================================

def load_css():
    """Load custom CSS for the application"""
    logo_base64 = get_logo_base64()
    
    css = f"""
    <style>
    /* Hide Streamlit default elements */
    .stDeployButton {{display: none !important;}}
    footer {{visibility: hidden !important;}}
    .stApp > header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    
    /* Main app styling */
    .stApp {{
        background: linear-gradient(135deg, 
            #f0f8ff 0%,     /* Light blue */
            #e6e6fa 50%,    /* Lavender */
            #f0fff0 100%    /* Light green */
        );
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background: linear-gradient(180deg, 
            #2d3748 0%,     /* Dark gray */
            #1a202c 100%   /* Dark blue-gray */
        );
        padding: 1rem;
    }}
    
    /* Sidebar content */
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stMarkdown,
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {{
        color: #ffffff !important;
        font-weight: 500;
    }}
    
    /* Language selector styling */
    .css-1d391kg .stSelectbox > div > div {{
        background-color: #4a5568 !important;
        color: #ffffff !important;
        border: 1px solid #718096 !important;
        border-radius: 8px !important;
    }}
    
    /* Navigation buttons */
    .nav-button {{
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white !important;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
        display: block;
        margin: 0.5rem 0;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
    }}
    
    .nav-button:hover {{
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3);
    }}
    
    /* Create campaign button */
    .create-button {{
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white !important;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        text-decoration: none;
        display: block;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
        font-size: 1.1rem;
    }}
    
    .create-button:hover {{
        background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
    }}
    
    /* Profile button */
    .profile-button {{
        background: linear-gradient(135deg, #9f7aea 0%, #805ad5 100%);
        color: white !important;
        border: none;
        padding: 0.5rem;
        border-radius: 50%;
        font-weight: 600;
        text-decoration: none;
        display: block;
        margin: 1rem auto;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 50px;
        height: 50px;
        font-size: 1.5rem;
    }}
    
    .profile-button:hover {{
        background: linear-gradient(135deg, #805ad5 0%, #6b46c1 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(159, 122, 234, 0.3);
    }}
    
    /* Main content area */
    .main-content {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    /* Logo styling */
    .logo-container {{
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
    }}
    
    .logo-image {{
        max-width: 250px;
        height: auto;
        margin: 0 auto;
        display: block;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
        animation: pulse 3s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.02); }}
    }}
    
    /* Tagline styling */
    .tagline {{
        text-align: center;
        font-size: 1.2rem;
        color: #2d3748;
        font-style: italic;
        margin-bottom: 2rem;
        font-weight: 500;
    }}
    
    /* TOOLTIP STYLES - AUTOMATIC TERM SIMPLIFICATION */
    .tooltip-term {{
        position: relative;
        display: inline;
        color: #2b6cb0;
        font-weight: 600;
        cursor: help;
        border-bottom: 2px dotted #2b6cb0;
        text-decoration: none;
    }}
    
    .tooltip-icon {{
        display: inline-block;
        margin-left: 2px;
        font-size: 0.8em;
        color: #2b6cb0;
        opacity: 0.7;
    }}
    
    .tooltip-text {{
        visibility: hidden;
        opacity: 0;
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        color: #ffffff;
        text-align: center;
        border-radius: 8px;
        padding: 12px 16px;
        z-index: 1000;
        width: 280px;
        font-size: 0.9rem;
        font-weight: 400;
        line-height: 1.4;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        pointer-events: none;
    }}
    
    .tooltip-text::after {{
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -8px;
        border-width: 8px;
        border-style: solid;
        border-color: #1a202c transparent transparent transparent;
    }}
    
    .tooltip-term:hover .tooltip-text {{
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(-5px);
    }}
    
    .tooltip-term:hover .tooltip-icon {{
        opacity: 1;
        transform: scale(1.2);
    }}
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {{
        background-color: #ffffff !important;
        color: #1a202c !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {{
        border-color: #48bb78 !important;
        box-shadow: 0 0 0 3px rgba(72, 187, 120, 0.1) !important;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3) !important;
    }}
    
    /* OAuth buttons */
    .oauth-button {{
        background: #ffffff;
        color: #1a202c;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        margin: 0.5rem 0;
        font-weight: 600;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
    }}
    
    .oauth-button:hover {{
        border-color: #48bb78;
        box-shadow: 0 2px 8px rgba(72, 187, 120, 0.2);
        transform: translateY(-1px);
    }}
    
    .oauth-button.google {{
        border-color: #4285f4;
    }}
    
    .oauth-button.google:hover {{
        border-color: #3367d6;
        box-shadow: 0 2px 8px rgba(66, 133, 244, 0.2);
    }}
    
    .oauth-button.facebook {{
        border-color: #1877f2;
    }}
    
    .oauth-button.facebook:hover {{
        border-color: #166fe5;
        box-shadow: 0 2px 8px rgba(24, 119, 242, 0.2);
    }}
    
    /* Content with automatic tooltips */
    .content-with-tooltips {{
        line-height: 1.8;
        font-size: 1.1rem;
        color: #2d3748;
    }}
    
    /* Campaign form styling */
    .campaign-form {{
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }}
    
    /* File upload styling */
    .stFileUploader > div > div {{
        background-color: #f7fafc !important;
        border: 2px dashed #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 2rem !important;
        text-align: center !important;
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .logo-image {{
            max-width: 200px;
        }}
        
        .main-content {{
            margin: 0.5rem;
            padding: 1rem;
        }}
        
        .tagline {{
            font-size: 1rem;
        }}
        
        .tooltip-text {{
            width: 240px;
            font-size: 0.8rem;
        }}
    }}
    
    @media (max-width: 480px) {{
        .logo-image {{
            max-width: 180px;
        }}
        
        .main-content {{
            margin: 0.25rem;
            padding: 0.75rem;
        }}
        
        .tooltip-text {{
            width: 200px;
            font-size: 0.75rem;
        }}
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

# ========================================
# SIDEBAR NAVIGATION
# ========================================

def render_sidebar():
    """Render the left sidebar with navigation and language selection"""
    with st.sidebar:
        # Language Selection
        st.markdown("### 🌍 Select Language:")
        
        languages = get_supported_languages()
        language_options = {lang["native"]: lang["code"] for lang in languages}
        
        selected_language_name = st.selectbox(
            "Choose your language",
            options=list(language_options.keys()),
            index=0,
            key="language_selector"
        )
        
        selected_language = language_options[selected_language_name]
        st.session_state.selected_language = selected_language
        
        st.markdown("---")
        
        # Show different navigation based on login status
        if st.session_state.get('logged_in', False):
            # Post-login navigation
            st.markdown("### 🧭 Navigation")
            
            # Home button
            if st.button("🏠 Home", key="nav_home", help="Go to home page"):
                st.session_state.current_page = "home"
                st.rerun()
            
            # Explore button
            if st.button("🔍 Explore", key="nav_explore", help="Explore campaigns"):
                st.session_state.current_page = "explore"
                st.rerun()
            
            # Search button
            if st.button("🔎 Search", key="nav_search", help="Search campaigns"):
                st.session_state.current_page = "search"
                st.rerun()
            
            st.markdown("---")
            
            # Create Campaign button
            st.markdown("""
            <div class="create-button" onclick="document.getElementById('create_campaign').click()">
                ➕ Create Campaign
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("", key="create_campaign", help="Create a new campaign"):
                st.session_state.current_page = "create_campaign"
                st.rerun()
            
            st.markdown("---")
            
            # Backend connection status
            backend_status = "🟢 Online" if check_backend_health() else "🔴 Offline"
            st.markdown(f"**Backend:** {backend_status}")
            
            # Profile button at bottom
            st.markdown("---")
            st.markdown("""
            <div class="profile-button" onclick="document.getElementById('profile').click()">
                👤
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("", key="profile", help="Go to your profile"):
                st.session_state.current_page = "profile"
                st.rerun()
        
        else:
            # Pre-login sidebar (minimal)
            st.markdown("### 📊 System Status")
            backend_status = "🟢 Online" if check_backend_health() else "🔴 Offline"
            st.markdown(f"**Backend:** {backend_status}")

def check_backend_health() -> bool:
    """Check if backend is healthy"""
    try:
        result = make_api_request("/health")
        return "error" not in result and result.get("status") == "healthy"
    except Exception:
        return False

# ========================================
# PAGE COMPONENTS
# ========================================

def render_header():
    """Render the main header with logo and tagline"""
    logo_base64 = get_logo_base64()
    
    if logo_base64:
        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" class="logo-image" alt="HAVEN Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="logo-container">
            <h1 style="color: #2d3748; font-size: 3rem; margin: 0;">HAVEN</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tagline">
        Help not just some people, but Help Humanity.
    </div>
    """, unsafe_allow_html=True)

def render_login_page():
    """Render the login page with OAuth buttons"""
    st.markdown("## 🔐 Login to HAVEN")
    
    # Login form
    with st.form("login_form"):
        email = st.text_input("📧 Email Address", placeholder="Enter your email")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        login_button = st.form_submit_button("🚀 Continue")
    
    if login_button:
        if email and password:
            # Mock login for demo
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.current_page = "home"
            st.rerun()
        else:
            st.error("Please enter both email and password")
    
    # OAuth buttons
    st.markdown("### 🔗 Or sign in with:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Sign in with Google", key="google_login", use_container_width=True):
            # Mock Google OAuth
            st.session_state.logged_in = True
            st.session_state.user_email = "user@gmail.com"
            st.session_state.current_page = "home"
            st.rerun()
    
    with col2:
        if st.button("📘 Sign in with Facebook", key="facebook_login", use_container_width=True):
            # Mock Facebook OAuth
            st.session_state.logged_in = True
            st.session_state.user_email = "user@facebook.com"
            st.session_state.current_page = "home"
            st.rerun()
    
    # Registration link
    st.markdown("---")
    st.markdown("**Not registered?** [Create an account](#)")

def render_home_page():
    """Render the home page with automatic term simplification"""
    st.markdown("## 🏠 Welcome to HAVEN")
    
    # Welcome message with automatic tooltips
    welcome_text = """
    Welcome to HAVEN, the revolutionary crowdfunding platform that's transforming how startups and entrepreneurs raise capital. 
    Our innovative approach combines traditional investment strategies with cutting-edge technology to create unprecedented 
    opportunities for both investors and project creators.
    
    Whether you're seeking funding for medical treatment, supporting an NGO or charity, or launching your next big idea, 
    HAVEN provides the tools and community you need to succeed.
    """
    
    welcome_with_tooltips = add_tooltips_to_text(welcome_text)
    
    st.markdown(f"""
    <div class="content-with-tooltips">
    {welcome_with_tooltips}
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    st.markdown("### 🎯 Platform Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        feature_text = """
        **🌐 Multi-language Support**
        - English, Hindi, Tamil, Telugu
        - Real-time translation
        - Localized content
        """
        feature_with_tooltips = add_tooltips_to_text(feature_text)
        st.markdown(f'<div class="content-with-tooltips">{feature_with_tooltips}</div>', unsafe_allow_html=True)
    
    with col2:
        feature_text = """
        **📝 Smart Simplification**
        - Automatic term detection
        - Hover tooltips for complex terms
        - Context-aware definitions
        """
        feature_with_tooltips = add_tooltips_to_text(feature_text)
        st.markdown(f'<div class="content-with-tooltips">{feature_with_tooltips}</div>', unsafe_allow_html=True)
    
    with col3:
        feature_text = """
        **🔐 Secure Authentication**
        - Google OAuth integration
        - Facebook OAuth integration
        - Secure session management
        """
        feature_with_tooltips = add_tooltips_to_text(feature_text)
        st.markdown(f'<div class="content-with-tooltips">{feature_with_tooltips}</div>', unsafe_allow_html=True)

def render_explore_page():
    """Render the explore page"""
    st.markdown("## 🔍 Explore Campaigns")
    
    # Campaign categories
    st.markdown("### 📂 Campaign Categories")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏥 Medical Treatment", use_container_width=True):
            st.info("Showing medical treatment campaigns...")
    
    with col2:
        if st.button("🤝 NGO / Charity", use_container_width=True):
            st.info("Showing NGO and charity campaigns...")
    
    with col3:
        if st.button("💡 Other Causes", use_container_width=True):
            st.info("Showing other cause campaigns...")
    
    # Sample campaigns with tooltips
    st.markdown("### 🌟 Featured Campaigns")
    
    sample_campaigns = [
        {
            "title": "Emergency Surgery Fund",
            "description": "Help raise funds for life-saving surgery for a young entrepreneur who needs immediate medical treatment.",
            "raised": "$15,000",
            "goal": "$50,000"
        },
        {
            "title": "Clean Water NGO Project",
            "description": "Support our charity initiative to provide clean water access to rural communities through innovative technology.",
            "raised": "$8,500",
            "goal": "$25,000"
        },
        {
            "title": "Educational Startup Platform",
            "description": "Invest in our revolutionary AI-powered platform that's transforming online education for students worldwide.",
            "raised": "$75,000",
            "goal": "$200,000"
        }
    ]
    
    for campaign in sample_campaigns:
        with st.expander(f"📋 {campaign['title']}", expanded=False):
            description_with_tooltips = add_tooltips_to_text(campaign['description'])
            st.markdown(f'<div class="content-with-tooltips">{description_with_tooltips}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Raised", campaign['raised'])
            with col2:
                st.metric("Goal", campaign['goal'])

def render_search_page():
    """Render the search page"""
    st.markdown("## 🔎 Search Campaigns")
    
    # Search form
    with st.form("search_form"):
        search_query = st.text_input("🔍 Search for campaigns", placeholder="Enter keywords...")
        
        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.selectbox("Category", ["All", "Medical Treatment", "NGO / Charity", "Other Cause"])
        with col2:
            amount_filter = st.selectbox("Funding Goal", ["All", "Under $10K", "$10K - $50K", "Over $50K"])
        
        search_button = st.form_submit_button("🔍 Search")
    
    if search_button and search_query:
        st.success(f"Searching for: '{search_query}' in {category_filter} category with {amount_filter} funding goal")
        
        # Mock search results with tooltips
        search_text = f"""
        Found 12 campaigns matching your search for '{search_query}'. These include various startups, 
        NGO projects, and medical treatment fundraising campaigns. Each campaign has been verified 
        for authenticity and compliance with our platform guidelines.
        """
        
        search_with_tooltips = add_tooltips_to_text(search_text)
        st.markdown(f'<div class="content-with-tooltips">{search_with_tooltips}</div>', unsafe_allow_html=True)

def render_create_campaign_page():
    """Render the create campaign page"""
    st.markdown("## ➕ Create New Campaign")
    
    with st.form("campaign_form"):
        st.markdown("### 📋 Campaign Details")
        
        # Purpose dropdown (first question as requested)
        purpose = st.selectbox(
            "Purpose of raising fund *",
            ["Select purpose...", "Medical Treatment", "NGO / Charity", "Other Cause"],
            help="Choose the main purpose for your fundraising campaign"
        )
        
        # Campaign name
        campaign_name = st.text_input(
            "Campaign Name *",
            placeholder="Enter a clear, descriptive name for your campaign"
        )
        
        # Basic description (second detail as requested)
        description = st.text_area(
            "Basic Description *",
            placeholder="Provide a detailed description of your campaign, including why you need funding and how it will be used...",
            height=150,
            help="Explain your campaign clearly - this will be automatically enhanced with helpful tooltips for complex terms"
        )
        
        # Funding goal
        funding_goal = st.number_input(
            "Funding Goal (USD) *",
            min_value=100,
            max_value=1000000,
            value=5000,
            step=100
        )
        
        # Campaign duration
        duration = st.selectbox(
            "Campaign Duration",
            ["30 days", "60 days", "90 days", "120 days"]
        )
        
        # Pictures/Media (third detail as requested)
        st.markdown("### 📸 Pictures of Actions")
        uploaded_files = st.file_uploader(
            "Upload images that show your cause, progress, or planned actions",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="Upload clear, relevant images that help tell your story"
        )
        
        # Additional details
        st.markdown("### 📝 Additional Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            contact_email = st.text_input("Contact Email *", placeholder="your.email@example.com")
            phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567")
        
        with col2:
            location = st.text_input("Location", placeholder="City, State/Country")
            website = st.text_input("Website (optional)", placeholder="https://yourwebsite.com")
        
        # Terms and conditions
        terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
        
        # Submit button
        submit_button = st.form_submit_button("🚀 Create Campaign")
    
    if submit_button:
        if purpose == "Select purpose...":
            st.error("Please select a purpose for your campaign")
        elif not campaign_name:
            st.error("Please enter a campaign name")
        elif not description:
            st.error("Please provide a campaign description")
        elif not contact_email:
            st.error("Please provide a contact email")
        elif not terms_accepted:
            st.error("Please accept the terms and conditions")
        else:
            st.success("🎉 Campaign created successfully!")
            st.balloons()
            
            # Show preview with tooltips
            st.markdown("### 📋 Campaign Preview")
            
            preview_text = f"""
            **{campaign_name}**
            
            Purpose: {purpose}
            Goal: ${funding_goal:,}
            Duration: {duration}
            
            {description}
            """
            
            preview_with_tooltips = add_tooltips_to_text(preview_text)
            st.markdown(f'<div class="content-with-tooltips">{preview_with_tooltips}</div>', unsafe_allow_html=True)
            
            if uploaded_files:
                st.markdown("**Uploaded Images:**")
                for file in uploaded_files:
                    st.image(file, caption=file.name, width=200)

def render_profile_page():
    """Render the profile page"""
    st.markdown("## 👤 Your Profile")
    
    # User info
    user_email = st.session_state.get('user_email', 'user@example.com')
    st.markdown(f"**Email:** {user_email}")
    
    # Profile type selection
    profile_type = st.radio(
        "Profile Type",
        ["Individual", "Organization"],
        help="Select whether you're an individual or representing an organization"
    )
    
    if profile_type == "Individual":
        st.markdown("### 👤 Individual Profile")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", value="John Doe")
            st.text_input("Phone Number", value="+1 (555) 123-4567")
        with col2:
            st.text_input("Location", value="New York, USA")
            st.date_input("Date of Birth")
        
        st.text_area("Bio", placeholder="Tell us about yourself...")
    
    else:
        st.markdown("### 🏢 Organization Profile")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Organization Name", value="ACME Foundation")
            st.selectbox("Organization Type", ["NGO", "Startup", "Charity", "Other"])
        with col2:
            st.text_input("Contact Person", value="Jane Smith")
            st.text_input("Registration Number", value="REG123456")
        
        st.text_area("Organization Description", placeholder="Describe your organization's mission and activities...")
    
    # Campaign history
    st.markdown("### 📊 Your Campaigns")
    
    campaign_history_text = """
    You have created 2 campaigns with a total funding goal of $75,000. Your campaigns have received 
    strong community support with an average success rate of 85%. Your most successful campaign 
    was for medical treatment which exceeded its funding goal by 120%.
    """
    
    history_with_tooltips = add_tooltips_to_text(campaign_history_text)
    st.markdown(f'<div class="content-with-tooltips">{history_with_tooltips}</div>', unsafe_allow_html=True)
    
    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.current_page = "login"
        st.rerun()

# ========================================
# MAIN APPLICATION
# ========================================

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="HAVEN - Crowdfunding Platform",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load CSS
    load_css()
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "en"
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    with st.container():
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        # Render header
        render_header()
        
        # Route to appropriate page
        if not st.session_state.logged_in:
            render_login_page()
        else:
            current_page = st.session_state.get('current_page', 'home')
            
            if current_page == "home":
                render_home_page()
            elif current_page == "explore":
                render_explore_page()
            elif current_page == "search":
                render_search_page()
            elif current_page == "create_campaign":
                render_create_campaign_page()
            elif current_page == "profile":
                render_profile_page()
            else:
                render_home_page()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

