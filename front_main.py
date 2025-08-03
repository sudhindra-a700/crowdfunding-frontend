import streamlit as st
import requests
import json
import base64
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional, Any
import re

# Page configuration
st.set_page_config(
    page_title="HAVEN - Help Humanity",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Environment variables
BACKEND_URL = os.getenv("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")

# HAVEN Logo (without white background)
HAVEN_LOGO_SVG = """
<svg width="200" height="60" viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg">
  <!-- House 1 -->
  <g transform="translate(10, 15)">
    <polygon points="15,5 25,15 5,15" fill="#2d5a27" stroke="#1a3d1a" stroke-width="1"/>
    <rect x="7" y="15" width="16" height="12" fill="#4a7c59" stroke="#2d5a27" stroke-width="1"/>
    <rect x="10" y="18" width="4" height="6" fill="#2d5a27"/>
    <rect x="16" y="18" width="3" height="3" fill="#87ceeb"/>
  </g>
  
  <!-- House 2 -->
  <g transform="translate(35, 12)">
    <polygon points="12,8 20,16 4,16" fill="#2d5a27" stroke="#1a3d1a" stroke-width="1"/>
    <rect x="6" y="16" width="12" height="15" fill="#4a7c59" stroke="#2d5a27" stroke-width="1"/>
    <rect x="8" y="20" width="3" height="7" fill="#2d5a27"/>
    <rect x="13" y="20" width="2" height="2" fill="#87ceeb"/>
  </g>
  
  <!-- Leaves -->
  <g transform="translate(55, 20)">
    <ellipse cx="5" cy="8" rx="4" ry="6" fill="#6b8e23" transform="rotate(-20 5 8)"/>
    <ellipse cx="12" cy="6" rx="3" ry="5" fill="#9acd32" transform="rotate(15 12 6)"/>
    <ellipse cx="8" cy="12" rx="3" ry="4" fill="#8fbc8f" transform="rotate(-10 8 12)"/>
  </g>
  
  <!-- HAVEN Text -->
  <text x="80" y="35" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#2d5a27">HAVEN</text>
</svg>
"""

# Custom CSS for proper styling
def load_css():
    st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main {
        padding: 0;
        margin: 0;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #e0ffcd 0%, #fdffcd 50%, #ffebbb 100%);
        padding: 20px;
        text-align: center;
        border-bottom: 2px solid #a8e6cf;
        margin-bottom: 0;
    }
    
    .header-logo {
        margin-bottom: 10px;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2d5a27;
        margin: 10px 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: #4a7c59;
        font-style: italic;
        margin: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #a8e6cf 0%, #dcedc1 100%);
    }
    
    /* Content area styling */
    .content-container {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6e6fa 50%, #ffffff 100%);
        min-height: 100vh;
        padding: 20px;
    }
    
    /* Authentication container */
    .auth-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 30px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 230, 207, 0.3);
    }
    
    .auth-title {
        text-align: center;
        color: #2d5a27;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 30px;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        background: rgba(240, 248, 255, 0.8);
        border: 2px solid #a8e6cf;
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        color: #2d3748;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4299e1;
        box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%);
        color: #2d5a27;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #dcedc1 0%, #a8e6cf 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(168, 230, 207, 0.4);
    }
    
    /* OAuth buttons */
    .oauth-container {
        margin: 20px 0;
        text-align: center;
    }
    
    .oauth-button {
        display: inline-block;
        margin: 5px;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .google-btn {
        background: #4285f4;
        color: white;
    }
    
    .google-btn:hover {
        background: #357ae8;
        transform: translateY(-2px);
    }
    
    .facebook-btn {
        background: #1877f2;
        color: white;
    }
    
    .facebook-btn:hover {
        background: #166fe5;
        transform: translateY(-2px);
    }
    
    /* Campaign cards */
    .campaign-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(168, 230, 207, 0.3);
        transition: all 0.3s ease;
    }
    
    .campaign-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    
    .campaign-title {
        color: #2d5a27;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .campaign-creator {
        color: #4a7c59;
        font-size: 1rem;
        margin-bottom: 15px;
    }
    
    .campaign-description {
        color: #2d3748;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    
    /* Progress bar */
    .progress-container {
        background: #e2e8f0;
        border-radius: 10px;
        height: 8px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #a8e6cf 0%, #4299e1 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .progress-text {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        color: #4a5568;
        margin-top: 5px;
    }
    
    /* Category grid */
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .category-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(168, 230, 207, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .category-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        background: rgba(168, 230, 207, 0.1);
    }
    
    .category-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        color: #4299e1;
    }
    
    .category-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2d5a27;
        margin-bottom: 5px;
    }
    
    .category-count {
        font-size: 0.9rem;
        color: #4a5568;
    }
    
    /* Search styling */
    .search-container {
        max-width: 600px;
        margin: 40px auto;
        text-align: center;
    }
    
    .search-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2d5a27;
        margin-bottom: 20px;
    }
    
    .search-subtitle {
        font-size: 1.1rem;
        color: #4a5568;
        margin-bottom: 30px;
    }
    
    /* Navigation styling */
    .nav-container {
        background: rgba(168, 230, 207, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .nav-button {
        background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%);
        color: #2d5a27;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        margin: 5px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        background: linear-gradient(135deg, #dcedc1 0%, #a8e6cf 100%);
        transform: translateY(-2px);
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
    }
    
    /* Hide Streamlit elements that show code */
    .stCodeBlock {
        display: none !important;
    }
    
    .stMarkdown pre {
        display: none !important;
    }
    
    /* Ensure proper text rendering */
    .stMarkdown {
        color: #2d3748;
    }
    
    /* Error message styling */
    .error-message {
        background: #fed7d7;
        color: #c53030;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #e53e3e;
        margin: 10px 0;
    }
    
    /* Success message styling */
    .success-message {
        background: #c6f6d5;
        color: #2f855a;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #38a169;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = 'English'

# API helper functions
def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API request to backend"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error: {response.status_code}"}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}

# Header component
def render_header():
    """Render the main header with logo"""
    st.markdown(f"""
    <div class="header-container">
        <div class="header-logo">
            {HAVEN_LOGO_SVG}
        </div>
        <div class="header-subtitle">Help not just some people, but Help Humanity</div>
    </div>
    """, unsafe_allow_html=True)

# Authentication functions
def render_login_page():
    """Render login page"""
    render_header()
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-container">
        <h2 class="auth-title">Login to HAVEN</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Login form
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.button("Continue", key="login_btn"):
                if email and password:
                    # Simulate login (replace with actual authentication)
                    st.session_state.authenticated = True
                    st.session_state.user_data = {"email": email, "name": "User"}
                    st.session_state.current_page = 'home'
                    st.rerun()
                else:
                    st.error("Please enter both email and password")
            
            # OAuth buttons
            st.markdown("""
            <div class="oauth-container">
                <p style="color: #4a5568; margin: 20px 0 10px 0;">Or continue with:</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_g, col_f = st.columns(2)
            
            with col_g:
                if st.button("🔍 Google", key="google_oauth"):
                    # Simulate OAuth login
                    st.session_state.authenticated = True
                    st.session_state.user_data = {"email": "user@gmail.com", "name": "Google User"}
                    st.session_state.current_page = 'home'
                    st.rerun()
            
            with col_f:
                if st.button("📘 Facebook", key="facebook_oauth"):
                    # Simulate OAuth login
                    st.session_state.authenticated = True
                    st.session_state.user_data = {"email": "user@facebook.com", "name": "Facebook User"}
                    st.session_state.current_page = 'home'
                    st.rerun()
            
            # Registration link
            st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <p style="color: #4a5568;">Don't have an account?</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Sign Up", key="signup_btn"):
                st.session_state.current_page = 'register'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_register_page():
    """Render registration page"""
    render_header()
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-container">
        <h2 class="auth-title">Join HAVEN</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Account type selection
            account_type = st.selectbox(
                "Account Type",
                ["Individual", "Organization"],
                help="Choose your account type"
            )
            
            if account_type == "Individual":
                # Individual registration form
                full_name = st.text_input("Full Name", placeholder="Enter your full name")
                email = st.text_input("Email", placeholder="Enter your email")
                phone = st.text_input("Phone", placeholder="Enter your phone number")
                password = st.text_input("Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                address = st.text_area("Address", placeholder="Enter your address")
                
            else:
                # Organization registration form
                org_name = st.text_input("Organization Name", placeholder="Enter organization name")
                email = st.text_input("Email", placeholder="Enter organization email")
                phone = st.text_input("Phone", placeholder="Enter organization phone")
                org_type = st.selectbox("Organization Type", ["NGO", "Startup", "Charity", "Other"])
                password = st.text_input("Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                description = st.text_area("Description", placeholder="Describe your organization")
                address = st.text_area("Address", placeholder="Enter organization address")
            
            if st.button("Create Account", key="register_btn"):
                # Simulate registration
                st.success("Account created successfully!")
                st.session_state.current_page = 'login'
                st.rerun()
            
            if st.button("Back to Login", key="back_login_btn"):
                st.session_state.current_page = 'login'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main application pages
def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            {HAVEN_LOGO_SVG}
        </div>
        """, unsafe_allow_html=True)
        
        # Language selector
        languages = ["English", "हिन्दी (Hindi)", "தமிழ் (Tamil)", "తెలుగు (Telugu)"]
        selected_lang = st.selectbox("🌍 Language", languages, index=0)
        st.session_state.selected_language = selected_lang
        
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🏠 Home", key="nav_home"):
            st.session_state.current_page = 'home'
            st.rerun()
        
        if st.button("🔍 Explore", key="nav_explore"):
            st.session_state.current_page = 'explore'
            st.rerun()
        
        if st.button("🔎 Search", key="nav_search"):
            st.session_state.current_page = 'search'
            st.rerun()
        
        st.markdown("---")
        
        # Create campaign button
        if st.button("➕ Create Campaign", key="nav_create"):
            st.session_state.current_page = 'create_campaign'
            st.rerun()
        
        st.markdown("---")
        
        # Backend status
        status = make_api_request("/health")
        if "error" not in status:
            st.success("🟢 Backend Connected")
        else:
            st.error("🔴 Backend Disconnected")
        
        # Profile button at bottom
        st.markdown("<br>" * 5, unsafe_allow_html=True)
        if st.button("👤 Profile", key="nav_profile"):
            st.session_state.current_page = 'profile'
            st.rerun()
        
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.current_page = 'login'
            st.rerun()

def render_home_page():
    """Render trending campaigns homepage"""
    render_header()
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <h1 style="color: #2d5a27; font-size: 2.5rem; margin-bottom: 10px;">Trending Campaigns</h1>
        <p style="color: #4a5568; font-size: 1.2rem;">Support the most popular projects on HAVEN.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get trending campaigns
    campaigns_data = make_api_request("/api/campaigns/trending")
    
    if "error" not in campaigns_data:
        campaigns = campaigns_data.get("trending_campaigns", [])
        
        for campaign in campaigns:
            st.markdown(f"""
            <div class="campaign-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <div style="background: #e2e8f0; width: 100%; height: 200px; border-radius: 8px; margin-bottom: 15px; display: flex; align-items: center; justify-content: center; color: #a0aec0; font-size: 1.2rem;">
                            600 × 400
                        </div>
                        <div class="campaign-title">{campaign['title']}</div>
                        <div class="campaign-creator">By {campaign['creator']}</div>
                        <div class="campaign-description">{campaign['description'][:100]}...</div>
                        
                        <div class="progress-container">
                            <div class="progress-bar" style="width: {campaign.get('percentage', 0)}%;"></div>
                        </div>
                        <div class="progress-text">
                            <span>₹{campaign['raised']:,} raised</span>
                            <span>{campaign.get('percentage', 0)}%</span>
                        </div>
                        <div style="color: #4a5568; font-size: 0.9rem; margin-top: 5px;">
                            ⏰ {campaign.get('days_left', 0)} days left
                        </div>
                    </div>
                    <div style="margin-left: 15px;">
                        <span style="background: #2d3748; color: white; padding: 5px 10px; border-radius: 15px; font-size: 0.8rem;">
                            ⚡ Trending
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Unable to load campaigns. Please check backend connection.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_explore_page():
    """Render explore categories page"""
    render_header()
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <h1 style="color: #2d5a27; font-size: 2.5rem; margin-bottom: 10px;">Explore Categories</h1>
        <p style="color: #4a5568; font-size: 1.2rem;">Discover campaigns by interest.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Categories data
    categories = [
        {"name": "Art & Design", "icon": "🎨", "count": 245},
        {"name": "Technology", "icon": "💻", "count": 189},
        {"name": "Community", "icon": "👥", "count": 312},
        {"name": "Film & Video", "icon": "🎬", "count": 156},
        {"name": "Music", "icon": "🎵", "count": 203},
        {"name": "Publishing", "icon": "📚", "count": 134}
    ]
    
    # Create 2-column grid
    col1, col2 = st.columns(2)
    
    for i, category in enumerate(categories):
        with col1 if i % 2 == 0 else col2:
            if st.button(f"{category['icon']}\n{category['name']}\n{category['count']} campaigns", 
                        key=f"cat_{category['name']}", 
                        help=f"Explore {category['name']} campaigns"):
                st.session_state.current_page = 'search'
                st.session_state.search_category = category['name']
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_search_page():
    """Render search page"""
    render_header()
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="search-container">
        <h1 class="search-title">Search Campaigns</h1>
        <p class="search-subtitle">Enter a term above to search for campaigns.</p>
        <p style="color: #4a5568;">You can search by title, description, or category.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        search_query = st.text_input("", placeholder="Search by keyword, category...", key="search_input")
        
        if st.button("🔍 Search", key="search_btn") or search_query:
            if search_query:
                # Perform search
                search_data = make_api_request("/api/search", "POST", {"query": search_query})
                
                if "error" not in search_data:
                    results = search_data.get("results", [])
                    
                    st.markdown(f"""
                    <div style="margin: 30px 0;">
                        <h3 style="color: #2d5a27;">Search Results ({len(results)} found)</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for result in results:
                        st.markdown(f"""
                        <div class="campaign-card">
                            <div class="campaign-title">{result['title']}</div>
                            <div class="campaign-creator">By {result['creator']}</div>
                            <div class="campaign-description">{result['description'][:150]}...</div>
                            <div style="margin-top: 10px;">
                                <span style="background: #a8e6cf; color: #2d5a27; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem;">
                                    {result['category']}
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Search failed. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_create_campaign_page():
    """Render create campaign page"""
    render_header()
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <h1 style="color: #2d5a27; font-size: 2.5rem; margin-bottom: 10px;">Create Campaign</h1>
        <p style="color: #4a5568; font-size: 1.2rem;">Start your fundraising journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Campaign creation form
            purpose = st.selectbox(
                "Purpose of raising fund",
                ["Medical Treatment", "NGO / Charity", "Other Cause"],
                help="Select the main purpose of your campaign"
            )
            
            title = st.text_input("Campaign Title", placeholder="Enter a compelling title")
            description = st.text_area("Basic Description", placeholder="Describe your campaign in detail")
            
            # Pictures upload
            st.markdown("**Pictures of Actions**")
            uploaded_files = st.file_uploader(
                "Upload images that show your cause",
                accept_multiple_files=True,
                type=['png', 'jpg', 'jpeg']
            )
            
            # Additional details
            goal = st.number_input("Funding Goal (₹)", min_value=1000, value=50000)
            duration = st.number_input("Campaign Duration (days)", min_value=1, max_value=365, value=30)
            
            creator = st.text_input("Creator Name", placeholder="Your name or organization")
            location = st.text_input("Location", placeholder="City, State")
            contact_email = st.text_input("Contact Email", placeholder="contact@example.com")
            contact_phone = st.text_input("Contact Phone", placeholder="+91-XXXXXXXXXX")
            
            if st.button("Create Campaign", key="create_campaign_btn"):
                if title and description and creator:
                    # Create campaign
                    campaign_data = {
                        "title": title,
                        "description": description,
                        "goal": goal,
                        "duration": duration,
                        "category": purpose,
                        "creator": creator,
                        "location": location,
                        "contact_email": contact_email,
                        "contact_phone": contact_phone,
                        "purpose": purpose.lower().replace(" ", "_")
                    }
                    
                    result = make_api_request("/api/campaigns", "POST", campaign_data)
                    
                    if "error" not in result:
                        st.success("Campaign created successfully!")
                        st.session_state.current_page = 'home'
                        st.rerun()
                    else:
                        st.error("Failed to create campaign. Please try again.")
                else:
                    st.error("Please fill in all required fields.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_profile_page():
    """Render profile page"""
    render_header()
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <h1 style="color: #2d5a27; font-size: 2.5rem; margin-bottom: 10px;">Profile</h1>
        <p style="color: #4a5568; font-size: 1.2rem;">Manage your account</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            user_data = st.session_state.user_data
            
            st.markdown(f"""
            <div class="campaign-card">
                <h3 style="color: #2d5a27;">Account Information</h3>
                <p><strong>Name:</strong> {user_data.get('name', 'User')}</p>
                <p><strong>Email:</strong> {user_data.get('email', 'user@example.com')}</p>
                <p><strong>Account Type:</strong> Individual</p>
                <p><strong>Member Since:</strong> January 2025</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main application
def main():
    """Main application function"""
    load_css()
    init_session_state()
    
    # Route to appropriate page
    if not st.session_state.authenticated:
        if st.session_state.current_page == 'register':
            render_register_page()
        else:
            render_login_page()
    else:
        # Render sidebar for authenticated users
        render_sidebar()
        
        # Route to main pages
        if st.session_state.current_page == 'home':
            render_home_page()
        elif st.session_state.current_page == 'explore':
            render_explore_page()
        elif st.session_state.current_page == 'search':
            render_search_page()
        elif st.session_state.current_page == 'create_campaign':
            render_create_campaign_page()
        elif st.session_state.current_page == 'profile':
            render_profile_page()
        else:
            render_home_page()

if __name__ == "__main__":
    main()

