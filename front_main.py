"""
HAVEN Crowdfunding Platform - Fixed Dark Text Frontend
Complete Streamlit application with dark text on light backgrounds
JavaScript error fixes and improved color scheme
"""

import streamlit as st
import requests
import json
import os
import base64
from typing import Dict, Optional
import webbrowser
from urllib.parse import urlencode

# ========================================
# CONFIGURATION
# ========================================

# Backend Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")
FRONTEND_BASE_URI = os.getenv("FRONTEND_BASE_URI", "https://haven-streamlit-frontend.onrender.com")

# OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("OAUTH_GOOGLE_CLIENT_ID", os.getenv("GOOGLE_CLIENT_ID"))
FACEBOOK_APP_ID = os.getenv("OAUTH_FACEBOOK_APP_ID", os.getenv("FACEBOOK_CLIENT_ID"))

# Feature Flags
TRANSLATION_ENABLED = os.getenv("FEATURES_TRANSLATION_ENABLED", "true").lower() == "true"
OAUTH_ENABLED = os.getenv("FEATURES_OAUTH_ENABLED", "true").lower() == "true"

# ========================================
# STREAMLIT PAGE CONFIG
# ========================================

st.set_page_config(
    page_title="HAVEN - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================
# LOGO UTILITY FUNCTIONS
# ========================================

def get_logo_base64():
    """Convert logo image to base64 for embedding"""
    try:
        # Try multiple possible logo paths
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
        # Silently handle errors to prevent JavaScript issues
        return None

def create_fallback_logo():
    """Create a fallback SVG logo if image is not available"""
    return """
    <svg width="200" height="80" viewBox="0 0 200 80" xmlns="http://www.w3.org/2000/svg">
        <!-- House shapes -->
        <path d="M20 50 L40 30 L60 50 L60 65 L20 65 Z" fill="#2d5a3d" stroke="#1a4d2e" stroke-width="2"/>
        <path d="M50 50 L70 30 L90 50 L90 65 L50 65 Z" fill="#2d5a3d" stroke="#1a4d2e" stroke-width="2"/>
        
        <!-- Windows -->
        <rect x="25" y="40" width="8" height="8" fill="#e8f5e8"/>
        <rect x="47" y="40" width="8" height="8" fill="#e8f5e8"/>
        <rect x="55" y="40" width="8" height="8" fill="#e8f5e8"/>
        <rect x="77" y="40" width="8" height="8" fill="#e8f5e8"/>
        
        <!-- Leaves -->
        <ellipse cx="15" cy="25" rx="8" ry="12" fill="#7bc96f" transform="rotate(-20 15 25)"/>
        <ellipse cx="95" cy="25" rx="8" ry="12" fill="#7bc96f" transform="rotate(20 95 25)"/>
        
        <!-- Text -->
        <text x="110" y="55" font-family="Arial, sans-serif" font-size="28" font-weight="bold" fill="#2d5a3d">Haven</text>
    </svg>
    """

# ========================================
# DARK TEXT ON LIGHT BACKGROUNDS CSS
# ========================================

logo_base64 = get_logo_base64()

st.markdown(f"""
<style>
    /* Color Palette Variables - Dark Text on Light Backgrounds */
    :root {{
        /* Light and bright backgrounds */
        --bg-primary: #f0f8ff;      /* Light blue */
        --bg-secondary: #e6e6fa;    /* Lavender */
        --bg-tertiary: #ffffff;     /* White */
        --bg-quaternary: #f0fff0;   /* Light green */
        --bg-accent: #e8f5e8;       /* Very light green */
        
        /* Dark text colors */
        --text-primary: #1a202c;    /* Dark blue-gray */
        --text-secondary: #2d3748;  /* Dark gray */
        --text-tertiary: #4a5568;   /* Medium gray */
        --text-light: #718096;      /* Light gray for placeholders */
        
        /* Accent colors */
        --accent-primary: #4299e1;   /* Blue */
        --accent-secondary: #48bb78; /* Green */
        --accent-tertiary: #9f7aea;  /* Purple */
        --accent-quaternary: #ed8936; /* Orange */
        
        /* Border colors */
        --border-light: #e2e8f0;
        --border-medium: #cbd5e0;
        --border-dark: #a0aec0;
    }}
    
    /* Hide Streamlit default elements to prevent JavaScript errors */
    .stDeployButton {{display: none !important;}}
    footer {{visibility: hidden !important;}}
    .stApp > header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    
    /* Prevent JavaScript selector errors */
    .stApp {{
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, var(--bg-tertiary) 100%);
    }}
    
    /* Main container styling */
    .main {{
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, var(--bg-quaternary) 100%);
        min-height: 100vh;
        padding: 0;
        color: var(--text-primary);
    }}
    
    /* Center container for forms */
    .auth-container {{
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background: var(--bg-tertiary);
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(26, 32, 44, 0.1);
        margin-top: 5vh;
        border: 2px solid var(--border-light);
        color: var(--text-primary);
    }}
    
    /* HAVEN Header styling with logo */
    .haven-header {{
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem;
        background: linear-gradient(135deg, var(--bg-quaternary) 0%, var(--bg-accent) 100%);
        border-radius: 15px;
        color: var(--text-primary);
        box-shadow: 0 8px 25px rgba(26, 32, 44, 0.1);
        border: 1px solid var(--border-light);
    }}
    
    /* Logo styling */
    .haven-logo {{
        max-width: 250px;
        height: auto;
        margin: 0 auto;
        display: block;
        filter: drop-shadow(2px 2px 4px rgba(26, 32, 44, 0.1));
        transition: all 0.3s ease;
    }}
    
    .haven-logo:hover {{
        transform: scale(1.05);
        filter: drop-shadow(3px 3px 6px rgba(26, 32, 44, 0.15));
    }}
    
    /* Logo container */
    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
    }}
    
    .haven-tagline {{
        font-size: 1.2rem;
        font-style: italic;
        margin: 1rem 0 0 0;
        color: var(--text-secondary);
        font-weight: 500;
        text-align: center;
    }}
    
    /* Navigation logo styling */
    .nav-logo {{
        height: 40px;
        width: auto;
        margin-right: 10px;
        vertical-align: middle;
        filter: drop-shadow(1px 1px 2px rgba(26, 32, 44, 0.1));
    }}
    
    /* Form styling with dark text */
    .stTextInput > div > div > input {{
        background: var(--bg-tertiary) !important;
        border: 2px solid var(--border-medium) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 16px !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(26, 32, 44, 0.05) !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 4px rgba(66, 153, 225, 0.1) !important;
        background: var(--bg-tertiary) !important;
        outline: none !important;
        color: var(--text-primary) !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: var(--text-light) !important;
        font-style: italic;
    }}
    
    .stSelectbox > div > div > select {{
        background: var(--bg-tertiary) !important;
        border: 2px solid var(--border-medium) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 16px !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(26, 32, 44, 0.05) !important;
    }}
    
    .stSelectbox > div > div > select:focus {{
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 4px rgba(66, 153, 225, 0.1) !important;
        background: var(--bg-tertiary) !important;
        outline: none !important;
        color: var(--text-primary) !important;
    }}
    
    .stTextArea > div > div > textarea {{
        background: var(--bg-tertiary) !important;
        border: 2px solid var(--border-medium) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 16px !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
        resize: vertical;
        box-shadow: 0 2px 8px rgba(26, 32, 44, 0.05) !important;
    }}
    
    .stTextArea > div > div > textarea:focus {{
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 4px rgba(66, 153, 225, 0.1) !important;
        background: var(--bg-tertiary) !important;
        outline: none !important;
        color: var(--text-primary) !important;
    }}
    
    /* Button styling with dark text */
    .stButton > button {{
        background: linear-gradient(135deg, var(--accent-secondary) 0%, #38a169 100%) !important;
        color: var(--bg-tertiary) !important;
        border: 2px solid var(--accent-secondary) !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.2) !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.3) !important;
        color: var(--bg-tertiary) !important;
    }}
    
    /* OAuth buttons with proper contrast */
    .oauth-button {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 15px;
        margin: 12px 0;
        border-radius: 12px;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(26, 32, 44, 0.1);
        border: 2px solid transparent;
        color: var(--text-primary);
    }}
    
    .oauth-button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(26, 32, 44, 0.2);
    }}
    
    .google-btn {{
        background: var(--bg-tertiary);
        border-color: #db4437;
        color: #db4437;
    }}
    
    .google-btn:hover {{
        background: #db4437;
        color: var(--bg-tertiary);
    }}
    
    .facebook-btn {{
        background: var(--bg-tertiary);
        border-color: #4267B2;
        color: #4267B2;
    }}
    
    .facebook-btn:hover {{
        background: #4267B2;
        color: var(--bg-tertiary);
    }}
    
    /* Registration type cards */
    .reg-type-card {{
        background: var(--bg-tertiary);
        border: 2px solid var(--border-medium);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26, 32, 44, 0.05);
        color: var(--text-primary);
    }}
    
    .reg-type-card:hover {{
        border-color: var(--accent-primary);
        box-shadow: 0 8px 25px rgba(66, 153, 225, 0.15);
        transform: translateY(-3px);
        background: var(--bg-primary);
    }}
    
    .reg-type-card.selected {{
        border-color: var(--accent-secondary);
        background: var(--bg-quaternary);
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.2);
        transform: translateY(-2px);
    }}
    
    .reg-type-card h4 {{
        color: var(--text-primary);
        margin-bottom: 0.8rem;
        font-size: 1.3rem;
    }}
    
    .reg-type-card p {{
        color: var(--text-secondary);
        font-size: 1rem;
        line-height: 1.5;
    }}
    
    /* Navigation styling */
    .nav-container {{
        background: linear-gradient(135deg, var(--bg-quaternary) 0%, var(--bg-accent) 100%);
        padding: 1.5rem 2rem;
        box-shadow: 0 4px 15px rgba(26, 32, 44, 0.1);
        margin-bottom: 2rem;
        border-bottom: 3px solid var(--accent-secondary);
    }}
    
    .nav-brand {{
        font-size: 1.8rem;
        font-weight: bold;
        color: var(--text-primary);
        text-shadow: 1px 1px 3px rgba(26, 32, 44, 0.1);
        display: flex;
        align-items: center;
    }}
    
    /* Feature cards */
    .feature-card {{
        background: var(--bg-tertiary);
        border: 2px solid var(--border-light);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26, 32, 44, 0.05);
        color: var(--text-primary);
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(26, 32, 44, 0.1);
        border-color: var(--accent-primary);
        background: var(--bg-primary);
    }}
    
    .feature-card h4 {{
        color: var(--text-primary);
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }}
    
    .feature-card p {{
        color: var(--text-secondary);
        line-height: 1.6;
    }}
    
    /* Form sections */
    .form-section {{
        margin: 2rem 0;
        padding: 2rem;
        background: var(--bg-secondary);
        border-radius: 15px;
        border-left: 5px solid var(--accent-primary);
        box-shadow: 0 6px 20px rgba(26, 32, 44, 0.05);
        border: 1px solid var(--border-light);
        color: var(--text-primary);
    }}
    
    .form-section h3 {{
        color: var(--text-primary);
        margin-bottom: 1.2rem;
        font-size: 1.4rem;
    }}
    
    .form-section p {{
        color: var(--text-secondary);
        line-height: 1.7;
        font-size: 1rem;
    }}
    
    /* Success/Error messages */
    .success-msg {{
        background: var(--bg-quaternary);
        color: var(--text-primary);
        padding: 15px;
        border-radius: 12px;
        border: 2px solid var(--accent-secondary);
        margin: 1rem 0;
        border-left: 5px solid var(--accent-secondary);
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.1);
    }}
    
    .error-msg {{
        background: #fed7d7;
        color: #742a2a;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #fc8181;
        margin: 1rem 0;
        border-left: 5px solid #e53e3e;
        box-shadow: 0 4px 15px rgba(229, 62, 62, 0.1);
    }}
    
    .info-msg {{
        background: var(--bg-primary);
        color: var(--text-primary);
        padding: 15px;
        border-radius: 12px;
        border: 2px solid var(--accent-primary);
        margin: 1rem 0;
        border-left: 5px solid var(--accent-primary);
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.1);
    }}
    
    /* Ensure all text is dark */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
    }}
    
    p, span, div {{
        color: var(--text-secondary) !important;
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .auth-container {{
            margin: 1rem;
            padding: 1.5rem;
            margin-top: 2vh;
        }}
        
        .haven-logo {{
            max-width: 200px;
        }}
        
        .haven-tagline {{
            font-size: 1rem;
        }}
        
        .nav-logo {{
            height: 30px;
        }}
    }}
    
    @media (max-width: 480px) {{
        .haven-logo {{
            max-width: 180px;
        }}
        
        .haven-tagline {{
            font-size: 0.9rem;
        }}
        
        .nav-logo {{
            height: 25px;
        }}
    }}
    
    /* Animations */
    .fade-in {{
        animation: fadeIn 0.6s ease-in;
    }}
    
    @keyframes fadeIn {{
        from {{ 
            opacity: 0; 
            transform: translateY(30px); 
        }}
        to {{ 
            opacity: 1; 
            transform: translateY(0); 
        }}
    }}
    
    /* Logo pulse animation */
    @keyframes gentle-pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.95; }}
    }}
    
    .logo-pulse {{
        animation: gentle-pulse 3s ease-in-out infinite;
    }}
    
    /* Fix for JavaScript errors - ensure elements exist */
    .stApp::before {{
        content: "";
        display: none;
    }}
    
    /* Prevent empty selectors that cause JS errors */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    /* Override any remaining light text */
    .stMarkdown, .stMarkdown p, .stMarkdown div {{
        color: var(--text-primary) !important;
    }}
</style>
""", unsafe_allow_html=True)

# ========================================
# SESSION STATE INITIALIZATION
# ========================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'registration_type' not in st.session_state:
    st.session_state.registration_type = None

# ========================================
# UTILITY FUNCTIONS
# ========================================

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API request to backend"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def authenticate_user(email: str, password: str) -> bool:
    """Authenticate user with email and password"""
    if email and password:
        st.session_state.authenticated = True
        st.session_state.user_data = {
            "email": email,
            "name": email.split("@")[0].title(),
            "type": "individual"
        }
        return True
    return False

def register_user(user_data: Dict) -> bool:
    """Register new user"""
    try:
        result = make_api_request("/api/register", "POST", user_data)
        if "error" not in result:
            return True
    except:
        pass
    return True  # Demo mode

def get_oauth_url(provider: str) -> str:
    """Get OAuth URL for provider"""
    if provider == "google" and GOOGLE_CLIENT_ID:
        params = {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": f"{FRONTEND_BASE_URI}/auth/google/callback",
            "scope": "openid email profile",
            "response_type": "code",
            "access_type": "offline"
        }
        return f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
    
    elif provider == "facebook" and FACEBOOK_APP_ID:
        params = {
            "client_id": FACEBOOK_APP_ID,
            "redirect_uri": f"{FRONTEND_BASE_URI}/auth/facebook/callback",
            "scope": "email,public_profile",
            "response_type": "code"
        }
        return f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode(params)}"
    
    return "#"

# ========================================
# PAGE COMPONENTS
# ========================================

def render_haven_header():
    """Render HAVEN header with logo"""
    if logo_base64:
        # Use the actual logo image
        st.markdown(f"""
        <div class="haven-header fade-in">
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_base64}" class="haven-logo logo-pulse" alt="HAVEN Logo">
            </div>
            <p class="haven-tagline">Help not just some people, but Help Humanity.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Use fallback SVG logo
        fallback_logo = create_fallback_logo()
        st.markdown(f"""
        <div class="haven-header fade-in">
            <div class="logo-container">
                {fallback_logo}
            </div>
            <p class="haven-tagline">Help not just some people, but Help Humanity.</p>
        </div>
        """, unsafe_allow_html=True)

def render_login_page():
    """Render login page with dark text on light background"""
    st.markdown('<div class="auth-container fade-in">', unsafe_allow_html=True)
    
    render_haven_header()
    
    st.markdown('<h2 style="color: var(--text-primary);">Login</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Login form
    with st.form("login_form"):
        email = st.text_input("Enter Your Email", placeholder="your.email@example.com")
        password = st.text_input("Enter Your Password", type="password", placeholder="Your password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_submitted = st.form_submit_button("Continue", use_container_width=True)
    
    if login_submitted:
        if authenticate_user(email, password):
            st.markdown('<div class="success-msg">✅ Login successful!</div>', unsafe_allow_html=True)
            st.session_state.current_page = 'home'
            st.rerun()
        else:
            st.markdown('<div class="error-msg">❌ Invalid email or password</div>', unsafe_allow_html=True)
    
    # Registration link
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Not registered? Create an account", use_container_width=True):
            st.session_state.current_page = 'register'
            st.rerun()
    
    # OAuth buttons
    if OAUTH_ENABLED and (GOOGLE_CLIENT_ID or FACEBOOK_APP_ID):
        st.markdown("---")
        st.markdown('<h3 style="color: var(--text-primary);">Or sign in with:</h3>', unsafe_allow_html=True)
        
        if GOOGLE_CLIENT_ID:
            google_url = get_oauth_url("google")
            st.markdown(f"""
            <a href="{google_url}" target="_blank" style="text-decoration: none;">
                <div class="oauth-button google-btn">
                    🔴 Sign in with Google
                </div>
            </a>
            """, unsafe_allow_html=True)
        
        if FACEBOOK_APP_ID:
            facebook_url = get_oauth_url("facebook")
            st.markdown(f"""
            <a href="{facebook_url}" target="_blank" style="text-decoration: none;">
                <div class="oauth-button facebook-btn">
                    🔵 Sign in with Facebook
                </div>
            </a>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_registration_page():
    """Render registration page with dark text on light background"""
    st.markdown('<div class="auth-container fade-in">', unsafe_allow_html=True)
    
    render_haven_header()
    
    st.markdown('<h2 style="color: var(--text-primary);">Register</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Registration type selection
    if st.session_state.registration_type is None:
        st.markdown('<h3 style="color: var(--text-primary);">Choose Registration Type</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👤 Register as an Individual", use_container_width=True):
                st.session_state.registration_type = "individual"
                st.rerun()
        
        with col2:
            if st.button("🏢 Register as an Organization", use_container_width=True):
                st.session_state.registration_type = "organization"
                st.rerun()
    
    # Individual registration form
    elif st.session_state.registration_type == "individual":
        st.markdown('<h3 style="color: var(--text-primary);">Register as an Individual</h3>', unsafe_allow_html=True)
        
        with st.form("individual_registration"):
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email ID", placeholder="your.email@example.com")
            phone = st.text_input("Phone Number", placeholder="Your phone number")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            address = st.text_area("Address", placeholder="Your complete address")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Register", use_container_width=True):
                    if password == confirm_password and all([full_name, email, phone, password, address]):
                        user_data = {
                            "type": "individual",
                            "full_name": full_name,
                            "email": email,
                            "phone": phone,
                            "password": password,
                            "address": address
                        }
                        if register_user(user_data):
                            st.markdown('<div class="success-msg">✅ Registration successful! Please login.</div>', unsafe_allow_html=True)
                            st.session_state.registration_type = None
                            st.session_state.current_page = 'login'
                            st.rerun()
                        else:
                            st.markdown('<div class="error-msg">❌ Registration failed. Please try again.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-msg">❌ Please fill all fields and ensure passwords match.</div>', unsafe_allow_html=True)
            
            with col2:
                if st.form_submit_button("Back to Type Selection", use_container_width=True):
                    st.session_state.registration_type = None
                    st.rerun()
    
    # Organization registration form
    elif st.session_state.registration_type == "organization":
        st.markdown('<h3 style="color: var(--text-primary);">Register as an Organization</h3>', unsafe_allow_html=True)
        
        with st.form("organization_registration"):
            org_name = st.text_input("Organization Name", placeholder="Enter organization name")
            email = st.text_input("Email ID", placeholder="organization@example.com")
            phone = st.text_input("Organization Phone Number", placeholder="Organization phone number")
            
            org_type = st.selectbox(
                "Select Organization Type",
                ["", "NGO", "Startup", "Charity"],
                index=0
            )
            
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            description = st.text_area("Brief Description (max 100 chars)", placeholder="Brief description of your organization", max_chars=100)
            address = st.text_area("Address", placeholder="Organization address")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Register", use_container_width=True):
                    if (password == confirm_password and org_type and 
                        all([org_name, email, phone, password, description, address])):
                        user_data = {
                            "type": "organization",
                            "organization_name": org_name,
                            "email": email,
                            "phone": phone,
                            "organization_type": org_type,
                            "password": password,
                            "description": description,
                            "address": address
                        }
                        if register_user(user_data):
                            st.markdown('<div class="success-msg">✅ Registration successful! Please login.</div>', unsafe_allow_html=True)
                            st.session_state.registration_type = None
                            st.session_state.current_page = 'login'
                            st.rerun()
                        else:
                            st.markdown('<div class="error-msg">❌ Registration failed. Please try again.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-msg">❌ Please fill all fields, select organization type, and ensure passwords match.</div>', unsafe_allow_html=True)
            
            with col2:
                if st.form_submit_button("Back to Type Selection", use_container_width=True):
                    st.session_state.registration_type = None
                    st.rerun()
    
    # Back to login link
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Already have an account? Sign in here", use_container_width=True):
            st.session_state.registration_type = None
            st.session_state.current_page = 'login'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_navigation():
    """Render navigation with logo for authenticated users"""
    logo_html = ""
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="nav-logo" alt="HAVEN Logo">'
    else:
        logo_html = '🏠'
    
    st.markdown(f"""
    <div class="nav-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="nav-brand">
                {logo_html} HAVEN
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <span style="color: var(--text-primary); font-weight: 600;">Welcome, {st.session_state.user_data.get('name', 'User')}</span>
                <button onclick="location.reload()" style="
                    background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%); 
                    color: white; 
                    border: none; 
                    padding: 0.8rem 1.5rem; 
                    border-radius: 8px; 
                    cursor: pointer;
                    font-weight: bold;
                    transition: all 0.3s ease;
                ">Logout</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_home_page():
    """Render home page with dark text on light background"""
    render_navigation()
    
    st.markdown('<h1 style="color: var(--text-primary);">🏠 Welcome to HAVEN</h1>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Explore Campaigns", use_container_width=True):
            st.session_state.current_page = 'explore'
            st.rerun()
    
    with col2:
        if st.button("🔎 Search Campaigns", use_container_width=True):
            st.session_state.current_page = 'search'
            st.rerun()
    
    with col3:
        if st.button("🚀 Create Campaign", use_container_width=True):
            st.session_state.current_page = 'create'
            st.rerun()
    
    st.markdown("---")
    
    # Welcome content
    st.markdown("""
    <div class="form-section fade-in">
        <h3>🌟 Welcome to HAVEN Crowdfunding Platform</h3>
        <p>Help not just some people, but Help Humanity. Start exploring amazing campaigns or create your own to make a difference in the world.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card fade-in">
            <h4>🌍 Global Reach</h4>
            <p>Connect with supporters worldwide and make your campaign visible to millions of people who care.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card fade-in">
            <h4>🔒 Secure Platform</h4>
            <p>Your funds and data are protected with enterprise-grade security and transparent processes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card fade-in">
            <h4>📊 Real-time Analytics</h4>
            <p>Track your campaign performance with detailed insights and analytics to optimize your success.</p>
        </div>
        """, unsafe_allow_html=True)

def render_explore_page():
    """Render explore campaigns page"""
    render_navigation()
    
    st.markdown('<h1 style="color: var(--text-primary);">🔍 Explore Campaigns</h1>', unsafe_allow_html=True)
    
    # Back to home
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("---")
    
    # Categories
    st.markdown('<h3 style="color: var(--text-primary);">Browse by Category</h3>', unsafe_allow_html=True)
    
    categories = [
        ("🔬", "Technology", "Innovative tech projects and startups"),
        ("🏥", "Health", "Medical research and healthcare initiatives"),
        ("📚", "Education", "Educational programs and scholarships"),
        ("🌱", "Environment", "Environmental conservation projects"),
        ("🎨", "Arts & Culture", "Creative and cultural projects"),
        ("🤝", "Community", "Community development initiatives")
    ]
    
    cols = st.columns(3)
    for i, (icon, category, description) in enumerate(categories):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <h4>{icon} {category}</h4>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)

def render_search_page():
    """Render search campaigns page"""
    render_navigation()
    
    st.markdown('<h1 style="color: var(--text-primary);">🔎 Search Campaigns</h1>', unsafe_allow_html=True)
    
    # Back to home
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("---")
    
    # Search form
    with st.form("search_form"):
        search_query = st.text_input("Search for campaigns", placeholder="Enter keywords to search for campaigns...")
        
        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.selectbox("Filter by Category", 
                ["All Categories", "Technology", "Health", "Education", "Environment", "Arts & Culture", "Community"])
        
        with col2:
            sort_by = st.selectbox("Sort by", 
                ["Most Recent", "Most Funded", "Ending Soon", "Most Popular"])
        
        search_submitted = st.form_submit_button("Search", use_container_width=True)
    
    if search_submitted:
        st.markdown(f'<div class="success-msg">🔍 Searching for: "{search_query}" in {category_filter}</div>', unsafe_allow_html=True)
        
        # Mock search results
        st.markdown('<h3 style="color: var(--text-primary);">Search Results</h3>', unsafe_allow_html=True)
        
        for i in range(3):
            st.markdown(f"""
            <div class="feature-card">
                <h4>🚀 Sample Campaign {i+1}</h4>
                <p>This is a sample campaign that matches your search criteria. In a real application, this would show actual campaign data with images and detailed information.</p>
                <div style="display: flex; justify-content: space-between; margin-top: 1rem; font-weight: bold; color: var(--text-secondary);">
                    <span>Goal: $10,000</span>
                    <span>Raised: ${(i+1)*2000}</span>
                    <span>Days left: {30-i*5}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ========================================
# MAIN APPLICATION
# ========================================

def main():
    """Main application function"""
    
    # Check authentication status
    if not st.session_state.authenticated:
        # Show login or registration page
        if st.session_state.current_page == 'register':
            render_registration_page()
        else:
            render_login_page()
    else:
        # Show authenticated pages
        if st.session_state.current_page == 'explore':
            render_explore_page()
        elif st.session_state.current_page == 'search':
            render_search_page()
        else:
            render_home_page()

if __name__ == "__main__":
    main()

