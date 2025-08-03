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

# Custom CSS - MINIMAL AND SAFE
def load_minimal_css():
    st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main styling */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        font-family: 'Roboto', sans-serif;
    }
    
    /* Increase all font sizes */
    .stMarkdown, .stText, p, div, span {
        font-size: 18px !important;
        line-height: 1.6 !important;
    }
    
    h1 { font-size: 3rem !important; }
    h2 { font-size: 2.5rem !important; }
    h3 { font-size: 2rem !important; }
    h4 { font-size: 1.8rem !important; }
    h5 { font-size: 1.5rem !important; }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4caf50, #81c784) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 15px 30px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3) !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        font-size: 16px !important;
        padding: 12px !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox > div > div > select {
        font-size: 16px !important;
        padding: 12px !important;
    }
    
    /* Card styling */
    .stContainer {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4caf50, #81c784) !important;
    }
    
    /* Metric styling */
    .metric-container {
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* Success/Error messages */
    .stSuccess {
        font-size: 16px !important;
        padding: 15px !important;
        border-radius: 8px !important;
    }
    
    .stError {
        font-size: 16px !important;
        padding: 15px !important;
        border-radius: 8px !important;
    }
    
    .stInfo {
        font-size: 16px !important;
        padding: 15px !important;
        border-radius: 8px !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 15px 25px !important;
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

# Header component using Streamlit native components
def render_header():
    # Create header container
    header_container = st.container()
    
    with header_container:
        # Create columns for layout
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Display logo if available
            if logo_base64:
                st.image(f"data:image/png;base64,{logo_base64}", width=200)
            
            # Title and subtitle using native Streamlit
            st.markdown("""
            <div style="text-align: center; background: linear-gradient(135deg, #2e7d32, #4caf50); 
                        padding: 30px; border-radius: 15px; margin: 20px 0;">
                <h1 style="color: white; margin: 0; font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    🏠 HAVEN
                </h1>
                <p style="color: #e8f5e8; margin: 0; font-size: 1.4rem; font-weight: 300;">
                    Crowdfunding Platform
                </p>
                <h4 style="color: white; margin: 10px 0 0 0; font-size: 1.6rem;">
                    Building Dreams Together
                </h4>
                <p style="color: #e8f5e8; margin: 0; font-size: 1.1rem;">
                    Empowering communities through collaborative funding
                </p>
            </div>
            """, unsafe_allow_html=True)

# Navigation using Streamlit sidebar
def render_navigation():
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("🔍 Explore", use_container_width=True):
            st.session_state.page = 'explore'
            st.rerun()
        
        if st.button("🔎 Search", use_container_width=True):
            st.session_state.page = 'search'
            st.rerun()
        
        if st.button("👤 Profile", use_container_width=True):
            st.session_state.page = 'profile'
            st.rerun()
        
        if st.session_state.user:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.token = None
                st.session_state.page = 'home'
                st.rerun()

# Authentication page using native Streamlit components
def render_auth_page():
    st.markdown("## 🔐 Welcome to HAVEN")
    st.markdown("Join thousands of people supporting meaningful causes and building a better tomorrow together.")
    
    # Create tabs for login and register
    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Register"])
    
    with tab1:
        st.markdown("### Sign in to your account")
        
        # OAuth buttons using native Streamlit
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Continue with Google", use_container_width=True, type="primary"):
                st.info("Google OAuth integration - Opening popup window...")
                # Add OAuth logic here
        
        with col2:
            if st.button("📘 Continue with Facebook", use_container_width=True):
                st.info("Facebook OAuth integration - Opening popup window...")
                # Add OAuth logic here
        
        st.markdown("---")
        st.markdown("**Or sign in with email:**")
        
        # Email login form
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
    
    with tab2:
        st.markdown("### Create your HAVEN account")
        
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

# Home page using native Streamlit components
def render_home_page():
    st.markdown("## 🏠 Welcome to HAVEN")
    
    # Hero section
    st.markdown("""
    <div style="background: white; padding: 30px; border-radius: 15px; text-align: center; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 20px 0;">
        <h3 style="color: #4caf50; margin-bottom: 20px;">
            ❤️ Make a Difference Today
        </h3>
        <p style="font-size: 1.3rem; margin-bottom: 25px; color: #333;">
            Join thousands of people supporting meaningful causes and building a better tomorrow together.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Start Exploring", use_container_width=True, type="primary"):
        st.session_state.page = 'explore'
        st.rerun()
    
    st.markdown("---")
    st.markdown("## 📈 Trending Campaigns")
    st.markdown("Discover the most popular campaigns making a real impact in communities worldwide.")
    
    # Fetch campaigns from backend
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaigns")
        if response.status_code == 200:
            campaigns_data = response.json()
            campaigns = campaigns_data.get("campaigns", [])
            
            # Display campaigns in grid
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

# Campaign card component using native Streamlit
def render_campaign_card(campaign):
    with st.container():
        # Campaign image
        if campaign.get('image_url'):
            st.image(campaign['image_url'], use_column_width=True)
        
        # Campaign title and description
        st.markdown(f"### {campaign['title']}")
        st.markdown(f"{campaign['description'][:120]}...")
        
        # Progress calculation
        progress = min(100, (campaign["raised"] / campaign["goal"]) * 100)
        
        # Progress bar
        st.progress(progress / 100)
        
        # Campaign stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Raised", f"₹{campaign['raised']:,.0f}")
        
        with col2:
            st.metric("📊 Funded", f"{progress:.0f}%")
        
        with col3:
            try:
                end_date = datetime.fromisoformat(campaign["end_date"].replace('Z', '+00:00'))
                days_remaining = max(0, (end_date - datetime.now()).days)
            except:
                days_remaining = 30
            st.metric("⏰ Days Left", f"{days_remaining}")
        
        # Donate button
        if st.button(f"❤️ Donate to {campaign['title'][:20]}...", key=f"donate_{campaign['id']}", use_container_width=True):
            st.success(f"Redirecting to donation page for {campaign['title']}")

# Explore page using native Streamlit components
def render_explore_page():
    st.markdown("## 🔍 Explore Categories")
    st.markdown("Browse campaigns by category to find causes that matter to you.")
    
    # Category grid
    categories = [
        {"name": "Medical", "icon": "🏥", "count": 45, "description": "Healthcare and medical support"},
        {"name": "Education", "icon": "🎓", "count": 32, "description": "Educational initiatives and scholarships"},
        {"name": "Community", "icon": "👥", "count": 28, "description": "Community development projects"},
        {"name": "Environment", "icon": "🌱", "count": 19, "description": "Environmental conservation"},
        {"name": "Technology", "icon": "💻", "count": 15, "description": "Tech innovation and startups"},
        {"name": "Arts", "icon": "🎨", "count": 12, "description": "Creative arts and culture"}
    ]
    
    # Display categories in grid
    for i in range(0, len(categories), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(categories):
                category = categories[i + j]
                with col:
                    with st.container():
                        st.markdown(f"""
                        <div style="background: white; padding: 25px; border-radius: 15px; text-align: center; 
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 10px 0; cursor: pointer;">
                            <div style="font-size: 3rem; margin-bottom: 15px;">{category['icon']}</div>
                            <h4 style="color: #4caf50; margin-bottom: 10px;">{category['name']}</h4>
                            <p style="color: #666; margin-bottom: 10px;">{category['description']}</p>
                            <p style="color: #4caf50; font-weight: 600;">{category['count']} campaigns</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"View {category['name']}", key=f"cat_{category['name']}", use_container_width=True):
                            st.success(f"Showing {category['name']} campaigns")

# Search page using native Streamlit components
def render_search_page():
    st.markdown("## 🔎 Search Campaigns")
    st.markdown("Find specific campaigns using keywords and filters.")
    
    # Search form
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

# Profile page
def render_profile_page():
    if not st.session_state.user:
        st.warning("⚠️ Please log in to view your profile.")
        return
    
    user = st.session_state.user
    
    st.markdown(f"## 👤 Welcome, {user.get('first_name', 'User')}!")
    
    # User info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Profile Information")
        st.write(f"**Name:** {user.get('first_name', '')} {user.get('last_name', '')}")
        st.write(f"**Email:** {user.get('email', '')}")
        st.write(f"**Type:** {user.get('user_type', '').title()}")
        st.write(f"**Phone:** {user.get('phone', 'Not provided')}")
    
    with col2:
        st.markdown("### 📊 Activity Summary")
        st.metric("💰 Total Donated", "₹0")
        st.metric("🎯 Campaigns Supported", "0")
        st.metric("🏆 Campaigns Created", "0")

# Create campaign page
def render_create_campaign_page():
    st.markdown("## ➕ Create New Campaign")
    
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
    # Load minimal CSS
    load_minimal_css()
    
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
        
        # Add create campaign button
        if st.button("➕ Create Campaign", use_container_width=True, type="secondary"):
            st.session_state.page = 'create'
            st.rerun()
        
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

