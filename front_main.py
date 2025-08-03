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

# Custom CSS with MaterializeCSS and HAVEN styling - FIXED HTML RENDERING
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
        --text-dark: #212121;
        --text-light: #ffffff;
        --background-light: #ffffff;
        --background-dark: #2e7d32;
    }
    
    /* Full page background */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        font-family: 'Roboto', sans-serif;
        font-size: 18px; /* Bigger base font size */
    }
    
    /* Header styling - Dark background with light text */
    .haven-header {
        background: linear-gradient(135deg, var(--haven-dark-green) 0%, var(--haven-green) 100%);
        padding: 25px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin-bottom: 40px;
    }
    
    .haven-logo {
        max-height: 70px;
        width: auto;
    }
    
    .haven-title {
        color: var(--text-light); /* Light text on dark background */
        font-size: 3rem; /* Bigger font */
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .haven-subtitle {
        color: #e8f5e8; /* Light text on dark background */
        font-size: 1.4rem; /* Bigger font */
        margin: 0;
        font-weight: 300;
    }
    
    .header-tagline {
        color: var(--text-light); /* Light text on dark background */
        font-size: 1.6rem; /* Bigger font */
        margin: 0;
        font-weight: 500;
    }
    
    .header-description {
        color: #e8f5e8; /* Light text on dark background */
        font-size: 1.1rem; /* Bigger font */
        margin: 0;
        font-weight: 300;
    }
    
    /* Navigation styling - Light background with dark text */
    .haven-nav {
        position: fixed;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        z-index: 1000;
        background: var(--background-light); /* Light background */
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 15px 10px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.1);
    }
    
    .nav-item {
        display: block;
        padding: 12px;
        margin: 8px 0;
        color: var(--text-dark); /* Dark text on light background */
        text-decoration: none;
        border-radius: 50%;
        transition: all 0.3s ease;
        text-align: center;
        position: relative;
        font-size: 1.2rem; /* Bigger icons */
    }
    
    .nav-item:hover {
        background: var(--haven-green);
        color: var(--text-light); /* Light text on dark background when hovered */
        transform: scale(1.1);
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
    }
    
    .nav-tooltip {
        position: absolute;
        right: 60px;
        top: 50%;
        transform: translateY(-50%);
        background: var(--text-dark); /* Dark background */
        color: var(--text-light); /* Light text */
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 16px; /* Bigger font */
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
        font-weight: 500;
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
            padding: 15px;
        }
        
        .nav-item {
            margin: 0;
            flex: 1;
        }
        
        .nav-tooltip {
            display: none;
        }
    }
    
    /* Card styling - Light background with dark text */
    .haven-card {
        background: var(--background-light); /* Light background */
        color: var(--text-dark); /* Dark text */
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        padding: 40px;
        margin: 30px 0;
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .haven-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }
    
    .haven-card h3, .haven-card h4, .haven-card h5 {
        color: var(--text-dark); /* Dark text on light background */
        font-weight: 600;
    }
    
    .haven-card p {
        color: #424242; /* Dark gray text on light background */
        font-size: 1.1rem; /* Bigger font */
        line-height: 1.7;
    }
    
    /* Campaign card styling - Light background with dark text */
    .campaign-card {
        background: var(--background-light); /* Light background */
        color: var(--text-dark); /* Dark text */
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin: 25px 0;
    }
    
    .campaign-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 70px rgba(0,0,0,0.2);
    }
    
    .campaign-image {
        width: 100%;
        height: 220px;
        object-fit: cover;
    }
    
    .campaign-content {
        padding: 30px;
    }
    
    .campaign-title {
        font-size: 1.6rem; /* Bigger font */
        font-weight: 600;
        color: var(--text-dark); /* Dark text on light background */
        margin-bottom: 15px;
        line-height: 1.4;
    }
    
    .campaign-description {
        color: #424242; /* Dark gray text on light background */
        font-size: 1.1rem; /* Bigger font */
        line-height: 1.7;
        margin-bottom: 25px;
    }
    
    .progress-container {
        background: #f5f5f5;
        border-radius: 12px;
        height: 10px;
        margin: 20px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, var(--haven-green), var(--haven-light-green));
        height: 100%;
        border-radius: 12px;
        transition: width 0.3s ease;
    }
    
    .campaign-stats {
        display: flex;
        justify-content: space-between;
        margin: 20px 0;
        font-size: 1rem; /* Bigger font */
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-weight: 600;
        color: var(--haven-green);
        font-size: 1.3rem; /* Bigger font */
    }
    
    .stat-label {
        color: #424242; /* Dark text on light background */
        font-size: 1rem; /* Bigger font */
        font-weight: 500;
    }
    
    /* Button styling */
    .btn-haven {
        background: linear-gradient(135deg, var(--haven-green), var(--haven-light-green));
        border: none;
        color: var(--text-light); /* Light text on dark background */
        padding: 15px 35px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1.1rem; /* Bigger font */
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
    }
    
    .btn-haven:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.4);
        background: linear-gradient(135deg, var(--haven-dark-green), var(--haven-green));
        color: var(--text-light); /* Keep light text */
    }
    
    /* Floating Action Button */
    .fixed-action-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
    }
    
    .btn-floating.btn-large {
        width: 75px;
        height: 75px;
        background: linear-gradient(135deg, #f44336, #d32f2f);
        box-shadow: 0 8px 25px rgba(244, 67, 54, 0.4);
        transition: all 0.3s ease;
    }
    
    .btn-floating.btn-large:hover {
        transform: scale(1.15) rotate(90deg);
        box-shadow: 0 15px 40px rgba(244, 67, 54, 0.6);
    }
    
    .btn-floating.btn-large i {
        line-height: 75px;
        font-size: 2.2rem; /* Bigger icon */
        color: var(--text-light); /* Light text on dark background */
    }
    
    /* OAuth button styling */
    .oauth-btn {
        width: 100%;
        margin: 15px 0;
        padding: 18px;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        font-size: 1.1rem; /* Bigger font */
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }
    
    .google-btn {
        background: #db4437;
        color: var(--text-light); /* Light text on dark background */
    }
    
    .google-btn:hover {
        background: #c23321;
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(219, 68, 55, 0.4);
        color: var(--text-light); /* Keep light text */
    }
    
    .facebook-btn {
        background: #3b5998;
        color: var(--text-light); /* Light text on dark background */
    }
    
    .facebook-btn:hover {
        background: #2d4373;
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(59, 89, 152, 0.4);
        color: var(--text-light); /* Keep light text */
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
            box-shadow: 0 0 0 15px rgba(76, 175, 80, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
        }
    }
    
    /* Form styling - Light background with dark text */
    .input-field {
        margin-bottom: 25px;
    }
    
    .input-field input, .input-field textarea {
        color: var(--text-dark); /* Dark text on light background */
        font-size: 1.1rem; /* Bigger font */
    }
    
    .input-field label {
        color: #424242; /* Dark text on light background */
        font-size: 1rem; /* Bigger font */
    }
    
    .input-field input:focus + label {
        color: var(--haven-green) !important;
    }
    
    .input-field input:focus {
        border-bottom: 2px solid var(--haven-green) !important;
        box-shadow: 0 1px 0 0 var(--haven-green) !important;
    }
    
    .input-field .prefix {
        color: #424242; /* Dark text */
        font-size: 1.2rem; /* Bigger icons */
    }
    
    .input-field .prefix.active {
        color: var(--haven-green);
    }
    
    .helper-text {
        font-size: 0.9rem; /* Bigger font */
        color: #424242; /* Dark text */
    }
    
    /* Category grid - Light background with dark text */
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 25px;
        margin: 40px 0;
    }
    
    .category-card {
        background: var(--background-light); /* Light background */
        color: var(--text-dark); /* Dark text */
        border-radius: 20px;
        padding: 35px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .category-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }
    
    .category-icon {
        font-size: 3.5rem; /* Bigger icons */
        color: var(--haven-green);
        margin-bottom: 20px;
    }
    
    .category-title {
        font-size: 1.4rem; /* Bigger font */
        font-weight: 600;
        color: var(--text-dark); /* Dark text on light background */
        margin-bottom: 12px;
    }
    
    .category-count {
        color: #424242; /* Dark text on light background */
        font-size: 1rem; /* Bigger font */
        font-weight: 500;
    }
    
    /* Text styling rules */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-dark); /* Dark text on light backgrounds */
        font-weight: 600;
    }
    
    p, span, div {
        color: var(--text-dark); /* Dark text on light backgrounds */
    }
    
    /* Dark background elements get light text */
    .haven-header *, 
    .btn-haven *, 
    .oauth-btn *, 
    .btn-floating * {
        color: var(--text-light) !important; /* Light text on dark backgrounds */
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .haven-title {
            font-size: 2.5rem; /* Bigger mobile font */
        }
        
        .haven-subtitle {
            font-size: 1.2rem; /* Bigger mobile font */
        }
        
        .header-tagline {
            font-size: 1.4rem; /* Bigger mobile font */
        }
        
        .header-description {
            font-size: 1rem; /* Bigger mobile font */
        }
        
        .haven-card {
            padding: 25px;
            margin: 20px 0;
        }
        
        .campaign-content {
            padding: 25px;
        }
        
        .campaign-title {
            font-size: 1.4rem; /* Bigger mobile font */
        }
        
        .campaign-description {
            font-size: 1rem; /* Bigger mobile font */
        }
        
        .fixed-action-btn {
            bottom: 120px;
            right: 20px;
        }
        
        .btn-floating.btn-large {
            width: 65px;
            height: 65px;
        }
        
        .btn-floating.btn-large i {
            line-height: 65px;
            font-size: 1.8rem;
        }
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in-right {
        animation: slideInRight 0.6s ease-out;
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
        const element = document.getElementById(sectionId);
        if (element) {
            element.scrollIntoView({
                behavior: 'smooth'
            });
        }
    }
    
    // Form validation
    function validateForm(formId) {
        const form = document.getElementById(formId);
        if (!form) return false;
        
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

# Header component - FIXED HTML RENDERING
def render_header():
    header_html = f"""
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
                        <h4 class="header-tagline">Building Dreams Together</h4>
                        <p class="header-description">Empowering communities through collaborative funding</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

# Navigation component - FIXED HTML RENDERING
def render_navigation():
    nav_html = """
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
    """
    st.markdown(nav_html, unsafe_allow_html=True)

# Floating Action Button - FIXED HTML RENDERING
def render_fab():
    fab_html = """
    <div class="fixed-action-btn">
        <a class="btn-floating btn-large waves-effect waves-light red" onclick="scrollToSection('create-campaign')">
            <i class="material-icons">add</i>
        </a>
    </div>
    """
    st.markdown(fab_html, unsafe_allow_html=True)

# Authentication page - FIXED HTML RENDERING
def render_auth_page():
    st.markdown('<div id="auth" class="section">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Welcome card
        welcome_html = """
        <div class="haven-card fade-in">
            <div class="center-align">
                <h3 style="color: var(--haven-green); margin-bottom: 30px;">
                    <i class="material-icons large">account_circle</i>
                    Welcome to HAVEN
                </h3>
                <p style="font-size: 1.2rem; margin-bottom: 30px;">
                    Join thousands of people supporting meaningful causes and building a better tomorrow together.
                </p>
            </div>
        </div>
        """
        st.markdown(welcome_html, unsafe_allow_html=True)
        
        # Login/Register tabs
        tab1, tab2 = st.tabs(["Sign In", "Register"])
        
        with tab1:
            # OAuth buttons - FIXED HTML RENDERING
            oauth_html = """
            <div class="center-align" style="margin: 30px 0;">
                <p style="font-size: 1.1rem; margin-bottom: 25px;">Sign in with your account:</p>
                
                <button class="oauth-btn google-btn pulse" onclick="openOAuthPopup('google')">
                    <i class="material-icons">search</i>
                    Continue with Google
                </button>
                
                <button class="oauth-btn facebook-btn pulse" onclick="openOAuthPopup('facebook')">
                    <i class="material-icons">facebook</i>
                    Continue with Facebook
                </button>
                
                <div class="divider" style="margin: 30px 0;"></div>
                <p style="font-size: 1rem; color: #666;">Or sign in with email:</p>
            </div>
            """
            st.markdown(oauth_html, unsafe_allow_html=True)
            
            # Email login form
            with st.form("login_form"):
                email = st.text_input("Email Address", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                remember_me = st.checkbox("Remember me")
                
                col1, col2 = st.columns(2)
                with col1:
                    login_submitted = st.form_submit_button("Sign In", use_container_width=True)
                with col2:
                    register_button = st.form_submit_button("Create Account", use_container_width=True)
                
                if login_submitted:
                    if email and password:
                        try:
                            response = requests.post(f"{BACKEND_URL}/api/auth/login", 
                                                   params={"email": email, "password": password})
                            if response.status_code == 200:
                                result = response.json()
                                st.session_state.token = result["access_token"]
                                st.session_state.user = result["user"]
                                st.success("Login successful!")
                                st.rerun()
                            else:
                                st.error("Invalid email or password")
                        except Exception as e:
                            st.error(f"Login error: {str(e)}")
                    else:
                        st.error("Please enter both email and password")
        
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

# Home page - FIXED HTML RENDERING
def render_home_page():
    st.markdown('<div id="home" class="section">', unsafe_allow_html=True)
    
    # Hero section
    hero_html = """
    <div class="haven-card fade-in">
        <div class="center-align">
            <h3 style="margin-bottom: 25px;">
                <i class="material-icons large" style="color: var(--haven-green);">favorite</i>
                Make a Difference Today
            </h3>
            <p style="font-size: 1.3rem; margin-bottom: 35px;">
                Join thousands of people supporting meaningful causes and building a better tomorrow together.
            </p>
            <button class="btn-large waves-effect waves-light btn-haven">
                Start Exploring
                <i class="material-icons right">arrow_forward</i>
            </button>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)
    
    # Trending campaigns header
    trending_header_html = """
    <div class="haven-card slide-in-right">
        <h4 style="margin-bottom: 30px;">
            <i class="material-icons left" style="color: var(--haven-green);">trending_up</i>
            Trending Campaigns
        </h4>
        <p style="font-size: 1.1rem;">
            Discover the most popular campaigns making a real impact in communities worldwide.
        </p>
    </div>
    """
    st.markdown(trending_header_html, unsafe_allow_html=True)
    
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

# Campaign card component - FIXED HTML RENDERING
def render_campaign_card(campaign):
    progress = min(100, (campaign["raised"] / campaign["goal"]) * 100)
    try:
        end_date = datetime.fromisoformat(campaign["end_date"].replace('Z', '+00:00'))
        days_remaining = max(0, (end_date - datetime.now()).days)
    except:
        days_remaining = 30  # Default fallback
    
    campaign_html = f"""
    <div class="campaign-card">
        <img src="{campaign.get('image_url', 'https://via.placeholder.com/400x220')}" 
             alt="{campaign['title']}" class="campaign-image">
        <div class="campaign-content">
            <h5 class="campaign-title">{campaign['title']}</h5>
            <p class="campaign-description">{campaign['description'][:120]}...</p>
            
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
            
            <div class="center-align" style="margin-top: 25px;">
                <button class="btn waves-effect waves-light btn-haven">
                    Donate Now
                    <i class="material-icons right">favorite</i>
                </button>
            </div>
        </div>
    </div>
    """
    st.markdown(campaign_html, unsafe_allow_html=True)

# Explore page - FIXED HTML RENDERING
def render_explore_page():
    st.markdown('<div id="explore" class="section">', unsafe_allow_html=True)
    
    explore_header_html = """
    <div class="haven-card fade-in">
        <h4 style="margin-bottom: 30px;">
            <i class="material-icons left" style="color: var(--haven-green);">explore</i>
            Explore Categories
        </h4>
        <p style="font-size: 1.1rem;">
            Browse campaigns by category to find causes that matter to you.
        </p>
    </div>
    """
    st.markdown(explore_header_html, unsafe_allow_html=True)
    
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
            category_html = f"""
            <div class="category-card">
                <i class="material-icons category-icon" style="color: {category['color']};">
                    {category['icon']}
                </i>
                <div class="category-title">{category['name']}</div>
                <div class="category-count">{category['count']} campaigns</div>
            </div>
            """
            st.markdown(category_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Search page - FIXED HTML RENDERING
def render_search_page():
    st.markdown('<div id="search" class="section">', unsafe_allow_html=True)
    
    search_header_html = """
    <div class="haven-card fade-in">
        <h4 style="margin-bottom: 30px;">
            <i class="material-icons left" style="color: var(--haven-green);">search</i>
            Search Campaigns
        </h4>
        <p style="font-size: 1.1rem;">
            Find specific campaigns using keywords and filters.
        </p>
    </div>
    """
    st.markdown(search_header_html, unsafe_allow_html=True)
    
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

if __name__ == "__main__":
    main()

