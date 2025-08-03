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

# Custom CSS with MaterializeCSS and HAVEN styling
def load_css():
    st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main container styling */
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* HAVEN brand colors */
    :root {
        --haven-green: #4caf50;
        --haven-light-green: #81c784;
        --haven-dark-green: #2e7d32;
        --haven-accent: #ff5722;
    }
    
    /* Full page background */
    .stApp {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        font-family: 'Roboto', sans-serif;
    }
    
    /* Header styling */
    .haven-header {
        background: linear-gradient(135deg, var(--haven-green) 0%, var(--haven-dark-green) 100%);
        padding: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    
    .haven-logo {
        max-height: 60px;
        width: auto;
    }
    
    .haven-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .haven-subtitle {
        color: #e8f5e8;
        font-size: 1.2rem;
        margin: 0;
        font-weight: 300;
    }
    
    /* Navigation styling */
    .haven-nav {
        position: fixed;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        z-index: 1000;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 15px 10px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .nav-item {
        display: block;
        padding: 12px;
        margin: 8px 0;
        color: var(--haven-green);
        text-decoration: none;
        border-radius: 50%;
        transition: all 0.3s ease;
        text-align: center;
        position: relative;
    }
    
    .nav-item:hover {
        background: var(--haven-green);
        color: white;
        transform: scale(1.1);
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
    }
    
    .nav-tooltip {
        position: absolute;
        right: 60px;
        top: 50%;
        transform: translateY(-50%);
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 14px;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
    }
    
    .nav-item:hover .nav-tooltip {
        opacity: 1;
    }
    
    /* Mobile navigation */
    @media (max-width: 768px) {
        .haven-nav {
            position: fixed;
            bottom: 20px;
            right: 20px;
            left: 20px;
            top: auto;
            transform: none;
            display: flex;
            justify-content: space-around;
            padding: 10px;
        }
        
        .nav-item {
            margin: 0;
            flex: 1;
        }
        
        .nav-tooltip {
            display: none;
        }
    }
    
    /* Card styling */
    .haven-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        padding: 30px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .haven-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 45px rgba(0,0,0,0.15);
    }
    
    /* Campaign card styling */
    .campaign-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin: 20px 0;
    }
    
    .campaign-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    }
    
    .campaign-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    
    .campaign-content {
        padding: 25px;
    }
    
    .campaign-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--haven-dark-green);
        margin-bottom: 10px;
    }
    
    .campaign-description {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    .progress-container {
        background: #f5f5f5;
        border-radius: 10px;
        height: 8px;
        margin: 15px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, var(--haven-green), var(--haven-light-green));
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .campaign-stats {
        display: flex;
        justify-content: space-between;
        margin: 15px 0;
        font-size: 0.9rem;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-weight: 600;
        color: var(--haven-green);
        font-size: 1.1rem;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.8rem;
    }
    
    /* Button styling */
    .btn-haven {
        background: linear-gradient(135deg, var(--haven-green), var(--haven-light-green));
        border: none;
        color: white;
        padding: 12px 30px;
        border-radius: 25px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .btn-haven:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
        background: linear-gradient(135deg, var(--haven-dark-green), var(--haven-green));
    }
    
    /* Floating Action Button */
    .fixed-action-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
    }
    
    .btn-floating.btn-large {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #f44336, #d32f2f);
        box-shadow: 0 8px 25px rgba(244, 67, 54, 0.4);
        transition: all 0.3s ease;
    }
    
    .btn-floating.btn-large:hover {
        transform: scale(1.1) rotate(90deg);
        box-shadow: 0 12px 35px rgba(244, 67, 54, 0.6);
    }
    
    .btn-floating.btn-large i {
        line-height: 70px;
        font-size: 2rem;
    }
    
    /* OAuth button styling */
    .oauth-btn {
        width: 100%;
        margin: 10px 0;
        padding: 15px;
        border-radius: 8px;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    
    .google-btn {
        background: #db4437;
        color: white;
    }
    
    .google-btn:hover {
        background: #c23321;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(219, 68, 55, 0.4);
    }
    
    .facebook-btn {
        background: #3b5998;
        color: white;
    }
    
    .facebook-btn:hover {
        background: #2d4373;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 89, 152, 0.4);
    }
    
    /* Pulse animation */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
        }
    }
    
    /* Form styling */
    .input-field input:focus + label {
        color: var(--haven-green) !important;
    }
    
    .input-field input:focus {
        border-bottom: 1px solid var(--haven-green) !important;
        box-shadow: 0 1px 0 0 var(--haven-green) !important;
    }
    
    .input-field .prefix.active {
        color: var(--haven-green);
    }
    
    /* Category grid */
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .category-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .category-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 45px rgba(0,0,0,0.15);
    }
    
    .category-icon {
        font-size: 3rem;
        color: var(--haven-green);
        margin-bottom: 15px;
    }
    
    .category-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--haven-dark-green);
        margin-bottom: 10px;
    }
    
    .category-count {
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .haven-title {
            font-size: 2rem;
        }
        
        .haven-subtitle {
            font-size: 1rem;
        }
        
        .haven-card {
            padding: 20px;
            margin: 15px 0;
        }
        
        .campaign-content {
            padding: 20px;
        }
        
        .fixed-action-btn {
            bottom: 100px;
            right: 20px;
        }
        
        .btn-floating.btn-large {
            width: 60px;
            height: 60px;
        }
        
        .btn-floating.btn-large i {
            line-height: 60px;
            font-size: 1.5rem;
        }
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in-right {
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    </style>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    """, unsafe_allow_html=True)

# JavaScript for OAuth popup and MaterializeCSS initialization
def load_javascript():
    st.markdown("""
    <script>
    // Initialize MaterializeCSS components
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize all MaterializeCSS components
        M.AutoInit();
        
        // Initialize dropdowns
        var dropdowns = document.querySelectorAll('.dropdown-trigger');
        M.Dropdown.init(dropdowns);
        
        // Initialize modals
        var modals = document.querySelectorAll('.modal');
        M.Modal.init(modals);
        
        // Initialize tooltips
        var tooltips = document.querySelectorAll('.tooltipped');
        M.Tooltip.init(tooltips);
        
        // Initialize floating action button
        var fab = document.querySelectorAll('.fixed-action-btn');
        M.FloatingActionButton.init(fab);
    });
    
    // OAuth popup functionality
    function openOAuthPopup(provider) {
        // Get OAuth URL from backend
        fetch(`${window.location.origin.replace('streamlit', 'fastapi')}/api/auth/oauth/${provider}/url`)
            .then(response => response.json())
            .then(data => {
                if (data.oauth_url) {
                    // Open popup window
                    const popup = window.open(
                        data.oauth_url,
                        'oauth',
                        'width=500,height=600,scrollbars=yes,resizable=yes,toolbar=no,menubar=no,location=no,directories=no,status=no'
                    );
                    
                    // Monitor popup for completion
                    const checkClosed = setInterval(() => {
                        if (popup.closed) {
                            clearInterval(checkClosed);
                            // Refresh the page to update login status
                            window.location.reload();
                        }
                    }, 1000);
                } else {
                    M.toast({html: 'Failed to get OAuth URL', classes: 'red'});
                }
            })
            .catch(error => {
                console.error('OAuth error:', error);
                M.toast({html: 'OAuth initialization failed', classes: 'red'});
            });
    }
    
    // Payment redirect functionality
    function redirectToPayment(paymentUrl) {
        window.open(paymentUrl, '_blank');
    }
    
    // Show toast notifications
    function showToast(message, className = 'green') {
        M.toast({html: message, classes: className});
    }
    
    // Smooth scroll to section
    function scrollToSection(sectionId) {
        document.getElementById(sectionId).scrollIntoView({
            behavior: 'smooth'
        });
    }
    
    // Form validation
    function validateForm(formId) {
        const form = document.getElementById(formId);
        const inputs = form.querySelectorAll('input[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('invalid');
                isValid = false;
            } else {
                input.classList.remove('invalid');
                input.classList.add('valid');
            }
        });
        
        return isValid;
    }
    </script>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'token' not in st.session_state:
        st.session_state.token = None

# Header component
def render_header():
    st.markdown(f"""
    <div class="haven-header">
        <div class="container">
            <div class="row valign-wrapper">
                <div class="col s12 m6 l4">
                    <div class="center-align">
                        {f'<img src="data:image/png;base64,{logo_base64}" class="haven-logo" alt="HAVEN Logo">' if logo_base64 else ''}
                        <h1 class="haven-title">HAVEN</h1>
                        <p class="haven-subtitle">Crowdfunding Platform</p>
                    </div>
                </div>
                <div class="col s12 m6 l8">
                    <div class="right-align hide-on-small-only">
                        <h4 style="color: white; margin: 0;">Building Dreams Together</h4>
                        <p style="color: #e8f5e8; margin: 0;">Empowering communities through collaborative funding</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Navigation component
def render_navigation():
    st.markdown("""
    <div class="haven-nav">
        <a href="#" class="nav-item" onclick="scrollToSection('home')">
            <i class="material-icons">home</i>
            <span class="nav-tooltip">Home</span>
        </a>
        <a href="#" class="nav-item" onclick="scrollToSection('explore')">
            <i class="material-icons">explore</i>
            <span class="nav-tooltip">Explore</span>
        </a>
        <a href="#" class="nav-item" onclick="scrollToSection('search')">
            <i class="material-icons">search</i>
            <span class="nav-tooltip">Search</span>
        </a>
        <a href="#" class="nav-item" onclick="scrollToSection('profile')">
            <i class="material-icons">person</i>
            <span class="nav-tooltip">Profile</span>
        </a>
        <a href="#" class="nav-item" onclick="scrollToSection('logout')">
            <i class="material-icons">logout</i>
            <span class="nav-tooltip">Logout</span>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Floating Action Button
def render_fab():
    st.markdown("""
    <div class="fixed-action-btn">
        <a class="btn-floating btn-large waves-effect waves-light red" onclick="scrollToSection('create-campaign')">
            <i class="material-icons">add</i>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Authentication page
def render_auth_page():
    st.markdown('<div id="auth" class="section">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="haven-card fade-in">
            <div class="center-align">
                <h4 style="color: var(--haven-green); margin-bottom: 30px;">
                    <i class="material-icons left">account_circle</i>
                    Welcome to HAVEN
                </h4>
            </div>
        """, unsafe_allow_html=True)
        
        # Login/Register tabs
        tab1, tab2 = st.tabs(["Sign In", "Register"])
        
        with tab1:
            st.markdown("""
            <form id="loginForm" class="row">
                <div class="row">
                    <div class="input-field col s12">
                        <i class="material-icons prefix">email</i>
                        <input id="email" type="email" class="validate" required>
                        <label for="email">Email</label>
                        <span class="helper-text" data-error="Please enter a valid email" data-success="Valid email"></span>
                    </div>
                </div>

                <div class="row">
                    <div class="input-field col s12">
                        <i class="material-icons prefix">lock</i>
                        <input id="password" type="password" class="validate" required minlength="6">
                        <label for="password">Password</label>
                        <span class="helper-text" data-error="Password must be at least 6 characters" data-success="Valid password"></span>
                    </div>
                </div>

                <div class="row">
                    <div class="col s12">
                        <label>
                            <input type="checkbox" id="remember" />
                            <span>Remember me</span>
                        </label>
                    </div>
                </div>

                <div class="row">
                    <div class="col s6">
                        <button class="btn waves-effect waves-light btn-haven" type="submit" style="width: 100%;">
                            Sign In
                            <i class="material-icons right">send</i>
                        </button>
                    </div>
                    <div class="col s6">
                        <button class="btn waves-effect waves-light grey" type="button" style="width: 100%;">
                            Register
                            <i class="material-icons right">person_add</i>
                        </button>
                    </div>
                </div>
            </form>

            <div class="divider" style="margin: 30px 0;"></div>

            <div class="row">
                <div class="col s12 center-align">
                    <p style="color: #666; margin-bottom: 20px;">Or continue with:</p>
                </div>
            </div>

            <div class="row">
                <div class="col s6">
                    <button class="btn waves-effect waves-light google-btn oauth-btn pulse" style="width: 100%;" onclick="openOAuthPopup('google')">
                        <i class="material-icons left">search</i>Google
                    </button>
                </div>
                <div class="col s6">
                    <button class="btn waves-effect waves-light facebook-btn oauth-btn pulse" style="width: 100%;" onclick="openOAuthPopup('facebook')">
                        <i class="material-icons left">facebook</i>Facebook
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            with st.form("register_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name", placeholder="Enter your first name")
                    email = st.text_input("Email", placeholder="your.email@example.com")
                    user_type = st.selectbox("Account Type", ["individual", "organization", "ngo"])
                
                with col2:
                    last_name = st.text_input("Last Name", placeholder="Enter your last name")
                    phone = st.text_input("Phone", placeholder="+91-9876543210")
                    password = st.text_input("Password", type="password", placeholder="Minimum 6 characters")
                
                address = st.text_area("Address", placeholder="Enter your complete address")
                
                col1, col2 = st.columns(2)
                with col1:
                    terms_agreed = st.checkbox("I agree to the Terms and Conditions")
                with col2:
                    newsletter = st.checkbox("Subscribe to newsletter")
                
                submitted = st.form_submit_button("Create Account", use_container_width=True)
                
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
                                st.success("Account created successfully!")
                                st.rerun()
                            else:
                                st.error("Registration failed. Please try again.")
                        except Exception as e:
                            st.error(f"Registration error: {str(e)}")
                    else:
                        st.error("Please fill in all required fields and agree to terms.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Home page
def render_home_page():
    st.markdown('<div id="home" class="section">', unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div class="haven-card fade-in">
        <div class="center-align">
            <h3 style="color: var(--haven-green); margin-bottom: 20px;">
                <i class="material-icons large">favorite</i>
                Make a Difference Today
            </h3>
            <p style="font-size: 1.2rem; color: #666; margin-bottom: 30px;">
                Join thousands of people supporting meaningful causes and building a better tomorrow together.
            </p>
            <button class="btn-large waves-effect waves-light btn-haven">
                Start Exploring
                <i class="material-icons right">arrow_forward</i>
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Trending campaigns
    st.markdown("""
    <div class="haven-card slide-in-right">
        <h4 style="color: var(--haven-green); margin-bottom: 30px;">
            <i class="material-icons left">trending_up</i>
            Trending Campaigns
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
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
            st.error("Failed to load campaigns")
    except Exception as e:
        st.error(f"Error loading campaigns: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Campaign card component
def render_campaign_card(campaign):
    progress = min(100, (campaign["raised"] / campaign["goal"]) * 100)
    days_remaining = max(0, (datetime.fromisoformat(campaign["end_date"].replace('Z', '+00:00')) - datetime.now()).days)
    
    st.markdown(f"""
    <div class="campaign-card">
        <img src="{campaign.get('image_url', 'https://via.placeholder.com/400x200')}" 
             alt="{campaign['title']}" class="campaign-image">
        <div class="campaign-content">
            <h5 class="campaign-title">{campaign['title']}</h5>
            <p class="campaign-description">{campaign['description'][:100]}...</p>
            
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress}%;"></div>
            </div>
            
            <div class="campaign-stats">
                <div class="stat-item">
                    <div class="stat-value">₹{campaign['raised']:,.0f}</div>
                    <div class="stat-label">Raised</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{progress:.0f}%</div>
                    <div class="stat-label">Funded</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{days_remaining}</div>
                    <div class="stat-label">Days Left</div>
                </div>
            </div>
            
            <div class="center-align" style="margin-top: 20px;">
                <button class="btn waves-effect waves-light btn-haven" 
                        onclick="showDonationForm('{campaign['id']}')">
                    Donate Now
                    <i class="material-icons right">favorite</i>
                </button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Explore page
def render_explore_page():
    st.markdown('<div id="explore" class="section">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="haven-card fade-in">
        <h4 style="color: var(--haven-green); margin-bottom: 30px;">
            <i class="material-icons left">explore</i>
            Explore Categories
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Category grid
    categories = [
        {"name": "Medical", "icon": "local_hospital", "count": 45, "color": "#f44336"},
        {"name": "Education", "icon": "school", "count": 32, "color": "#2196f3"},
        {"name": "Community", "icon": "group", "count": 28, "color": "#4caf50"},
        {"name": "Environment", "icon": "eco", "count": 19, "color": "#8bc34a"},
        {"name": "Technology", "icon": "computer", "count": 15, "color": "#9c27b0"},
        {"name": "Arts", "icon": "palette", "count": 12, "color": "#ff9800"}
    ]
    
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="category-card" onclick="filterByCategory('{category['name'].lower()}')">
                <i class="material-icons category-icon" style="color: {category['color']};">
                    {category['icon']}
                </i>
                <div class="category-title">{category['name']}</div>
                <div class="category-count">{category['count']} campaigns</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Search page
def render_search_page():
    st.markdown('<div id="search" class="section">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="haven-card fade-in">
        <h4 style="color: var(--haven-green); margin-bottom: 30px;">
            <i class="material-icons left">search</i>
            Search Campaigns
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("search_form"):
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            search_query = st.text_input("Search campaigns", placeholder="Enter keywords...")
        
        with col2:
            category_filter = st.selectbox("Category", ["All", "Medical", "Education", "Community", "Environment", "Technology", "Arts"])
        
        with col3:
            st.write("")  # Spacing
            search_submitted = st.form_submit_button("Search", use_container_width=True)
        
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
                        st.success(f"Found {len(campaigns)} campaigns")
                        
                        # Display search results
                        for i in range(0, len(campaigns), 3):
                            cols = st.columns(3)
                            for j, col in enumerate(cols):
                                if i + j < len(campaigns):
                                    campaign = campaigns[i + j]
                                    with col:
                                        render_campaign_card(campaign)
                    else:
                        st.info("No campaigns found matching your search.")
                else:
                    st.error("Search failed. Please try again.")
            except Exception as e:
                st.error(f"Search error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Donation form
def render_donation_form():
    st.markdown('<div id="donation" class="section">', unsafe_allow_html=True)
    
    if 'selected_campaign' in st.session_state:
        campaign = st.session_state.selected_campaign
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"""
            <div class="haven-card fade-in">
                <h4 style="color: var(--haven-green); margin-bottom: 20px;">
                    <i class="material-icons left">favorite</i>
                    Donate to: {campaign['title']}
                </h4>
                <p style="color: #666; margin-bottom: 30px;">
                    Your contribution will make a real difference!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("donation_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    donor_name = st.text_input("Full Name", placeholder="Enter your full name")
                    donor_email = st.text_input("Email", placeholder="your.email@example.com")
                
                with col2:
                    donor_phone = st.text_input("Phone Number", placeholder="+91-9876543210")
                    amount = st.number_input("Donation Amount (₹)", min_value=100, max_value=100000, value=1000)
                
                message = st.text_area("Message (Optional)", placeholder="Leave a message for the campaign creator...")
                is_anonymous = st.checkbox("Make this donation anonymous")
                
                submitted = st.form_submit_button("Donate Now", use_container_width=True)
                
                if submitted:
                    if donor_name and donor_email and donor_phone and amount:
                        # Create donation payment
                        donation_data = {
                            "campaign_id": campaign["id"],
                            "amount": amount,
                            "donor_name": donor_name,
                            "donor_email": donor_email,
                            "donor_phone": donor_phone,
                            "message": message,
                            "is_anonymous": is_anonymous
                        }
                        
                        try:
                            headers = {"Authorization": f"Bearer {st.session_state.token}"}
                            response = requests.post(
                                f"{BACKEND_URL}/api/payments/create-donation",
                                json=donation_data,
                                headers=headers
                            )
                            
                            if response.status_code == 200:
                                payment_data = response.json()
                                
                                st.success("Redirecting to payment gateway...")
                                st.markdown(f"""
                                <script>
                                    redirectToPayment('{payment_data["payment_url"]}');
                                </script>
                                """, unsafe_allow_html=True)
                                
                                st.info(f"Payment ID: {payment_data['payment_request_id']}")
                                st.info(f"Amount: ₹{payment_data['amount']}")
                            else:
                                st.error("Failed to create payment. Please try again.")
                        except Exception as e:
                            st.error(f"Payment error: {str(e)}")
                    else:
                        st.error("Please fill in all required fields.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main app
def main():
    # Load CSS and JavaScript
    load_css()
    load_javascript()
    
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
        
        # Render floating action button
        render_fab()
        
        # Render main content
        render_home_page()
        render_explore_page()
        render_search_page()
        
        # Render donation form if campaign selected
        if 'selected_campaign' in st.session_state:
            render_donation_form()

if __name__ == "__main__":
    main()

