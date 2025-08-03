import streamlit as st
import requests
import base64
from datetime import datetime
import json
import os
from urllib.parse import urlencode
import time

# Page configuration
st.set_page_config(
    page_title="HAVEN - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Backend URL
BACKEND_URL = "https://haven-fastapi-backend.onrender.com"

# Load HAVEN logo
def load_logo():
    try:
        with open("/home/ubuntu/upload/haven_logo.png", "rb") as f:
            logo_data = f.read()
        return base64.b64encode(logo_data).decode()
    except:
        return None

# Custom CSS for exact design match
def load_custom_css():
    st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Login page styling - Light blue background */
    .login-container {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        min-height: 100vh;
        padding: 2rem;
        color: #1a237e;
    }
    
    /* Registration page styling - Light red background */
    .register-container {
        background: linear-gradient(135deg, #ffcdd2 0%, #f8bbd9 100%);
        min-height: 100vh;
        padding: 2rem;
        color: #263238;
    }
    
    /* Trending page styling - Light blue background */
    .trending-container {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        min-height: 100vh;
        padding: 2rem;
        color: #1a237e;
    }
    
    /* Search page styling - Light purple background */
    .search-container {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        min-height: 100vh;
        padding: 2rem;
        color: #212121;
    }
    
    /* Explore page styling - Light purple background */
    .explore-container {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        min-height: 100vh;
        padding: 2rem;
        color: #212121;
    }
    
    /* Profile page styling - Light purple background */
    .profile-container {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        min-height: 100vh;
        padding: 2rem;
        color: #212121;
    }
    
    /* Campaign detail styling - Light green background */
    .campaign-container {
        background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 100%);
        min-height: 100vh;
        padding: 2rem;
        color: #263238;
    }
    
    /* HAVEN logo styling */
    .haven-logo {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .haven-logo img {
        max-width: 200px;
        height: auto;
    }
    
    /* Tagline styling */
    .tagline {
        text-align: center;
        font-size: 1.2rem;
        font-style: italic;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    
    /* Login card styling */
    .login-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: 0 auto;
    }
    
    /* Registration card styling */
    .register-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* OAuth buttons styling - matching first image */
    .oauth-button {
        width: 100%;
        padding: 12px;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
        margin: 8px 0;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        transition: all 0.3s ease;
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
    
    /* Campaign card styling */
    .campaign-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .campaign-card:hover {
        transform: translateY(-5px);
    }
    
    /* Category card styling */
    .category-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    
    .category-card:hover {
        transform: translateY(-5px);
    }
    
    .category-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Progress bar styling */
    .progress-container {
        background: #f0f0f0;
        border-radius: 10px;
        height: 8px;
        margin: 10px 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #4caf50, #8bc34a);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Bottom navigation styling */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 1px solid #e0e0e0;
        padding: 10px 0;
        display: flex;
        justify-content: space-around;
        z-index: 1000;
    }
    
    .nav-item {
        text-align: center;
        cursor: pointer;
        padding: 5px;
        transition: color 0.3s ease;
    }
    
    .nav-item:hover {
        color: #4caf50;
    }
    
    /* Typography */
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    h2 {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    p {
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        font-size: 16px;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        font-size: 16px;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        font-size: 16px;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
    }
    
    /* Search box styling */
    .search-box {
        background: white;
        border-radius: 25px;
        padding: 15px 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .login-card, .register-card {
            margin: 1rem;
            padding: 1.5rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .haven-logo img {
            max-width: 150px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# OAuth integration functions
def get_oauth_url(provider):
    """Generate OAuth URL for Google or Facebook"""
    if provider == "google":
        params = {
            "client_id": "your-google-client-id",
            "redirect_uri": "https://haven-streamlit-frontend.onrender.com/auth/callback",
            "scope": "openid email profile",
            "response_type": "code",
            "state": "google"
        }
        return f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
    
    elif provider == "facebook":
        params = {
            "client_id": "your-facebook-app-id",
            "redirect_uri": "https://haven-streamlit-frontend.onrender.com/auth/callback",
            "scope": "email,public_profile",
            "response_type": "code",
            "state": "facebook"
        }
        return f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode(params)}"

def oauth_login_button(provider, text, icon):
    """Create OAuth login button with popup functionality"""
    button_class = f"{provider}-btn oauth-button"
    
    oauth_url = get_oauth_url(provider)
    
    button_html = f"""
    <button class="{button_class}" onclick="openOAuthPopup('{oauth_url}', '{provider}')">
        {icon} {text}
    </button>
    
    <script>
    function openOAuthPopup(url, provider) {{
        const popup = window.open(
            url,
            'oauth_' + provider,
            'width=500,height=600,scrollbars=yes,resizable=yes,status=yes,location=yes,toolbar=no,menubar=no'
        );
        
        // Check for popup completion
        const checkClosed = setInterval(() => {{
            if (popup.closed) {{
                clearInterval(checkClosed);
                // Refresh the page to check for authentication
                window.location.reload();
            }}
        }}, 1000);
    }}
    </script>
    """
    
    st.markdown(button_html, unsafe_allow_html=True)

# API functions
def fetch_campaigns():
    """Fetch campaigns from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaigns", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except:
        return []

def fetch_categories():
    """Fetch categories from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/categories", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return [
                {"name": "Art & Design", "count": 25, "icon": "🎨"},
                {"name": "Technology", "count": 18, "icon": "💻"},
                {"name": "Community", "count": 32, "icon": "👥"},
                {"name": "Film & Video", "count": 14, "icon": "🎬"},
                {"name": "Music", "count": 22, "icon": "🎵"},
                {"name": "Publishing", "count": 16, "icon": "📚"}
            ]
    except:
        return [
            {"name": "Art & Design", "count": 25, "icon": "🎨"},
            {"name": "Technology", "count": 18, "icon": "💻"},
            {"name": "Community", "count": 32, "icon": "👥"},
            {"name": "Film & Video", "count": 14, "icon": "🎬"},
            {"name": "Music", "count": 22, "icon": "🎵"},
            {"name": "Publishing", "count": 16, "icon": "📚"}
        ]

def search_campaigns(query):
    """Search campaigns"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaigns/search", 
                              params={"q": query}, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except:
        return []

# Page components
def render_logo():
    """Render HAVEN logo"""
    logo_base64 = load_logo()
    if logo_base64:
        st.markdown(f"""
        <div class="haven-logo">
            <img src="data:image/png;base64,{logo_base64}" alt="HAVEN Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="haven-logo">
            <h1 style="font-size: 3rem; margin: 0; color: #4caf50;">HAVEN</h1>
        </div>
        """, unsafe_allow_html=True)

def render_tagline():
    """Render tagline"""
    st.markdown("""
    <div class="tagline">
        Help not just some people, but Help Humanity.
    </div>
    """, unsafe_allow_html=True)

def login_page():
    """Login page matching first image design"""
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    render_logo()
    render_tagline()
    
    # Login card
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Login form
    st.markdown("### Login")
    
    with st.form("login_form"):
        email = st.text_input("Enter Your Email", placeholder="Enter Your Email")
        password = st.text_input("Enter Your Password", type="password", placeholder="Enter Your Password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("Continue", use_container_width=True)
        with col2:
            if st.form_submit_button("Forgot Password?", use_container_width=True):
                st.info("Password reset functionality coming soon!")
    
    if login_btn and email and password:
        # Login logic here
        st.success("Login successful!")
        st.session_state.authenticated = True
        st.session_state.user_email = email
        st.rerun()
    
    # Create account link
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        Not registered? <a href="?page=register" style="color: #4caf50; text-decoration: none;">Create an account</a>
    </div>
    """, unsafe_allow_html=True)
    
    # OAuth buttons - matching first image
    st.markdown("### or you can sign in with")
    
    col1, col2 = st.columns(2)
    with col1:
        oauth_login_button("google", "Google", "🔍")
    with col2:
        oauth_login_button("facebook", "Facebook", "📘")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def register_page():
    """Registration page with Individual/Organization forms"""
    st.markdown('<div class="register-container">', unsafe_allow_html=True)
    
    render_logo()
    
    st.markdown('<div class="register-card">', unsafe_allow_html=True)
    
    st.markdown("## Register")
    
    # Account type selection
    account_type = st.selectbox("Select Account Type", ["Individual", "Organization"])
    
    if account_type == "Individual":
        # Individual registration form (matching second image)
        st.markdown("### Register as an Individual")
        
        with st.form("individual_register"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name", placeholder="R PRAKASH")
                email = st.text_input("Email ID", placeholder="prakashr00@rediffmail.com")
                phone = st.text_input("Phone Number", placeholder="09936528585")
                otp = st.text_input("Enter OTP", placeholder="Enter OTP")
            
            with col2:
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                address = st.text_area("Address", placeholder="Enter your address")
                
                # Document upload for verification
                st.markdown("**Identity Verification (Upload any one):**")
                document_type = st.selectbox("Document Type", 
                    ["Aadhar Card", "PAN Card", "Passport", "Driving License", "Voter ID"])
                document_file = st.file_uploader("Upload Document", type=['pdf', 'jpg', 'png'])
            
            register_btn = st.form_submit_button("Register", use_container_width=True)
            
            if register_btn:
                if password == confirm_password:
                    st.success("Individual registration successful!")
                else:
                    st.error("Passwords do not match!")
    
    else:
        # Organization registration form (matching fourth image)
        st.markdown("### Register as an Organization")
        
        with st.form("organization_register"):
            col1, col2 = st.columns(2)
            with col1:
                org_name = st.text_input("Organization Name", placeholder="Organization Name")
                org_phone = st.text_input("Organization Phone Number", placeholder="Organization Phone Number")
                org_type = st.selectbox("Select Organization Type", 
                    ["NGO", "Non-Profit", "Social Enterprise", "Charity", "Foundation"])
                org_description = st.text_area("Brief Description (max 100 chars)", 
                    placeholder="Brief Description (max 100 chars)", max_chars=100)
            
            with col2:
                contact_person = st.text_input("Contact Person Name")
                contact_email = st.text_input("Contact Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                # Certificate upload for verification
                st.markdown("**Organization Verification (Required):**")
                cert_type = st.selectbox("Certificate Type", 
                    ["Certificate of Incorporation", "GST Certificate", "12A Certificate", 
                     "80G Certificate", "FCRA Certificate"])
                cert_file = st.file_uploader("Upload Certificate", type=['pdf', 'jpg', 'png'])
            
            register_btn = st.form_submit_button("Register", use_container_width=True)
            
            if register_btn:
                if password == confirm_password:
                    st.success("Organization registration successful!")
                else:
                    st.error("Passwords do not match!")
    
    # Sign in link
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        Already have an account? <a href="?page=login" style="color: #4caf50; text-decoration: none;">Sign in here</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def trending_page():
    """Trending campaigns page (matching 5th and 10th images)"""
    st.markdown('<div class="trending-container">', unsafe_allow_html=True)
    
    render_logo()
    
    st.markdown("# Trending Campaigns")
    st.markdown("Support the most popular projects on HAVEN.")
    
    # Trending badge
    st.markdown("""
    <div style="text-align: right; margin: 20px 0;">
        <span style="background: black; color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold;">
            ⚡ Trending
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch and display campaigns
    campaigns = fetch_campaigns()
    
    if campaigns:
        for campaign in campaigns[:5]:  # Show top 5 trending
            st.markdown('<div class="campaign-card">', unsafe_allow_html=True)
            
            # Campaign image placeholder
            st.markdown("""
            <div style="background: #e0e0e0; height: 200px; border-radius: 10px; 
                        display: flex; align-items: center; justify-content: center; 
                        margin-bottom: 15px; color: #666;">
                600 × 400
            </div>
            """, unsafe_allow_html=True)
            
            # Campaign details
            st.markdown(f"### {campaign.get('campaign_name', 'Campaign Title')}")
            st.markdown(f"By {campaign.get('org_name', 'Organization')}")
            st.markdown(f"{campaign.get('description', 'Campaign description')}")
            
            # Progress bar
            raised = campaign.get('amount_raised', 0)
            goal = campaign.get('funding_goal', 100000)
            progress = min((raised / goal) * 100, 100) if goal > 0 else 0
            
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress}%"></div>
            </div>
            <p>₹{raised:,} raised • {progress:.0f}%</p>
            <p>⏰ 30 days left</p>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Loading trending campaigns...")
    
    st.markdown('</div>', unsafe_allow_html=True)

def search_page():
    """Search campaigns page (matching 6th image)"""
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    render_logo()
    
    st.markdown("# Search Campaigns")
    
    # Search box
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    search_query = st.text_input("", placeholder="Search by keyword, category...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Search instructions
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <p style="font-size: 1.2rem; color: #666;">Enter a term above to search for campaigns.</p>
        <p style="color: #888;">You can search by title, description, or category.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search results
    if search_query:
        results = search_campaigns(search_query)
        if results:
            st.markdown(f"### Found {len(results)} campaigns")
            for campaign in results:
                st.markdown('<div class="campaign-card">', unsafe_allow_html=True)
                st.markdown(f"**{campaign.get('campaign_name', 'Campaign')}**")
                st.markdown(f"By {campaign.get('org_name', 'Organization')}")
                st.markdown(f"{campaign.get('description', 'Description')}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No campaigns found. Try different keywords.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def explore_page():
    """Explore categories page (matching 7th and 8th images)"""
    st.markdown('<div class="explore-container">', unsafe_allow_html=True)
    
    render_logo()
    
    st.markdown("# Explore Categories")
    st.markdown("Discover campaigns by interest.")
    
    # Categories grid
    categories = fetch_categories()
    
    # Display categories in 2-column grid
    for i in range(0, len(categories), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(categories):
                cat = categories[i]
                st.markdown(f"""
                <div class="category-card">
                    <div class="category-icon">{cat.get('icon', '📁')}</div>
                    <h3>{cat['name']}</h3>
                    <p>{cat.get('count', 0)} campaigns</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if i + 1 < len(categories):
                cat = categories[i + 1]
                st.markdown(f"""
                <div class="category-card">
                    <div class="category-icon">{cat.get('icon', '📁')}</div>
                    <h3>{cat['name']}</h3>
                    <p>{cat.get('count', 0)} campaigns</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def campaign_detail_page(campaign_id):
    """Campaign detail page (matching 9th image - hand-drawn sketch)"""
    st.markdown('<div class="campaign-container">', unsafe_allow_html=True)
    
    render_logo()
    
    # Campaign picture
    st.markdown("""
    <div style="background: #e0e0e0; height: 300px; border-radius: 15px; 
                display: flex; align-items: center; justify-content: center; 
                margin-bottom: 20px; color: #666; font-size: 1.2rem;">
        Campaign Picture
    </div>
    """, unsafe_allow_html=True)
    
    # Organization info with fraud indicator
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Organization Name")
    with col2:
        st.markdown("""
        <div style="text-align: right;">
            <span style="color: green;">● Verified</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Campaign details
    st.markdown("## Campaign Title")
    st.markdown("### Share")
    st.markdown("### Donate")
    
    # Donation box
    st.markdown("""
    <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <p>Will open a box down below asking for amount which after pressing will open UPI page of organization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top 3 Donators
    st.markdown("### Top 3 Donators of Campaign")
    for i in range(1, 4):
        st.markdown(f"{i}. Anonymous Donor - ₹{1000 * (4-i):,}")
    
    # Reviews section
    st.markdown("### Reviews")
    st.markdown("""
    <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <p><strong>Fraud Detection Explanation</strong></p>
        <p>This campaign has been verified through our fraud detection system. 
        All documents have been authenticated and the organization is legitimate.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def profile_page():
    """User profile page"""
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    
    render_logo()
    
    st.markdown("# User Profile")
    
    if st.session_state.get('authenticated'):
        st.markdown(f"### Welcome, {st.session_state.get('user_email', 'User')}!")
        
        # Profile tabs
        tab1, tab2, tab3 = st.tabs(["Profile Info", "My Donations", "My Campaigns"])
        
        with tab1:
            st.markdown("#### Profile Information")
            st.text_input("Name", value="John Doe")
            st.text_input("Email", value=st.session_state.get('user_email', ''))
            st.text_input("Phone", value="+91 9876543210")
            
            if st.button("Update Profile"):
                st.success("Profile updated successfully!")
        
        with tab2:
            st.markdown("#### My Donations")
            st.markdown("**Recent Donations:**")
            donations = [
                {"campaign": "Clean Water Project", "amount": 5000, "date": "2024-01-15"},
                {"campaign": "Education Support", "amount": 2000, "date": "2024-01-10"},
                {"campaign": "Medical Aid", "amount": 3000, "date": "2024-01-05"}
            ]
            
            for donation in donations:
                st.markdown(f"- **{donation['campaign']}**: ₹{donation['amount']:,} on {donation['date']}")
        
        with tab3:
            st.markdown("#### My Campaigns")
            if st.session_state.get('user_type') == 'organization':
                st.markdown("**Active Campaigns:**")
                st.markdown("- Education for All: ₹45,000 raised (75% of goal)")
                st.markdown("- Clean Water Initiative: ₹32,000 raised (64% of goal)")
            else:
                st.info("Only organizations can create campaigns.")
    else:
        st.warning("Please log in to view your profile.")
        if st.button("Go to Login"):
            st.session_state.current_page = "login"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def bottom_navigation():
    """Bottom navigation bar"""
    st.markdown("""
    <div class="bottom-nav">
        <div class="nav-item" onclick="setPage('trending')">
            <div style="font-size: 1.5rem;">📈</div>
            <div style="font-size: 0.8rem;">Trending</div>
        </div>
        <div class="nav-item" onclick="setPage('search')">
            <div style="font-size: 1.5rem;">🔍</div>
            <div style="font-size: 0.8rem;">Search</div>
        </div>
        <div class="nav-item" onclick="setPage('explore')">
            <div style="font-size: 1.5rem;">📱</div>
            <div style="font-size: 0.8rem;">Explore</div>
        </div>
        <div class="nav-item" onclick="setPage('profile')">
            <div style="font-size: 1.5rem;">👤</div>
            <div style="font-size: 0.8rem;">Profile</div>
        </div>
    </div>
    
    <script>
    function setPage(page) {
        window.location.href = '?page=' + page;
    }
    </script>
    """, unsafe_allow_html=True)

# Main application
def main():
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"
    
    # Get page from URL parameters
    query_params = st.experimental_get_query_params()
    page = query_params.get('page', ['login'])[0]
    
    # Route to appropriate page
    if not st.session_state.authenticated and page not in ['login', 'register']:
        page = 'login'
    
    if page == 'login':
        login_page()
    elif page == 'register':
        register_page()
    elif page == 'trending':
        trending_page()
        bottom_navigation()
    elif page == 'search':
        search_page()
        bottom_navigation()
    elif page == 'explore':
        explore_page()
        bottom_navigation()
    elif page == 'profile':
        profile_page()
        bottom_navigation()
    elif page.startswith('campaign_'):
        campaign_id = page.split('_')[1]
        campaign_detail_page(campaign_id)
        bottom_navigation()
    else:
        # Default to trending if authenticated, login if not
        if st.session_state.authenticated:
            trending_page()
            bottom_navigation()
        else:
            login_page()

if __name__ == "__main__":
    main()

