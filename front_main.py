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
def load_logo():
    """Load HAVEN logo from file or use base64 encoded version"""
    try:
        # Try to load from file first
        with open("/home/ubuntu/upload/haven_logo.png", "rb") as f:
            logo_data = f.read()
            return base64.b64encode(logo_data).decode()
    except:
        # Fallback to a simple text logo if image not found
        return None

logo_base64 = load_logo()

# Safe MaterializeCSS with custom color scheme
def load_safe_materialize_css():
    st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom color scheme variables */
    :root {
        --registration-bg: #ffcdd2;     /* Light red for registration */
        --profile-search-bg: #f3e5f5;  /* Light purple for profile and search */
        --trending-login-bg: #e3f2fd;  /* Light blue for trending and login */
        --login-alt-bg: #f1f8e9;       /* Light green for login page */
        --other-bg: #d7ccc8;           /* Light brown for other elements */
        
        --text-dark-1: #263238;        /* Dark blue-grey */
        --text-dark-2: #212121;        /* Dark grey */
        --text-dark-3: #1a237e;        /* Dark blue */
        
        --haven-green: #4caf50;
        --haven-accent: #ff5722;
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        font-family: 'Roboto', sans-serif;
    }
    
    /* Increase all font sizes for better readability */
    .stMarkdown, .stText, p, div, span {
        font-size: 18px !important;
        line-height: 1.6 !important;
    }
    
    h1 { font-size: 3rem !important; color: var(--text-dark-2) !important; }
    h2 { font-size: 2.5rem !important; color: var(--text-dark-2) !important; }
    h3 { font-size: 2rem !important; color: var(--text-dark-2) !important; }
    h4 { font-size: 1.8rem !important; color: var(--text-dark-2) !important; }
    h5 { font-size: 1.5rem !important; color: var(--text-dark-2) !important; }
    
    /* Safe MaterializeCSS card styling with custom backgrounds */
    .haven-card {
        padding: 30px;
        margin: 20px 0;
        border-radius: 15px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .haven-card:hover {
        transform: translateY(-5px);
    }
    
    /* Page-specific background colors */
    .registration-card {
        background-color: var(--registration-bg) !important;
        color: var(--text-dark-1) !important;
    }
    
    .profile-search-card {
        background-color: var(--profile-search-bg) !important;
        color: var(--text-dark-2) !important;
    }
    
    .trending-login-card {
        background-color: var(--trending-login-bg) !important;
        color: var(--text-dark-3) !important;
    }
    
    .login-alt-card {
        background-color: var(--login-alt-bg) !important;
        color: var(--text-dark-1) !important;
    }
    
    .other-card {
        background-color: var(--other-bg) !important;
        color: var(--text-dark-2) !important;
    }
    
    /* Header styling with gradient */
    .haven-header {
        background: linear-gradient(135deg, var(--haven-green) 0%, #81c784 100%);
        padding: 30px 0;
        margin-bottom: 30px;
    }
    
    .haven-logo {
        max-height: 80px;
        width: auto;
    }
    
    /* Safe button styling using Streamlit's system */
    .stButton > button {
        background: linear-gradient(135deg, var(--haven-green), #81c784) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4) !important;
    }
    
    /* Safe input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        font-size: 16px !important;
        padding: 12px !important;
        border-radius: 8px !important;
        border: 2px solid #e0e0e0 !important;
        background-color: white !important;
        color: var(--text-dark-2) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--haven-green) !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
    }
    
    /* Safe progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--haven-green), #81c784) !important;
        border-radius: 10px !important;
    }
    
    /* Safe metric styling */
    .stMetric {
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
    
    /* Safe tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 15px 25px !important;
        border-radius: 8px !important;
        color: var(--text-dark-2) !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--haven-green) !important;
        color: white !important;
    }
    
    /* Safe success/error message styling */
    .stSuccess {
        font-size: 16px !important;
        padding: 15px !important;
        border-radius: 8px !important;
        background-color: #c8e6c9 !important;
        color: var(--text-dark-1) !important;
    }
    
    .stError {
        font-size: 16px !important;
        padding: 15px !important;
        border-radius: 8px !important;
        background-color: #ffcdd2 !important;
        color: var(--text-dark-1) !important;
    }
    
    .stInfo {
        font-size: 16px !important;
        padding: 15px !important;
        border-radius: 8px !important;
        background-color: #e3f2fd !important;
        color: var(--text-dark-3) !important;
    }
    
    /* Safe sidebar styling */
    .css-1d391kg {
        background-color: white !important;
        border-right: 2px solid #e0e0e0 !important;
    }
    
    /* Campaign card specific styling */
    .campaign-stats {
        display: flex;
        justify-content: space-between;
        margin: 20px 0;
        font-size: 16px;
    }
    
    .stat-item {
        text-align: center;
        flex: 1;
    }
    
    .stat-value {
        font-weight: 700;
        color: var(--haven-green);
        font-size: 1.4rem;
        display: block;
    }
    
    .stat-label {
        color: var(--text-dark-2);
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .haven-card {
            padding: 20px;
            margin: 15px 0;
        }
        
        h1 { font-size: 2.5rem !important; }
        h2 { font-size: 2rem !important; }
        h3 { font-size: 1.8rem !important; }
        h4 { font-size: 1.5rem !important; }
        h5 { font-size: 1.3rem !important; }
        
        .stMarkdown, .stText, p, div, span {
            font-size: 16px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'token' not in st.session_state:
        st.session_state.token = None

# Header component using safe MaterializeCSS
def render_header():
    header_html = f"""
    <div class="haven-header z-depth-2">
        <div class="container">
            <div class="row valign-wrapper">
                <div class="col s12 m6 l4 center-align">
                    {f'<img src="data:image/png;base64,{logo_base64}" class="haven-logo" alt="HAVEN Logo">' if logo_base64 else ''}
                    <h1 class="white-text" style="margin: 10px 0 5px 0; font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                        HAVEN
                    </h1>
                    <p class="white-text light" style="margin: 0; font-size: 1.4rem;">
                        Crowdfunding Platform
                    </p>
                </div>
                <div class="col s12 m6 l8 right-align hide-on-small-only">
                    <h4 class="white-text light" style="margin: 0; font-size: 1.8rem;">
                        Building Dreams Together
                    </h4>
                    <p class="white-text" style="margin: 0; font-size: 1.2rem; opacity: 0.9;">
                        Empowering communities through collaborative funding
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

# Navigation using Streamlit sidebar (safe approach)
def render_navigation():
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        # Navigation buttons using Streamlit native components
        if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.page == 'home' else "secondary"):
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("🔍 Explore", use_container_width=True, type="primary" if st.session_state.page == 'explore' else "secondary"):
            st.session_state.page = 'explore'
            st.rerun()
        
        if st.button("🔎 Search", use_container_width=True, type="primary" if st.session_state.page == 'search' else "secondary"):
            st.session_state.page = 'search'
            st.rerun()
        
        if st.button("👤 Profile", use_container_width=True, type="primary" if st.session_state.page == 'profile' else "secondary"):
            st.session_state.page = 'profile'
            st.rerun()
        
        if st.session_state.user:
            if st.button("➕ Create Campaign", use_container_width=True, type="primary" if st.session_state.page == 'create' else "secondary"):
                st.session_state.page = 'create'
                st.rerun()
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.token = None
                st.session_state.page = 'home'
                st.rerun()

# Authentication page with safe MaterializeCSS
def render_auth_page():
    # Welcome section using safe MaterializeCSS
    welcome_html = """
    <div class="container">
        <div class="row">
            <div class="col s12 m8 offset-m2">
                <div class="login-alt-card haven-card z-depth-3 center-align">
                    <h3 style="margin-bottom: 25px;">
                        🔐 Welcome to HAVEN
                    </h3>
                    <p class="flow-text" style="font-size: 1.3rem; margin-bottom: 30px;">
                        Join thousands of people supporting meaningful causes and building a better tomorrow together.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(welcome_html, unsafe_allow_html=True)
    
    # Create tabs for login and register using Streamlit native
    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Register"])
    
    with tab1:
        # Login page background
        login_card_html = """
        <div class="container">
            <div class="row">
                <div class="col s12 m6 offset-m3">
                    <div class="trending-login-card haven-card z-depth-3">
                        <h4 class="center-align" style="margin-bottom: 30px;">Sign in to your account</h4>
        """
        st.markdown(login_card_html, unsafe_allow_html=True)
        
        # OAuth buttons using Streamlit native (safe approach)
        st.markdown("### Continue with social media:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Continue with Google", use_container_width=True, type="primary"):
                st.info("🔄 Google OAuth integration - Opening popup window...")
                # Add OAuth logic here
        
        with col2:
            if st.button("📘 Continue with Facebook", use_container_width=True):
                st.info("🔄 Facebook OAuth integration - Opening popup window...")
                # Add OAuth logic here
        
        st.markdown("---")
        st.markdown("**Or sign in with email:**")
        
        # Email login form using Streamlit native
        with st.form("login_form"):
            email = st.text_input("📧 Email Address", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            remember_me = st.checkbox("Remember me")
            
            col1, col2 = st.columns(2)
            with col1:
                login_submitted = st.form_submit_button("🚀 Sign In", use_container_width=True, type="primary")
            with col2:
                register_button = st.form_submit_button("📝 Create Account", use_container_width=True)
            
            if login_submitted:
                if email and password:
                    try:
                        response = requests.post(f"{BACKEND_URL}/api/auth/login", 
                                               params={"email": email, "password": password})
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.token = result["access_token"]
                            st.session_state.user = result["user"]
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password")
                    except Exception as e:
                        st.error(f"❌ Login error: {str(e)}")
                else:
                    st.error("⚠️ Please enter both email and password")
        
        # Close login card
        st.markdown("</div></div></div></div>", unsafe_allow_html=True)
    
    with tab2:
        # Registration page background
        register_card_html = """
        <div class="container">
            <div class="row">
                <div class="col s12 m8 offset-m2">
                    <div class="registration-card haven-card z-depth-3">
                        <h4 class="center-align" style="margin-bottom: 30px;">Create your HAVEN account</h4>
        """
        st.markdown(register_card_html, unsafe_allow_html=True)
        
        # Registration form using Streamlit native
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("👤 First Name", placeholder="Enter your first name")
                email = st.text_input("📧 Email", placeholder="your.email@example.com")
                user_type = st.selectbox("🏢 Account Type", ["individual", "organization", "ngo"])
            
            with col2:
                last_name = st.text_input("👤 Last Name", placeholder="Enter your last name")
                phone = st.text_input("📱 Phone", placeholder="+91-9876543210")
                password = st.text_input("🔒 Password", type="password", placeholder="Minimum 6 characters")
            
            address = st.text_area("🏠 Address", placeholder="Enter your complete address")
            
            col1, col2 = st.columns(2)
            with col1:
                terms_agreed = st.checkbox("✅ I agree to the Terms and Conditions")
            with col2:
                newsletter = st.checkbox("📧 Subscribe to newsletter")
            
            submitted = st.form_submit_button("🎉 Create Account", use_container_width=True, type="primary")
            
            if submitted:
                if first_name and last_name and email and password and terms_agreed:
                    # Register user
                    user_data = {
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "phone": phone,
                        "user_type": user_type,
                        "address": address,
                        "password": password
                    }
                    
                    try:
                        response = requests.post(f"{BACKEND_URL}/api/auth/register", json=user_data)
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.token = result["access_token"]
                            st.session_state.user = result["user"]
                            st.success("✅ Account created successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Registration failed. Please try again.")
                    except Exception as e:
                        st.error(f"❌ Registration error: {str(e)}")
                else:
                    st.error("⚠️ Please fill in all required fields and agree to terms.")
        
        # Close registration card
        st.markdown("</div></div></div></div>", unsafe_allow_html=True)

# Home page with safe MaterializeCSS
def render_home_page():
    # Hero section using safe MaterializeCSS
    hero_html = """
    <div class="container">
        <div class="row">
            <div class="col s12">
                <div class="trending-login-card haven-card z-depth-3 center-align">
                    <h3 style="margin-bottom: 25px;">
                        ❤️ Make a Difference Today
                    </h3>
                    <p class="flow-text" style="font-size: 1.3rem; margin-bottom: 35px;">
                        Join thousands of people supporting meaningful causes and building a better tomorrow together.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)
    
    if st.button("🚀 Start Exploring", use_container_width=True, type="primary"):
        st.session_state.page = 'explore'
        st.rerun()
    
    # Trending campaigns section
    trending_header_html = """
    <div class="container">
        <div class="row">
            <div class="col s12">
                <div class="trending-login-card haven-card z-depth-2">
                    <h4 style="margin-bottom: 20px;">
                        📈 Trending Campaigns
                    </h4>
                    <p class="flow-text">
                        Discover the most popular campaigns making a real impact in communities worldwide.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(trending_header_html, unsafe_allow_html=True)
    
    # Fetch campaigns from backend
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaigns")
        if response.status_code == 200:
            campaigns_data = response.json()
            campaigns = campaigns_data.get("campaigns", [])
            
            # Display campaigns in grid using safe MaterializeCSS
            for i in range(0, len(campaigns), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(campaigns):
                        campaign = campaigns[i + j]
                        with col:
                            render_campaign_card(campaign)
        else:
            st.error("❌ Failed to load campaigns")
    except Exception as e:
        st.error(f"❌ Error loading campaigns: {str(e)}")

# Campaign card component using safe MaterializeCSS
def render_campaign_card(campaign):
    progress = min(100, (campaign["raised"] / campaign["goal"]) * 100)
    try:
        end_date = datetime.fromisoformat(campaign["end_date"].replace('Z', '+00:00'))
        days_remaining = max(0, (end_date - datetime.now()).days)
    except:
        days_remaining = 30
    
    # Campaign card using safe MaterializeCSS
    campaign_html = f"""
    <div class="other-card haven-card z-depth-2" style="margin: 15px 0;">
        <div style="text-align: center;">
            <h5 style="margin-bottom: 15px; font-weight: 600;">{campaign['title']}</h5>
            <p style="margin-bottom: 20px; line-height: 1.6;">{campaign['description'][:120]}...</p>
        </div>
    </div>
    """
    st.markdown(campaign_html, unsafe_allow_html=True)
    
    # Progress bar using Streamlit native
    st.progress(progress / 100)
    
    # Campaign stats using safe MaterializeCSS
    stats_html = f"""
    <div class="campaign-stats">
        <div class="stat-item">
            <span class="stat-value">₹{campaign['raised']:,.0f}</span>
            <span class="stat-label">Raised</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{progress:.0f}%</span>
            <span class="stat-label">Funded</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{days_remaining}</span>
            <span class="stat-label">Days Left</span>
        </div>
    </div>
    """
    st.markdown(stats_html, unsafe_allow_html=True)
    
    # Donate button using Streamlit native
    if st.button(f"❤️ Donate", key=f"donate_{campaign['id']}", use_container_width=True):
        st.success(f"Redirecting to donation page for {campaign['title']}")

# Explore page with safe MaterializeCSS
def render_explore_page():
    # Explore header
    explore_header_html = """
    <div class="container">
        <div class="row">
            <div class="col s12">
                <div class="other-card haven-card z-depth-3">
                    <h4 style="margin-bottom: 20px;">
                        🔍 Explore Categories
                    </h4>
                    <p class="flow-text">
                        Browse campaigns by category to find causes that matter to you.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(explore_header_html, unsafe_allow_html=True)
    
    # Category grid using safe MaterializeCSS
    categories = [
        {"name": "Medical", "icon": "🏥", "count": 45, "description": "Healthcare and medical support"},
        {"name": "Education", "icon": "🎓", "count": 32, "description": "Educational initiatives and scholarships"},
        {"name": "Community", "icon": "👥", "count": 28, "description": "Community development projects"},
        {"name": "Environment", "icon": "🌱", "count": 19, "description": "Environmental conservation"},
        {"name": "Technology", "icon": "💻", "count": 15, "description": "Tech innovation and startups"},
        {"name": "Arts", "icon": "🎨", "count": 12, "description": "Creative arts and culture"}
    ]
    
    # Display categories using safe MaterializeCSS grid
    category_grid_html = """
    <div class="container">
        <div class="row">
    """
    
    for i, category in enumerate(categories):
        category_grid_html += f"""
            <div class="col s12 m6 l4">
                <div class="other-card haven-card z-depth-2 center-align" style="margin: 15px 0; cursor: pointer;">
                    <div style="font-size: 3rem; margin-bottom: 15px;">{category['icon']}</div>
                    <h5 style="margin-bottom: 10px; font-weight: 600;">{category['name']}</h5>
                    <p style="margin-bottom: 10px; font-size: 1rem;">{category['description']}</p>
                    <p style="font-weight: 600; font-size: 1.1rem;">{category['count']} campaigns</p>
                </div>
            </div>
        """
    
    category_grid_html += """
        </div>
    </div>
    """
    
    st.markdown(category_grid_html, unsafe_allow_html=True)
    
    # Category buttons using Streamlit native
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            if st.button(f"View {category['name']}", key=f"cat_{category['name']}", use_container_width=True):
                st.success(f"Showing {category['name']} campaigns")

# Search page with safe MaterializeCSS
def render_search_page():
    # Search header
    search_header_html = """
    <div class="container">
        <div class="row">
            <div class="col s12">
                <div class="profile-search-card haven-card z-depth-3">
                    <h4 style="margin-bottom: 20px;">
                        🔎 Search Campaigns
                    </h4>
                    <p class="flow-text">
                        Find specific campaigns using keywords and filters.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(search_header_html, unsafe_allow_html=True)
    
    # Search form using Streamlit native
    with st.form("search_form"):
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            search_query = st.text_input("🔍 Search campaigns", placeholder="Enter keywords...")
        
        with col2:
            category_filter = st.selectbox("📂 Category", ["All", "Medical", "Education", "Community", "Environment", "Technology", "Arts"])
        
        with col3:
            st.write("")  # Spacing
            search_submitted = st.form_submit_button("🔍 Search", use_container_width=True, type="primary")
        
        if search_submitted and search_query:
            try:
                params = {"query": search_query}
                if category_filter != "All":
                    params["category"] = category_filter.lower()
                
                response = requests.post(f"{BACKEND_URL}/api/search", params=params)
                if response.status_code == 200:
                    results = response.json()
                    campaigns = results.get("campaigns", [])
                    
                    if campaigns:
                        st.success(f"✅ Found {len(campaigns)} campaigns")
                        
                        # Display search results
                        for i in range(0, len(campaigns), 3):
                            cols = st.columns(3)
                            for j, col in enumerate(cols):
                                if i + j < len(campaigns):
                                    campaign = campaigns[i + j]
                                    with col:
                                        render_campaign_card(campaign)
                    else:
                        st.info("ℹ️ No campaigns found matching your search.")
                else:
                    st.error("❌ Search failed. Please try again.")
            except Exception as e:
                st.error(f"❌ Search error: {str(e)}")

# Profile page with safe MaterializeCSS
def render_profile_page():
    if not st.session_state.user:
        st.warning("⚠️ Please log in to view your profile.")
        return
    
    user = st.session_state.user
    
    # Profile header
    profile_header_html = f"""
    <div class="container">
        <div class="row">
            <div class="col s12">
                <div class="profile-search-card haven-card z-depth-3 center-align">
                    <h3 style="margin-bottom: 20px;">
                        👤 Welcome, {user.get('first_name', 'User')}!
                    </h3>
                    <p class="flow-text">
                        Manage your profile and track your contributions to meaningful causes.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(profile_header_html, unsafe_allow_html=True)
    
    # Profile information using safe MaterializeCSS
    col1, col2 = st.columns(2)
    
    with col1:
        profile_info_html = f"""
        <div class="profile-search-card haven-card z-depth-2">
            <h5 style="margin-bottom: 20px;">📋 Profile Information</h5>
            <p><strong>Name:</strong> {user.get('first_name', '')} {user.get('last_name', '')}</p>
            <p><strong>Email:</strong> {user.get('email', '')}</p>
            <p><strong>Type:</strong> {user.get('user_type', '').title()}</p>
            <p><strong>Phone:</strong> {user.get('phone', 'Not provided')}</p>
        </div>
        """
        st.markdown(profile_info_html, unsafe_allow_html=True)
    
    with col2:
        activity_html = """
        <div class="profile-search-card haven-card z-depth-2">
            <h5 style="margin-bottom: 20px;">📊 Activity Summary</h5>
        </div>
        """
        st.markdown(activity_html, unsafe_allow_html=True)
        
        # Activity metrics using Streamlit native
        st.metric("💰 Total Donated", "₹0")
        st.metric("🎯 Campaigns Supported", "0")
        st.metric("🏆 Campaigns Created", "0")

# Create campaign page
def render_create_campaign_page():
    # Create campaign header
    create_header_html = """
    <div class="container">
        <div class="row">
            <div class="col s12">
                <div class="other-card haven-card z-depth-3 center-align">
                    <h3 style="margin-bottom: 20px;">
                        ➕ Create New Campaign
                    </h3>
                    <p class="flow-text">
                        Start your journey to make a positive impact in the world.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(create_header_html, unsafe_allow_html=True)
    
    # Create campaign form using Streamlit native
    with st.form("create_campaign_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("📝 Campaign Title", placeholder="Enter campaign title")
            category = st.selectbox("📂 Category", ["medical", "education", "community", "environment", "technology", "arts"])
            goal = st.number_input("💰 Funding Goal (₹)", min_value=1000, max_value=10000000, value=50000)
        
        with col2:
            location = st.selectbox("📍 Location", ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"])
            duration = st.number_input("⏰ Duration (days)", min_value=1, max_value=365, value=30)
            contact_email = st.text_input("📧 Contact Email", placeholder="contact@example.com")
        
        description = st.text_area("📄 Description", placeholder="Describe your campaign in detail...", height=150)
        
        # File upload for images
        uploaded_files = st.file_uploader("📸 Upload Images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        
        submitted = st.form_submit_button("🚀 Create Campaign", use_container_width=True, type="primary")
        
        if submitted:
            if title and description and goal:
                st.success("✅ Campaign created successfully!")
                st.balloons()
            else:
                st.error("⚠️ Please fill in all required fields.")

# Main app
def main():
    # Load safe MaterializeCSS
    load_safe_materialize_css()
    
    # Initialize session state
    init_session_state()
    
    # Render header
    render_header()
    
    # Check authentication
    if not st.session_state.user:
        render_auth_page()
    else:
        # Render navigation
        render_navigation()
        
        # Render pages based on selection
        if st.session_state.page == 'home':
            render_home_page()
        elif st.session_state.page == 'explore':
            render_explore_page()
        elif st.session_state.page == 'search':
            render_search_page()
        elif st.session_state.page == 'profile':
            render_profile_page()
        elif st.session_state.page == 'create':
            render_create_campaign_page()
        else:
            render_home_page()

if __name__ == "__main__":
    main()

