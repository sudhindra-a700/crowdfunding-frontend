import streamlit as st
import requests
import json
import base64
from datetime import datetime, timedelta
import uuid
import os

# Configuration
BACKEND_URL = os.environ.get("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")

# Page configuration
st.set_page_config(
    page_title="HAVEN - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load HAVEN logo
@st.cache_data
def load_logo():
    """Load HAVEN logo from file or use base64 encoded version"""
    try:
        # Try to load from file first
        with open("/home/ubuntu/upload/haven_logo.png", "rb") as f:
            logo_data = f.read()
            return base64.b64encode(logo_data).decode()
    except:
        # Fallback: try from current directory
        try:
            with open("haven_logo.png", "rb") as f:
                logo_data = f.read()
                return base64.b64encode(logo_data).decode()
        except:
            return None

# Safe MaterializeCSS with custom color scheme
def load_safe_materialize():
    st.markdown("""
    <style>
    /* Import MaterializeCSS safely */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom color scheme variables */
    :root {
        --registration-bg: #ffcdd2;    /* Light red for registration */
        --profile-search-bg: #f3e5f5;  /* Light purple for profile and search */
        --trending-login-bg: #e3f2fd;  /* Light blue for trending and login */
        --login-alt-bg: #f1f8e9;       /* Light green for login page */
        --other-bg: #d7ccc8;           /* Light brown for other elements */
        
        --text-dark-1: #263238;        /* Dark blue-grey */
        --text-dark-2: #212121;        /* Dark grey */
        --text-dark-3: #1a237e;        /* Dark blue */
        
        --haven-green: #4caf50;        /* HAVEN brand green */
        --haven-accent: #ff5722;       /* HAVEN accent color */
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, var(--trending-login-bg) 0%, #f8f9fa 100%);
        font-family: 'Roboto', sans-serif;
        font-size: 18px;
    }
    
    /* Increase all font sizes for better readability */
    .stApp, .stApp * {
        font-size: 18px !important;
    }
    
    h1 { font-size: 2.5rem !important; color: var(--text-dark-3); }
    h2 { font-size: 2rem !important; color: var(--text-dark-2); }
    h3 { font-size: 1.6rem !important; color: var(--text-dark-2); }
    h4 { font-size: 1.4rem !important; color: var(--text-dark-1); }
    p { font-size: 1.1rem !important; line-height: 1.6; }
    
    /* Safe MaterializeCSS classes */
    .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
    .row { display: flex; flex-wrap: wrap; margin: 0 -12px; }
    .col { flex: 1; padding: 0 12px; }
    .s12 { width: 100%; }
    .m6 { width: 50%; }
    .l4 { width: 33.333%; }
    .center-align { text-align: center; }
    .right-align { text-align: right; }
    .left-align { text-align: left; }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 16px 0;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Button styling */
    .btn-haven {
        background: var(--haven-green) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    .btn-haven:hover {
        background: #45a049 !important;
        transform: translateY(-1px) !important;
    }
    
    /* Page-specific backgrounds */
    .page-login { background: var(--trending-login-bg); color: var(--text-dark-3); }
    .page-register { background: var(--registration-bg); color: var(--text-dark-1); }
    .page-profile { background: var(--profile-search-bg); color: var(--text-dark-2); }
    .page-search { background: var(--profile-search-bg); color: var(--text-dark-2); }
    .page-trending { background: var(--trending-login-bg); color: var(--text-dark-3); }
    
    /* Progress bar styling */
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, var(--haven-green), #66bb6a);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .container { padding: 0 10px; }
        .row { margin: 0 -6px; }
        .col { padding: 0 6px; }
        .m6, .l4 { width: 100%; }
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.6rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user' not in st.session_state:
    st.session_state.user = None

# API helper functions
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_campaigns(page=1, limit=10, category=None, trending=None):
    """Fetch campaigns from backend API"""
    try:
        params = {"page": page, "limit": limit}
        if category:
            params["category"] = category
        if trending is not None:
            params["trending"] = trending
            
        response = requests.get(f"{BACKEND_URL}/api/campaigns", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch campaigns: {response.status_code}")
            return {"campaigns": [], "pagination": {"total": 0}}
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return {"campaigns": [], "pagination": {"total": 0}}

@st.cache_data(ttl=300)
def fetch_categories():
    """Fetch categories from backend API"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/categories", timeout=10)
        if response.status_code == 200:
            return response.json().get("categories", [])
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching categories: {str(e)}")
        return []

@st.cache_data(ttl=300)
def search_campaigns(query, category=None):
    """Search campaigns via backend API"""
    try:
        params = {"q": query}
        if category:
            params["category"] = category
            
        response = requests.get(f"{BACKEND_URL}/api/search", params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get("campaigns", [])
        else:
            return []
    except Exception as e:
        st.error(f"Error searching campaigns: {str(e)}")
        return []

def display_logo():
    """Display HAVEN logo"""
    logo_base64 = load_logo()
    if logo_base64:
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <img src="data:image/png;base64,{logo_base64}" 
                 style="max-width: 200px; height: auto;" 
                 alt="HAVEN Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h1 style="color: var(--haven-green); font-size: 3rem; margin: 0;">🏠 HAVEN</h1>
            <p style="color: var(--text-dark-2); font-size: 1.2rem; margin: 5px 0;">Crowdfunding Platform</p>
        </div>
        """, unsafe_allow_html=True)

def display_campaign_card(campaign):
    """Display a campaign card using Streamlit native components"""
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(campaign.get('image_url', 'https://picsum.photos/300/200'), 
                    width=300, caption=campaign['organization'])
        
        with col2:
            st.subheader(campaign['title'])
            st.write(campaign['description'][:150] + "..." if len(campaign['description']) > 150 else campaign['description'])
            
            # Progress bar
            progress = campaign.get('progress', 0)
            st.progress(progress / 100)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Raised", f"₹{campaign['current_amount']:,}")
            with col_b:
                st.metric("Goal", f"₹{campaign['target_amount']:,}")
            with col_c:
                st.metric("Days Left", campaign['days_left'])
            
            if st.button(f"Donate Now", key=f"donate_{campaign['id']}", type="primary"):
                st.session_state.selected_campaign = campaign
                st.session_state.page = 'donate'
                st.rerun()

def login_page():
    """Login page with your exact design"""
    st.markdown('<div class="page-login">', unsafe_allow_html=True)
    
    # Display logo
    display_logo()
    
    # Tagline
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <h3 style="color: var(--text-dark-3); font-weight: 300;">Help not just some people, but Help Humanity</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Login/Register tabs
    tab1, tab2 = st.tabs(["Sign In", "Register"])
    
    with tab1:
        st.markdown("### Welcome Back")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            remember = st.checkbox("Remember me")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Sign In", type="primary", use_container_width=True):
                    if email and password:
                        st.session_state.user = {"email": email, "name": "User"}
                        st.session_state.page = 'home'
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Please fill in all fields")
            
            with col2:
                if st.form_submit_button("Register", use_container_width=True):
                    st.session_state.page = 'register'
                    st.rerun()
        
        st.markdown("---")
        st.markdown("**Or continue with:**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Google", use_container_width=True, type="secondary"):
                st.info("OAuth integration coming soon!")
        with col2:
            if st.button("📘 Facebook", use_container_width=True, type="secondary"):
                st.info("OAuth integration coming soon!")
    
    with tab2:
        st.markdown("### Create Account")
        
        with st.form("register_form"):
            account_type = st.selectbox("Account Type", ["Individual", "Organization", "NGO"])
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            address = st.text_area("Address", max_chars=200)
            
            terms = st.checkbox("I agree to the Terms and Conditions")
            newsletter = st.checkbox("Subscribe to newsletter")
            
            if st.form_submit_button("Create Account", type="primary", use_container_width=True):
                if all([first_name, last_name, email, password, confirm_password, terms]):
                    if password == confirm_password:
                        st.session_state.user = {"email": email, "name": f"{first_name} {last_name}"}
                        st.session_state.page = 'home'
                        st.success("Registration successful!")
                        st.rerun()
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all required fields and accept terms")

def home_page():
    """Home page with trending campaigns"""
    st.markdown('<div class="page-trending">', unsafe_allow_html=True)
    
    # Header with logo
    display_logo()
    
    st.markdown("## 🔥 Trending Campaigns")
    
    # Fetch trending campaigns
    campaigns_data = fetch_campaigns(trending=True, limit=6)
    campaigns = campaigns_data.get('campaigns', [])
    
    if campaigns:
        # Display campaigns in grid
        for i in range(0, len(campaigns), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                if i < len(campaigns):
                    display_campaign_card(campaigns[i])
            
            with col2:
                if i + 1 < len(campaigns):
                    display_campaign_card(campaigns[i + 1])
    else:
        st.info("No trending campaigns available at the moment.")
    
    # Quick stats
    st.markdown("---")
    st.markdown("### Platform Statistics")
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Campaigns", stats.get('total_campaigns', 0))
            with col2:
                st.metric("Total Raised", f"₹{stats.get('total_raised', 0):,}")
            with col3:
                st.metric("Total Donors", stats.get('total_donors', 0))
            with col4:
                st.metric("Success Rate", f"{stats.get('success_rate', 0)}%")
    except:
        st.info("Statistics temporarily unavailable")

def explore_page():
    """Explore categories page"""
    st.markdown('<div class="page-profile">', unsafe_allow_html=True)
    
    display_logo()
    st.markdown("## 🔍 Explore Categories")
    
    # Fetch categories
    categories = fetch_categories()
    
    if categories:
        # Display categories in grid
        cols = st.columns(2)
        for i, category in enumerate(categories):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <h4>{category['name']}</h4>
                        <p>{category['count']} campaigns</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View {category['name']}", key=f"cat_{i}"):
                        st.session_state.selected_category = category['name']
                        st.session_state.page = 'category'
                        st.rerun()
    else:
        st.info("Categories are loading...")

def search_page():
    """Search campaigns page"""
    st.markdown('<div class="page-search">', unsafe_allow_html=True)
    
    display_logo()
    st.markdown("## 🔍 Search Campaigns")
    
    # Search form
    with st.form("search_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            query = st.text_input("Search campaigns...", placeholder="Enter keywords, organization name, or campaign title")
        with col2:
            category = st.selectbox("Category", ["All"] + [cat['name'] for cat in fetch_categories()])
        
        if st.form_submit_button("Search", type="primary"):
            if query:
                # Perform search
                search_category = None if category == "All" else category
                results = search_campaigns(query, search_category)
                
                st.markdown(f"### Search Results ({len(results)} found)")
                
                if results:
                    for campaign in results:
                        display_campaign_card(campaign)
                else:
                    st.info("No campaigns found matching your search criteria.")
            else:
                st.warning("Please enter a search query.")

def profile_page():
    """User profile page"""
    st.markdown('<div class="page-profile">', unsafe_allow_html=True)
    
    display_logo()
    
    if st.session_state.user:
        st.markdown(f"## 👤 Welcome, {st.session_state.user['name']}!")
        
        tab1, tab2, tab3 = st.tabs(["Profile", "My Donations", "Settings"])
        
        with tab1:
            st.markdown("### Profile Information")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Name", value=st.session_state.user['name'])
                st.text_input("Email", value=st.session_state.user['email'])
            with col2:
                st.text_input("Phone", placeholder="Add phone number")
                st.text_area("Bio", placeholder="Tell us about yourself")
        
        with tab2:
            st.markdown("### My Donations")
            st.info("Your donation history will appear here.")
        
        with tab3:
            st.markdown("### Settings")
            st.checkbox("Email notifications")
            st.checkbox("SMS notifications")
            if st.button("Logout", type="secondary"):
                st.session_state.user = None
                st.session_state.page = 'login'
                st.rerun()

# Navigation
def render_navigation():
    """Render navigation sidebar"""
    with st.sidebar:
        st.markdown("### Navigation")
        
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("🔍 Search", use_container_width=True):
            st.session_state.page = 'search'
            st.rerun()
        
        if st.button("📂 Explore", use_container_width=True):
            st.session_state.page = 'explore'
            st.rerun()
        
        if st.session_state.user:
            if st.button("👤 Profile", use_container_width=True):
                st.session_state.page = 'profile'
                st.rerun()
        else:
            if st.button("🔑 Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()

# Main app
def main():
    # Load safe MaterializeCSS
    load_safe_materialize()
    
    # Show navigation if logged in
    if st.session_state.user:
        render_navigation()
    
    # Route to appropriate page
    if st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'search':
        search_page()
    elif st.session_state.page == 'explore':
        explore_page()
    elif st.session_state.page == 'profile':
        profile_page()
    else:
        # Default to login
        st.session_state.page = 'login'
        login_page()

if __name__ == "__main__":
    main()

