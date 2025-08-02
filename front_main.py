import streamlit as st
import requests
import os
import json
import re

# Set page config for wide layout and initial title
st.set_page_config(layout="wide", page_title="HAVEN Crowdfunding")

# --- Configuration ---
# Use the backend URL from an environment variable, or default to localhost
BACKEND_URL = os.getenv("BACKEND_URL", "http://haven-fastapi-backend.onrender.com")

# --- Custom CSS for global styling --- #
custom_css = """
<style>
    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700&display=swap");

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: "Poppins", sans-serif;
    }

    body {
        display: grid;
        height: 100vh;
        width: 100%;
        place-items: center;
        background-color: #f0f2e6; /* Light green background */
        color: #000; /* Darker text for contrast */
        padding: 10px;
    }

    .stApp {
        background-color: #f0f2e6; /* Apply to Streamlit app background */
        color: #000;
    }
    
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 30px;
    }

    .header-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0;
    }

    .header-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        color: #555;
        margin-top: 5px;
    }
    
    .container {
        background: #fff;
        width: 100%;
        max-width: 900px;
        padding: 25px 30px;
        border-radius: 5px;
        box-shadow: 0 10px 10px rgba(0, 0, 0, 0.15);
        margin: 20px auto;
    }

    .title {
        font-size: 25px;
        font-weight: 500;
        position: relative;
        text-align: center;
        margin-bottom: 20px;
    }

    .title::before {
        content: "";
        position: absolute;
        left: 0;
        bottom: 0;
        height: 3px;
        width: 30px;
        border-radius: 5px;
        background: linear-gradient(135deg, #008744, #125439);
    }
    
    .input-box {
        margin: 15px 0;
    }

    .input-box .details {
        font-weight: 500;
    }

    .input-box input {
        height: 45px;
        width: 100%;
        outline: none;
        font-size: 16px;
        border-radius: 5px;
        padding-left: 15px;
        border: 1px solid #ccc;
        border-bottom-width: 2px;
        transition: all 0.3s ease;
    }

    .input-box input:focus,
    .input-box input:valid {
        border-color: #008744;
    }

    .button-container {
        height: 45px;
        margin: 45px 0;
    }

    .button-container input {
        height: 100%;
        width: 100%;
        border-radius: 5px;
        border: none;
        color: #fff;
        font-size: 18px;
        font-weight: 500;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #008744, #125439);
    }

    .button-container input:hover {
        background: linear-gradient(-135deg, #008744, #125439);
    }

    .login-link, .social-login-container {
        text-align: center;
        margin-top: 15px;
    }

    .login-link a {
        color: #008744;
        text-decoration: none;
    }

    .login-link a:hover {
        text-decoration: underline;
    }

    .social-login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .social-login-button {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        max-width: 300px;
        padding: 10px;
        margin-top: 10px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        border: 1px solid #ccc;
        text-decoration: none; /* Make it look like a button, not a link */
        color: #000;
    }

    .social-login-button:hover {
        background-color: #f0f0f0;
    }

    .google-btn {
        background-color: #fff;
        color: #000;
        border: 1px solid #ccc;
    }

    .facebook-btn {
        background-color: #4267B2;
        color: #fff;
        border: none;
    }

    .social-icon {
        width: 20px;
        height: 20px;
        margin-right: 10px;
    }

    .st-emotion-cache-18ni7ap { /* Target the main block container to remove padding */
        padding-top: 0rem;
    }

    .st-emotion-cache-13k95a9 { /* Adjust padding for the main content area */
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
    }

    .stButton>button {
        width: 100%;
        border-radius: 5px;
        border: none;
        color: #fff;
        font-size: 18px;
        font-weight: 500;
        letter-spacing: 1px;
        cursor: pointer;
        background: linear-gradient(135deg, #008744, #125439);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(-135deg, #008744, #125439);
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
st.markdown("<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'>", unsafe_allow_html=True)

# --- Session State Initialization --- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# --- Page Rendering Functions --- #

def render_app_header():
    """Renders the consistent HAVEN header across all pages."""
    st.markdown("""
        <div class="header-container">
            <h1 class="header-title">HAVEN</h1>
            <p class="header-subtitle">Your platform for trustworthy and transparent crowdfunding.</p>
        </div>
    """, unsafe_allow_html=True)

def render_login_page():
    """Renders the login page with OAuth buttons and links."""
    render_app_header()
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Login</div>", unsafe_allow_html=True)
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Sign In")
        if submitted:
            # Placeholder for future login logic
            st.warning("Standard login is not yet implemented. Please use OAuth.")

    # Social Login Buttons
    st.markdown("<div class='social-login-container'>", unsafe_allow_html=True)
    
    # Get the URL for Google login and create an anchor tag
    google_login_url = f"{BACKEND_URL}/auth/google/login"
    st.markdown(f"<a href='{google_login_url}' class='social-login-button google-btn'><img class='social-icon' src='https://img.icons8.com/color/48/000000/google-logo.png' alt='Google Icon'> Sign in with Google</a>", unsafe_allow_html=True)

    # Get the URL for Facebook login and create an anchor tag
    facebook_login_url = f"{BACKEND_URL}/auth/facebook/login"
    st.markdown(f"<a href='{facebook_login_url}' class='social-login-button facebook-btn'><img class='social-icon' src='https://img.icons8.com/fluency/48/000000/facebook-new.png' alt='Facebook Icon'> Sign in with Facebook</a>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # "Create an account" link to open in a new tab
    st.markdown("<div class='login-link'>Don't have an account? <a href='?page=register' target='_blank'>Create an account</a></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_register_page():
    """Renders the registration page."""
    render_app_header()
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Registration</div>", unsafe_allow_html=True)
    st.warning("Registration is not yet implemented. Please use OAuth from the main login page.")
    # "Sign in here" link to open in a new tab
    st.markdown("<div class='login-link'>Already have an account? <a href='?page=login' target='_blank'>Sign in here</a></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_home_page():
    """Renders the home page after successful login."""
    render_app_header()
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update(current_page='home'))
    st.sidebar.button("Explore", on_click=lambda: st.session_state.update(current_page='explore'))
    st.sidebar.button("Search", on_click=lambda: st.session_state.update(current_page='search'))
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update(logged_in=False, current_page='login'))
    st.header(f"Welcome, {st.session_state.user_info.get('name', 'User')}!")
    st.write("This is the main home page content.")
    st.json(st.session_state.user_info)

def render_explore_page():
    """Renders the explore page."""
    render_app_header()
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update(current_page='home'))
    st.sidebar.button("Explore", on_click=lambda: st.session_state.update(current_page='explore'))
    st.sidebar.button("Search", on_click=lambda: st.session_state.update(current_page='search'))
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update(logged_in=False, current_page='login'))
    st.header("Explore Campaigns")
    st.write("Content for exploring different campaigns.")

def render_search_page():
    """Renders the search page."""
    render_app_header()
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update(current_page='home'))
    st.sidebar.button("Explore", on_click=lambda: st.session_state.update(current_page='explore'))
    st.sidebar.button("Search", on_click=lambda: st.session_state.update(current_page='search'))
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update(logged_in=False, current_page='login'))
    st.header("Search for Campaigns")
    st.write("Search functionality will be implemented here.")

# --- Main App Logic ---

# Check URL parameters for page navigation (for links that open in new tabs)
query_params = st.query_params
if "page" in query_params:
    st.session_state.current_page = query_params["page"]

# Render current page
if st.session_state.current_page == 'login':
    render_login_page()
elif st.session_state.current_page == 'register':
    render_register_page()
elif st.session_state.logged_in:
    if st.session_state.current_page == 'home':
        render_home_page()
    elif st.session_state.current_page == 'explore':
        render_explore_page()
    elif st.session_state.current_page == 'search':
        render_search_page()
    # Add more pages here as needed
else:
    # If not logged in, always redirect to login page
    st.session_state.current_page = 'login'
    render_login_page()

# Placeholder for automatic term simplification
# This would ideally be integrated into the content rendering functions
# For example, when displaying campaign details, run them through simplify_text()

# Example usage of simplify_text (for demonstration)
# st.write(simplify_text("This campaign aims to provide resources and training to local farmers to transition to organic and sustainable farming methods."))

# You can add a button to test backend connectivity (for debugging)
if st.sidebar.button("Test Backend Connection"):
    try:
        response_data = requests.get(f"{BACKEND_URL}/health")
        if response_data.status_code == 200:
            st.success(f"Backend response: {response_data.json()}")
        else:
            st.error(f"Failed to get response from backend. Status: {response_data.status_code}")
    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to backend at {BACKEND_URL}. Please ensure the backend is running.")

