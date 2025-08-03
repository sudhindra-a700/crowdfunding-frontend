"""
HAVEN Crowdfunding Platform - Complete Streamlit Frontend
Updated for Render Python3 Runtime with Environment Variables
Enhanced with 4-language translation and term simplification
"""

import streamlit as st
import requests
import json
import asyncio
import time
import os
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="HAVEN Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# CONFIGURATION FROM ENVIRONMENT VARIABLES
# ========================================

# Backend Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")
FRONTEND_BASE_URI = os.getenv("FRONTEND_BASE_URI", "https://haven-streamlit-frontend.onrender.com")

# OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("OAUTH_GOOGLE_CLIENT_ID", os.getenv("GOOGLE_CLIENT_ID"))
GOOGLE_CLIENT_SECRET = os.getenv("OAUTH_GOOGLE_CLIENT_SECRET", os.getenv("GOOGLE_CLIENT_SECRET"))
FACEBOOK_APP_ID = os.getenv("OAUTH_FACEBOOK_APP_ID", os.getenv("FACEBOOK_CLIENT_ID"))
FACEBOOK_APP_SECRET = os.getenv("OAUTH_FACEBOOK_APP_SECRET", os.getenv("FACEBOOK_CLIENT_SECRET"))

# Feature Flags
TRANSLATION_ENABLED = os.getenv("FEATURES_TRANSLATION_ENABLED", "true").lower() == "true"
SIMPLIFICATION_ENABLED = os.getenv("FEATURES_SIMPLIFICATION_ENABLED", "true").lower() == "true"
OAUTH_ENABLED = os.getenv("FEATURES_OAUTH_ENABLED", "true").lower() == "true"
ANALYTICS_ENABLED = os.getenv("FEATURES_ANALYTICS_ENABLED", "true").lower() == "true"

# Session Configuration
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "default-secret-key")
SESSION_MAX_AGE = int(os.getenv("SESSION_MAX_AGE", "3600"))

# Performance Settings
CACHE_TTL = int(os.getenv("PERFORMANCE_CACHE_TTL", "3600"))
MAX_REQUESTS_PER_MINUTE = int(os.getenv("PERFORMANCE_MAX_REQUESTS_PER_MINUTE", "60"))
API_TIMEOUT = int(os.getenv("PERFORMANCE_API_TIMEOUT", "30"))

# Translation Settings
TRANSLATION_CACHE_TTL = int(os.getenv("TRANSLATION_CACHE_TTL", "3600"))
TRANSLATION_BATCH_SIZE = int(os.getenv("TRANSLATION_BATCH_SIZE", "8"))
TRANSLATION_MAX_LENGTH = int(os.getenv("TRANSLATION_MAX_TEXT_LENGTH", "5000"))
TRANSLATION_DEFAULT_LANGUAGE = os.getenv("TRANSLATION_DEFAULT_LANGUAGE", "en")

# Simplification Settings
SIMPLIFICATION_CACHE_TTL = int(os.getenv("SIMPLIFICATION_CACHE_TTL", "7200"))
SIMPLIFICATION_DEFAULT_LEVEL = os.getenv("SIMPLIFICATION_DEFAULT_LEVEL", "simple")

# Environment Detection
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ========================================
# TRANSLATIONS DICTIONARY
# ========================================

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
        'welcome_banner_text': 'HAVEN',
        'welcome_banner_tagline': 'Help not just some people, but Help Humanity.',
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
        'check_spelling': 'Check spelling and try different terms',
        'register_individual': 'Register as an Individual',
        'register_organization': 'Register as an Organization',
        'organization_type': 'Organization Type',
        'ngo': 'NGO',
        'startup': 'Startup',
        'charity': 'Charity'
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
        'welcome_banner_text': 'हेवन',
        'welcome_banner_tagline': 'सिर्फ कुछ लोगों की नहीं, बल्कि मानवता की मदद करें।',
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
        'check_spelling': 'वर्तनी जांचें और अलग शब्दों का प्रयास करें',
        'register_individual': 'व्यक्तिगत के रूप में पंजीकरण करें',
        'register_organization': 'संगठन के रूप में पंजीकरण करें',
        'organization_type': 'संगठन प्रकार',
        'ngo': 'एनजीओ',
        'startup': 'स्टार्टअप',
        'charity': 'चैरिटी'
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
        'not_registered': 'பதிவு செய்யப்படவில்லையா?',
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
        'welcome_banner_text': 'ஹேவன்',
        'welcome_banner_tagline': 'சில மக்களுக்கு மட்டுமல்ல, மனிதகுலத்திற்கு உதவுங்கள்.',
        'trending_campaigns': 'பிரபலமான பிரச்சாரங்கள்',
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
        'filter_category': 'சிறந்த முடிவுகளுக்கு வகை அடிப்படையில் வடிகட்டவும்',
        'check_spelling': 'எழுத்துப்பிழையைச் சரிபார்த்து வெவ்வேறு சொற்களை முயற்சிக்கவும்',
        'register_individual': 'தனிநபராக பதிவு செய்யவும்',
        'register_organization': 'அமைப்பாக பதிவு செய்யவும்',
        'organization_type': 'அமைப்பு வகை',
        'ngo': 'என்ஜிஓ',
        'startup': 'ஸ்டார்ட்அப்',
        'charity': 'தொண்டு'
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
        'not_registered': 'నమోదు కాలేదా?',
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
        'registration_type': 'నమోదు రకం',
        'home': 'హోమ్',
        'explore': 'అన్వేషించండి',
        'search': 'వెతకండి',
        'profile': 'ప్రొఫైల్',
        'logout': 'లాగ్అవుట్',
        'welcome_banner_text': 'హేవెన్',
        'welcome_banner_tagline': 'కేవలం కొంతమందికి కాకుండా, మానవత్వానికి సహాయం చేయండి.',
        'trending_campaigns': 'ట్రెండింగ్ ప్రచారాలు',
        'categories': 'వర్గాలు',
        'technology': 'సాంకేతికత',
        'health': 'ఆరోగ్యం',
        'education': 'విద్య',
        'environment': 'పర్యావరణం',
        'arts': 'కళలు మరియు సంస్కృతి',
        'community': 'సమాజం',
        'search_campaigns': 'ప్రచారాలను వెతకండి',
        'search_placeholder': 'ప్రచారాలను వెతకడానికి కీలక పదాలను నమోదు చేయండి...',
        'search_tips': 'వెతుకులాట చిట్కాలు',
        'use_keywords': 'ప్రచారానికి సంబంధించిన నిర్దిష్ట కీలక పదాలను ఉపయోగించండి',
        'filter_category': 'మెరుగైన ఫలితాల కోసం వర్గం ద్వారా ఫిల్టర్ చేయండి',
        'check_spelling': 'స్పెల్లింగ్ తనిఖీ చేసి వేరే పదాలను ప్రయత్నించండి',
        'register_individual': 'వ్యక్తిగతంగా నమోదు చేసుకోండి',
        'register_organization': 'సంస్థగా నమోదు చేసుకోండి',
        'organization_type': 'సంస్థ రకం',
        'ngo': 'ఎన్‌జిఓ',
        'startup': 'స్టార్టప్',
        'charity': 'దాతృత్వం'
    }
}

# Language configuration
SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "flag": "🇺🇸", "native": "English"},
    "hi": {"name": "Hindi", "flag": "🇮🇳", "native": "हिन्दी"},
    "ta": {"name": "Tamil", "flag": "🇮🇳", "native": "தமிழ்"},
    "te": {"name": "Telugu", "flag": "🇮🇳", "native": "తెలుగు"}
}

# ========================================
# CUSTOM CSS FOR LIGHT GREEN THEME
# ========================================

st.markdown("""
<style>
    /* Main theme colors */
    .main {
        background-color: #f1f8e9;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #e8f5e8;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #4caf50, #66bb6a);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Translation bar styling */
    .translation-bar {
        background-color: #c8e6c9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin-bottom: 1rem;
    }
    
    /* Feature card styling */
    .feature-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #4caf50;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #45a049;
    }
    
    /* Environment indicator */
    .env-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background-color: #4caf50;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 3px;
        font-size: 0.8rem;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# Environment indicator (for debugging)
if DEBUG_MODE:
    st.markdown(f"""
    <div class="env-indicator">
        ENV: {ENVIRONMENT} | DEBUG: {DEBUG_MODE}
    </div>
    """, unsafe_allow_html=True)

# ========================================
# SESSION STATE INITIALIZATION
# ========================================

if 'current_language' not in st.session_state:
    st.session_state.current_language = TRANSLATION_DEFAULT_LANGUAGE
if 'translation_enabled' not in st.session_state:
    st.session_state.translation_enabled = TRANSLATION_ENABLED
if 'simplification_enabled' not in st.session_state:
    st.session_state.simplification_enabled = SIMPLIFICATION_ENABLED
if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False

# ========================================
# UTILITY FUNCTIONS
# ========================================

def validate_configuration():
    """Validate that required environment variables are set"""
    required_vars = {
        "BACKEND_URL": BACKEND_URL,
        "OAUTH_GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
        "OAUTH_FACEBOOK_APP_ID": FACEBOOK_APP_ID,
        "SESSION_SECRET_KEY": SESSION_SECRET_KEY
    }
    
    missing_vars = []
    for var_name, var_value in required_vars.items():
        if not var_value or var_value == "your-actual-secret":
            missing_vars.append(var_name)
    
    if missing_vars:
        st.error(f"⚠️ Missing required environment variables: {', '.join(missing_vars)}")
        st.info("Please configure these variables in your Render environment group.")
        return False
    
    return True

def show_configuration():
    """Display current configuration (for debugging)"""
    if DEBUG_MODE:
        with st.expander("🔧 Configuration (Debug Mode)"):
            st.json({
                "backend_url": BACKEND_URL,
                "translation_enabled": TRANSLATION_ENABLED,
                "simplification_enabled": SIMPLIFICATION_ENABLED,
                "oauth_enabled": OAUTH_ENABLED,
                "environment": ENVIRONMENT,
                "cache_ttl": CACHE_TTL,
                "google_client_id": GOOGLE_CLIENT_ID[:20] + "..." if GOOGLE_CLIENT_ID else "Not set",
                "facebook_app_id": FACEBOOK_APP_ID[:10] + "..." if FACEBOOK_APP_ID else "Not set"
            })

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API request to backend"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=API_TIMEOUT)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=API_TIMEOUT)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        if DEBUG_MODE:
            st.error(f"API request failed: {str(e)}")
        return {"error": str(e)}
    except Exception as e:
        if DEBUG_MODE:
            st.error(f"Unexpected error: {str(e)}")
        return {"error": str(e)}

@st.cache_data(ttl=TRANSLATION_CACHE_TTL)
def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    """Translate text using backend API with caching"""
    if not text or source_language == target_language or not TRANSLATION_ENABLED:
        return text
    
    try:
        data = {
            "text": text[:TRANSLATION_MAX_LENGTH],
            "source_language": source_language,
            "target_language": target_language
        }
        
        result = make_api_request("/api/translate", "POST", data)
        
        if "error" not in result:
            return result.get("translated_text", text)
        else:
            return text
    
    except Exception:
        return text

@st.cache_data(ttl=SIMPLIFICATION_CACHE_TTL)
def simplify_text(text: str, level: str = None) -> str:
    """Simplify text using backend API with caching"""
    if not text or not SIMPLIFICATION_ENABLED:
        return text
    
    if level is None:
        level = SIMPLIFICATION_DEFAULT_LEVEL
    
    try:
        data = {
            "text": text,
            "target_level": level
        }
        
        result = make_api_request("/api/simplify", "POST", data)
        
        if "error" not in result:
            return result.get("simplified_text", text)
        else:
            return text
    
    except Exception:
        return text

def get_text(key: str, language: str = None) -> str:
    """Get translated text for the current language"""
    if language is None:
        language = st.session_state.current_language
    
    # Map language codes to translation keys
    lang_map = {
        "en": "English",
        "hi": "Hindi", 
        "ta": "Tamil",
        "te": "Telugu"
    }
    
    lang_key = lang_map.get(language, "English")
    
    if lang_key in TRANSLATIONS and key in TRANSLATIONS[lang_key]:
        return TRANSLATIONS[lang_key][key]
    else:
        # Fallback to English
        return TRANSLATIONS["English"].get(key, key)

def display_text_with_translation(text: str, key: str = None):
    """Display text with optional translation and simplification"""
    if not text:
        return
    
    # Apply translation if enabled
    if st.session_state.translation_enabled and st.session_state.current_language != "en":
        translated_text = translate_text(text, st.session_state.current_language, "en")
    else:
        translated_text = text
    
    # Apply simplification if enabled
    if st.session_state.simplification_enabled:
        simplified_text = simplify_text(translated_text)
    else:
        simplified_text = translated_text
    
    # Display the text
    st.markdown(simplified_text)

# ========================================
# UI COMPONENTS
# ========================================

def render_header():
    """Render main header with branding"""
    st.markdown(f"""
    <div class="main-header">
        <h1>🏠 {get_text('welcome_banner_text')}</h1>
        <p>{get_text('welcome_banner_tagline')}</p>
    </div>
    """, unsafe_allow_html=True)

def render_language_controls():
    """Render language and simplification controls"""
    if not (TRANSLATION_ENABLED or SIMPLIFICATION_ENABLED):
        return
    
    st.markdown("""
    <div class="translation-bar">
        <h4>🌍 Language & Accessibility Settings</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if TRANSLATION_ENABLED:
            # Language selector
            language_options = [
                f"{lang_info['flag']} {lang_info['native']}" 
                for lang_code, lang_info in SUPPORTED_LANGUAGES.items()
            ]
            
            selected_lang_display = st.selectbox(
                "Select Language",
                language_options,
                index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.current_language),
                key="language_selector"
            )
            
            # Extract language code from selection
            for lang_code, lang_info in SUPPORTED_LANGUAGES.items():
                if f"{lang_info['flag']} {lang_info['native']}" == selected_lang_display:
                    if st.session_state.current_language != lang_code:
                        st.session_state.current_language = lang_code
                        st.rerun()
                    break
    
    with col2:
        if TRANSLATION_ENABLED:
            # Translation toggle
            translation_enabled = st.checkbox(
                "🔄 Enable Translation",
                value=st.session_state.translation_enabled,
                help="Translate content to your selected language"
            )
            
            if translation_enabled != st.session_state.translation_enabled:
                st.session_state.translation_enabled = translation_enabled
                st.rerun()
    
    with col3:
        if SIMPLIFICATION_ENABLED:
            # Simplification toggle
            simplification_enabled = st.checkbox(
                "💡 Simplify Complex Terms",
                value=st.session_state.simplification_enabled,
                help="Make complex financial and technical terms easier to understand"
            )
            
            if simplification_enabled != st.session_state.simplification_enabled:
                st.session_state.simplification_enabled = simplification_enabled
                st.rerun()
    
    # Show current settings
    active_features = []
    if st.session_state.translation_enabled and TRANSLATION_ENABLED:
        lang_name = SUPPORTED_LANGUAGES[st.session_state.current_language]['native']
        active_features.append(f"Translating to {lang_name}")
    if st.session_state.simplification_enabled and SIMPLIFICATION_ENABLED:
        active_features.append("Simplifying complex terms")
    
    if active_features:
        st.info(f"Active: {' | '.join(active_features)}")

@st.cache_data(ttl=60)
def test_backend_connection():
    """Test backend connection and return status"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return {"status": "connected", "data": response.json()}
        else:
            return {"status": "error", "message": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def render_navigation():
    """Render main navigation sidebar"""
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        # Configuration validation
        config_valid = validate_configuration()
        
        if not config_valid:
            st.error("⚠️ Configuration incomplete")
        
        # Backend connection status
        connection_status = test_backend_connection()
        if connection_status["status"] == "connected":
            st.success("✅ Backend Connected")
            
            # Show feature status
            if "data" in connection_status:
                features = connection_status["data"].get("features", {})
                if features.get("translation"):
                    st.success("✅ Translation Available")
                if features.get("simplification"):
                    st.success("✅ Simplification Available")
        else:
            st.error(f"❌ Backend: {connection_status['message']}")
        
        # Main pages
        page = st.radio(
            "Choose a page:",
            [
                f"🏠 {get_text('home')}",
                f"🔍 {get_text('explore')} Campaigns", 
                "🚀 Create Campaign",
                f"👤 {get_text('profile')}",
                "🔐 Authentication",
                "🌍 Translation Hub" if TRANSLATION_ENABLED else None,
                "💡 Simplification Center" if SIMPLIFICATION_ENABLED else None,
                "📊 Analytics" if ANALYTICS_ENABLED else None
            ]
        )
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("## ⚡ Quick Actions")
        
        if TRANSLATION_ENABLED and st.button("🔄 Toggle Translation"):
            st.session_state.translation_enabled = not st.session_state.translation_enabled
            st.rerun()
        
        if SIMPLIFICATION_ENABLED and st.button("💡 Toggle Simplification"):
            st.session_state.simplification_enabled = not st.session_state.simplification_enabled
            st.rerun()
        
        # Configuration display
        show_configuration()
    
    return page

# ========================================
# PAGE FUNCTIONS
# ========================================

def render_home_page():
    """Render the home page"""
    st.markdown(f"# 🏠 {get_text('welcome_banner_text')}")
    
    display_text_with_translation(f"Welcome to {get_text('welcome_banner_text')} - {get_text('subtitle')}")
    display_text_with_translation(get_text('welcome_banner_tagline'))
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🌍 Multilingual Support</h3>
            <p>Access the platform in English, Hindi, Tamil, and Telugu</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>💡 Smart Simplification</h3>
            <p>Complex terms explained in simple language</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🔒 Secure Platform</h3>
            <p>Safe and transparent crowdfunding</p>
        </div>
        """, unsafe_allow_html=True)

def render_explore_page():
    """Render the explore campaigns page"""
    st.markdown(f"# 🔍 {get_text('explore')} Campaigns")
    
    display_text_with_translation("Discover amazing campaigns from creators around the world.")
    
    # Categories
    st.markdown(f"## {get_text('categories')}")
    
    categories = [
        ("🔬", get_text('technology')),
        ("🏥", get_text('health')),
        ("📚", get_text('education')),
        ("🌱", get_text('environment')),
        ("🎨", get_text('arts')),
        ("🤝", get_text('community'))
    ]
    
    cols = st.columns(3)
    for i, (icon, category) in enumerate(categories):
        with cols[i % 3]:
            if st.button(f"{icon} {category}", key=f"cat_{i}"):
                st.info(f"Showing {category} campaigns...")

def render_authentication_page():
    """Render the authentication page"""
    st.markdown("# 🔐 Authentication")
    
    if OAUTH_ENABLED and GOOGLE_CLIENT_ID and FACEBOOK_APP_ID:
        st.markdown("### OAuth Login")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"🔴 {get_text('sign_in_google')}", key="google_oauth"):
                google_auth_url = f"{BACKEND_URL}/auth/google"
                st.markdown(f"[Click here to sign in with Google]({google_auth_url})")
        
        with col2:
            if st.button(f"🔵 {get_text('sign_in_facebook')}", key="facebook_oauth"):
                facebook_auth_url = f"{BACKEND_URL}/auth/facebook"
                st.markdown(f"[Click here to sign in with Facebook]({facebook_auth_url})")
    else:
        st.warning("OAuth not configured. Please set up OAuth credentials in environment variables.")
    
    st.markdown("---")
    
    # Manual login form
    st.markdown(f"### {get_text('login')}")
    
    with st.form("login_form"):
        email = st.text_input(get_text('email'))
        password = st.text_input(get_text('password'), type="password")
        
        if st.form_submit_button(get_text('login')):
            if email and password:
                st.success(f"Login attempted for {email}")
            else:
                st.error("Please fill in all fields")

def render_translation_hub():
    """Render the translation hub page"""
    if not TRANSLATION_ENABLED:
        st.error("Translation feature is not enabled")
        return
    
    st.markdown("# 🌍 Translation Hub")
    
    st.markdown("### Translate Text")
    
    # Source text input
    source_text = st.text_area("Enter text to translate:", height=100)
    
    # Language selection
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox(
            "From Language:",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]['flag']} {SUPPORTED_LANGUAGES[x]['native']}"
        )
    
    with col2:
        target_lang = st.selectbox(
            "To Language:",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]['flag']} {SUPPORTED_LANGUAGES[x]['native']}"
        )
    
    if st.button("🔄 Translate") and source_text:
        if source_lang != target_lang:
            with st.spinner("Translating..."):
                translated = translate_text(source_text, target_lang, source_lang)
                st.success("Translation completed!")
                st.markdown("### Result:")
                st.write(translated)
        else:
            st.warning("Please select different source and target languages")

def render_simplification_center():
    """Render the simplification center page"""
    if not SIMPLIFICATION_ENABLED:
        st.error("Simplification feature is not enabled")
        return
    
    st.markdown("# 💡 Simplification Center")
    
    st.markdown("### Simplify Complex Text")
    
    # Text input
    complex_text = st.text_area("Enter complex text to simplify:", height=100)
    
    # Simplification level
    level = st.selectbox(
        "Simplification Level:",
        options=["very_simple", "simple", "moderate"],
        index=1
    )
    
    if st.button("💡 Simplify") and complex_text:
        with st.spinner("Simplifying..."):
            simplified = simplify_text(complex_text, level)
            st.success("Simplification completed!")
            st.markdown("### Result:")
            st.write(simplified)

# ========================================
# MAIN APPLICATION
# ========================================

def main():
    """Main application function"""
    # Validate configuration first
    if not validate_configuration():
        st.stop()
    
    # Render header
    render_header()
    
    # Render language controls
    render_language_controls()
    
    # Render navigation and get selected page
    selected_page = render_navigation()
    
    # Route to appropriate page
    if selected_page.startswith("🏠"):
        render_home_page()
    elif selected_page.startswith("🔍"):
        render_explore_page()
    elif selected_page.startswith("🚀"):
        st.markdown("# 🚀 Create Campaign")
        st.info("Campaign creation feature coming soon!")
    elif selected_page.startswith("👤"):
        st.markdown(f"# 👤 {get_text('profile')}")
        st.info("Profile management feature coming soon!")
    elif selected_page.startswith("🔐"):
        render_authentication_page()
    elif selected_page.startswith("🌍"):
        render_translation_hub()
    elif selected_page.startswith("💡"):
        render_simplification_center()
    elif selected_page.startswith("📊"):
        st.markdown("# 📊 Analytics")
        st.info("Analytics dashboard coming soon!")
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🏠 {get_text('welcome_banner_text')} {get_text('subtitle')} | Environment: {ENVIRONMENT}</p>
        <p>🌍 Supporting {len(SUPPORTED_LANGUAGES)} languages | 💡 AI-powered simplification | 🛡️ Secure & transparent</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# Export configuration for other modules
__all__ = [
    'BACKEND_URL', 'TRANSLATION_ENABLED', 'SIMPLIFICATION_ENABLED', 
    'OAUTH_ENABLED', 'make_api_request', 'translate_text', 'simplify_text'
]

