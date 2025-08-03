import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Page configuration
st.set_page_config(
    page_title="HAVEN - Help Humanity",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Environment variables
BACKEND_URL = os.environ.get("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")

# MaterializeCSS and custom styling with OAuth popup support
def load_materialize_css():
    st.markdown("""
    <head>
        <!-- MaterializeCSS -->
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
        
        <!-- Custom fonts -->
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    </head>
    
    <style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Reset Streamlit styling */
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        font-family: 'Roboto', sans-serif;
    }
    
    /* Custom HAVEN theme colors */
    .haven-primary { background-color: #4caf50 !important; }
    .haven-secondary { background-color: #8bc34a !important; }
    .haven-accent { background-color: #cddc39 !important; }
    
    /* Header styling */
    .haven-header {
        background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%);
        padding: 30px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .haven-logo {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0;
    }
    
    .haven-tagline {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.9);
        font-weight: 300;
        margin: 10px 0 0 0;
    }
    
    /* Enhanced Form Styling */
    .form-container {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 16px 48px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    .input-field input:focus + label {
        color: #4caf50 !important;
    }
    
    .input-field input:focus {
        border-bottom: 1px solid #4caf50 !important;
        box-shadow: 0 1px 0 0 #4caf50 !important;
    }
    
    .input-field .prefix.active {
        color: #4caf50 !important;
    }
    
    /* OAuth popup styling */
    .oauth-popup {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        z-index: 10000;
        display: none;
        justify-content: center;
        align-items: center;
    }
    
    .oauth-popup.active {
        display: flex;
    }
    
    .oauth-popup-content {
        background: white;
        border-radius: 15px;
        padding: 30px;
        max-width: 400px;
        width: 90%;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .oauth-popup-close {
        position: absolute;
        top: 15px;
        right: 20px;
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
        color: #666;
    }
    
    /* Profile page styling */
    .profile-header {
        background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%);
        color: white;
        padding: 40px 0;
        text-align: center;
    }
    
    .profile-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 4px solid white;
        margin: 0 auto 20px;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        color: #4caf50;
    }
    
    .profile-stats {
        display: flex;
        justify-content: space-around;
        margin: 30px 0;
    }
    
    .profile-stat {
        text-align: center;
    }
    
    .profile-stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #4caf50;
        display: block;
    }
    
    .profile-stat-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .verification-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .verification-verified {
        background: #4caf50;
        color: white;
    }
    
    .verification-pending {
        background: #ff9800;
        color: white;
    }
    
    .verification-rejected {
        background: #f44336;
        color: white;
    }
    
    /* Document upload styling */
    .document-upload-area {
        border: 2px dashed #4caf50;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        background: rgba(76, 175, 80, 0.05);
        margin: 20px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .document-upload-area:hover {
        background: rgba(76, 175, 80, 0.1);
        border-color: #45a049;
    }
    
    .document-upload-icon {
        font-size: 48px;
        color: #4caf50;
        margin-bottom: 15px;
    }
    
    /* Campaign/Donation cards */
    .activity-card {
        border-radius: 15px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin: 15px 0;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .activity-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    .activity-card-header {
        background: #f8f9fa;
        padding: 15px 20px;
        border-bottom: 1px solid #e9ecef;
    }
    
    .activity-card-body {
        padding: 20px;
    }
    
    .activity-amount {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4caf50;
    }
    
    .activity-date {
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Vertical navbar */
    .vertical-navbar {
        position: fixed;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        z-index: 1000;
        background: rgba(255,255,255,0.95);
        border-radius: 25px;
        padding: 15px 8px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    .vertical-navbar a {
        display: block;
        margin: 10px 0;
        color: #4caf50;
        text-decoration: none;
        padding: 12px;
        border-radius: 50%;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .vertical-navbar a:hover {
        background: #4caf50;
        color: white;
        transform: scale(1.1);
    }
    
    .vertical-navbar .material-icons {
        font-size: 24px;
    }
    
    /* Floating Action Button */
    .fab-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
    }
    
    .fab-custom {
        background: linear-gradient(135deg, #ff5722 0%, #ff7043 100%) !important;
        box-shadow: 0 8px 32px rgba(255, 87, 34, 0.4) !important;
    }
    
    .fab-custom:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 40px rgba(255, 87, 34, 0.6) !important;
    }
    
    /* Authentication styling */
    .auth-container {
        max-width: 600px;
        margin: 50px auto;
        padding: 0;
    }
    
    .auth-card {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 16px 48px rgba(0,0,0,0.1);
    }
    
    .auth-header {
        background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%);
        color: white;
        padding: 30px;
        text-align: center;
    }
    
    .auth-body {
        padding: 40px;
        background: white;
    }
    
    /* Pulse effect for OAuth buttons */
    .oauth-btn {
        margin: 10px 0;
        border-radius: 25px;
        text-transform: none;
        font-size: 16px;
        padding: 0 30px;
        height: 50px;
        line-height: 50px;
    }
    
    .google-btn {
        background: #db4437 !important;
    }
    
    .facebook-btn {
        background: #3b5998 !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .vertical-navbar {
            position: fixed;
            bottom: 0;
            right: 0;
            left: 0;
            top: auto;
            transform: none;
            border-radius: 0;
            padding: 10px;
            display: flex;
            justify-content: space-around;
        }
        
        .vertical-navbar a {
            margin: 0 5px;
        }
        
        .fab-container {
            bottom: 80px;
        }
        
        .haven-logo {
            font-size: 2.5rem;
        }
        
        .haven-tagline {
            font-size: 1.1rem;
        }
        
        .form-container {
            padding: 20px;
            margin: 10px;
        }
        
        .profile-stats {
            flex-direction: column;
            gap: 20px;
        }
    }
    
    /* Custom button styling */
    .btn-haven {
        background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%);
        border-radius: 25px;
        text-transform: none;
        font-weight: 500;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
    }
    
    .btn-haven:hover {
        background: linear-gradient(135deg, #45a049 0%, #7cb342 100%);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False

# API functions with authentication
def get_headers():
    if st.session_state.access_token:
        return {"Authorization": f"Bearer {st.session_state.access_token}"}
    return {}

def get_oauth_url(provider):
    try:
        response = requests.get(f"{BACKEND_URL}/api/auth/oauth/{provider}/url", timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_user_profile(user_id):
    try:
        response = requests.get(f"{BACKEND_URL}/api/profile/{user_id}", timeout=10)
        if response.status_code == 200:
            return response.json().get('profile')
    except:
        pass
    return None

def get_my_profile():
    try:
        response = requests.get(f"{BACKEND_URL}/api/profile/me", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json().get('profile')
    except:
        pass
    return None

def get_verification_requirements():
    try:
        response = requests.get(f"{BACKEND_URL}/api/verification/requirements", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_campaigns():
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaigns", timeout=10)
        if response.status_code == 200:
            return response.json().get('campaigns', [])
    except:
        pass
    return []

# Header component
def show_header():
    st.markdown("""
    <div class="haven-header">
        <div class="container">
            <div class="row">
                <div class="col s12 center-align">
                    <div class="haven-logo">🏠 HAVEN 🌿</div>
                    <div class="haven-tagline">Help not just some people, but Help Humanity</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Vertical navbar
def show_vertical_navbar():
    navbar_html = """
    <div class="vertical-navbar">
        <a href="#" onclick="changePage('home')" data-tooltip="Home" data-position="left">
            <i class="material-icons">home</i>
        </a>
        <a href="#" onclick="changePage('explore')" data-tooltip="Explore" data-position="left">
            <i class="material-icons">explore</i>
        </a>
        <a href="#" onclick="changePage('search')" data-tooltip="Search" data-position="left">
            <i class="material-icons">search</i>
        </a>
        <a href="#" onclick="changePage('create')" data-tooltip="Create" data-position="left">
            <i class="material-icons">add_circle</i>
        </a>
        <a href="#" onclick="changePage('profile')" data-tooltip="Profile" data-position="left">
            <i class="material-icons">person</i>
        </a>
        <a href="#" onclick="logout()" data-tooltip="Logout" data-position="left">
            <i class="material-icons">exit_to_app</i>
        </a>
    </div>
    
    <script>
    // Initialize MaterializeCSS components
    document.addEventListener('DOMContentLoaded', function() {
        var tooltips = document.querySelectorAll('[data-tooltip]');
        M.Tooltip.init(tooltips);
        
        var selects = document.querySelectorAll('select');
        M.FormSelect.init(selects);
    });
    </script>
    """
    
    components.html(navbar_html, height=0)

# Floating Action Button
def show_fab():
    fab_html = """
    <div class="fab-container">
        <a class="btn-floating btn-large waves-effect waves-light fab-custom" onclick="createCampaign()">
            <i class="material-icons">add</i>
        </a>
    </div>
    
    <script>
    function createCampaign() {
        console.log('Create campaign clicked');
    }
    </script>
    """
    
    components.html(fab_html, height=0)

# OAuth Login with Popup
def show_login():
    show_header()
    
    st.markdown("""
    <div class="container">
        <div class="auth-container">
            <div class="card auth-card">
                <div class="auth-header">
                    <h4 style="margin: 0; font-weight: 300;">Welcome to HAVEN</h4>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Sign in to start helping humanity</p>
                </div>
                <div class="auth-body">
                    <form id="loginForm">
                        <div class="row">
                            <div class="input-field col s12">
                                <i class="material-icons prefix">email</i>
                                <input id="email" type="email" class="validate" required>
                                <label for="email">Email Address</label>
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
                                <button class="btn waves-effect waves-light grey" type="button" onclick="showRegister()" style="width: 100%;">
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
                </div>
            </div>
        </div>
    </div>
    
    <!-- OAuth Popup -->
    <div id="oauthPopup" class="oauth-popup">
        <div class="oauth-popup-content">
            <button class="oauth-popup-close" onclick="closeOAuthPopup()">&times;</button>
            <div id="oauthContent">
                <div class="preloader-wrapper big active">
                    <div class="spinner-layer spinner-blue-only">
                        <div class="circle-clipper left">
                            <div class="circle"></div>
                        </div>
                        <div class="gap-patch">
                            <div class="circle"></div>
                        </div>
                        <div class="circle-clipper right">
                            <div class="circle"></div>
                        </div>
                    </div>
                </div>
                <p style="margin-top: 20px;">Opening authentication window...</p>
            </div>
        </div>
    </div>
    
    <script>
    let oauthWindow = null;
    
    function openOAuthPopup(provider) {
        const popup = document.getElementById('oauthPopup');
        popup.classList.add('active');
        
        // Get OAuth URL from backend
        fetch(`""" + BACKEND_URL + """/api/auth/oauth/${provider}/url`)
            .then(response => response.json())
            .then(data => {
                if (data.oauth_url) {
                    // Open popup window
                    oauthWindow = window.open(
                        data.oauth_url,
                        'oauth',
                        'width=500,height=600,scrollbars=yes,resizable=yes'
                    );
                    
                    // Update popup content
                    document.getElementById('oauthContent').innerHTML = `
                        <i class="material-icons large" style="color: #4caf50;">security</i>
                        <h5>Authenticate with ${provider.charAt(0).toUpperCase() + provider.slice(1)}</h5>
                        <p>Please complete the authentication in the popup window.</p>
                        <button class="btn waves-effect waves-light grey" onclick="closeOAuthPopup()">Cancel</button>
                    `;
                    
                    // Monitor popup
                    const checkClosed = setInterval(() => {
                        if (oauthWindow.closed) {
                            clearInterval(checkClosed);
                            closeOAuthPopup();
                        }
                    }, 1000);
                    
                    // Listen for OAuth completion
                    window.addEventListener('message', function(event) {
                        if (event.data.type === 'oauth_success') {
                            clearInterval(checkClosed);
                            oauthWindow.close();
                            closeOAuthPopup();
                            
                            // Handle successful authentication
                            M.toast({html: 'Authentication successful!', classes: 'green'});
                            // Redirect or update UI
                            setTimeout(() => {
                                window.location.reload();
                            }, 1000);
                        }
                    });
                }
            })
            .catch(error => {
                console.error('OAuth error:', error);
                M.toast({html: 'Authentication failed. Please try again.', classes: 'red'});
                closeOAuthPopup();
            });
    }
    
    function closeOAuthPopup() {
        const popup = document.getElementById('oauthPopup');
        popup.classList.remove('active');
        if (oauthWindow) {
            oauthWindow.close();
            oauthWindow = null;
        }
    }
    
    function showRegister() {
        console.log('Show register form');
    }
    
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        fetch('""" + BACKEND_URL + """/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                M.toast({html: 'Login successful!', classes: 'green'});
                // Store token and redirect
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('user_data', JSON.stringify(data.user));
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                M.toast({html: 'Login failed. Please check your credentials.', classes: 'red'});
            }
        })
        .catch(error => {
            console.error('Login error:', error);
            M.toast({html: 'Login failed. Please try again.', classes: 'red'});
        });
    });
    </script>
    """, unsafe_allow_html=True)

# User Profile Page
def show_profile():
    show_header()
    show_vertical_navbar()
    show_fab()
    
    # Get current user's profile
    profile = get_my_profile()
    if not profile:
        st.error("Unable to load profile")
        return
    
    # Profile header
    verification_class = f"verification-{profile.get('verification_status', 'pending')}"
    verification_text = profile.get('verification_status', 'pending').title()
    
    st.markdown(f"""
    <div class="profile-header">
        <div class="container">
            <div class="profile-avatar">
                <i class="material-icons">person</i>
            </div>
            <h3 style="margin: 0; font-weight: 300;">{profile.get('first_name', '')} {profile.get('last_name', '')}</h3>
            <p style="margin: 10px 0; opacity: 0.9;">{profile.get('email', '')}</p>
            <span class="verification-badge {verification_class}">{verification_text}</span>
            {f'<p style="margin: 15px 0; opacity: 0.9;">{profile.get("organization_name", "")}</p>' if profile.get('organization_name') else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Profile stats
    if profile.get('user_type') == 'individual':
        total_donated = profile.get('total_donations', 0)
        donation_count = len(profile.get('donations', []))
        
        st.markdown(f"""
        <div class="container">
            <div class="profile-stats">
                <div class="profile-stat">
                    <span class="profile-stat-number">₹{total_donated:,.0f}</span>
                    <span class="profile-stat-label">Total Donated</span>
                </div>
                <div class="profile-stat">
                    <span class="profile-stat-number">{donation_count}</span>
                    <span class="profile-stat-label">Donations Made</span>
                </div>
                <div class="profile-stat">
                    <span class="profile-stat-number">{len(profile.get('documents', []))}</span>
                    <span class="profile-stat-label">Documents</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        total_raised = profile.get('total_raised', 0)
        campaign_count = profile.get('total_campaigns', 0)
        
        st.markdown(f"""
        <div class="container">
            <div class="profile-stats">
                <div class="profile-stat">
                    <span class="profile-stat-number">₹{total_raised:,.0f}</span>
                    <span class="profile-stat-label">Total Raised</span>
                </div>
                <div class="profile-stat">
                    <span class="profile-stat-number">{campaign_count}</span>
                    <span class="profile-stat-label">Campaigns</span>
                </div>
                <div class="profile-stat">
                    <span class="profile-stat-number">{len(profile.get('documents', []))}</span>
                    <span class="profile-stat-label">Documents</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    st.markdown('<div class="container" style="margin-top: 40px;">', unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📋 Activity", "📄 Verification", "⚙️ Settings"])
    
    with tab1:
        if profile.get('user_type') == 'individual':
            st.subheader("💝 Your Donations")
            donations = profile.get('donations', [])
            
            if donations:
                for donation in donations:
                    st.markdown(f"""
                    <div class="activity-card">
                        <div class="activity-card-header">
                            <strong>{donation.get('campaign_title', 'Unknown Campaign')}</strong>
                            <span class="activity-date" style="float: right;">{donation.get('created_at', '')[:10]}</span>
                        </div>
                        <div class="activity-card-body">
                            <div class="activity-amount">₹{donation.get('amount', 0):,.0f}</div>
                            {f'<p style="margin-top: 10px; color: #666;">"{donation.get("message", "")}"</p>' if donation.get('message') else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("You haven't made any donations yet. Start supporting campaigns to make a difference!")
        
        else:
            st.subheader("🎯 Your Campaigns")
            campaigns = profile.get('campaigns', [])
            
            if campaigns:
                for campaign in campaigns:
                    progress = (campaign.get('raised', 0) / campaign.get('goal', 1)) * 100
                    
                    st.markdown(f"""
                    <div class="activity-card">
                        <div class="activity-card-header">
                            <strong>{campaign.get('title', 'Unknown Campaign')}</strong>
                            <span class="activity-date" style="float: right;">{campaign.get('created_at', '')[:10]}</span>
                        </div>
                        <div class="activity-card-body">
                            <div class="activity-amount">₹{campaign.get('raised', 0):,.0f} / ₹{campaign.get('goal', 0):,.0f}</div>
                            <div class="progress" style="margin: 15px 0;">
                                <div class="determinate" style="width: {min(progress, 100)}%; background: #4caf50;"></div>
                            </div>
                            <p style="color: #666;">{campaign.get('description', '')[:100]}...</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("You haven't created any campaigns yet. Click the + button to create your first campaign!")
    
    with tab2:
        st.subheader("🔒 Account Verification")
        
        # Get verification requirements
        requirements = get_verification_requirements()
        if requirements:
            st.markdown(f"""
            <div class="card">
                <div class="card-content">
                    <h6 style="color: #4caf50; margin-bottom: 15px;">Verification Requirements</h6>
                    <p>{requirements.get('instructions', '')}</p>
                    <p><strong>Required documents:</strong> {requirements.get('required_documents', 1)}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Document upload form
            st.markdown("""
            <div class="form-container">
                <h6 style="color: #4caf50; margin-bottom: 20px;">Upload Verification Document</h6>
                <form id="documentForm" enctype="multipart/form-data">
                    <div class="input-field">
                        <select id="documentType" required>
                            <option value="" disabled selected>Choose document type</option>
            """, unsafe_allow_html=True)
            
            for doc_type in requirements.get('document_types', []):
                st.markdown(f'<option value="{doc_type["type"]}">{doc_type["name"]}</option>', unsafe_allow_html=True)
            
            st.markdown("""
                        </select>
                        <label>Document Type</label>
                    </div>
                    
                    <div class="input-field">
                        <input id="documentNumber" type="text">
                        <label for="documentNumber">Document Number (Optional)</label>
                    </div>
                    
                    <div class="document-upload-area" onclick="document.getElementById('documentFile').click()">
                        <div class="document-upload-icon">📄</div>
                        <h6>Click to upload document</h6>
                        <p>Supported formats: PDF, JPG, PNG (Max 5MB)</p>
                        <input type="file" id="documentFile" style="display: none;" accept=".pdf,.jpg,.jpeg,.png" required>
                    </div>
                    
                    <button class="btn waves-effect waves-light btn-haven" type="submit" style="width: 100%; margin-top: 20px;">
                        Upload Document
                        <i class="material-icons right">cloud_upload</i>
                    </button>
                </form>
            </div>
            
            <script>
            document.getElementById('documentForm').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formData = new FormData();
                formData.append('document_type', document.getElementById('documentType').value);
                formData.append('document_number', document.getElementById('documentNumber').value);
                formData.append('document_file', document.getElementById('documentFile').files[0]);
                
                fetch('""" + BACKEND_URL + """/api/verification/upload', {
                    method: 'POST',
                    headers: {
                        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                    },
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        M.toast({html: 'Document uploaded successfully!', classes: 'green'});
                        setTimeout(() => {
                            window.location.reload();
                        }, 1000);
                    } else {
                        M.toast({html: 'Upload failed. Please try again.', classes: 'red'});
                    }
                })
                .catch(error => {
                    console.error('Upload error:', error);
                    M.toast({html: 'Upload failed. Please try again.', classes: 'red'});
                });
            });
            </script>
            """, unsafe_allow_html=True)
        
        # Show uploaded documents
        documents = profile.get('documents', [])
        if documents:
            st.subheader("📋 Uploaded Documents")
            for doc in documents:
                status_class = f"verification-{doc.get('verification_status', 'pending')}"
                status_text = doc.get('verification_status', 'pending').title()
                
                st.markdown(f"""
                <div class="activity-card">
                    <div class="activity-card-header">
                        <strong>{doc.get('document_type', '').replace('_', ' ').title()}</strong>
                        <span class="verification-badge {status_class}" style="float: right;">{status_text}</span>
                    </div>
                    <div class="activity-card-body">
                        <p><strong>File:</strong> {doc.get('file_name', 'Unknown')}</p>
                        <p><strong>Uploaded:</strong> {doc.get('uploaded_at', '')[:10]}</p>
                        {f'<p><strong>Number:</strong> {doc.get("document_number", "")}</p>' if doc.get('document_number') else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("⚙️ Profile Settings")
        
        # Profile update form
        st.markdown("""
        <div class="form-container">
            <h6 style="color: #4caf50; margin-bottom: 20px;">Update Profile Information</h6>
            <form id="profileForm">
                <div class="row">
                    <div class="input-field col s6">
                        <input id="firstName" type="text" class="validate" required>
                        <label for="firstName">First Name</label>
                    </div>
                    <div class="input-field col s6">
                        <input id="lastName" type="text" class="validate" required>
                        <label for="lastName">Last Name</label>
                    </div>
                </div>
                
                <div class="row">
                    <div class="input-field col s12">
                        <input id="phone" type="tel" class="validate">
                        <label for="phone">Phone Number</label>
                    </div>
                </div>
                
                <div class="row">
                    <div class="input-field col s12">
                        <textarea id="bio" class="materialize-textarea" data-length="500"></textarea>
                        <label for="bio">Bio</label>
                    </div>
                </div>
                
                <div class="row">
                    <div class="input-field col s12">
                        <input id="website" type="url" class="validate">
                        <label for="website">Website</label>
                    </div>
                </div>
                
                <button class="btn waves-effect waves-light btn-haven" type="submit" style="width: 100%;">
                    Update Profile
                    <i class="material-icons right">save</i>
                </button>
            </form>
        </div>
        
        <script>
        // Pre-fill form with current data
        document.addEventListener('DOMContentLoaded', function() {
            const profile = """ + json.dumps(profile) + """;
            
            if (profile.first_name) document.getElementById('firstName').value = profile.first_name;
            if (profile.last_name) document.getElementById('lastName').value = profile.last_name;
            if (profile.phone) document.getElementById('phone').value = profile.phone;
            if (profile.bio) document.getElementById('bio').value = profile.bio;
            if (profile.website) document.getElementById('website').value = profile.website;
            
            // Update labels
            M.updateTextFields();
            M.textareaAutoResize(document.getElementById('bio'));
        });
        
        document.getElementById('profileForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            formData.append('first_name', document.getElementById('firstName').value);
            formData.append('last_name', document.getElementById('lastName').value);
            formData.append('phone', document.getElementById('phone').value);
            formData.append('bio', document.getElementById('bio').value);
            formData.append('website', document.getElementById('website').value);
            
            fetch('""" + BACKEND_URL + """/api/profile/me', {
                method: 'PUT',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    M.toast({html: 'Profile updated successfully!', classes: 'green'});
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    M.toast({html: 'Update failed. Please try again.', classes: 'red'});
                }
            })
            .catch(error => {
                console.error('Update error:', error);
                M.toast({html: 'Update failed. Please try again.', classes: 'red'});
            });
        });
        </script>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Public Profile View
def show_public_profile(user_id):
    show_header()
    show_vertical_navbar()
    show_fab()
    
    # Get user's public profile
    profile = get_user_profile(user_id)
    if not profile:
        st.error("User not found")
        return
    
    # Profile header (similar to private profile but with limited info)
    verification_class = f"verification-{profile.get('verification_status', 'pending')}"
    verification_text = profile.get('verification_status', 'pending').title()
    
    st.markdown(f"""
    <div class="profile-header">
        <div class="container">
            <div class="profile-avatar">
                <i class="material-icons">person</i>
            </div>
            <h3 style="margin: 0; font-weight: 300;">{profile.get('first_name', '')} {profile.get('last_name', '')}</h3>
            <span class="verification-badge {verification_class}">{verification_text}</span>
            {f'<p style="margin: 15px 0; opacity: 0.9;">{profile.get("organization_name", "")}</p>' if profile.get('organization_name') else ''}
            {f'<p style="margin: 10px 0; opacity: 0.8;">{profile.get("bio", "")}</p>' if profile.get('bio') else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show public activity based on user type
    st.markdown('<div class="container" style="margin-top: 40px;">', unsafe_allow_html=True)
    
    if profile.get('user_type') == 'individual':
        st.subheader("💝 Public Donations")
        donations = profile.get('donations', [])
        
        if donations:
            for donation in donations:
                st.markdown(f"""
                <div class="activity-card">
                    <div class="activity-card-header">
                        <strong>{donation.get('campaign_title', 'Unknown Campaign')}</strong>
                        <span class="activity-date" style="float: right;">{donation.get('created_at', '')[:10]}</span>
                    </div>
                    <div class="activity-card-body">
                        <div class="activity-amount">₹{donation.get('amount', 0):,.0f}</div>
                        {f'<p style="margin-top: 10px; color: #666;">"{donation.get("message", "")}"</p>' if donation.get('message') else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No public donations to display.")
    
    else:
        st.subheader("🎯 Campaigns")
        campaigns = profile.get('campaigns', [])
        
        if campaigns:
            for campaign in campaigns:
                progress = (campaign.get('raised', 0) / campaign.get('goal', 1)) * 100
                
                st.markdown(f"""
                <div class="activity-card">
                    <div class="activity-card-header">
                        <strong>{campaign.get('title', 'Unknown Campaign')}</strong>
                        <span class="activity-date" style="float: right;">{campaign.get('created_at', '')[:10]}</span>
                    </div>
                    <div class="activity-card-body">
                        <div class="activity-amount">₹{campaign.get('raised', 0):,.0f} / ₹{campaign.get('goal', 0):,.0f}</div>
                        <div class="progress" style="margin: 15px 0;">
                            <div class="determinate" style="width: {min(progress, 100)}%; background: #4caf50;"></div>
                        </div>
                        <p style="color: #666;">{campaign.get('description', '')[:100]}...</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No campaigns to display.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Home page (simplified for space)
def show_home():
    show_header()
    show_vertical_navbar()
    show_fab()
    
    st.markdown("""
    <div class="container" style="margin-top: 40px;">
        <div class="row">
            <div class="col s12">
                <h4 class="center-align" style="color: #4caf50; font-weight: 300;">🔥 Trending Campaigns</h4>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get and display campaigns
    campaigns = get_campaigns()
    
    if campaigns:
        for i, campaign in enumerate(campaigns[:4]):  # Show first 4 campaigns
            if i % 2 == 0:
                st.markdown('<div class="container"><div class="row">', unsafe_allow_html=True)
            
            progress = (campaign.get('raised', 0) / campaign.get('goal', 1)) * 100
            days_left = (datetime.fromisoformat(campaign.get('end_date', '').replace('Z', '+00:00')) - datetime.now()).days
            
            st.markdown(f"""
            <div class="col s12 m6">
                <div class="card campaign-card">
                    <div class="card-content">
                        <span class="card-title" style="font-weight: 500;">{campaign.get('title', '')}</span>
                        <p style="color: #666; line-height: 1.6; margin-bottom: 15px;">{campaign.get('description', '')[:120]}...</p>
                        <p style="color: #4caf50; font-weight: 500; margin-bottom: 10px;">by {campaign.get('creator_name', '')}</p>
                        
                        <div class="progress" style="margin: 15px 0;">
                            <div class="determinate" style="width: {min(progress, 100)}%; background: #4caf50;"></div>
                        </div>
                        
                        <div class="row" style="margin: 15px 0 0 0;">
                            <div class="col s4">
                                <span style="color: #4caf50; font-weight: 500;">₹{campaign.get('raised', 0):,.0f}</span>
                                <br><small style="color: #999;">raised</small>
                            </div>
                            <div class="col s4 center-align">
                                <span style="color: #4caf50; font-weight: 500;">{progress:.0f}%</span>
                                <br><small style="color: #999;">funded</small>
                            </div>
                            <div class="col s4 right-align">
                                <span style="color: #4caf50; font-weight: 500;">{max(days_left, 0)}</span>
                                <br><small style="color: #999;">days left</small>
                            </div>
                        </div>
                    </div>
                    <div class="card-action">
                        <a href="#" class="waves-effect waves-light btn haven-primary" style="border-radius: 20px;">View Campaign</a>
                        <a href="#" class="waves-effect waves-light btn-flat" style="color: #4caf50;">Share</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if i % 2 == 1 or i == len(campaigns) - 1:
                st.markdown('</div></div>', unsafe_allow_html=True)

# Main navigation handler
def handle_navigation():
    st.sidebar.title("Navigation")
    
    if st.sidebar.button("🏠 Home"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    if st.sidebar.button("👤 Profile"):
        st.session_state.current_page = 'profile'
        st.rerun()
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user_data = {}
        st.session_state.access_token = None
        st.session_state.current_page = 'login'
        st.rerun()

# Main application
def main():
    load_materialize_css()
    init_session_state()
    
    # Check for stored authentication
    if not st.session_state.authenticated:
        # Try to get token from browser storage via JavaScript
        token_check = components.html("""
        <script>
        const token = localStorage.getItem('access_token');
        const userData = localStorage.getItem('user_data');
        
        if (token && userData) {
            // Send token to Streamlit
            window.parent.postMessage({
                type: 'auth_token',
                token: token,
                user_data: JSON.parse(userData)
            }, '*');
        }
        </script>
        """, height=0)
    
    if not st.session_state.authenticated:
        show_login()
    else:
        handle_navigation()
        
        if st.session_state.current_page == 'home':
            show_home()
        elif st.session_state.current_page == 'profile':
            show_profile()
        else:
            show_home()

if __name__ == "__main__":
    main()

