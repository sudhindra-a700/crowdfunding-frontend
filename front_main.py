import streamlit as st
import requests
import json
import base64
import os
from datetime import datetime, timedelta
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
BACKEND_URL = os.environ.get("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")

# HAVEN Logo (without white background)
HAVEN_LOGO_SVG = """
<svg width="200" height="60" viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg">
  <!-- House 1 -->
  <g transform="translate(10, 15)">
    <polygon points="15,5 25,15 15,15" fill="#2d5a27" stroke="#1a3d1a" stroke-width="1"/>
    <rect x="10" y="15" width="12" height="12" fill="#4a7c59" stroke="#2d5a27" stroke-width="1"/>
    <rect x="13" y="18" width="3" height="6" fill="#2d5a27"/>
  </g>
  
  <!-- House 2 -->
  <g transform="translate(35, 12)">
    <polygon points="12,8 20,16 16,16" fill="#2d5a27" stroke="#1a3d1a" stroke-width="1"/>
    <rect x="8" y="16" width="9" height="9" fill="#4a7c59" stroke="#2d5a27" stroke-width="1"/>
    <rect x="10" y="19" width="2" height="4" fill="#2d5a27"/>
  </g>
  
  <!-- Leaves -->
  <g transform="translate(55, 20)">
    <ellipse cx="5" cy="8" rx="4" ry="6" fill="#6b8e23" transform="rotate(15 5 8)"/>
    <ellipse cx="12" cy="6" rx="3" ry="5" fill="#9acd32" transform="rotate(-20 12 6)"/>
    <ellipse cx="8" cy="12" rx="3" ry="4" fill="#6b8e23" transform="rotate(45 8 12)"/>
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
        margin-bottom: 20px;
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
        background: linear-gradient(135deg, #f0ffff 0%, #e6e6fa 50%, #ffffff 100%);
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
    
    /* Form styling */
    .stTextInput > div > div > input {
        background: #f8fff8;
        border: 2px solid #a8e6cf;
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        color: #2d5a27;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4a7c59;
        box-shadow: 0 0 0 3px rgba(168, 230, 207, 0.3);
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
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin: 5px 0;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #dcedc1 0%, #a8e6cf 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(168, 230, 207, 0.4);
    }
    
    /* OAuth button styling */
    .oauth-button {
        display: inline-block;
        padding: 12px 24px;
        margin: 5px;
        background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%);
        color: #2d5a27;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid #a8e6cf;
    }
    
    .oauth-button:hover {
        background: linear-gradient(135deg, #dcedc1 0%, #a8e6cf 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(168, 230, 207, 0.4);
        text-decoration: none;
        color: #2d5a27;
    }
    
    /* Campaign card styling */
    .campaign-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(168, 230, 207, 0.3);
        transition: all 0.3s ease;
    }
    
    .campaign-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* Progress bar styling */
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #a8e6cf 0%, #4a7c59 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Category grid styling */
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .category-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(168, 230, 207, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .category-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        background: rgba(168, 230, 207, 0.1);
    }
    
    /* Success/Error messages */
    .success-message {
        background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%);
        color: #2d5a27;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #4a7c59;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ffaaa5 0%, #ffd3b6 100%);
        color: #8b0000;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #ff6b6b;
    }
    
    /* Hide Streamlit elements that might show HTML */
    .element-container {
        background: transparent !important;
    }
    
    /* Ensure no HTML code is visible */
    code {
        display: none !important;
    }
    
    pre {
        display: none !important;
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

# API functions
def get_campaigns():
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaigns", timeout=10)
        if response.status_code == 200:
            return response.json().get('campaigns', [])
    except:
        pass
    return []

def get_trending_campaigns():
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaigns/trending", timeout=10)
        if response.status_code == 200:
            return response.json().get('campaigns', [])
    except:
        pass
    return []

def get_categories():
    try:
        response = requests.get(f"{BACKEND_URL}/api/categories", timeout=10)
        if response.status_code == 200:
            return response.json().get('categories', {})
    except:
        pass
    return {}

def search_campaigns(query, category=None):
    try:
        data = {"query": query, "limit": 20}
        if category:
            data["category"] = category
        response = requests.post(f"{BACKEND_URL}/api/search", json=data, timeout=10)
        if response.status_code == 200:
            return response.json().get('campaigns', [])
    except:
        pass
    return []

def create_campaign(campaign_data):
    try:
        response = requests.post(f"{BACKEND_URL}/api/campaigns", json=campaign_data, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# Authentication functions
def show_login():
    st.markdown(f"""
    <div class="header-container">
        <div class="header-logo">
            {HAVEN_LOGO_SVG}
        </div>
        <div class="header-subtitle">Help not just some people, but Help Humanity</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    st.markdown("## Login to HAVEN")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_submitted = st.form_submit_button("Continue")
        with col2:
            if st.form_submit_button("Sign Up"):
                st.session_state.current_page = 'register'
                st.rerun()
    
    if login_submitted and email and password:
        # Simple authentication (in production, verify with backend)
        st.session_state.authenticated = True
        st.session_state.user_data = {"email": email, "name": email.split("@")[0]}
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("### Or continue with:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Google", key="google_login"):
            # OAuth would be handled here
            st.session_state.authenticated = True
            st.session_state.user_data = {"email": "user@gmail.com", "name": "Google User"}
            st.session_state.current_page = 'home'
            st.rerun()
    
    with col2:
        if st.button("📘 Facebook", key="facebook_login"):
            # OAuth would be handled here
            st.session_state.authenticated = True
            st.session_state.user_data = {"email": "user@facebook.com", "name": "Facebook User"}
            st.session_state.current_page = 'home'
            st.rerun()
    
    st.markdown("Don't have an account?")
    if st.button("Create Account"):
        st.session_state.current_page = 'register'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_register():
    st.markdown(f"""
    <div class="header-container">
        <div class="header-logo">
            {HAVEN_LOGO_SVG}
        </div>
        <div class="header-subtitle">Help not just some people, but Help Humanity</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    st.markdown("## Register for HAVEN")
    
    account_type = st.selectbox("Account Type", ["Individual", "Organization"])
    
    if account_type == "Individual":
        with st.form("individual_register"):
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            address = st.text_area("Address")
            
            if st.form_submit_button("Register as Individual"):
                if password == confirm_password:
                    st.success("Registration successful!")
                    st.session_state.authenticated = True
                    st.session_state.user_data = {"email": email, "name": full_name, "type": "individual"}
                    st.session_state.current_page = 'home'
                    st.rerun()
                else:
                    st.error("Passwords do not match!")
    
    else:  # Organization
        with st.form("organization_register"):
            org_name = st.text_input("Organization Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            org_type = st.selectbox("Organization Type", ["NGO", "Startup", "Charity"])
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            description = st.text_area("Organization Description")
            address = st.text_area("Address")
            
            if st.form_submit_button("Register as Organization"):
                if password == confirm_password:
                    st.success("Registration successful!")
                    st.session_state.authenticated = True
                    st.session_state.user_data = {"email": email, "name": org_name, "type": "organization"}
                    st.session_state.current_page = 'home'
                    st.rerun()
                else:
                    st.error("Passwords do not match!")
    
    if st.button("Back to Login"):
        st.session_state.current_page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_header():
    st.markdown(f"""
    <div class="header-container">
        <div class="header-logo">
            {HAVEN_LOGO_SVG}
        </div>
        <div class="header-subtitle">Help not just some people, but Help Humanity</div>
    </div>
    """, unsafe_allow_html=True)

def show_sidebar():
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.user_data.get('name', 'User')}!")
        
        if st.button("🏠 Home"):
            st.session_state.current_page = 'home'
            st.rerun()
        
        if st.button("🔍 Explore"):
            st.session_state.current_page = 'explore'
            st.rerun()
        
        if st.button("🔎 Search"):
            st.session_state.current_page = 'search'
            st.rerun()
        
        if st.button("➕ Create Campaign"):
            st.session_state.current_page = 'create'
            st.rerun()
        
        if st.button("👤 Profile"):
            st.session_state.current_page = 'profile'
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_data = {}
            st.session_state.current_page = 'login'
            st.rerun()

def show_campaign_card(campaign):
    st.markdown(f"""
    <div class="campaign-card">
        <img src="{campaign.get('image_url', 'https://via.placeholder.com/600x400/4CAF50/FFFFFF?text=Campaign')}" 
             style="width: 100%; height: 200px; object-fit: cover; border-radius: 10px; margin-bottom: 15px;">
        <h3 style="color: #2d5a27; margin: 10px 0;">{campaign['title']}</h3>
        <p style="color: #4a7c59; margin: 10px 0;">{campaign['description'][:100]}...</p>
        <p style="color: #2d5a27; font-weight: bold;">by {campaign['creator']}</p>
        
        <div class="progress-bar">
            <div class="progress-fill" style="width: {campaign['percentage']}%;"></div>
        </div>
        
        <div style="display: flex; justify-content: space-between; margin: 10px 0;">
            <span style="color: #4a7c59;"><strong>₹{campaign['raised']:,}</strong> raised</span>
            <span style="color: #4a7c59;"><strong>{campaign['percentage']}%</strong> funded</span>
            <span style="color: #4a7c59;"><strong>{campaign['days_left']}</strong> days left</span>
        </div>
        
        <div style="text-align: center; margin-top: 15px;">
            <button style="background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%); 
                           color: #2d5a27; border: none; padding: 10px 20px; 
                           border-radius: 8px; font-weight: bold; cursor: pointer;">
                View Campaign
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_home():
    show_header()
    
    st.markdown("## 🔥 Trending Campaigns")
    
    campaigns = get_trending_campaigns()
    if not campaigns:
        campaigns = [
            {
                "id": 1,
                "title": "Clean Water for Rural Villages",
                "description": "Providing clean drinking water access to 500 families in rural Maharashtra",
                "goal": 500000,
                "raised": 325000,
                "percentage": 65,
                "days_left": 15,
                "creator": "Water for All NGO",
                "image_url": "https://via.placeholder.com/600x400/4CAF50/FFFFFF?text=Clean+Water+Project"
            },
            {
                "id": 2,
                "title": "Education for Underprivileged Children",
                "description": "Building a school and providing education materials for 200 children in slums",
                "goal": 750000,
                "raised": 450000,
                "percentage": 60,
                "days_left": 25,
                "creator": "Bright Future Foundation",
                "image_url": "https://via.placeholder.com/600x400/2196F3/FFFFFF?text=Education+Project"
            },
            {
                "id": 3,
                "title": "Medical Treatment for Cancer Patients",
                "description": "Providing free cancer treatment and medicines for 50 patients from low-income families",
                "goal": 1000000,
                "raised": 780000,
                "percentage": 78,
                "days_left": 8,
                "creator": "Hope Cancer Care",
                "image_url": "https://via.placeholder.com/600x400/E91E63/FFFFFF?text=Cancer+Treatment"
            }
        ]
    
    for campaign in campaigns:
        show_campaign_card(campaign)

def show_explore():
    show_header()
    
    st.markdown("## 🔍 Explore Categories")
    
    categories = get_categories()
    if not categories:
        categories = {
            "Art & Design": {"icon": "🎨", "count": 12},
            "Technology": {"icon": "💻", "count": 8},
            "Community": {"icon": "👥", "count": 15},
            "Film & Video": {"icon": "🎬", "count": 6},
            "Music": {"icon": "🎵", "count": 9},
            "Publishing": {"icon": "📚", "count": 4},
            "Education": {"icon": "🎓", "count": 11},
            "Medical": {"icon": "🏥", "count": 7},
            "Environment": {"icon": "🌱", "count": 5}
        }
    
    # Create category grid
    cols = st.columns(3)
    for i, (category, info) in enumerate(categories.items()):
        with cols[i % 3]:
            if st.button(f"{info['icon']} {category}\n{info['count']} campaigns", key=f"cat_{i}"):
                st.session_state.current_page = 'search'
                st.session_state.search_category = category
                st.rerun()

def show_search():
    show_header()
    
    st.markdown("## 🔎 Search Campaigns")
    
    search_query = st.text_input("Search for campaigns...", placeholder="Enter keywords to search")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🔍 Search"):
            if search_query:
                results = search_campaigns(search_query)
                st.markdown(f"### Search Results for '{search_query}'")
                for campaign in results:
                    show_campaign_card(campaign)
    
    with col2:
        st.markdown("### Quick Filters")
        if st.button("Medical"):
            results = search_campaigns("medical")
            for campaign in results:
                show_campaign_card(campaign)

def show_create_campaign():
    show_header()
    
    st.markdown("## ➕ Create New Campaign")
    
    with st.form("create_campaign"):
        purpose = st.selectbox("Purpose", ["Medical Treatment", "NGO / Charity", "Other Cause"])
        title = st.text_input("Campaign Title")
        description = st.text_area("Campaign Description")
        goal = st.number_input("Funding Goal (₹)", min_value=1000, value=100000)
        duration = st.number_input("Campaign Duration (days)", min_value=1, max_value=365, value=30)
        category = st.selectbox("Category", ["Medical", "Education", "Community", "Environment", "Technology"])
        
        st.markdown("### Contact Information")
        creator = st.text_input("Creator/Organization Name")
        location = st.text_input("Location")
        contact_email = st.text_input("Contact Email")
        contact_phone = st.text_input("Contact Phone")
        
        if st.form_submit_button("Create Campaign"):
            campaign_data = {
                "title": title,
                "description": description,
                "goal": goal,
                "duration": duration,
                "category": category,
                "creator": creator,
                "location": location,
                "contact_email": contact_email,
                "contact_phone": contact_phone,
                "purpose": purpose
            }
            
            result = create_campaign(campaign_data)
            if result:
                st.success("Campaign created successfully!")
                st.session_state.current_page = 'home'
                st.rerun()
            else:
                st.error("Failed to create campaign. Please try again.")

def show_profile():
    show_header()
    
    st.markdown("## 👤 Profile")
    
    user_data = st.session_state.user_data
    
    st.markdown(f"**Name:** {user_data.get('name', 'N/A')}")
    st.markdown(f"**Email:** {user_data.get('email', 'N/A')}")
    st.markdown(f"**Account Type:** {user_data.get('type', 'individual').title()}")
    
    st.markdown("### Account Settings")
    
    with st.form("profile_update"):
        new_name = st.text_input("Name", value=user_data.get('name', ''))
        new_email = st.text_input("Email", value=user_data.get('email', ''))
        
        if st.form_submit_button("Update Profile"):
            st.session_state.user_data.update({"name": new_name, "email": new_email})
            st.success("Profile updated successfully!")

# Main application
def main():
    load_css()
    init_session_state()
    
    if not st.session_state.authenticated:
        if st.session_state.current_page == 'register':
            show_register()
        else:
            show_login()
    else:
        show_sidebar()
        
        if st.session_state.current_page == 'home':
            show_home()
        elif st.session_state.current_page == 'explore':
            show_explore()
        elif st.session_state.current_page == 'search':
            show_search()
        elif st.session_state.current_page == 'create':
            show_create_campaign()
        elif st.session_state.current_page == 'profile':
            show_profile()
        else:
            show_home()

if __name__ == "__main__":
    main()

