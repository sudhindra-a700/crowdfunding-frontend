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

# MaterializeCSS and custom styling with enhanced form support
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
    
    /* Select dropdown styling */
    .select-wrapper input.select-dropdown:focus {
        border-bottom: 1px solid #4caf50 !important;
        box-shadow: 0 1px 0 0 #4caf50 !important;
    }
    
    .dropdown-content li > a, .dropdown-content li > span {
        color: #4caf50 !important;
    }
    
    .dropdown-content li:hover, .dropdown-content li.active {
        background-color: rgba(76, 175, 80, 0.1) !important;
    }
    
    /* Textarea styling */
    .materialize-textarea:focus:not([readonly]) {
        border-bottom: 1px solid #4caf50 !important;
        box-shadow: 0 1px 0 0 #4caf50 !important;
    }
    
    .materialize-textarea:focus:not([readonly]) + label {
        color: #4caf50 !important;
    }
    
    /* Checkbox styling */
    [type="checkbox"]:checked + span:not(.lever):before {
        border-right: 2px solid #4caf50;
        border-bottom: 2px solid #4caf50;
    }
    
    [type="checkbox"]:checked + span:not(.lever):after {
        border: 2px solid #4caf50;
        background-color: #4caf50;
    }
    
    /* Radio button styling */
    [type="radio"]:checked + span:after, [type="radio"].with-gap:checked + span:after {
        background-color: #4caf50;
    }
    
    [type="radio"]:checked + span:after, [type="radio"].with-gap:checked + span:before, [type="radio"].with-gap:checked + span:after {
        border: 2px solid #4caf50;
    }
    
    /* Switch styling */
    .switch label input[type=checkbox]:checked + .lever {
        background-color: rgba(76, 175, 80, 0.5);
    }
    
    .switch label input[type=checkbox]:checked + .lever:after {
        background-color: #4caf50;
    }
    
    /* Range slider styling */
    input[type=range]::-webkit-slider-thumb {
        background-color: #4caf50;
    }
    
    input[type=range]::-moz-range-thumb {
        background: #4caf50;
    }
    
    .range-field input[type=range]:focus:not(.active)::-webkit-slider-runnable-track {
        background: #4caf50;
    }
    
    /* File input styling */
    .file-field .btn {
        background-color: #4caf50;
    }
    
    .file-field .btn:hover {
        background-color: #45a049;
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
    
    /* Card panels */
    .info-card {
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin: 20px 0;
    }
    
    .info-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.2);
    }
    
    .campaign-card {
        border-radius: 15px;
        overflow: hidden;
        transition: all 0.3s ease;
        margin: 20px 0;
    }
    
    .campaign-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .campaign-image {
        height: 250px;
        background-size: cover;
        background-position: center;
        position: relative;
    }
    
    .campaign-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(transparent, rgba(0,0,0,0.7));
        color: white;
        padding: 20px;
    }
    
    /* Progress bars */
    .progress-custom {
        background-color: #e0e0e0;
        border-radius: 10px;
        height: 8px;
        margin: 15px 0;
    }
    
    .progress-custom .determinate {
        background: linear-gradient(90deg, #4caf50 0%, #8bc34a 100%);
        border-radius: 10px;
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
    
    /* Category grid */
    .category-card {
        border-radius: 15px;
        text-align: center;
        padding: 30px 20px;
        transition: all 0.3s ease;
        cursor: pointer;
        margin: 10px 0;
    }
    
    .category-card:hover {
        transform: translateY(-5px);
    }
    
    .category-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        display: block;
    }
    
    /* Form validation styling */
    .input-field .helper-text {
        color: #f44336;
        font-size: 12px;
    }
    
    .input-field input.valid {
        border-bottom: 1px solid #4caf50;
        box-shadow: 0 1px 0 0 #4caf50;
    }
    
    .input-field input.invalid {
        border-bottom: 1px solid #f44336;
        box-shadow: 0 1px 0 0 #f44336;
    }
    
    .input-field label.active {
        color: #4caf50;
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
    }
    
    /* Tooltips */
    .material-tooltip {
        background: #4caf50;
        border-radius: 8px;
        font-size: 12px;
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
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False

# API functions (same as before)
def get_campaigns():
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaigns", timeout=10)
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
        // Initialize tooltips
        var tooltips = document.querySelectorAll('[data-tooltip]');
        M.Tooltip.init(tooltips);
        
        // Initialize select dropdowns
        var selects = document.querySelectorAll('select');
        M.FormSelect.init(selects);
        
        // Initialize datepicker
        var datepickers = document.querySelectorAll('.datepicker');
        M.Datepicker.init(datepickers);
        
        // Initialize character counter
        var textareas = document.querySelectorAll('textarea');
        M.CharacterCounter.init(textareas);
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

# Enhanced Login Form
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
                            <button class="btn waves-effect waves-light google-btn oauth-btn pulse" style="width: 100%;" onclick="googleLogin()">
                                <i class="material-icons left">search</i>Google
                            </button>
                        </div>
                        <div class="col s6">
                            <button class="btn waves-effect waves-light facebook-btn oauth-btn pulse" style="width: 100%;" onclick="facebookLogin()">
                                <i class="material-icons left">facebook</i>Facebook
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function showRegister() {
        console.log('Show register form');
    }
    
    function googleLogin() {
        console.log('Google login');
    }
    
    function facebookLogin() {
        console.log('Facebook login');
    }
    
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('Login form submitted');
    });
    </script>
    """, unsafe_allow_html=True)

# Enhanced Registration Form
def show_register():
    show_header()
    
    st.markdown("""
    <div class="container">
        <div class="auth-container">
            <div class="card auth-card">
                <div class="auth-header">
                    <h4 style="margin: 0; font-weight: 300;">Join HAVEN</h4>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Create your account to start making a difference</p>
                </div>
                <div class="auth-body">
                    <form id="registerForm">
                        <div class="row">
                            <div class="input-field col s12">
                                <i class="material-icons prefix">account_circle</i>
                                <select id="accountType" required>
                                    <option value="" disabled selected>Choose account type</option>
                                    <option value="individual">Individual</option>
                                    <option value="organization">Organization</option>
                                    <option value="ngo">NGO/Charity</option>
                                </select>
                                <label>Account Type</label>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s6">
                                <i class="material-icons prefix">person</i>
                                <input id="firstName" type="text" class="validate" required>
                                <label for="firstName">First Name</label>
                                <span class="helper-text" data-error="First name is required"></span>
                            </div>
                            <div class="input-field col s6">
                                <input id="lastName" type="text" class="validate" required>
                                <label for="lastName">Last Name</label>
                                <span class="helper-text" data-error="Last name is required"></span>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s12">
                                <i class="material-icons prefix">email</i>
                                <input id="regEmail" type="email" class="validate" required>
                                <label for="regEmail">Email Address</label>
                                <span class="helper-text" data-error="Please enter a valid email"></span>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s12">
                                <i class="material-icons prefix">phone</i>
                                <input id="phone" type="tel" class="validate" required>
                                <label for="phone">Phone Number</label>
                                <span class="helper-text" data-error="Phone number is required"></span>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s6">
                                <i class="material-icons prefix">lock</i>
                                <input id="regPassword" type="password" class="validate" required minlength="8">
                                <label for="regPassword">Password</label>
                                <span class="helper-text" data-error="Password must be at least 8 characters"></span>
                            </div>
                            <div class="input-field col s6">
                                <i class="material-icons prefix">lock_outline</i>
                                <input id="confirmPassword" type="password" class="validate" required>
                                <label for="confirmPassword">Confirm Password</label>
                                <span class="helper-text" data-error="Passwords must match"></span>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s12">
                                <i class="material-icons prefix">location_on</i>
                                <textarea id="address" class="materialize-textarea" data-length="200" required></textarea>
                                <label for="address">Address</label>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col s12">
                                <label>
                                    <input type="checkbox" id="terms" required />
                                    <span>I agree to the <a href="#" style="color: #4caf50;">Terms of Service</a> and <a href="#" style="color: #4caf50;">Privacy Policy</a></span>
                                </label>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col s12">
                                <label>
                                    <input type="checkbox" id="newsletter" />
                                    <span>Subscribe to our newsletter for updates</span>
                                </label>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col s6">
                                <button class="btn waves-effect waves-light btn-haven" type="submit" style="width: 100%;">
                                    Create Account
                                    <i class="material-icons right">person_add</i>
                                </button>
                            </div>
                            <div class="col s6">
                                <button class="btn waves-effect waves-light grey" type="button" onclick="showLogin()" style="width: 100%;">
                                    Back to Login
                                    <i class="material-icons right">arrow_back</i>
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function showLogin() {
        console.log('Show login form');
    }
    
    document.getElementById('registerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const password = document.getElementById('regPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (password !== confirmPassword) {
            M.toast({html: 'Passwords do not match!', classes: 'red'});
            return;
        }
        
        M.toast({html: 'Registration successful!', classes: 'green'});
        console.log('Registration form submitted');
    });
    </script>
    """, unsafe_allow_html=True)

# Enhanced Campaign Creation Form
def show_create_campaign():
    show_header()
    show_vertical_navbar()
    show_fab()
    
    st.markdown("""
    <div class="container" style="margin-top: 40px;">
        <div class="row">
            <div class="col s12">
                <h4 class="center-align" style="color: #4caf50; font-weight: 300;">➕ Create New Campaign</h4>
            </div>
        </div>
        
        <div class="row">
            <div class="col s12 m10 offset-m1">
                <div class="form-container">
                    <form id="campaignForm">
                        <div class="row">
                            <div class="input-field col s12 m6">
                                <i class="material-icons prefix">category</i>
                                <select id="purpose" required>
                                    <option value="" disabled selected>Select campaign purpose</option>
                                    <option value="medical">Medical Treatment</option>
                                    <option value="education">Education</option>
                                    <option value="disaster">Disaster Relief</option>
                                    <option value="community">Community Development</option>
                                    <option value="environment">Environmental</option>
                                    <option value="animal">Animal Welfare</option>
                                    <option value="sports">Sports</option>
                                    <option value="arts">Arts & Culture</option>
                                    <option value="technology">Technology</option>
                                    <option value="other">Other</option>
                                </select>
                                <label>Campaign Purpose</label>
                            </div>
                            <div class="input-field col s12 m6">
                                <i class="material-icons prefix">location_on</i>
                                <select id="location" required>
                                    <option value="" disabled selected>Select location</option>
                                    <option value="mumbai">Mumbai</option>
                                    <option value="delhi">Delhi</option>
                                    <option value="bangalore">Bangalore</option>
                                    <option value="chennai">Chennai</option>
                                    <option value="kolkata">Kolkata</option>
                                    <option value="hyderabad">Hyderabad</option>
                                    <option value="pune">Pune</option>
                                    <option value="other">Other</option>
                                </select>
                                <label>Location</label>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s12">
                                <i class="material-icons prefix">title</i>
                                <input id="campaignTitle" type="text" class="validate" required maxlength="100">
                                <label for="campaignTitle">Campaign Title</label>
                                <span class="helper-text" data-error="Title is required (max 100 characters)"></span>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s12">
                                <i class="material-icons prefix">description</i>
                                <textarea id="campaignDescription" class="materialize-textarea" data-length="1000" required></textarea>
                                <label for="campaignDescription">Campaign Description</label>
                                <span class="helper-text">Describe your campaign in detail. What is the cause? How will the funds be used?</span>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s12 m6">
                                <i class="material-icons prefix">attach_money</i>
                                <input id="fundingGoal" type="number" class="validate" required min="1000" max="10000000">
                                <label for="fundingGoal">Funding Goal (₹)</label>
                                <span class="helper-text" data-error="Goal must be between ₹1,000 and ₹1,00,00,000"></span>
                            </div>
                            <div class="input-field col s12 m6">
                                <i class="material-icons prefix">schedule</i>
                                <input id="duration" type="number" class="validate" required min="1" max="365">
                                <label for="duration">Campaign Duration (days)</label>
                                <span class="helper-text" data-error="Duration must be between 1 and 365 days"></span>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s12 m6">
                                <i class="material-icons prefix">person</i>
                                <input id="creatorName" type="text" class="validate" required>
                                <label for="creatorName">Creator/Organization Name</label>
                                <span class="helper-text" data-error="Creator name is required"></span>
                            </div>
                            <div class="input-field col s12 m6">
                                <i class="material-icons prefix">email</i>
                                <input id="contactEmail" type="email" class="validate" required>
                                <label for="contactEmail">Contact Email</label>
                                <span class="helper-text" data-error="Valid email is required"></span>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s12 m6">
                                <i class="material-icons prefix">phone</i>
                                <input id="contactPhone" type="tel" class="validate" required>
                                <label for="contactPhone">Contact Phone</label>
                                <span class="helper-text" data-error="Phone number is required"></span>
                            </div>
                            <div class="input-field col s12 m6">
                                <i class="material-icons prefix">language</i>
                                <input id="website" type="url" class="validate">
                                <label for="website">Website (Optional)</label>
                                <span class="helper-text" data-error="Please enter a valid URL"></span>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="file-field input-field col s12">
                                <div class="btn haven-primary">
                                    <span><i class="material-icons left">cloud_upload</i>Campaign Images</span>
                                    <input type="file" multiple accept="image/*">
                                </div>
                                <div class="file-path-wrapper">
                                    <input class="file-path validate" type="text" placeholder="Upload campaign images (max 5)">
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col s12">
                                <h6 style="color: #4caf50; margin-bottom: 20px;">Campaign Settings</h6>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col s12 m6">
                                <div class="switch">
                                    <label>
                                        Private Campaign
                                        <input type="checkbox" id="isPrivate">
                                        <span class="lever"></span>
                                        Public Campaign
                                    </label>
                                </div>
                                <p style="font-size: 12px; color: #666; margin-top: 10px;">
                                    Private campaigns are only visible to people with the link
                                </p>
                            </div>
                            <div class="col s12 m6">
                                <div class="switch">
                                    <label>
                                        Manual Approval
                                        <input type="checkbox" id="autoApprove" checked>
                                        <span class="lever"></span>
                                        Auto Approve
                                    </label>
                                </div>
                                <p style="font-size: 12px; color: #666; margin-top: 10px;">
                                    Auto approve donations or require manual approval
                                </p>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col s12">
                                <label>
                                    <input type="checkbox" id="agreeTerms" required />
                                    <span>I agree to the <a href="#" style="color: #4caf50;">Campaign Terms</a> and confirm that all information provided is accurate</span>
                                </label>
                            </div>
                        </div>
                        
                        <div class="row" style="margin-top: 30px;">
                            <div class="col s12 m6">
                                <button class="btn waves-effect waves-light btn-haven" type="submit" style="width: 100%;">
                                    Create Campaign
                                    <i class="material-icons right">send</i>
                                </button>
                            </div>
                            <div class="col s12 m6">
                                <button class="btn waves-effect waves-light grey" type="button" onclick="saveDraft()" style="width: 100%;">
                                    Save as Draft
                                    <i class="material-icons right">save</i>
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function saveDraft() {
        M.toast({html: 'Campaign saved as draft!', classes: 'blue'});
        console.log('Save as draft');
    }
    
    document.getElementById('campaignForm').addEventListener('submit', function(e) {
        e.preventDefault();
        M.toast({html: 'Campaign created successfully!', classes: 'green'});
        console.log('Campaign form submitted');
    });
    </script>
    """, unsafe_allow_html=True)

# Enhanced Search Form
def show_search():
    show_header()
    show_vertical_navbar()
    show_fab()
    
    st.markdown("""
    <div class="container" style="margin-top: 40px;">
        <div class="row">
            <div class="col s12">
                <h4 class="center-align" style="color: #4caf50; font-weight: 300;">🔎 Search Campaigns</h4>
            </div>
        </div>
        
        <div class="row">
            <div class="col s12 m8 offset-m2">
                <div class="form-container">
                    <form id="searchForm">
                        <div class="row">
                            <div class="input-field col s12">
                                <i class="material-icons prefix">search</i>
                                <input id="searchQuery" type="text" class="validate" placeholder="Search for campaigns...">
                                <label for="searchQuery">Search Keywords</label>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s12 m6">
                                <i class="material-icons prefix">category</i>
                                <select id="searchCategory">
                                    <option value="" selected>All Categories</option>
                                    <option value="medical">Medical</option>
                                    <option value="education">Education</option>
                                    <option value="disaster">Disaster Relief</option>
                                    <option value="community">Community</option>
                                    <option value="environment">Environment</option>
                                    <option value="animal">Animal Welfare</option>
                                    <option value="sports">Sports</option>
                                    <option value="arts">Arts & Culture</option>
                                    <option value="technology">Technology</option>
                                </select>
                                <label>Category</label>
                            </div>
                            <div class="input-field col s12 m6">
                                <i class="material-icons prefix">location_on</i>
                                <select id="searchLocation">
                                    <option value="" selected>All Locations</option>
                                    <option value="mumbai">Mumbai</option>
                                    <option value="delhi">Delhi</option>
                                    <option value="bangalore">Bangalore</option>
                                    <option value="chennai">Chennai</option>
                                    <option value="kolkata">Kolkata</option>
                                    <option value="hyderabad">Hyderabad</option>
                                    <option value="pune">Pune</option>
                                </select>
                                <label>Location</label>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col s12">
                                <h6 style="color: #4caf50; margin-bottom: 20px;">Funding Goal Range</h6>
                                <p class="range-field">
                                    <input type="range" id="fundingRange" min="1000" max="1000000" value="500000" />
                                </p>
                                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #666;">
                                    <span>₹1,000</span>
                                    <span id="rangeValue">₹5,00,000</span>
                                    <span>₹10,00,000</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col s12">
                                <h6 style="color: #4caf50; margin-bottom: 20px;">Campaign Status</h6>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col s12 m4">
                                <label>
                                    <input name="status" type="radio" value="active" checked />
                                    <span>Active Campaigns</span>
                                </label>
                            </div>
                            <div class="col s12 m4">
                                <label>
                                    <input name="status" type="radio" value="completed" />
                                    <span>Completed Campaigns</span>
                                </label>
                            </div>
                            <div class="col s12 m4">
                                <label>
                                    <input name="status" type="radio" value="all" />
                                    <span>All Campaigns</span>
                                </label>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col s12">
                                <h6 style="color: #4caf50; margin-bottom: 20px;">Sort By</h6>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="input-field col s12 m6">
                                <select id="sortBy">
                                    <option value="recent" selected>Most Recent</option>
                                    <option value="popular">Most Popular</option>
                                    <option value="funded">Most Funded</option>
                                    <option value="ending">Ending Soon</option>
                                    <option value="goal">Funding Goal</option>
                                </select>
                                <label>Sort Order</label>
                            </div>
                            <div class="input-field col s12 m6">
                                <select id="resultsPerPage">
                                    <option value="10" selected>10 Results</option>
                                    <option value="20">20 Results</option>
                                    <option value="50">50 Results</option>
                                    <option value="100">100 Results</option>
                                </select>
                                <label>Results Per Page</label>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col s12 m6">
                                <button class="btn waves-effect waves-light btn-haven" type="submit" style="width: 100%;">
                                    <i class="material-icons left">search</i>Search Campaigns
                                </button>
                            </div>
                            <div class="col s12 m6">
                                <button class="btn waves-effect waves-light grey" type="button" onclick="clearSearch()" style="width: 100%;">
                                    <i class="material-icons left">clear</i>Clear Filters
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    // Update range value display
    document.getElementById('fundingRange').addEventListener('input', function() {
        const value = parseInt(this.value);
        const formatted = new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(value);
        document.getElementById('rangeValue').textContent = formatted;
    });
    
    function clearSearch() {
        document.getElementById('searchForm').reset();
        document.getElementById('rangeValue').textContent = '₹5,00,000';
        M.FormSelect.init(document.querySelectorAll('select'));
        M.toast({html: 'Search filters cleared!', classes: 'blue'});
    }
    
    document.getElementById('searchForm').addEventListener('submit', function(e) {
        e.preventDefault();
        M.toast({html: 'Searching campaigns...', classes: 'green'});
        console.log('Search form submitted');
    });
    </script>
    """, unsafe_allow_html=True)

# Home page (same as before but with form integration)
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
    
    # Sample campaigns (same as before)
    campaigns = [
        {
            "title": "Clean Water for Rural Villages",
            "description": "Providing clean drinking water access to 500 families in rural Maharashtra through sustainable well construction and water purification systems.",
            "goal": 500000,
            "raised": 325000,
            "percentage": 65,
            "days_left": 15,
            "creator": "Water for All NGO",
            "image": "https://images.unsplash.com/photo-1541919329513-35f7af297129?w=600&h=400&fit=crop"
        },
        {
            "title": "Education for Underprivileged Children",
            "description": "Building a school and providing education materials for 200 children in urban slums, including books, uniforms, and digital learning tools.",
            "goal": 750000,
            "raised": 450000,
            "percentage": 60,
            "days_left": 25,
            "creator": "Bright Future Foundation",
            "image": "https://images.unsplash.com/photo-1497486751825-1233686d5d80?w=600&h=400&fit=crop"
        }
    ]
    
    for i, campaign in enumerate(campaigns):
        if i % 2 == 0:
            st.markdown('<div class="container"><div class="row">', unsafe_allow_html=True)
        
        col_class = "s12 m6"
        
        st.markdown(f"""
        <div class="col {col_class}">
            <div class="card campaign-card">
                <div class="campaign-image" style="background-image: url('{campaign['image']}');">
                    <div class="campaign-overlay">
                        <span class="card-title" style="font-weight: 500;">{campaign['title']}</span>
                    </div>
                </div>
                <div class="card-content">
                    <p style="color: #666; line-height: 1.6; margin-bottom: 15px;">{campaign['description'][:120]}...</p>
                    <p style="color: #4caf50; font-weight: 500; margin-bottom: 10px;">by {campaign['creator']}</p>
                    
                    <div class="progress-custom">
                        <div class="determinate" style="width: {campaign['percentage']}%;"></div>
                    </div>
                    
                    <div class="row" style="margin: 15px 0 0 0;">
                        <div class="col s4">
                            <span style="color: #4caf50; font-weight: 500;">₹{campaign['raised']:,}</span>
                            <br><small style="color: #999;">raised</small>
                        </div>
                        <div class="col s4 center-align">
                            <span style="color: #4caf50; font-weight: 500;">{campaign['percentage']}%</span>
                            <br><small style="color: #999;">funded</small>
                        </div>
                        <div class="col s4 right-align">
                            <span style="color: #4caf50; font-weight: 500;">{campaign['days_left']}</span>
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
    
    if st.sidebar.button("🔍 Explore"):
        st.session_state.current_page = 'explore'
        st.rerun()
    
    if st.sidebar.button("🔎 Search"):
        st.session_state.current_page = 'search'
        st.rerun()
    
    if st.sidebar.button("➕ Create Campaign"):
        st.session_state.current_page = 'create'
        st.rerun()
    
    if st.sidebar.button("📝 Register"):
        st.session_state.current_page = 'register'
        st.rerun()
    
    if st.sidebar.button("👤 Profile"):
        st.session_state.current_page = 'profile'
        st.rerun()
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user_data = {}
        st.session_state.current_page = 'login'
        st.rerun()

# Profile page (simplified for space)
def show_profile():
    show_header()
    show_vertical_navbar()
    show_fab()
    
    user_data = st.session_state.user_data
    
    st.markdown(f"""
    <div class="container" style="margin-top: 40px;">
        <div class="row">
            <div class="col s12 m8 offset-m2">
                <div class="card">
                    <div class="card-content">
                        <div class="row">
                            <div class="col s12 center-align">
                                <i class="material-icons large" style="color: #4caf50;">account_circle</i>
                                <h4 style="color: #4caf50; font-weight: 300;">{user_data.get('name', 'User')}</h4>
                                <p style="color: #666;">{user_data.get('email', 'user@example.com')}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Explore page (simplified for space)
def show_explore():
    show_header()
    show_vertical_navbar()
    show_fab()
    
    st.markdown("""
    <div class="container" style="margin-top: 40px;">
        <div class="row">
            <div class="col s12">
                <h4 class="center-align" style="color: #4caf50; font-weight: 300;">🔍 Explore Categories</h4>
            </div>
        </div>
        
        <div class="row">
            <div class="col s12 m4">
                <div class="card-panel red category-card waves-effect waves-light">
                    <div class="category-icon">🏥</div>
                    <h5 style="color: white; font-weight: 400; margin: 10px 0;">Medical</h5>
                    <p style="color: rgba(255,255,255,0.9); margin: 0;">15 campaigns</p>
                </div>
            </div>
            <div class="col s12 m4">
                <div class="card-panel blue category-card waves-effect waves-light">
                    <div class="category-icon">🎓</div>
                    <h5 style="color: white; font-weight: 400; margin: 10px 0;">Education</h5>
                    <p style="color: rgba(255,255,255,0.9); margin: 0;">12 campaigns</p>
                </div>
            </div>
            <div class="col s12 m4">
                <div class="card-panel green category-card waves-effect waves-light">
                    <div class="category-icon">🌱</div>
                    <h5 style="color: white; font-weight: 400; margin: 10px 0;">Environment</h5>
                    <p style="color: rgba(255,255,255,0.9); margin: 0;">8 campaigns</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main application
def main():
    load_materialize_css()
    init_session_state()
    
    if not st.session_state.authenticated:
        if st.session_state.current_page == 'register':
            show_register()
        else:
            show_login()
    else:
        handle_navigation()
        
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

