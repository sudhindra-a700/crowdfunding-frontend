"""
HAVEN Crowdfunding Platform - Clean Frontend with Proper Navigation
Fixed to remove unnecessary "Navigate to registration" button
Only the "Create an account" link (red circled) connects to registration
"""

import streamlit as st
import requests
import json
import base64
import time
import os
import re
from urllib.parse import urlencode, parse_qs, urlparse

# Configuration
BACKEND_URL = "https://srv-d1sq8ser433s73eke7v0.onrender.com"

# Language translations
TRANSLATIONS = {
    'English': {
        'title': 'HAVEN',
        'subtitle': 'Crowdfunding Platform',
        'login': 'Login',
        'register': 'Register',
        'email': 'Email',
        'password': 'Password',
        'confirm_password': 'Confirm Password',
        'continue': 'Continue',
        'not_registered': 'Not registered?',
        'create_account': 'Create an account',
        'already_have_account': 'Already have an account?',
        'sign_in_here': 'Sign in here',
        'sign_in_google': 'Sign in with Google',
        'sign_in_facebook': 'Sign in with Facebook',
        'individual': 'Individual',
        'organization': 'Organization',
        'full_name': 'Full Name',
        'organization_name': 'Organization Name',
        'phone': 'Phone Number',
        'address': 'Address',
        'registration_type': 'Registration Type',
        'home': 'Home',
        'explore': 'Explore',
        'search': 'Search',
        'profile': 'Profile',
        'logout': 'Logout',
        'welcome': 'Welcome to HAVEN',
        'platform_description': 'Your trusted crowdfunding platform for meaningful projects',
        'trending_campaigns': 'Trending Campaigns',
        'categories': 'Categories',
        'technology': 'Technology',
        'health': 'Health',
        'education': 'Education',
        'environment': 'Environment',
        'arts': 'Arts & Culture',
        'community': 'Community',
        'search_campaigns': 'Search Campaigns',
        'search_placeholder': 'Enter keywords to search for campaigns...',
        'search_tips': 'Search Tips',
        'use_keywords': 'Use specific keywords related to the campaign',
        'filter_category': 'Filter by category for better results',
        'check_spelling': 'Check spelling and try different terms'
    },
    'Hindi': {
        'title': 'हेवन',
        'subtitle': 'क्राउडफंडिंग प्लेटफॉर्म',
        'login': 'लॉगिन',
        'register': 'रजिस्टर',
        'email': 'ईमेल',
        'password': 'पासवर्ड',
        'confirm_password': 'पासवर्ड की पुष्टि करें',
        'continue': 'जारी रखें',
        'not_registered': 'पंजीकृत नहीं हैं?',
        'create_account': 'खाता बनाएं',
        'already_have_account': 'पहले से खाता है?',
        'sign_in_here': 'यहाँ साइन इन करें',
        'sign_in_google': 'Google से साइन इन करें',
        'sign_in_facebook': 'Facebook से साइन इन करें',
        'individual': 'व्यक्तिगत',
        'organization': 'संगठन',
        'full_name': 'पूरा नाम',
        'organization_name': 'संगठन का नाम',
        'phone': 'फोन नंबर',
        'address': 'पता',
        'registration_type': 'पंजीकरण प्रकार',
        'home': 'होम',
        'explore': 'एक्सप्लोर',
        'search': 'खोजें',
        'profile': 'प्रोफाइल',
        'logout': 'लॉगआउट',
        'welcome': 'हेवन में आपका स्वागत है',
        'platform_description': 'सार्थक परियोजनाओं के लिए आपका विश्वसनीय क्राउडफंडिंग प्लेटफॉर्म',
        'trending_campaigns': 'ट्रेंडिंग कैंपेन',
        'categories': 'श्रेणियां',
        'technology': 'तकनीक',
        'health': 'स्वास्थ्य',
        'education': 'शिक्षा',
        'environment': 'पर्यावरण',
        'arts': 'कला और संस्कृति',
        'community': 'समुदाय',
        'search_campaigns': 'कैंपेन खोजें',
        'search_placeholder': 'कैंपेन खोजने के लिए कीवर्ड दर्ज करें...',
        'search_tips': 'खोज सुझाव',
        'use_keywords': 'कैंपेन से संबंधित विशिष्ट कीवर्ड का उपयोग करें',
        'filter_category': 'बेहतर परिणामों के लिए श्रेणी के अनुसार फ़िल्टर करें',
        'check_spelling': 'वर्तनी जांचें और विभिन्न शब्दों का प्रयास करें'
    },
    'Tamil': {
        'title': 'ஹேவன்',
        'subtitle': 'க்ரவுட்ஃபண்டிங் தளம்',
        'login': 'உள்நுழைவு',
        'register': 'பதிவு',
        'email': 'மின்னஞ்சல்',
        'password': 'கடவுச்சொல்',
        'confirm_password': 'கடவுச்சொல்லை உறுதிப்படுத்தவும்',
        'continue': 'தொடரவும்',
        'not_registered': 'பதிவு செய்யவில்லையா?',
        'create_account': 'கணக்கை உருவாக்கவும்',
        'already_have_account': 'ஏற்கனவே கணக்கு உள்ளதா?',
        'sign_in_here': 'இங்கே உள்நுழையவும்',
        'sign_in_google': 'Google உடன் உள்நுழையவும்',
        'sign_in_facebook': 'Facebook உடன் உள்நுழையவும்',
        'individual': 'தனிநபர்',
        'organization': 'அமைப்பு',
        'full_name': 'முழு பெயர்',
        'organization_name': 'அமைப்பின் பெயர்',
        'phone': 'தொலைபேசி எண்',
        'address': 'முகவரி',
        'registration_type': 'பதிவு வகை',
        'home': 'முகப்பு',
        'explore': 'ஆராயவும்',
        'search': 'தேடவும்',
        'profile': 'சுயவிவரம்',
        'logout': 'வெளியேறவும்',
        'welcome': 'ஹேவனுக்கு வரவேற்கிறோம்',
        'platform_description': 'அர்த்தமுள்ள திட்டங்களுக்கான உங்கள் நம்பகமான க்ரவுட்ஃபண்டிங் தளம்',
        'trending_campaigns': 'டிரெண்டிங் பிரச்சாரங்கள்',
        'categories': 'வகைகள்',
        'technology': 'தொழில்நுட்பம்',
        'health': 'சுகாதாரம்',
        'education': 'கல்வி',
        'environment': 'சுற்றுச்சூழல்',
        'arts': 'கலை மற்றும் கலாச்சாரம்',
        'community': 'சமூகம்',
        'search_campaigns': 'பிரச்சாரங்களைத் தேடவும்',
        'search_placeholder': 'பிரச்சாரங்களைத் தேட முக்கிய வார்த்தைகளை உள்ளிடவும்...',
        'search_tips': 'தேடல் குறிப்புகள்',
        'use_keywords': 'பிரச்சாரத்துடன் தொடர்புடைய குறிப்பிட்ட முக்கிய வார்த்தைகளைப் பயன்படுத்தவும்',
        'filter_category': 'சிறந்த முடிவுகளுக்கு வகை வாரியாக வடிகட்டவும்',
        'check_spelling': 'எழுத்துப்பிழையைச் சரிபார்த்து வெவ்வேறு சொற்களை முயற்சிக்கவும்'
    },
    'Telugu': {
        'title': 'హేవెన్',
        'subtitle': 'క్రౌడ్‌ఫండింగ్ ప్లాట్‌ఫారమ్',
        'login': 'లాగిన్',
        'register': 'రిజిస్టర్',
        'email': 'ఇమెయిల్',
        'password': 'పాస్‌వర్డ్',
        'confirm_password': 'పాస్‌వర్డ్‌ను నిర్ధారించండి',
        'continue': 'కొనసాగించు',
        'not_registered': 'రిజిస్టర్ కాలేదా?',
        'create_account': 'ఖాతా సృష్టించండి',
        'already_have_account': 'ఇప్పటికే ఖాతా ఉందా?',
        'sign_in_here': 'ఇక్కడ సైన్ ఇన్ చేయండి',
        'sign_in_google': 'Google తో సైన్ ఇన్ చేయండి',
        'sign_in_facebook': 'Facebook తో సైన్ ఇన్ చేయండి',
        'individual': 'వ్యక్తిగత',
        'organization': 'సంస్థ',
        'full_name': 'పూర్తి పేరు',
        'organization_name': 'సంస్థ పేరు',
        'phone': 'ఫోన్ నంబర్',
        'address': 'చిరునామా',
        'registration_type': 'రిజిస్ట్రేషన్ రకం',
        'home': 'హోమ్',
        'explore': 'అన్వేషించు',
        'search': 'వెతకండి',
        'profile': 'ప్రొఫైల్',
        'logout': 'లాగ్అవుట్',
        'welcome': 'హేవెన్‌కు స్వాగతం',
        'platform_description': 'అర్థవంతమైన ప్రాజెక్టుల కోసం మీ విశ్వసనీయ క్రౌడ్‌ఫండింగ్ ప్లాట్‌ఫారమ్',
        'trending_campaigns': 'ట్రెండింగ్ క్యాంపెయిన్‌లు',
        'categories': 'వర్గాలు',
        'technology': 'సాంకేతికత',
        'health': 'ఆరోగ్యం',
        'education': 'విద్య',
        'environment': 'పర్యావరణం',
        'arts': 'కళలు మరియు సంస్కృతి',
        'community': 'సమాజం',
        'search_campaigns': 'క్యాంపెయిన్‌లను వెతకండి',
        'search_placeholder': 'క్యాంపెయిన్‌లను వెతకడానికి కీవర్డ్‌లను నమోదు చేయండి...',
        'search_tips': 'వెతుకులాట చిట్కాలు',
        'use_keywords': 'క్యాంపెయిన్‌కు సంబంధించిన నిర్దిష్ట కీవర్డ్‌లను ఉపయోగించండి',
        'filter_category': 'మెరుగైన ఫలితాల కోసం వర్గం వారీగా ఫిల్టర్ చేయండి',
        'check_spelling': 'స్పెల్లింగ్ తనిఖీ చేసి వేర్వేరు పదాలను ప్రయత్నించండి'
    }
}

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'user_token' not in st.session_state:
    st.session_state.user_token = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def get_text(key):
    """Get translated text for the current language"""
    return TRANSLATIONS[st.session_state.language].get(key, key)

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    
    /* Global Styles */
    .stApp {
        background-color: #f0f2e6;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container Styles */
    .main-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem auto;
        max-width: 500px;
    }
    
    /* Title Styles */
    .app-title {
        background: linear-gradient(135deg, #ed4599 0%, #ff0080 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .app-subtitle {
        color: #666;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* OAuth Button Styles */
    .oauth-button {
        display: block;
        width: 100%;
        padding: 12px 20px;
        margin: 10px 0;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
        text-decoration: none;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
        color: white !important;
    }
    
    .oauth-google {
        background: linear-gradient(135deg, #db4437 0%, #cc3333 100%);
    }
    
    .oauth-facebook {
        background: linear-gradient(135deg, #4267B2 0%, #365899 100%);
    }
    
    .oauth-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        text-decoration: none;
        color: white !important;
    }
    
    /* Form Styles */
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        font-family: 'Poppins', sans-serif;
        color: #333;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ed4599;
        box-shadow: 0 0 0 3px rgba(237, 69, 153, 0.1);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #ed4599 0%, #ff0080 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 500;
        width: 100%;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(237, 69, 153, 0.3);
        background: linear-gradient(135deg, #ff0080 0%, #ed4599 100%);
    }
    
    /* Navigation Link Styles */
    .nav-link {
        color: #ed4599 !important;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .nav-link:hover {
        color: #ff0080 !important;
        text-decoration: underline;
    }
    
    /* Category Card Styles */
    .category-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
        margin: 1rem 0;
        border: 2px solid transparent;
    }
    
    .category-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        border-color: #ed4599;
    }
    
    .category-icon {
        font-size: 2.5rem;
        color: #ed4599;
        margin-bottom: 1rem;
    }
    
    .category-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    /* Campaign Card Styles */
    .campaign-card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        overflow: hidden;
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .campaign-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .campaign-image {
        width: 100%;
        height: 200px;
        background: linear-gradient(135deg, #ed4599 0%, #ff0080 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .campaign-content {
        padding: 1.5rem;
    }
    
    .campaign-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .campaign-description {
        color: #666;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    
    .campaign-progress {
        background: #f0f2e6;
        border-radius: 10px;
        height: 8px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .campaign-progress-bar {
        background: linear-gradient(135deg, #ed4599 0%, #ff0080 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* User Profile Widget */
    .user-profile {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .user-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ed4599 0%, #ff0080 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 0 auto 0.5rem;
    }
    
    .user-name {
        text-align: center;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .user-email {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Search Styles */
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .search-tips {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 4px solid #ed4599;
    }
    
    .search-tips h4 {
        color: #ed4599;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .search-tips ul {
        color: #666;
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .search-tips li {
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-container {
            margin: 0.5rem;
            padding: 1.5rem;
        }
        
        .app-title {
            font-size: 2.5rem;
        }
        
        .oauth-button {
            font-size: 14px;
            padding: 10px 16px;
        }
    }
    
    /* Text Color Fixes */
    .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: #333 !important;
    }
    
    .stSelectbox label, .stTextInput label {
        color: #333 !important;
        font-weight: 500;
    }
    
    /* Dark button text should be white */
    .stButton > button {
        color: white !important;
    }
    
    /* Light background text should be dark */
    .main-container * {
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

def check_backend_connection():
    """Check if backend is accessible"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def safe_json_parse(response):
    """Safely parse JSON response with fallback"""
    try:
        return response.json()
    except:
        return {"detail": f"Server error (Status: {response.status_code})"}

def handle_oauth_callback():
    """Handle OAuth callback from URL parameters"""
    try:
        query_params = st.query_params
        
        # Check for access token
        access_token = query_params.get('access_token')
        if access_token:
            st.session_state.user_token = access_token
            
            # Get user info
            user_info = query_params.get('user_info')
            if user_info:
                try:
                    import json
                    st.session_state.user_info = json.loads(user_info)
                except:
                    st.session_state.user_info = {"name": "OAuth User", "email": "user@oauth.com"}
            
            st.session_state.current_page = 'home'
            st.success("Successfully logged in with OAuth!")
            st.rerun()
            
        # Check for error
        error = query_params.get('error')
        if error:
            st.error(f"OAuth login failed: {error}")
            
    except Exception as e:
        st.error(f"Error handling OAuth callback: {str(e)}")

def render_oauth_buttons():
    """Render OAuth login buttons"""
    st.markdown("### " + get_text('sign_in_google'))
    
    # Check OAuth provider status
    try:
        response = requests.get(f"{BACKEND_URL}/auth/status", timeout=5)
        if response.status_code == 200:
            status = safe_json_parse(response)
            google_available = status.get('google_oauth', {}).get('available', False)
            facebook_available = status.get('facebook_oauth', {}).get('available', False)
        else:
            google_available = False
            facebook_available = False
    except:
        google_available = False
        facebook_available = False
    
    # Google OAuth Button
    if google_available:
        google_url = f"{BACKEND_URL}/auth/google"
        st.markdown(f"""
        <a href="{google_url}" class="oauth-button oauth-google">
            <i class="fab fa-google"></i> {get_text('sign_in_google')}
        </a>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="oauth-button" style="background: #ccc; color: #666; cursor: not-allowed;">
            <i class="fab fa-google"></i> {get_text('sign_in_google')} (Not Available)
        </div>
        """, unsafe_allow_html=True)
    
    # Facebook OAuth Button
    if facebook_available:
        facebook_url = f"{BACKEND_URL}/auth/facebook"
        st.markdown(f"""
        <a href="{facebook_url}" class="oauth-button oauth-facebook">
            <i class="fab fa-facebook-f"></i> {get_text('sign_in_facebook')}
        </a>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="oauth-button" style="background: #ccc; color: #666; cursor: not-allowed;">
            <i class="fab fa-facebook-f"></i> {get_text('sign_in_facebook')} (Not Available)
        </div>
        """, unsafe_allow_html=True)

def login_user_backend(email, password):
    """Login user via backend API"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/login",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = safe_json_parse(response)
            st.session_state.user_token = data.get('access_token')
            st.session_state.user_info = data.get('user_info', {})
            st.session_state.current_page = 'home'
            st.success("Login successful!")
            st.rerun()
        else:
            error_data = safe_json_parse(response)
            st.error(f"Login failed: {error_data.get('detail', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
    except Exception as e:
        st.error(f"Login error: {str(e)}")

def register_user_backend(user_data):
    """Register user via backend API"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/register",
            json=user_data,
            timeout=10
        )
        
        if response.status_code == 200:
            st.success("Registration successful! Please login with your credentials.")
            st.session_state.current_page = 'login'
            st.rerun()
        else:
            # Safe error handling for non-JSON responses
            try:
                error_data = response.json()
                error_message = error_data.get('detail', 'Unknown error')
            except:
                error_message = f"Registration failed (Status: {response.status_code})"
            
            st.error(f"Registration failed: {error_message}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
    except Exception as e:
        st.error(f"Registration error: {str(e)}")

def render_user_profile():
    """Render user profile widget"""
    if st.session_state.user_info:
        user_info = st.session_state.user_info
        name = user_info.get('name', 'User')
        email = user_info.get('email', 'user@example.com')
        
        st.markdown(f"""
        <div class="user-profile">
            <div class="user-avatar">{name[0].upper()}</div>
            <div class="user-name">{name}</div>
            <div class="user-email">{email}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(get_text('logout')):
            st.session_state.user_token = None
            st.session_state.user_info = None
            st.session_state.current_page = 'login'
            st.rerun()

def render_login_page():
    """Render the login page"""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown(f'<h1 class="app-title">{get_text("title")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="app-subtitle">{get_text("subtitle")}</p>', unsafe_allow_html=True)
    
    # OAuth buttons (outside form)
    render_oauth_buttons()
    
    # Login form
    with st.form(key='login_form'):
        st.markdown(f"### {get_text('login')}")
        
        email = st.text_input(get_text('email'), placeholder="Enter your email")
        password = st.text_input(get_text('password'), type="password", placeholder="Enter your password")
        
        submit_button = st.form_submit_button(get_text('continue'))
        
        if submit_button:
            if email and password:
                login_user_backend(email, password)
            else:
                st.error("Please fill in all fields")
    
    # Registration link (this is the red circled link that should work)
    st.markdown(f"""
    <div style="text-align: center; margin-top: 1rem;">
        <span style="color: #666;">{get_text('not_registered')} </span>
        <a href="#" class="nav-link" onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'register'}}, '*')">{get_text('create_account')}</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Handle the registration navigation
    if st.button("", key="hidden_register_button", help="Navigate to registration"):
        st.session_state.current_page = 'register'
        st.rerun()
    
    # JavaScript to handle the link click
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const links = document.querySelectorAll('.nav-link');
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                // Trigger the hidden button click
                const hiddenButton = window.parent.document.querySelector('[data-testid="baseButton-secondary"]');
                if (hiddenButton) {
                    hiddenButton.click();
                }
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_register_page():
    """Render the registration page"""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown(f'<h1 class="app-title">{get_text("title")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="app-subtitle">{get_text("subtitle")}</p>', unsafe_allow_html=True)
    
    # Registration form
    with st.form(key='register_form'):
        st.markdown(f"### {get_text('register')}")
        
        # Registration type
        registration_type = st.selectbox(
            get_text('registration_type'),
            [get_text('individual'), get_text('organization')]
        )
        
        # Common fields
        email = st.text_input(get_text('email'), placeholder="Enter your email")
        password = st.text_input(get_text('password'), type="password", placeholder="Enter your password")
        confirm_password = st.text_input(get_text('confirm_password'), type="password", placeholder="Confirm your password")
        
        # Type-specific fields
        if registration_type == get_text('individual'):
            full_name = st.text_input(get_text('full_name'), placeholder="Enter your full name")
            phone = st.text_input(get_text('phone'), placeholder="Enter your phone number")
            address = st.text_area(get_text('address'), placeholder="Enter your address")
            
            user_data = {
                "email": email,
                "password": password,
                "user_type": "individual",
                "full_name": full_name,
                "phone": phone,
                "address": address
            }
        else:
            organization_name = st.text_input(get_text('organization_name'), placeholder="Enter organization name")
            phone = st.text_input(get_text('phone'), placeholder="Enter organization phone")
            address = st.text_area(get_text('address'), placeholder="Enter organization address")
            
            user_data = {
                "email": email,
                "password": password,
                "user_type": "organization",
                "organization_name": organization_name,
                "phone": phone,
                "address": address
            }
        
        submit_button = st.form_submit_button(get_text('register'))
        
        if submit_button:
            if password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            elif email and password:
                register_user_backend(user_data)
            else:
                st.error("Please fill in all required fields")
    
    # Back to login link
    st.markdown(f"""
    <div style="text-align: center; margin-top: 1rem;">
        <span style="color: #666;">{get_text('already_have_account')} </span>
        <a href="#" class="nav-link" onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'login'}}, '*')">{get_text('sign_in_here')}</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Handle the login navigation
    if st.button("", key="hidden_login_button", help="Navigate to login"):
        st.session_state.current_page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_home_page():
    """Render the home page"""
    st.markdown(f'<h1 class="app-title">{get_text("welcome")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="app-subtitle">{get_text("platform_description")}</p>', unsafe_allow_html=True)
    
    # Trending campaigns
    st.markdown(f"## {get_text('trending_campaigns')}")
    
    # Sample campaigns
    campaigns = [
        {"title": "Clean Water Initiative", "description": "Providing clean water access to rural communities", "progress": 75, "raised": "$15,000", "goal": "$20,000"},
        {"title": "Education for All", "description": "Building schools in underserved areas", "progress": 60, "raised": "$30,000", "goal": "$50,000"},
        {"title": "Green Energy Project", "description": "Solar panel installation for villages", "progress": 40, "raised": "$8,000", "goal": "$20,000"}
    ]
    
    for campaign in campaigns:
        st.markdown(f"""
        <div class="campaign-card">
            <div class="campaign-image">{campaign['title']}</div>
            <div class="campaign-content">
                <div class="campaign-title">{campaign['title']}</div>
                <div class="campaign-description">{campaign['description']}</div>
                <div class="campaign-progress">
                    <div class="campaign-progress-bar" style="width: {campaign['progress']}%"></div>
                </div>
                <div style="display: flex; justify-content: space-between; color: #666;">
                    <span>Raised: {campaign['raised']}</span>
                    <span>Goal: {campaign['goal']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_explore_page():
    """Render the explore page"""
    st.markdown(f'<h1 class="app-title">{get_text("explore")}</h1>', unsafe_allow_html=True)
    st.markdown(f"## {get_text('categories')}")
    
    # Categories
    categories = [
        {"name": get_text('technology'), "icon": "fas fa-laptop-code"},
        {"name": get_text('health'), "icon": "fas fa-heartbeat"},
        {"name": get_text('education'), "icon": "fas fa-graduation-cap"},
        {"name": get_text('environment'), "icon": "fas fa-leaf"},
        {"name": get_text('arts'), "icon": "fas fa-palette"},
        {"name": get_text('community'), "icon": "fas fa-users"}
    ]
    
    # Display categories in a grid
    cols = st.columns(2)
    for i, category in enumerate(categories):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="category-card">
                <div class="category-icon">
                    <i class="{category['icon']}"></i>
                </div>
                <div class="category-title">{category['name']}</div>
            </div>
            """, unsafe_allow_html=True)

def render_search_page():
    """Render the search page"""
    st.markdown(f'<h1 class="app-title">{get_text("search_campaigns")}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Search input
    search_query = st.text_input(
        "",
        placeholder=get_text('search_placeholder'),
        key="search_input"
    )
    
    if st.button("🔍 Search", key="search_button"):
        if search_query:
            st.success(f"Searching for: {search_query}")
            # Here you would implement actual search functionality
        else:
            st.warning("Please enter a search term")
    
    # Search tips
    st.markdown(f"""
    <div class="search-tips">
        <h4><i class="fas fa-lightbulb"></i> {get_text('search_tips')}</h4>
        <ul>
            <li>{get_text('use_keywords')}</li>
            <li>{get_text('filter_category')}</li>
            <li>{get_text('check_spelling')}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with navigation and user info"""
    with st.sidebar:
        # Language selector
        st.markdown("### Select Language:")
        language = st.selectbox(
            "",
            options=list(TRANSLATIONS.keys()),
            index=list(TRANSLATIONS.keys()).index(st.session_state.language),
            key="language_selector"
        )
        
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### Navigation")
        
        # Backend connection test
        if st.button("Test Backend Connection"):
            if check_backend_connection():
                st.success("✅ Backend is connected!")
            else:
                st.error("❌ Backend connection failed!")
        
        # User authentication status
        if st.session_state.user_token:
            render_user_profile()
            
            st.markdown("---")
            
            # Navigation for authenticated users
            if st.button(get_text('home')):
                st.session_state.current_page = 'home'
                st.rerun()
            
            if st.button(get_text('explore')):
                st.session_state.current_page = 'explore'
                st.rerun()
            
            if st.button(get_text('search')):
                st.session_state.current_page = 'search'
                st.rerun()
        
        else:
            # Navigation for non-authenticated users
            if st.button("Login"):
                st.session_state.current_page = 'login'
                st.rerun()
            
            if st.button("Register"):
                st.session_state.current_page = 'register'
                st.rerun()

def main():
    """Main application function"""
    st.set_page_config(
        page_title="HAVEN - Crowdfunding Platform",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    apply_custom_css()
    
    # Handle OAuth callback
    handle_oauth_callback()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    if st.session_state.current_page == 'login':
        render_login_page()
    elif st.session_state.current_page == 'register':
        render_register_page()
    elif st.session_state.current_page == 'home':
        render_home_page()
    elif st.session_state.current_page == 'explore':
        render_explore_page()
    elif st.session_state.current_page == 'search':
        render_search_page()
    else:
        render_login_page()

if __name__ == "__main__":
    main()

