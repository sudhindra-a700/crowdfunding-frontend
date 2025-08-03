import streamlit as st
import requests
import json
import base64
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="HAVEN - Help Humanity",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Pure.css and custom CSS
def load_css():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/pure-min.css" integrity="sha384-X38yfunGUhNzHpBaEBsWLO+A0HDYOQi8ufWDkZ0k9e0eXz/tH3II7uKZ9msv++Ls" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/grids-responsive-min.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Pure.css Custom Styling for HAVEN */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #f0fff0 0%, #e6ffe6 100%);
        margin: 0;
        padding: 0;
    }
    
    .haven-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Header Styling */
    .haven-header {
        text-align: center;
        padding: 30px 0;
        background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%);
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .haven-logo {
        font-size: 3.5rem;
        font-weight: bold;
        color: #2d5016;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .haven-tagline {
        font-size: 1.2rem;
        color: #4a5568;
        font-style: italic;
        margin-bottom: 0;
    }
    
    /* Sidebar Styling */
    .haven-sidebar {
        position: fixed;
        left: 0;
        top: 0;
        width: 280px;
        height: 100vh;
        background: linear-gradient(180deg, #a8e6cf 0%, #dcedc1 100%);
        padding: 20px;
        box-shadow: 4px 0 15px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        overflow-y: auto;
    }
    
    .sidebar-logo {
        text-align: center;
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .sidebar-logo h2 {
        color: #2d5016;
        font-size: 2rem;
        margin: 0;
        font-weight: bold;
    }
    
    .sidebar-nav {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .sidebar-nav li {
        margin-bottom: 15px;
    }
    
    .sidebar-nav a {
        display: flex;
        align-items: center;
        padding: 15px 20px;
        color: #2d5016;
        text-decoration: none;
        border-radius: 10px;
        transition: all 0.3s ease;
        font-weight: 500;
        background: rgba(255, 255, 255, 0.2);
    }
    
    .sidebar-nav a:hover {
        background: rgba(255, 255, 255, 0.4);
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-nav i {
        margin-right: 15px;
        font-size: 1.2rem;
        width: 20px;
        text-align: center;
    }
    
    .language-selector {
        margin-top: 30px;
        padding-top: 20px;
        border-top: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .language-selector select {
        width: 100%;
        padding: 12px;
        border: none;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.9);
        color: #2d5016;
        font-weight: 500;
    }
    
    /* Main Content */
    .main-content {
        margin-left: 300px;
        padding: 20px;
        min-height: 100vh;
    }
    
    /* Pure.css Button Customization */
    .pure-button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .pure-button:hover {
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4);
    }
    
    .pure-button-primary {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
    }
    
    .pure-button-primary:hover {
        background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%);
        box-shadow: 0 6px 20px rgba(66, 153, 225, 0.4);
    }
    
    /* Campaign Cards */
    .campaign-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(168, 230, 207, 0.3);
    }
    
    .campaign-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .campaign-image {
        width: 100%;
        height: 250px;
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e0 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        color: #718096;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .campaign-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2d3748;
        margin-bottom: 10px;
    }
    
    .campaign-creator {
        color: #718096;
        margin-bottom: 15px;
        font-style: italic;
    }
    
    .campaign-description {
        color: #4a5568;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    .campaign-stats {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding: 15px;
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 10px;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2d3748;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #718096;
        margin-top: 5px;
    }
    
    .progress-bar {
        width: 100%;
        height: 12px;
        background: #e2e8f0;
        border-radius: 6px;
        overflow: hidden;
        margin-bottom: 15px;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #48bb78 0%, #38a169 100%);
        border-radius: 6px;
        transition: width 0.3s ease;
    }
    
    /* Category Grid */
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 25px;
        margin-top: 30px;
    }
    
    .category-card {
        background: white;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
    }
    
    .category-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        border-color: #a8e6cf;
    }
    
    .category-icon {
        font-size: 3rem;
        margin-bottom: 20px;
        color: #48bb78;
    }
    
    .category-name {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2d3748;
        margin-bottom: 10px;
    }
    
    .category-count {
        color: #718096;
        font-size: 0.9rem;
    }
    
    /* Forms */
    .pure-form input, .pure-form textarea, .pure-form select {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px 15px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: white;
    }
    
    .pure-form input:focus, .pure-form textarea:focus, .pure-form select:focus {
        border-color: #a8e6cf;
        box-shadow: 0 0 0 3px rgba(168, 230, 207, 0.2);
        outline: none;
    }
    
    .form-group {
        margin-bottom: 25px;
    }
    
    .form-label {
        display: block;
        margin-bottom: 8px;
        font-weight: 600;
        color: #2d3748;
    }
    
    /* Search Page */
    .search-container {
        max-width: 600px;
        margin: 0 auto;
        text-align: center;
        padding: 60px 20px;
    }
    
    .search-title {
        font-size: 3rem;
        font-weight: bold;
        color: #2d3748;
        margin-bottom: 20px;
    }
    
    .search-subtitle {
        font-size: 1.2rem;
        color: #718096;
        margin-bottom: 40px;
    }
    
    .search-box {
        display: flex;
        max-width: 500px;
        margin: 0 auto 30px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border-radius: 50px;
        overflow: hidden;
    }
    
    .search-input {
        flex: 1;
        border: none;
        padding: 18px 25px;
        font-size: 1.1rem;
        outline: none;
    }
    
    .search-button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        border: none;
        padding: 18px 30px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .search-button:hover {
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
    }
    
    /* OAuth Buttons */
    .oauth-container {
        display: flex;
        gap: 15px;
        justify-content: center;
        margin: 25px 0;
    }
    
    .oauth-button {
        display: flex;
        align-items: center;
        padding: 12px 20px;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        background: white;
        color: #4a5568;
        text-decoration: none;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .oauth-button:hover {
        border-color: #a8e6cf;
        background: #f7fafc;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }
    
    .oauth-button i {
        margin-right: 10px;
        font-size: 1.2rem;
    }
    
    .google-button {
        border-color: #db4437;
        color: #db4437;
    }
    
    .facebook-button {
        border-color: #4267b2;
        color: #4267b2;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .haven-sidebar {
            transform: translateX(-100%);
            transition: transform 0.3s ease;
        }
        
        .haven-sidebar.open {
            transform: translateX(0);
        }
        
        .main-content {
            margin-left: 0;
        }
        
        .campaign-stats {
            flex-direction: column;
            gap: 15px;
        }
        
        .category-grid {
            grid-template-columns: 1fr;
        }
        
        .search-title {
            font-size: 2rem;
        }
        
        .oauth-container {
            flex-direction: column;
            align-items: center;
        }
    }
    
    /* Trending Badge */
    .trending-badge {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .trending-badge i {
        margin-right: 8px;
    }
    
    /* Login/Register Forms */
    .auth-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    
    .auth-title {
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #2d3748;
        margin-bottom: 30px;
    }
    
    /* Backend Status */
    .backend-status {
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 10px 15px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        z-index: 1000;
    }
    
    .status-online {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
    }
    
    .status-offline {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'English'

# Backend configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'https://haven-fastapi-backend.onrender.com')

# Language translations
TRANSLATIONS = {
    'English': {
        'title': 'HAVEN',
        'tagline': 'Help not just some people, but Help Humanity',
        'login': 'Login',
        'register': 'Register',
        'home': 'Home',
        'explore': 'Explore',
        'search': 'Search',
        'create_campaign': 'Create Campaign',
        'profile': 'Profile',
        'trending_campaigns': 'Trending Campaigns',
        'explore_categories': 'Explore Categories',
        'search_campaigns': 'Search Campaigns',
        'email': 'Email',
        'password': 'Password',
        'continue': 'Continue',
        'sign_up': 'Sign Up',
        'google_signin': 'Continue with Google',
        'facebook_signin': 'Continue with Facebook'
    },
    'Hindi': {
        'title': 'हेवन',
        'tagline': 'केवल कुछ लोगों की नहीं, बल्कि मानवता की मदद करें',
        'login': 'लॉगिन',
        'register': 'पंजीकरण',
        'home': 'होम',
        'explore': 'खोजें',
        'search': 'खोज',
        'create_campaign': 'अभियान बनाएं',
        'profile': 'प्रोफाइल',
        'trending_campaigns': 'ट्रेंडिंग अभियान',
        'explore_categories': 'श्रेणियां खोजें',
        'search_campaigns': 'अभियान खोजें',
        'email': 'ईमेल',
        'password': 'पासवर्ड',
        'continue': 'जारी रखें',
        'sign_up': 'साइन अप',
        'google_signin': 'Google के साथ जारी रखें',
        'facebook_signin': 'Facebook के साथ जारी रखें'
    },
    'Tamil': {
        'title': 'ஹேவன்',
        'tagline': 'சிலரை மட்டும் அல்ல, மனிதகுலத்திற்கு உதவுங்கள்',
        'login': 'உள்நுழைவு',
        'register': 'பதிவு',
        'home': 'முகப்பு',
        'explore': 'ஆராயுங்கள்',
        'search': 'தேடல்',
        'create_campaign': 'பிரச்சாரம் உருவாக்கவும்',
        'profile': 'சுயவிவரம்',
        'trending_campaigns': 'டிரெண்டிங் பிரச்சாரங்கள்',
        'explore_categories': 'வகைகளை ஆராயுங்கள்',
        'search_campaigns': 'பிரச்சாரங்களைத் தேடுங்கள்',
        'email': 'மின்னஞ்சல்',
        'password': 'கடவுச்சொல்',
        'continue': 'தொடரவும்',
        'sign_up': 'பதிவு செய்யவும்',
        'google_signin': 'Google உடன் தொடரவும்',
        'facebook_signin': 'Facebook உடன் தொடரவும்'
    },
    'Telugu': {
        'title': 'హేవెన్',
        'tagline': 'కొంతమందికి మాత్రమే కాకుండా, మానవత్వానికి సహాయం చేయండి',
        'login': 'లాగిన్',
        'register': 'నమోదు',
        'home': 'హోమ్',
        'explore': 'అన్వేషించండి',
        'search': 'వెతకండి',
        'create_campaign': 'ప్రచారం సృష్టించండి',
        'profile': 'ప్రొఫైల్',
        'trending_campaigns': 'ట్రెండింగ్ ప్రచారాలు',
        'explore_categories': 'వర్గాలను అన్వేషించండి',
        'search_campaigns': 'ప్రచారాలను వెతకండి',
        'email': 'ఇమెయిల్',
        'password': 'పాస్‌వర్డ్',
        'continue': 'కొనసాగించండి',
        'sign_up': 'సైన్ అప్',
        'google_signin': 'Google తో కొనసాగించండి',
        'facebook_signin': 'Facebook తో కొనసాగించండి'
    }
}

def get_text(key):
    """Get translated text based on selected language"""
    return TRANSLATIONS[st.session_state.selected_language].get(key, key)

def check_backend_status():
    """Check if backend is online"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def render_backend_status():
    """Render backend status indicator"""
    is_online = check_backend_status()
    status_class = "status-online" if is_online else "status-offline"
    status_text = "Backend Online" if is_online else "Backend Offline"
    status_icon = "🟢" if is_online else "🔴"
    
    st.markdown(f"""
    <div class="backend-status {status_class}">
        {status_icon} {status_text}
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render navigation sidebar for authenticated users"""
    if not st.session_state.authenticated:
        return
    
    st.markdown(f"""
    <div class="haven-sidebar">
        <div class="sidebar-logo">
            <h2>{get_text('title')}</h2>
        </div>
        
        <ul class="sidebar-nav">
            <li><a href="#" onclick="setPage('home')"><i class="fas fa-home"></i>{get_text('home')}</a></li>
            <li><a href="#" onclick="setPage('explore')"><i class="fas fa-compass"></i>{get_text('explore')}</a></li>
            <li><a href="#" onclick="setPage('search')"><i class="fas fa-search"></i>{get_text('search')}</a></li>
            <li><a href="#" onclick="setPage('create_campaign')" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); color: white;"><i class="fas fa-plus"></i>{get_text('create_campaign')}</a></li>
            <li style="margin-top: auto;"><a href="#" onclick="setPage('profile')"><i class="fas fa-user"></i>{get_text('profile')}</a></li>
        </ul>
        
        <div class="language-selector">
            <select onchange="changeLanguage(this.value)">
                <option value="English" {'selected' if st.session_state.selected_language == 'English' else ''}>English</option>
                <option value="Hindi" {'selected' if st.session_state.selected_language == 'Hindi' else ''}>हिन्दी</option>
                <option value="Tamil" {'selected' if st.session_state.selected_language == 'Tamil' else ''}>தமிழ்</option>
                <option value="Telugu" {'selected' if st.session_state.selected_language == 'Telugu' else ''}>తెలుగు</option>
            </select>
        </div>
    </div>
    
    <script>
    function setPage(page) {{
        window.parent.postMessage({{type: 'setPage', page: page}}, '*');
    }}
    
    function changeLanguage(lang) {{
        window.parent.postMessage({{type: 'changeLanguage', language: lang}}, '*');
    }}
    </script>
    """, unsafe_allow_html=True)

def render_login_page():
    """Render login page with Pure.css styling"""
    st.markdown(f"""
    <div class="haven-container">
        <div class="haven-header">
            <h1 class="haven-logo">{get_text('title')}</h1>
            <p class="haven-tagline">{get_text('tagline')}</p>
        </div>
        
        <div class="auth-container">
            <h2 class="auth-title">{get_text('login')}</h2>
            
            <form class="pure-form pure-form-stacked">
                <div class="form-group">
                    <label class="form-label" for="email">{get_text('email')}</label>
                    <input type="email" id="email" class="pure-input-1" placeholder="Enter your email">
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="password">{get_text('password')}</label>
                    <input type="password" id="password" class="pure-input-1" placeholder="Enter your password">
                </div>
                
                <button type="button" class="pure-button pure-button-primary pure-input-1" onclick="login()">{get_text('continue')}</button>
            </form>
            
            <div class="oauth-container">
                <a href="#" class="oauth-button google-button" onclick="googleLogin()">
                    <i class="fab fa-google"></i>{get_text('google_signin')}
                </a>
                <a href="#" class="oauth-button facebook-button" onclick="facebookLogin()">
                    <i class="fab fa-facebook-f"></i>{get_text('facebook_signin')}
                </a>
            </div>
            
            <div style="text-align: center; margin-top: 25px;">
                <p>Don't have an account? <a href="#" onclick="setPage('register')" style="color: #48bb78; font-weight: 600;">{get_text('sign_up')}</a></p>
            </div>
        </div>
    </div>
    
    <script>
    function login() {{
        // Simulate login for demo
        window.parent.postMessage({{type: 'login', success: true}}, '*');
    }}
    
    function googleLogin() {{
        // Simulate Google OAuth
        window.parent.postMessage({{type: 'oauth', provider: 'google'}}, '*');
    }}
    
    function facebookLogin() {{
        // Simulate Facebook OAuth
        window.parent.postMessage({{type: 'oauth', provider: 'facebook'}}, '*');
    }}
    
    function setPage(page) {{
        window.parent.postMessage({{type: 'setPage', page: page}}, '*');
    }}
    </script>
    """, unsafe_allow_html=True)

def render_register_page():
    """Render registration page"""
    st.markdown(f"""
    <div class="main-content">
        <div class="haven-container">
            <div class="auth-container">
                <h2 class="auth-title">{get_text('register')}</h2>
                
                <form class="pure-form pure-form-stacked">
                    <div class="form-group">
                        <label class="form-label">Account Type</label>
                        <select class="pure-input-1" onchange="toggleAccountType(this.value)">
                            <option value="">Select account type</option>
                            <option value="individual">Individual</option>
                            <option value="organization">Organization</option>
                        </select>
                    </div>
                    
                    <div id="individual-fields" style="display: none;">
                        <div class="form-group">
                            <label class="form-label">Full Name</label>
                            <input type="text" class="pure-input-1" placeholder="Enter your full name">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Phone Number</label>
                            <input type="tel" class="pure-input-1" placeholder="Enter your phone number">
                        </div>
                    </div>
                    
                    <div id="organization-fields" style="display: none;">
                        <div class="form-group">
                            <label class="form-label">Organization Name</label>
                            <input type="text" class="pure-input-1" placeholder="Enter organization name">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Organization Type</label>
                            <select class="pure-input-1">
                                <option value="">Select type</option>
                                <option value="ngo">NGO</option>
                                <option value="startup">Startup</option>
                                <option value="charity">Charity</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Description</label>
                            <textarea class="pure-input-1" rows="3" placeholder="Describe your organization"></textarea>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">{get_text('email')}</label>
                        <input type="email" class="pure-input-1" placeholder="Enter your email">
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">{get_text('password')}</label>
                        <input type="password" class="pure-input-1" placeholder="Create a password">
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Confirm Password</label>
                        <input type="password" class="pure-input-1" placeholder="Confirm your password">
                    </div>
                    
                    <button type="button" class="pure-button pure-button-primary pure-input-1" onclick="register()">Create Account</button>
                </form>
                
                <div style="text-align: center; margin-top: 25px;">
                    <p>Already have an account? <a href="#" onclick="setPage('login')" style="color: #48bb78; font-weight: 600;">{get_text('login')}</a></p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function toggleAccountType(type) {{
        document.getElementById('individual-fields').style.display = type === 'individual' ? 'block' : 'none';
        document.getElementById('organization-fields').style.display = type === 'organization' ? 'block' : 'none';
    }}
    
    function register() {{
        window.parent.postMessage({{type: 'register', success: true}}, '*');
    }}
    
    function setPage(page) {{
        window.parent.postMessage({{type: 'setPage', page: page}}, '*');
    }}
    </script>
    """, unsafe_allow_html=True)

def render_home_page():
    """Render trending campaigns homepage"""
    # Sample campaign data
    campaigns = [
        {
            'id': 1,
            'title': 'Help Build Clean Water Wells',
            'creator': 'Water for All Foundation',
            'description': 'Providing clean drinking water to rural communities across India. Every donation helps build sustainable water infrastructure.',
            'raised': 75000,
            'goal': 100000,
            'percentage': 75,
            'days_left': 30,
            'image': '600 × 400'
        },
        {
            'id': 2,
            'title': 'Education for Underprivileged Children',
            'creator': 'Bright Future NGO',
            'description': 'Supporting education initiatives for children who cannot afford school fees and supplies.',
            'raised': 45000,
            'goal': 80000,
            'percentage': 56,
            'days_left': 45,
            'image': '600 × 400'
        },
        {
            'id': 3,
            'title': 'Medical Treatment for Cancer Patients',
            'creator': 'Hope Medical Center',
            'description': 'Funding critical medical treatments for cancer patients who cannot afford healthcare costs.',
            'raised': 120000,
            'goal': 150000,
            'percentage': 80,
            'days_left': 20,
            'image': '600 × 400'
        }
    ]
    
    st.markdown(f"""
    <div class="main-content">
        <div class="haven-container">
            <h1 style="font-size: 3rem; font-weight: bold; color: #2d3748; margin-bottom: 10px;">{get_text('trending_campaigns')}</h1>
            <p style="font-size: 1.2rem; color: #718096; margin-bottom: 40px;">Support the most popular projects on HAVEN.</p>
            
            <div class="pure-g">
    """, unsafe_allow_html=True)
    
    for campaign in campaigns:
        st.markdown(f"""
                <div class="pure-u-1">
                    <div class="campaign-card">
                        <div class="trending-badge">
                            <i class="fas fa-bolt"></i>Trending
                        </div>
                        
                        <div class="campaign-image">{campaign['image']}</div>
                        
                        <h3 class="campaign-title">{campaign['title']}</h3>
                        <p class="campaign-creator">By {campaign['creator']}</p>
                        <p class="campaign-description">{campaign['description']}</p>
                        
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {campaign['percentage']}%"></div>
                        </div>
                        
                        <div class="campaign-stats">
                            <div class="stat-item">
                                <div class="stat-value">₹{campaign['raised']:,}</div>
                                <div class="stat-label">raised</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{campaign['percentage']}%</div>
                                <div class="stat-label">funded</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{campaign['days_left']}</div>
                                <div class="stat-label">days left</div>
                            </div>
                        </div>
                        
                        <button class="pure-button pure-button-primary" onclick="viewCampaign({campaign['id']})">View Campaign</button>
                    </div>
                </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
    </div>
    
    <script>
    function viewCampaign(id) {
        window.parent.postMessage({type: 'viewCampaign', campaignId: id}, '*');
    }
    </script>
    """, unsafe_allow_html=True)

def render_explore_page():
    """Render explore categories page"""
    categories = [
        {'name': 'Art & Design', 'icon': 'fas fa-palette', 'count': 245},
        {'name': 'Technology', 'icon': 'fas fa-laptop-code', 'count': 189},
        {'name': 'Community', 'icon': 'fas fa-users', 'count': 312},
        {'name': 'Film & Video', 'icon': 'fas fa-video', 'count': 156},
        {'name': 'Music', 'icon': 'fas fa-music', 'count': 203},
        {'name': 'Publishing', 'icon': 'fas fa-book', 'count': 134}
    ]
    
    st.markdown(f"""
    <div class="main-content">
        <div class="haven-container">
            <h1 style="font-size: 3rem; font-weight: bold; color: #2d3748; margin-bottom: 10px;">{get_text('explore_categories')}</h1>
            <p style="font-size: 1.2rem; color: #718096; margin-bottom: 40px;">Discover campaigns by interest.</p>
            
            <div class="category-grid">
    """, unsafe_allow_html=True)
    
    for category in categories:
        st.markdown(f"""
                <div class="category-card" onclick="exploreCategory('{category['name']}')">
                    <div class="category-icon">
                        <i class="{category['icon']}"></i>
                    </div>
                    <h3 class="category-name">{category['name']}</h3>
                    <p class="category-count">{category['count']} campaigns</p>
                </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
    </div>
    
    <script>
    function exploreCategory(category) {
        window.parent.postMessage({type: 'exploreCategory', category: category}, '*');
    }
    </script>
    """, unsafe_allow_html=True)

def render_search_page():
    """Render search campaigns page"""
    st.markdown(f"""
    <div class="main-content">
        <div class="search-container">
            <h1 class="search-title">{get_text('search_campaigns')}</h1>
            
            <div class="search-box">
                <input type="text" class="search-input" placeholder="Search by keyword, category..." id="searchInput">
                <button class="search-button" onclick="performSearch()">
                    <i class="fas fa-search"></i>
                </button>
            </div>
            
            <p class="search-subtitle">Enter a term above to search for campaigns.</p>
            <p style="color: #718096;">You can search by title, description, or category.</p>
            
            <div id="searchResults" style="margin-top: 40px;"></div>
        </div>
    </div>
    
    <script>
    function performSearch() {{
        const query = document.getElementById('searchInput').value;
        if (query.trim()) {{
            window.parent.postMessage({{type: 'search', query: query}}, '*');
        }}
    }}
    
    document.getElementById('searchInput').addEventListener('keypress', function(e) {{
        if (e.key === 'Enter') {{
            performSearch();
        }}
    }});
    </script>
    """, unsafe_allow_html=True)

def render_create_campaign_page():
    """Render create campaign page"""
    st.markdown(f"""
    <div class="main-content">
        <div class="haven-container">
            <h1 style="font-size: 3rem; font-weight: bold; color: #2d3748; margin-bottom: 10px;">{get_text('create_campaign')}</h1>
            <p style="font-size: 1.2rem; color: #718096; margin-bottom: 40px;">Start your campaign to help humanity.</p>
            
            <form class="pure-form pure-form-stacked" style="max-width: 600px; margin: 0 auto;">
                <div class="form-group">
                    <label class="form-label">Purpose of raising fund</label>
                    <select class="pure-input-1" id="campaignPurpose">
                        <option value="">Select purpose</option>
                        <option value="medical">Medical Treatment</option>
                        <option value="ngo">NGO / Charity</option>
                        <option value="other">Other Cause</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Campaign Title</label>
                    <input type="text" class="pure-input-1" placeholder="Enter campaign title" id="campaignTitle">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Basic Description</label>
                    <textarea class="pure-input-1" rows="5" placeholder="Describe your campaign in detail..." id="campaignDescription"></textarea>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Pictures of Actions</label>
                    <input type="file" class="pure-input-1" multiple accept="image/*" id="campaignImages">
                    <small style="color: #718096;">Upload images that show your cause in action</small>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Funding Goal (₹)</label>
                    <input type="number" class="pure-input-1" placeholder="Enter target amount" id="fundingGoal">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Campaign Duration (days)</label>
                    <input type="number" class="pure-input-1" placeholder="Enter duration in days" id="campaignDuration">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Location</label>
                    <input type="text" class="pure-input-1" placeholder="Enter location" id="campaignLocation">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Contact Email</label>
                    <input type="email" class="pure-input-1" placeholder="Enter contact email" id="contactEmail">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Contact Phone</label>
                    <input type="tel" class="pure-input-1" placeholder="Enter contact phone" id="contactPhone">
                </div>
                
                <button type="button" class="pure-button pure-button-primary pure-input-1" onclick="createCampaign()">Create Campaign</button>
            </form>
        </div>
    </div>
    
    <script>
    function createCampaign() {{
        const campaignData = {{
            purpose: document.getElementById('campaignPurpose').value,
            title: document.getElementById('campaignTitle').value,
            description: document.getElementById('campaignDescription').value,
            goal: document.getElementById('fundingGoal').value,
            duration: document.getElementById('campaignDuration').value,
            location: document.getElementById('campaignLocation').value,
            email: document.getElementById('contactEmail').value,
            phone: document.getElementById('contactPhone').value
        }};
        
        if (campaignData.purpose && campaignData.title && campaignData.description) {{
            window.parent.postMessage({{type: 'createCampaign', data: campaignData}}, '*');
        }} else {{
            alert('Please fill in all required fields');
        }}
    }}
    </script>
    """, unsafe_allow_html=True)

def render_campaign_detail_page(campaign_id):
    """Render individual campaign detail page"""
    # Sample campaign detail data
    campaign = {
        'id': campaign_id,
        'title': 'Help Build Clean Water Wells',
        'creator': 'Water for All Foundation',
        'organization': 'Water for All Foundation',
        'location': 'Rural Maharashtra, India',
        'contact': 'contact@waterforall.org',
        'description': 'Our mission is to provide clean drinking water to rural communities across India. This campaign will fund the construction of 10 new water wells in villages that currently lack access to safe drinking water. Each well will serve approximately 200 families and will be maintained by trained local technicians.',
        'raised': 75000,
        'goal': 100000,
        'percentage': 75,
        'donors': 156,
        'days_left': 30,
        'image': '600 × 400',
        'top_donors': [
            {'name': 'Anonymous', 'amount': 10000},
            {'name': 'Rajesh Kumar', 'amount': 8500},
            {'name': 'Priya Sharma', 'amount': 7200}
        ],
        'updates': [
            {'date': '2025-01-15', 'message': 'Construction of first well completed successfully!'},
            {'date': '2025-01-10', 'message': 'Site survey completed for all 10 locations.'},
            {'date': '2025-01-05', 'message': 'Campaign launched with community support.'}
        ]
    }
    
    st.markdown(f"""
    <div class="main-content">
        <div class="haven-container">
            <button class="pure-button" onclick="goBack()" style="margin-bottom: 20px;">
                <i class="fas fa-arrow-left"></i> Back to Campaigns
            </button>
            
            <div class="campaign-image" style="height: 300px; margin-bottom: 30px;">{campaign['image']}</div>
            
            <h1 style="font-size: 2.5rem; font-weight: bold; color: #2d3748; margin-bottom: 15px;">{campaign['title']}</h1>
            
            <div class="pure-g" style="margin-bottom: 30px;">
                <div class="pure-u-1 pure-u-md-2-3">
                    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); margin-right: 20px;">
                        <h3 style="color: #2d3748; margin-bottom: 15px;">Organization Information</h3>
                        <p><strong>Organization:</strong> {campaign['organization']}</p>
                        <p><strong>Location:</strong> {campaign['location']}</p>
                        <p><strong>Contact:</strong> {campaign['contact']}</p>
                        
                        <div style="margin: 25px 0;">
                            <button class="pure-button" style="margin-right: 15px; background: #4299e1; color: white;">
                                <i class="fas fa-share"></i> Share
                            </button>
                            <button class="pure-button pure-button-primary">
                                <i class="fas fa-heart"></i> Donate Now
                            </button>
                        </div>
                    </div>
                </div>
                
                <div class="pure-u-1 pure-u-md-1-3">
                    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);">
                        <div class="progress-bar" style="margin-bottom: 20px;">
                            <div class="progress-fill" style="width: {campaign['percentage']}%"></div>
                        </div>
                        
                        <div class="campaign-stats" style="flex-direction: column; text-align: center;">
                            <div class="stat-item" style="margin-bottom: 15px;">
                                <div class="stat-value">₹{campaign['raised']:,}</div>
                                <div class="stat-label">raised of ₹{campaign['goal']:,}</div>
                            </div>
                            <div class="stat-item" style="margin-bottom: 15px;">
                                <div class="stat-value">{campaign['donors']}</div>
                                <div class="stat-label">donors</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{campaign['days_left']}</div>
                                <div class="stat-label">days left</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="pure-g">
                <div class="pure-u-1 pure-u-md-2-3">
                    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); margin-right: 20px; margin-bottom: 25px;">
                        <h3 style="color: #2d3748; margin-bottom: 15px;">About This Campaign</h3>
                        <p style="line-height: 1.8; color: #4a5568;">{campaign['description']}</p>
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); margin-right: 20px;">
                        <h3 style="color: #2d3748; margin-bottom: 15px;">Campaign Updates</h3>
    """, unsafe_allow_html=True)
    
    for update in campaign['updates']:
        st.markdown(f"""
                        <div style="border-left: 4px solid #48bb78; padding-left: 15px; margin-bottom: 20px;">
                            <p style="font-weight: 600; color: #2d3748; margin-bottom: 5px;">{update['date']}</p>
                            <p style="color: #4a5568; margin: 0;">{update['message']}</p>
                        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
                    </div>
                </div>
                
                <div class="pure-u-1 pure-u-md-1-3">
                    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);">
                        <h3 style="color: #2d3748; margin-bottom: 15px;">Top Donors</h3>
    """, unsafe_allow_html=True)
    
    for i, donor in enumerate(campaign['top_donors'], 1):
        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #e2e8f0;">
                            <div>
                                <span style="font-weight: 600; color: #2d3748;">{i}. {donor['name']}</span>
                            </div>
                            <div>
                                <span style="color: #48bb78; font-weight: 600;">₹{donor['amount']:,}</span>
                            </div>
                        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function goBack() {
        window.parent.postMessage({type: 'setPage', page: 'home'}, '*');
    }
    </script>
    """, unsafe_allow_html=True)

def render_profile_page():
    """Render user profile page"""
    st.markdown(f"""
    <div class="main-content">
        <div class="haven-container">
            <h1 style="font-size: 3rem; font-weight: bold; color: #2d3748; margin-bottom: 40px;">{get_text('profile')}</h1>
            
            <div class="pure-g">
                <div class="pure-u-1 pure-u-md-1-2">
                    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); margin-right: 20px;">
                        <h3 style="color: #2d3748; margin-bottom: 20px;">Profile Information</h3>
                        
                        <form class="pure-form pure-form-stacked">
                            <div class="form-group">
                                <label class="form-label">Full Name</label>
                                <input type="text" class="pure-input-1" value="John Doe" readonly>
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">Email</label>
                                <input type="email" class="pure-input-1" value="john.doe@example.com" readonly>
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">Account Type</label>
                                <input type="text" class="pure-input-1" value="Individual" readonly>
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">Member Since</label>
                                <input type="text" class="pure-input-1" value="January 2025" readonly>
                            </div>
                            
                            <button type="button" class="pure-button pure-button-primary">Edit Profile</button>
                        </form>
                    </div>
                </div>
                
                <div class="pure-u-1 pure-u-md-1-2">
                    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);">
                        <h3 style="color: #2d3748; margin-bottom: 20px;">Activity Summary</h3>
                        
                        <div class="campaign-stats" style="flex-direction: column;">
                            <div class="stat-item" style="margin-bottom: 20px;">
                                <div class="stat-value">3</div>
                                <div class="stat-label">Campaigns Created</div>
                            </div>
                            <div class="stat-item" style="margin-bottom: 20px;">
                                <div class="stat-value">₹25,000</div>
                                <div class="stat-label">Total Raised</div>
                            </div>
                            <div class="stat-item" style="margin-bottom: 20px;">
                                <div class="stat-value">12</div>
                                <div class="stat-label">Campaigns Supported</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">₹5,500</div>
                                <div class="stat-label">Total Donated</div>
                            </div>
                        </div>
                        
                        <button type="button" class="pure-button" style="margin-top: 20px; width: 100%;" onclick="logout()">Logout</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function logout() {{
        window.parent.postMessage({{type: 'logout'}}, '*');
    }}
    </script>
    """, unsafe_allow_html=True)

# Main application logic
def main():
    load_css()
    
    # Handle JavaScript messages
    if 'js_message' in st.session_state:
        message = st.session_state.js_message
        if message.get('type') == 'login' or message.get('type') == 'oauth':
            st.session_state.authenticated = True
            st.session_state.current_page = 'home'
        elif message.get('type') == 'logout':
            st.session_state.authenticated = False
            st.session_state.current_page = 'login'
        elif message.get('type') == 'setPage':
            st.session_state.current_page = message.get('page', 'home')
        elif message.get('type') == 'changeLanguage':
            st.session_state.selected_language = message.get('language', 'English')
        elif message.get('type') == 'viewCampaign':
            st.session_state.current_page = 'campaign_detail'
            st.session_state.selected_campaign = message.get('campaignId')
        
        # Clear the message
        del st.session_state.js_message
        st.rerun()
    
    # Render appropriate page
    if not st.session_state.authenticated:
        if st.session_state.current_page == 'register':
            render_register_page()
        else:
            render_login_page()
    else:
        render_sidebar()
        
        if st.session_state.current_page == 'home':
            render_home_page()
        elif st.session_state.current_page == 'explore':
            render_explore_page()
        elif st.session_state.current_page == 'search':
            render_search_page()
        elif st.session_state.current_page == 'create_campaign':
            render_create_campaign_page()
        elif st.session_state.current_page == 'campaign_detail':
            campaign_id = st.session_state.get('selected_campaign', 1)
            render_campaign_detail_page(campaign_id)
        elif st.session_state.current_page == 'profile':
            render_profile_page()
        else:
            render_home_page()
    
    render_backend_status()

if __name__ == "__main__":
    main()

