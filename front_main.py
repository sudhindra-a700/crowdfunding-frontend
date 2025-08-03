"""
HAVEN Crowdfunding Platform - Complete Streamlit Frontend
Enhanced with 4-language translation and term simplification
"""

import streamlit as st
import requests
import json
import asyncio
import time
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

<<<<<<< HEAD
# Get backend URL from environment or use default
BACKEND_URL = os.getenv("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "https://haven-streamlit-frontend.onrender.com")

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
        'welcome_banner_text': 'HAVEN',  # New key for the main banner title
        'welcome_banner_tagline': 'Help not just some people, but Help Humanity.',  # New key for the banner tagline
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
        'charity': 'Chariy',
        'description': 'Brief Description (max 100 chars)',
        'complete_profile_title': 'Complete Your Profile',
        'provide_details': 'Please provide the additional details to complete your registration.',
        'update_profile': 'Update Profile',
        'contact_person_details': 'Contact Person Details',
        'organization_details': 'Organization Details',
        'create_campaign': 'Create Campaign',
        'campaign_name': 'Campaign Name',
        'campaign_description_full': 'Campaign Description',
        'goal_amount': 'Goal Amount',
        'campaign_category': 'Campaign Category',
        'upload_image': 'Upload Campaign Image',
        'submit_campaign': 'Submit Campaign',
        'campaign_creation_success': 'Campaign created successfully!',
        'campaign_creation_failed': 'Campaign creation failed:',
        'only_org_can_create_campaign': 'Only organization accounts can create campaigns.'
    },
    'Hindi': {
        'title': 'हेवन',
        'subtitle': 'क्राउडफंडिंग प्लेटफॉर्म',
        'login': 'लॉगिन',
        'register': 'रजिस्टर',
        'email': 'ईमेल',
        'password': 'पासवर्ड की पुष्टि करें',
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
        'welcome_banner_text': 'हेवन',  # New key for the main banner title
        'welcome_banner_tagline': 'केवल कुछ लोगों की नहीं, बल्कि मानवता की मदद करें।',  # New key for the banner tagline
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
        'check_spelling': 'वर्तनी जांचें और विभिन्न शब्दों का प्रयास करें',
        'register_individual': 'व्यक्तिगत के रूप में पंजीकरण करें',
        'register_organization': 'संगठन के रूप में पंजीकरण करें',
        'organization_type': 'संगठन प्रकार',
        'ngo': 'एनजीओ',
        'startup': 'स्टार्टअप',
        'charity': 'चैरिटी',
        'description': 'संक्षिप्त विवरण (अधिकतम 100 अक्षर)',
        'complete_profile_title': 'अपनी प्रोफ़ाइल पूरी करें',
        'provide_details': 'अपनी प्रोफ़ाइल पूरी करने के लिए कृपया अतिरिक्त विवरण प्रदान करें।',
        'update_profile': 'प्रोफ़ाइल अपडेट करें',
        'contact_person_details': 'संपर्क व्यक्ति विवरण',
        'organization_details': 'संगठन विवरण',
        'create_campaign': 'अभियान बनाएं',
        'campaign_name': 'अभियान का नाम',
        'campaign_description_full': 'अभियान विवरण',
        'goal_amount': 'लक्ष्य राशि',
        'campaign_category': 'अभियान श्रेणी',
        'upload_image': 'अभियान छवि अपलोड करें',
        'submit_campaign': 'अभियान जमा करें',
        'campaign_creation_success': 'अभियान सफलतापूर्वक बनाया गया!',
        'campaign_creation_failed': 'अभियान निर्माण विफल रहा:',
        'only_org_can_create_campaign': 'केवल संगठन खाते ही अभियान बना सकते हैं।'
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
        'welcome_banner_text': 'ஹேவன்',  # New key for the main banner title
        'welcome_banner_tagline': 'சிலருக்கு மட்டுமல்ல, மனிதகுலத்திற்கு உதவுங்கள்.',  # New key for the banner tagline
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
        'check_spelling': 'எழுத்துப்பிழையைச் சரிபார்த்து வெவ்வேறு சொற்களை முயற்சிக்கவும்',
        'register_individual': 'தனிநபராக பதிவு செய்யவும்',
        'register_organization': 'அமைப்பாக பதிவு செய்யவும்',
        'organization_type': 'அமைப்பு வகை',
        'ngo': 'என்ஜிஓ',
        'startup': 'ஸ்டார்ட்அப்',
        'charity': 'தொண்டு',
        'description': 'சுருக்கமான விளக்கம் (அதிகபட்சம் 100 எழுத்துக்கள்)',
        'complete_profile_title': 'உங்கள் சுயவிவரத்தை பூர்த்தி செய்யவும்',
        'provide_details': 'உங்கள் பதிவை முடிக்க கூடுதல் விவரங்களை வழங்கவும்.',
        'update_profile': 'சுயவிவரத்தை புதுப்பிக்கவும்',
        'contact_person_details': 'தொடர்பு நபர் விவரங்கள்',
        'organization_details': 'அமைப்பு விவரங்கள்',
        'create_campaign': 'பிரச்சாரத்தை உருவாக்கு',
        'campaign_name': 'பிரச்சாரத்தின் பெயர்',
        'campaign_description_full': 'பிரச்சார விளக்கம்',
        'goal_amount': 'இலக்கு தொகை',
        'campaign_category': 'பிரச்சார வகை',
        'upload_image': 'பிரச்சாரப் படத்தை பதிவேற்று',
        'submit_campaign': 'பிரச்சாரத்தை சமர்ப்பி',
        'campaign_creation_success': 'பிரச்சாரம் வெற்றிகரமாக உருவாக்கப்பட்டது!',
        'campaign_creation_failed': 'பிரச்சார உருவாக்கம் தோல்வியடைந்தது:',
        'only_org_can_create_campaign': 'அமைப்பு கணக்குகள் மட்டுமே பிரச்சாரங்களை உருவாக்க முடியும்।'
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
        'welcome_banner_text': 'హేవెన్',  # New key for the main banner title
        'welcome_banner_tagline': 'కేవలం కొందరికి కాదు, మానవత్వానికి సహాయం చేయండి.',  # New key for the banner tagline
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
        'filter_category': 'బెటర్ ఫలితాల కోసం వర్గం వారీగా ఫిల్టర్ చేయండి',
        'check_spelling': 'స్పెల్లింగ్ తనిఖీ చేసి వేర్వేరు పదాలను ప్రయత్నించండి',
        'register_individual': 'వ్యక్తిగతంగా నమోదు చేసుకోండి',
        'register_organization': 'సంస్థగా నమోదు చేసుకోండి',
        'organization_type': 'సంస్థ రకం',
        'ngo': 'ఎన్‌జిఓ',
        'startup': 'స్టార్టప్',
        'charity': 'దాతృత్వం',
        'description': 'సంక్షిప్త వివరణ (గరిష్టంగా 100 అక్షరాలు)',
        'complete_profile_title': 'మీ ప్రొఫైల్‌ను పూర్తి చేయండి',
        'provide_details': 'మీ பதிவை முடிக்க கூடுதல் விவரங்களை வழங்கவும்.',
        'update_profile': 'ప్రొఫైల్‌ను అప్‌డేట్ చేయండి',
        'contact_person_details': 'సంప్రదింపు వ్యక్తి వివరాలు',
        'organization_details': 'సంస్థ వివరాలు',
        'create_campaign': 'అభియాన్ సృష్టించు',
        'campaign_name': 'అభియాన్ పేరు',
        'campaign_description_full': 'అభియాన్ వివరణ',
        'goal_amount': 'లక్ష్యం మొత్తం',
        'campaign_category': 'అభియాన్ వర్గం',
        'upload_image': 'అభియాన్ చిత్రాన్ని అప్‌లోడ్ చేయండి',
        'submit_campaign': 'అభియాన్ సమర్పించు',
        'campaign_creation_success': 'అభియాన్ విజయవంతంగా సృష్టించబడింది!',
        'campaign_creation_failed': 'అభియాన్ సృష్టి విఫలమైంది:',
        'only_org_can_create_campaign': 'సంస్థ ఖాతాలు మాత్రమే అభియాన్‌లను సృష్టించగలవు।'
    }
}

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'user_token' not in st.session_state:
    st.session_state.user_token = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
# Initialize selected_reg_type for immediate rendering control
if 'selected_reg_type_register' not in st.session_state:  # Changed key to be specific to register page
    st.session_state.selected_reg_type_register = TRANSLATIONS['English'][
        'individual']  # Default to English 'Individual'
if 'selected_reg_type_oauth' not in st.session_state:  # Added key for OAuth completion page
    st.session_state.selected_reg_type_oauth = TRANSLATIONS['English']['individual']  # Default for OAuth completion

# Firebase configuration (REPLACE WITH YOUR ACTUAL FIREBASE CONFIG)
# This should ideally come from environment variables for production
FIREBASE_CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
}


def get_text(key):
    return TRANSLATIONS[st.session_state.language].get(key, key)


def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap'); /* Added Great Vibes font */

    .stApp {
        background-color: #f0f2e6 !important;
        font-family: 'Poppins', sans-serif;
=======
# Configure Streamlit page
st.set_page_config(
    page_title="HAVEN Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
BACKEND_URL = st.secrets.get("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")
DEFAULT_LANGUAGE = "en"

# Language configuration
SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "flag": "🇺🇸", "native": "English"},
    "hi": {"name": "Hindi", "flag": "🇮🇳", "native": "हिन्दी"},
    "ta": {"name": "Tamil", "flag": "🇮🇳", "native": "தமிழ்"},
    "te": {"name": "Telugu", "flag": "🇮🇳", "native": "తెలుగు"}
}

# Custom CSS for light green theme
st.markdown("""
<style>
    /* Main theme colors */
    .main {
        background-color: #f1f8e9;
>>>>>>> fd0f666ea8655d0250a75c9378e7acbbdf0b5a9a
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #e8f5e8;
    }
<<<<<<< HEAD

    .html-container-wide {
        background: #fff;
        width: 100%;
        max-width: 900px;
        padding: 25px 30px;
        border-radius: 5px;
        box-shadow: 0 10px 10px rgba(0, 0, 0, 0.15);
        margin: 20px auto;
        color: #000;
    }

    .html-title {
        font-size: 30px;
        font-weight: 600;
        margin: 20px 0 10px 0;
        position: relative;
        color: #2d5a2d; /* Darker green for titles for contrast */
    }

    .html-title:before {
        content: "";
        position: absolute;
        height: 4px;
        width: 33px;
        left: 0;
        bottom: 3px;
        border-radius: 5px;
        background: linear-gradient(to right, #4CAF50 0%, #388E3C 100%);
    }

    .html-title-register {
        font-size: 30px;
        font-weight: 600;
        margin-bottom: 30px;
        position: relative;
        color: #2d5a2d; /* Darker green for titles for contrast */
    }

    .html-title-register::before {
        content: "";
        position: absolute;
        height: 4px;
        width: 33px;
        left: 0;
        bottom: -5px;
        border-radius: 5px;
        background: linear-gradient(to right, #4CAF50 0%, #388E3C 100%);
    }

    .html-input-box {
        width: 100%;
        height: 45px;
        margin-top: 20px;
        position: relative;
    }

    .html-input-box input, .html-input-box select {
        width: 100%;
        height: 100%;
        outline: none;
        font-size: 16px;
        border: none;
        background: transparent;
        color: #333 !important; /* Slightly darker input text for contrast */
        border-bottom: 2px solid #ccc;
        padding-left: 5px;
        font-family: 'Poppins', sans-serif;
    }

    .html-input-box input::placeholder {
        color: #777; /* Darker placeholder for contrast */
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background: #f8f8f8 !important; /* Added light background color */
        border: 1px solid #ddd !important; /* Added full border */
        border-radius: 5px !important; /* Rounded corners for input fields */
        padding: 10px !important; /* Increased padding */
        font-size: 16px !important;
        color: #333 !important;
        font-family: 'Poppins', sans-serif !important;
        height: 45px !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.06); /* Subtle inner shadow */
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #4CAF50 !important; /* Highlight border on focus */
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important; /* Subtle focus ring */
    }

    .stTextInput > div > div > input::placeholder {
        color: #777 !important; /* Darker placeholder for contrast */
    }

    .html-button {
        margin-top: 30px;
    }

    .html-submit-button {
        background: linear-gradient(to right, #4CAF50 0%, #388E3C 100%) !important;
        font-size: 17px !important;
        color: #fff !important;
        border-radius: 5px !important;
        cursor: pointer;
        padding: 10px 0 !important;
        transition: all 0.3s ease;
        border: none !important;
        width: 100% !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
    }

    .html-submit-button:hover {
        letter-spacing: 1px;
        background: linear-gradient(to left, #4CAF50 0%, #388E3C 100%) !important;
        color: #fff !important;
    }

    .stButton > button {
        background: linear-gradient(to right, #4CAF50 0%, #388E3C 100%) !important;
        font-size: 17px !important;
        color: #fff !important;
        border-radius: 5px !important;
        cursor: pointer;
        padding: 10px 0 !important;
        transition: all 0.3s ease;
        border: none !important;
        width: 100% !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
    }

    .stButton > button:hover {
        letter-spacing: 1px;
        background: linear-gradient(to left, #4CAF50 0%, #388E3C 100%) !important;
        color: #fff !important;
        transform: none !important;
        box-shadow: none !important;
    }

    .html-option {
        font-size: 14px;
        text-align: center;
        margin: 20px 0;
        color: #333; /* Darker text for contrast */
    }

    .html-option a {
        color: #4CAF50 !important;
        text-decoration: none;
        font-weight: 500;
        cursor: pointer;
    }

    .html-option a:hover {
        color: #388E3C !important;
        text_decoration: underline;
    }

    .html-oauth-google, .html-oauth-facebook {
        display: block;
        height: 45px;
        width: 100%;
        font-size: 15px;
        text-decoration: none;
        padding-left: 20px;
        line-height: 45px;
        color: #fff !important;
        border_radius: 5px;
        transition: all 0.3s ease;
        margin_bottom: 15px;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
    }

    .html-oauth-google {
        background: linear-gradient(to right, #db4437 0%, #e57373 100%);
    }

    .html-oauth-google:hover {
        background: linear-gradient(to left, #db4437 0%, #e57373 100%);
        color: #fff !important;
        text-decoration: none;
    }

    .html-oauth-facebook {
        background: linear-gradient(to right, #3b5998 0%, #476bb8 100%);
    }

    .html-oauth-facebook:hover {
        background: linear-gradient(to left, #3b5998 0%, #476bb8 100%);
        color: #fff !important;
        text-decoration: none;
    }

    .html-oauth-google i, .html-oauth-facebook i {
        padding-right: 12px;
        font-size: 20px;
    }

    .html-form-wrapper {
        display: flex;
        flex-direction: column;
        gap: 30px;
    }

    .html-form-box {
        background: #fafafa;
        padding: 20px;
        border-radius: 8px;
        flex: 1;
    }

    .html-form-box h3 {
        margin-bottom: 10px;
        font-size: 18px;
        font-weight: 600;
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
        color: #2d5a2d; /* Darker green for section titles */
    }

    .html-input-box-register {
        width: 100%;
        height: 45px;
        margin-top: 15px;
        position: relative;
    }

    @media (min-width: 768px) {
        .html-form-wrapper {
            flex-direction: row;
        }

        .html-form-box {
            width: 48%;
        }
    }

    @media (max-width: 480px) {
        .html-container {
            padding: 20px 15px;
        }

        .html-container-wide {
            padding: 20px 15px;
        }

        .html-title, .html-title-register {
            font-size: 24px;
        }

        .html-input-box, .html-input-box-register {
            height: 40px;
        }

        .html-input-box input, .html-input-box select,
        .html-input-box-register input, .html-input-box-register select {
            font-size: 14px;
        }

        .html-submit-button {
            font-size: 15px !important;
            padding: 8px 0 !important;
        }
    }

    .sidebar-section {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    .sidebar-title {
        color: #2d5a2d; /* Darker green for sidebar titles */
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }

    .sidebar-link {
        display: block;
        color: #333; /* Darker text for contrast */
        text-decoration: none;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f0f0f0;
        transition: color 0.3s ease;
        cursor: pointer;
    }

    .sidebar-link:hover {
        color: #4CAF50;
        text-decoration: none;
    }

    .sidebar-link:last-child {
        border-bottom: none;
    }

    .status-connected {
        color: #28a745;
        font-weight: 600;
    }

    .status-disconnected {
        color: #dc3545;
        font-weight: 600;
    }

    .user-profile {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box_shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    .user-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
        display: flex;
        align-items: center;
        justify-content: center;
=======
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #4caf50, #66bb6a);
        padding: 1rem;
        border-radius: 10px;
>>>>>>> fd0f666ea8655d0250a75c9378e7acbbdf0b5a9a
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
    
    /* Success message styling */
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    /* Term tooltip styling */
    .term-tooltip {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 4px;
        padding: 0.5rem;
        margin: 0.25rem 0;
        font-size: 0.9em;
    }
    
    /* Language selector styling */
    .language-selector {
        background-color: #e8f5e8;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_language' not in st.session_state:
    st.session_state.current_language = DEFAULT_LANGUAGE
if 'translation_enabled' not in st.session_state:
    st.session_state.translation_enabled = False
if 'simplification_enabled' not in st.session_state:
    st.session_state.simplification_enabled = False
if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False

# Utility functions
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
        st.error(f"API request failed: {str(e)}")
        return {"error": str(e)}
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return {"error": str(e)}

def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    """Translate text using backend API"""
    if not text or source_language == target_language:
        return text
    
    try:
        data = {
            "text": text,
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

def simplify_text(text: str, level: str = "simple") -> str:
    """Simplify text using backend API"""
    if not text:
        return text
    
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

def get_term_definition(term: str) -> Optional[str]:
    """Get simple definition for a term"""
    try:
        result = make_api_request(f"/api/simplify/define/{term}")
        
        if "error" not in result:
            return result.get("simple_definition")
        else:
            return None
    
    except Exception:
        return None

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

# Header component
def render_header():
    """Render main header with branding"""
    st.markdown("""
    <div class="main-header">
        <h1>🏠 HAVEN Crowdfunding Platform</h1>
        <p>Empowering Innovation Through Community Funding</p>
    </div>
    """, unsafe_allow_html=True)

<<<<<<< HEAD
    # Firebase SDK scripts
    st.markdown(f"""
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-auth-compat.js"></script>
    <script>
        // Initialize Firebase
        const firebaseConfig = {json.dumps(FIREBASE_CONFIG)};
        if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
    }
        const auth = firebase.auth();

        // Function to sign in with email/password
        window.signInWithEmailPassword = async (email, password) => {
    try {
    const userCredential = await auth.signInWithEmailAndPassword(email, password);
    const idToken = await userCredential.user.getIdToken();
    // Send idToken to Streamlit via postMessage
    window.parent.postMessage({{
    streamlit: {{
        type: 'SET_PAGE_STATE',
        payload: {{
            id_token: idToken,
            action: 'login'
        }}
    }}
    }}, '*');
    } catch (error) {
        wi
    dow.parent.postMessage({{
            streamlit: {{
                type: 'SET_PAGE_STATE',
                payload: {{
                    error: error.message,
                    action: 'login_error'
                }}
            }}
        }}, '*');
    }
    };

    // Function to register
    with email/p
    ssword window.createUserWithEmailPassword = async (email, password) => {
    try { const userCredential = await auth.createUserWithEmailAndPassword(email, password);
    const idToken = await userCredential.user.getIdToken();
    // Send idToken to Streamlit via postMessage
    window.parent.postMessage({{
    streamlit: {{
        type: 'SET_PAGE_STATE',
        payload: {{
            id_token: idToken,
            action: 'register'
        }}
    }}
    }}, '*');
    } catch (error) {
        windw.parent
    .postMessage({{
            streamlit: {{
                type: 'SET_PAGE_STATE',
                payload: {{
                    error: error.message,
                    action: 'register_error'
                }}
            }}
        }}, '*');
    }
    };

    // Function to sign out
    window
    .
    sign
    utFirebase = async () => {
    try {
    aw ait auth.signOut();
    window.parent.postMessage({{
    streamlit: {{
        type: 'SET_PAGE_STATE',
        payload: {{
            action: 'logout_success'
        }}
    }}
    }}, '*');
    } catch (error) {
        wndow.pa
    ent.postMessage({{
            streamlit: {{
                type: 'SET_PAGE_STATE',
                payload: {{
                    error: error.message,
                    action: 'logout_error'
                }}
            }}
        }}, '*');
    }
    };
    </script>
      """,  u nsafe_ a
        ml=True)
  
  
  def check_backend_connection():
      try:
          endpoints = ['/health', '/docs', '/']
  
          for endpoint in endpoints:
              try:
                  response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=10)
                  if response.status_code in [200, 404]:
                      return True, "Connected"
              except:
                  continue
  
          return False, "All endpoints failed"
  
      except Exception as e:
          return False, f"Connection error: {str(e)}")
  
  def safe_json_parse(response):
      try:
          return response.json()
      except:
          return {"detail": f"Server error (Status: {response.status_code})"}
  
  def handle_oauth_callback():
      try:
          query_params = st.query_params
  
          access_token = query_params.get('access_token')
          user_info_str = query_params.get('user_info')
  
          if access_token and user_info_str:
              st.session_state.user_token = access_token
              try:
                  user_info = json.loads(user_info_str)
                  st.session_state.user_info = user_info
              except json.JSONDecodeError:
                  st.session_state.user_info = {"name": "OAuth User", "email": "user@oauth.com", "user_type": "individual"}
  
              # Check if it's a new registration needing profile completion
              if st.session_state.user_info.get('user_type') == 'individual' and \
                 not st.session_state.user_info.get('phone') and \
                 not st.session_state.user_info.get('address'):
                  st.session_state.current_page = 'complete_oauth_profile'
                  st.success("Please complete your profile details.")
              elif st.session_state.user_info.get('user_type') == 'organization' and \
                   not st.session_state.user_info.get('organization_name'):
                  st.session_state.current_page = 'complete_oauth_profile'
                  st.success("Please complete your organization profile details.")
              else:
                  st.session_state.current_page = 'home'
                  st.success("Successfully logged in with OAuth!")
              st.rerun()
  
          error = query_params.get('error')
          if error:
              st.error(f"OAuth login failed: {error}")
  
      except Exception as e:
          st.error(f"Error handling OAuth callback: {str(e)}")
  
  def render_oauth_buttons(is_register_page=False):
      try:
          response = requests.get(f"{BACKEND_URL}/auth/status", timeout=10)
          if response.status_code == 200:
              status = safe_json_parse(response)
              google_available = status.get('google_available', False)
              facebook_available = status.get('facebook_available', False)
          else:
              google_available = False
              facebook_available = False
      except:
          google_available = False
          facebook_available = False
  
      google_params = {"register_oauth": "true"} if is_register_page else {}
      facebook_params = {"register_oauth": "true"} if is_register_page else {}
  
      google_url = f"{BACKEND_URL}/auth/google?{urlencode(google_params)}"
      facebook_url = f"{BACKEND_URL}/auth/facebook?{urlencode(facebook_params)}"
  
      if google_available:
          st.markdown(f"""
      <a href="{goo \
        } "
    clas s ="html-oauth-g

    ogle" >
<i class="fab fa-g o

g l


"></i >{get_text('sign _ i n _ g oogle')}
</a>
""", unsafe_al

o w _ html=True)
    else:
        st.markdown(f"""
<div class="html-oaut h-g


ogle" style="background: #ccc; color: #666; cursor: not-allowed;">
<i class="fab fa-g o

g l


"></i >{get_text('sign _ i n _ g oogle')}
</div>
""", unsafe_

l l ow_ html=True)

    if facebook_available:
        st.markdown(f"""
<a href="{facebook_ur l
" cl a ss="html-oauth-f


ceboo k">
<i class="fab fa-f a

e b


ok-f" ></i>{get_text('sign _ i n _ f acebook')}
</a>
""", unsafe_al

o w _ html=True)
    else:
        st.markdown(f"""
<div class="html-oaut h-f


ceboo k" style="background: #ccc; color: #666; cursor: not-allowed;">
<i class="fab fa-f a

e b


ok-f" ></i>{get_text('sign _ i n _ f acebook')}
</div>
""", unsafe_

l l ow_ html=True)

def login_user_backend(id_token):
    try:
        response = requests.post(
            f"{BACKEND_URL}/login",
            json={"id_token": id_token},
            timeout=15
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

def register_user_backend(id_token, user_type, individual_data=None, organization_data=None):
    try:
        payload = {
            "id_token": id_token,
            "user_type": user_type
        }
        if individual_data:
            payload["individual_data"] = individual_data
        if organization_data:
            payload["organization_data"] = organization_data

        response = requests.post(
            f"{BACKEND_URL}/register",
            json=payload,
            timeout=15
        )

        if response.status_code == 200:
            data = safe_json_parse(response)
            st.session_state.user_token = data.get('access_token')
            st.session_state.user_info = data.get('user_info', {})
            st.session_state.current_page = 'home' # Go to home after registration
            st.success("Registration successful! You are now logged in.")
            st.rerun()
        else:
            error_data = safe_json_parse(response)
            st.error(f"Registration failed: {error_data.get('detail', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
    except Exception as e:
        st.error(f"Registration error: {str(e)}")

def update_user_profile_backend(user_data, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{BACKEND_URL}/update_profile",
            json=user_data,
            headers=headers,
            timeout=15
        )

        if response.status_code == 200:
            updated_user_info = safe_json_parse(response)
            st.session_state.user_info = updated_user_info # Update with fresh data from backend
            st.success("Profile updated successfully!")
            st.session_state.current_page = 'home'
            st.rerun()
        else:
            error_data = safe_json_parse(response)
            st.error(f"Profile update failed: {error_data.get('detail', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
    except Exception as e:
        st.error(f"Profile update error: {str(e)}")

def create_campaign_backend(campaign_data, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{BACKEND_URL}/create_campaign",
            json=campaign_data,
            headers=headers,
            timeout=30  # Increased timeout for image upload
        )

        if response.status_code == 200:
            st.success(get_text('campaign_creation_success'))
            st.session_state.current_page = 'home'  # Navigate back to home or campaigns list
            st.rerun()
        else:
            error_data = safe_json_parse(response)
            st.error(f"{get_text('campaign_creation_failed')} {error_data.get('detail', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error during campaign creation: {str(e)}")
    except Exception as e:
        st.error(f"Campaign creation error: {str(e)}")

def render_user_profile():
    if st.session_state.user_info:
        user_info = st.session_state.user_info
        name = user_info.get('name', user_info.get('contact_full_name', 'User'))
        email = user_info.get('email', 'user@example.com')
        user_type = user_info.get('user_type', 'individual')

        st.markdown(f"""
<div class="user-prof ile"


>
<d iv class="user- a

a tar"


>{na me[0].upper() if name else 'U'}</div>
<div class=" u s er- n

m e">{


name } ({user_typ e .capitalize()})</div>
<div class= " u ser -

m ail"


>{em ail}</div>
</ d iv>
""" ,   uns a

e _ all ow_html=True)

        # Logout button
        if st.button(get_text('logout'), key="firebase_logout_button"):
            # Call JavaScript function to sign out from Firebase
            st.components.v1.html("""
<script>
window.si gnOutF irebase();
</script>
""", hei g ht=0,  width=0)
# Handle logout success/error via postMessage in handle_js_messages

def render_login_page():
st.markdown('<div class="html-container">', unsafe_allow_html=True)

st.markdown(f'<div class="html-title">{get_text("login")}</div>', unsafe_allow_html=True)

with st.form(key='login_form'):
email = st.text_input("", placeholder="Enter Your Email", key="login_email")
password = st.text_input("", type="password", placeholder="Enter Your Password", key="login_password")

submit_button = st.form_submit_button(get_text('continue'))

if submit_button:
if email and password:
    # Call JavaScript function to sign in with Firebase
    st.components.v1.html(f"""
<script>
window.si gnInWi thEmailPassword("{email}", "{password}");
</script>
""", hei g ht=0,  width=0)
# The response will be handled by handle_js_messages
else:
st.error("Please fill in all fields")

st.markdown(f"""
<div class="html-o pti


n">
{ get_text('not_ r


gistered')}
<a href="{FRONTEND _
ASE_ U RL}?page=register" target="_blank">{
get_t e xt('crea t e_account')}</a>
</div>
""",   u n saf e _al low_html=True)

    render_oauth_buttons(is_register_page=False)

    st.markdown('</div>', unsafe_allow_html=True)

def render_register_page():
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)

    st.markdown(f'<div class="html-title-register">{get_text("register")}</div>', unsafe_allow_html=True)

    registration_type_options = [get_text('individual'), get_text('organization')]

    if 'selected_reg_type_register' not in st.session_state:
        st.session_state.selected_reg_type_register = registration_type_options[0]

    selected_type = st.selectbox(
        "Select Registration Type",
        options=registration_type_options,
        index=registration_type_options.index(st.session_state.selected_reg_type_register),
        key="reg_type_selector_outside_form_register"
    )
    if selected_type != st.session_state.selected_reg_type_register:
        st.session_state.selected_reg_type_register = selected_type
        st.rerun()

    with st.form(key='register_form'):
        email, password, confirm_password = "", "", ""
        full_name, phone, address = "", "", ""
        contact_full_name, contact_phone = "", ""
        org_name, org_type, org_description = "", "", ""
        ngo_darpan_id, pan, fcra_number = "", "", ""

        user_data_for_backend = {}
        is_valid_input = False

        if st.session_state.selected_reg_type_register == get_text('individual'):
            st.markdown(f"""<div class="html - for


-box" ><h3>{get_text(" r e gi s ter_individual")}</h3>""", unsafe _ a ll o w_html=True)

            full_name = st.text_input("", placeholder="Full Name", key="reg_full_name_ind")
            email = st.text_input("", placeholder="Email ID", key="reg_email_ind")
            phone = st.text_input("", placeholder="Phone Number", key="reg_phone_ind")
            password = st.text_input("", type="password", placeholder="Password", key="reg_password_ind")
            confirm_password = st.text_input("", type="password", placeholder="Confirm Password", key="reg_confirm_password_ind")
            address = st.text_area("", placeholder="Address", key="reg_address_individual_ind")

            st.markdown('</div>', unsafe_allow_html=True)

            individual_data = {
                "full_name": full_name,
                "phone": phone,
                "address": address
            }
            user_data_for_backend = {"user_type": "individual", "individual_data": individual_data}
            is_valid_input = bool(full_name and email and phone and password and confirm_password and address)

        elif st.session_state.selected_reg_type_register == get_text('organization'):
            st.markdown(f"""<div class="html - form-box" ><h3>{get_text(" c o nt a ct_person_details")}</h3>""", unsafe _ a ll o w_html=True)

            contact_full_name = st.text_input("", placeholder="Contact Person Full Name", key="reg_contact_full_name_org")
            email = st.text_input("", placeholder="Contact Person Email ID (for login)", key="reg_email_org_contact_org")
            contact_phone = st.text_input("", placeholder="Contact Person Phone Number", key="reg_contact_phone_org")
            password = st.text_input("", type="password", placeholder="Password", key="reg_password_org_contact_org")
            confirm_password = st.text_input("", type="password", placeholder="Confirm Password", key="reg_confirm_password_org_contact_org")

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(f"""<div class="html - form-box" ><h3>{get_text(" o r ga n ization_details")}</h3>""", unsafe _ a ll o w_html=True)

            org_name = st.text_input("", placeholder="Organization Name", key="reg_org_name_org")
            org_type = st.selectbox("",
                                   options=["", get_text('ngo'), get_text('startup'), get_text('charity')],
                                   key="reg_org_type_select_org")
            org_description = st.text_input("", placeholder=get_text('description'), key="reg_org_description_org")
            address = st.text_area("", placeholder="Organization Address", key="reg_address_organization_org")
            ngo_darpan_id = st.text_input("", placeholder="NGO Darpan ID (Optional)", key="reg_ngo_darpan_id_org")
            pan = st.text_input("", placeholder="PAN (Optional)", key="reg_pan_org")
            fcra_number = st.text_input("", placeholder="FCRA Number (Optional)", key="reg_fcra_number_org")

            st.markdown('</div>', unsafe_allow_html=True)

            organization_data = {
                "contact_full_name": contact_full_name,
                "contact_phone": contact_phone,
                "organization_name": org_name,
                "organization_type": org_type,
                "description": org_description,
                "address": address,
                "ngo_darpan_id": ngo_darpan_id,
                "pan": pan,
                "fcra_number": fcra_number
            }
            user_data_for_backend = {"user_type": "organization", "organization_data": organization_data}
            is_valid_input = bool(contact_full_name and email and contact_phone and password and confirm_password and
                                  org_name and org_type and org_description and address)

        submit_button = st.form_submit_button(get_text('register'))

        if submit_button:
            if not is_valid_input:
                st.error("Please fill in all required fields for the selected registration type.")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                # Call JavaScript function to create user with Firebase
                st.components.v1.html(f"""
<script>
window. createUser WithEmailPassword("{email}", "{password}");
</script>
""", heigh t =0, wi dth=0)
# Store additional data in session state temporarily until Firebase ID token is received
st.session_state.temp_registration_data = user_data_for_backend
st.session_state.temp_registration_data['email'] = email # Store email for reference

st.markdown(f"""
<div class="html-opt ion"


>
{g et_text('alrea d


_have_account')}
<a href="{FRONTEND_ B
SE_U R L}?page=login" target="_blank">{
get_te x t('sign_ i n_here')}</a>
</div>
""",  u n s afe _ all ow_html=True)

    st.markdown("""
<div class="oauth- div


der">
<span>or sign u p

w ith so cial ac
ou
t</span>
</div>
""" ,   unsa fe_ a llo w_html=True)

    render_oauth_buttons(is_register_page=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_complete_oauth_profile_page():
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)
    st.markdown(f'<div class="html-title-register">{get_text("complete_profile_title")}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="color: #333; text-align: center; margin-bottom: 20px;">{get_text("provide_details")}</p>',
        unsafe_allow_html=True)

    user_info = st.session_state.get('user_info', {})
    oauth_email = user_info.get('email', '')
    oauth_name = user_info.get('name', '')

    if 'selected_reg_type_oauth' not in st.session_state:
        st.session_state.selected_reg_type_oauth = user_info.get('user_type', TRANSLATIONS['English']['individual'])

    selected_type_oauth = st.selectbox(
        "Select Your User Type",
        options=[get_text('individual'), get_text('organization')],
        index=(
            [get_text('individual'), get_text('organization')].index(st.session_state.selected_reg_type_oauth)),
        key="complete_reg_type_selector_outside_form_oauth"
    )
    if selected_type_oauth != st.session_state.selected_reg_type_oauth:
        st.session_state.selected_reg_type_oauth = selected_type_oauth
        st.rerun()

    with st.form(key='complete_profile_form'):
        st.markdown(f"""<div class="html-f o rm-


rappe r">""", unsafe_allow _ html=True)

        st.markdown(f"""<div class="html-f o rm-box">< h3>OAuth Details < / h3 > </div>""", un s a fe _ a l low _ html=True)
        st.text_input("Email", value=oauth_email, disabled=True, key="oauth_email_display_cp")
        st.text_input("Name", value=oauth_name, disabled=True, key="oauth_name_display_cp")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""<div class="html-f o rm-box">< h3>Additional De t a il s </h3></div>""", un s a fe _ a l low _ html=True)

        user_data_to_send = {"user_type": selected_type_oauth}
        is_valid_input = False

        if selected_type_oauth == get_text('individual'):
            phone = st.text_input("", placeholder="Phone Number", value=user_info.get('phone', ''), key="complete_phone_ind_cp")
            address = st.text_area("", placeholder="Address", value=user_info.get('address', ''), key="complete_address_ind_cp")

            user_data_to_send.update({
                "full_name": oauth_name,
                "phone": phone,
                "address": address,
            })
            is_valid_input = bool(phone and address)

        elif selected_type_oauth == get_text('organization'):
            st.markdown(f"""<h4>{get_text("con t ac t _person_details")}</h4>""", unsafe_a l l ow _ html=True)
            contact_full_name = st.text_input("Contact Person Full Name", value=user_info.get('contact_full_name', oauth_name), disabled=True,
                                              key="complete_contact_full_name_org_cp")
            contact_phone = st.text_input("", placeholder="Contact Person Phone Number", value=user_info.get('contact_phone', ''),
                                          key="complete_contact_phone_org_cp")

            st.markdown(f"""<h4>{get_text("org a ni z ation_details")}</h4>""", unsafe_a l l ow _ html=True)
            org_name = st.text_input("", placeholder="Organization Name", value=user_info.get('organization_name', ''), key="complete_org_name_org_cp")
            org_type = st.selectbox("Organization Type",
                                   options=["", get_text('ngo'), get_text('startup'), get_text('charity')],
                                   index=(
                                       ["", get_text('ngo'), get_text('startup'), get_text('charity')].index(user_info.get('organization_type', '') if user_info.get('organization_type') in ["", get_text('ngo'), get_text('startup'), get_text('charity')] else "")
                                   ),
                                   key="complete_org_type_select_org_cp")
            org_description = st.text_input("", placeholder=get_text('description'), value=user_info.get('description', ''),
                                            key="complete_org_description_org_cp")
            address = st.text_area("", placeholder="Organization Address", value=user_info.get('address', ''), key="complete_address_org_org_cp")
            ngo_darpan_id = st.text_input("", placeholder="NGO Darpan ID (Optional)", value=user_info.get('ngo_darpan_id', ''), key="complete_ngo_darpan_id_org_cp")
            pan = st.text_input("", placeholder="PAN (Optional)", value=user_info.get('pan', ''), key="complete_pan_org_cp")
            fcra_number = st.text_input("", placeholder="FCRA Number (Optional)", value=user_info.get('fcra_number', ''), key="complete_fcra_number_org_cp")


            user_data_to_send.update({
                "contact_full_name": contact_full_name,
                "contact_phone": contact_phone,
                "organization_name": org_name,
                "organization_type": org_type,
                "description": org_description,
                "address": address,
                "ngo_darpan_id": ngo_darpan_id,
                "pan": pan,
                "fcra_number": fcra_number
            })
            is_valid_input = bool(contact_full_name and contact_phone and org_name and org_type and org_description and address)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        submit_button = st.form_submit_button(get_text('update_profile'))

        if submit_button:
            if not is_valid_input:
                st.error("Please fill in all required fields for your selected user type.")
            elif st.session_state.user_token:
                update_user_profile_backend(user_data_to_send, st.session_state.user_token)
            else:
                st.error("Authentication token missing. Please try logging in again.")

    st.markdown('</div>', unsafe_allow_html=True)

def render_create_campaign_button():
    # Only show if user is logged in and is an organization
    if st.session_state.user_token and st.session_state.user_info and \
            st.session_state.user_info.get('user_type') == 'organization':
        st.markdown(f"""
<div style="text-

l ign
 cent e r; margin-top: 20px;">
<button class="c rea te-cam


aign- button" onclick="window.parent.postMessage({{streamlit: {{type: 'SET_PAGE_STATE', payload: 'create_campaign'}}}}, '*');">
+
</button>
</di v>
"" " , unsa fe_ a llo w_html=True)

def render_create_campaign_page():
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)
    st.markdown(f'<div class="html-title-register">{get_text("create_campaign")}</div>', unsafe_allow_html=True)

    if not (st.session_state.user_token and st.session_state.user_info and \
            st.session_state.user_info.get('user_type') == 'organization'):
        st.warning(get_text('only_org_can_create_campaign'))
        return

    with st.form(key='create_campaign_form'):
        campaign_name = st.text_input("", placeholder=get_text('campaign_name'), key="campaign_name_input")
        description = st.text_area("", placeholder=get_text('campaign_description_full'),
                                   key="campaign_description_input")
        goal_amount = st.number_input("", min_value=100.0, value=1000.0, step=100.0, format="%.2f",
                                      placeholder=get_text('goal_amount'), key="goal_amount_input")
        category = st.selectbox("",
                                options=["", get_text('technology'), get_text('health'), get_text('education'),
                                         get_text('environment'), get_text('arts'), get_text('community')],
                                placeholder=get_text('campaign_category'), key="campaign_category_select")

        uploaded_file = st.file_uploader(get_text('upload_image'), type=["png", "jpg", "jpeg"],
                                         key="campaign_image_uploader")

        submit_button = st.form_submit_button(get_text('submit_campaign'))

        if submit_button:
            if not all([campaign_name, description, goal_amount, category]):
                st.error("Please fill in all campaign details.")
            elif category == "":
                st.error("Please select a campaign category.")
            else:
                image_base64 = None
                if uploaded_file is not None:
                    bytes_data = uploaded_file.getvalue()
                    image_base64 = base64.b64encode(bytes_data).decode('utf-8')

                campaign_data = {
                    "campaign_name": campaign_name,
                    "description": description,
                    "goal": float(goal_amount),
                    "category": category,
                    "image_base64": image_base64
                }
                create_campaign_backend(campaign_data, st.session_state.user_token)

    st.markdown('</div>', unsafe_allow_html=True)


def render_home_page():
    st.markdown(f'<h1 class="app-title">{get_text("explore")}</h1>', unsafe_allow_html=True)
    st.markdown(f"## {get_text('trending_campaigns')}")

    try:
        response = requests.get(f"{BACKEND_URL}/campaigns", timeout=10)
        if response.status_code == 200:
            campaigns = response.json()
        else:
            st.error(f"Failed to load campaigns: {response.status_code} - {response.text}")
            campaigns = []
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error fetching campaigns: {str(e)}")
        campaigns = []

    if not campaigns:
        st.info("No campaigns found. Create one if you are an organization!")

    for campaign in campaigns:
        progress_percent = (campaign.get('funded', 0) / campaign.get('goal', 1)) * 100 if campaign.get('goal', 1) > 0 else 0
        progress_percent = min(100, max(0, progress_percent))

        st.markdown(f"""
<div class="campaig n-c


rd"> <div class="campa i

n -im


ge"> <img src="{campaig n \

g et( \
ima g e_url', 'https://placehold.co/600x400/4CAF50/ffffff?text=Campaign+Image')}"
alt="{campaign['campaig n _name']}"
style="width:100%; height : 200px; object-fit:cover; border-radius: 12px 12px 0 0;">
</div>
<div class= "ca m pai gn- con


ent">
<div class="campai g

- tit


e">{c ampaign['campaign _ name']}</div>
<div class="c a m pai g

- des


ripti on">{campaign['descript i on']}</div>
<div style="f o n t-s i

e : 0
9em;  c olor: #777; margin-bottom: 0.5rem;">
By: {campaign.get( 'author', 'N/A')} | Category: {campaign.get('category', 'N/A')}
</div>
<div class="ca m pai gn- pro


ress" >
<div class="campai g

- pro


ress- bar" style="width: {progress_percent}%"></div>
</div>
<div st y l e=" d

s p lay : f lex
 just i fy-content: space-between; color: #666; font-weight: 500;">
<span>Raised: ${cam pai gn.g e t('funded', 0):,}</span>
<span>Goal: $ { c ampa ign .get ( 'goal', 0):,}</span>
</div>
<div s t y le=" tex t -al ign : r
ght;  f ont-size: 0.8em; color: #999; margin-top: 0.5rem;">
Days Left: {round(c ampaign
.get('days_left', 'N/A'))} | Status: {campaign.get('verification_status', 'N/A')}
</div>
</div>
</div> "" ",  uns a fe_ all o w_h tml=True)

def render_explore_page():
    st.markdown(f'<h1 class="app-title">{get_text("explore")}</h1>', unsafe_allow_html=True)
    st.markdown(f"## {get_text('categories')}")

    categories = [
        {"name": get_text('technology'), "icon": "fas fa-laptop-code"},
        {"name": get_text('health'), "icon": "fas fa-heartbeat"},
        {"name": get_text('education'), "icon": "fas fa-graduation-cap"},
        {"name": get_text('environment'), "icon": "fas fa-leaf"},
        {"name": get_text('arts'), "icon": "fas fa-palette"},
        {"name": get_text('community'), "icon": "fas fa-users"}
    ]

    cols = st.columns(2)
    for i, category in enumerate(categories):
        with cols[i % 2]:
            st.markdown(f"""
<div class="category-c ard"


>
<d iv class="catego r

- ico


">
<i class="{categor y

' i


on']} "></i>
</div>
<div cl a s s = "

a t ego ry- tit


e">{c ategory['name']}< / div>
</div>
""", u n s afe _

l l ow_ html=True)

def render_search_page():
    st.markdown(f'<h1 class="app-title">{get_text("search_campaigns")}</h1>', unsafe_allow_html=True)

    st.markdown('<div class="search-container">', unsafe_allow_html=True)

    search_query = st.text_input(
        "Search Campaigns",
        placeholder=get_text('search_placeholder'),
        key="search_input"
    )

    if st.button("🔍 Search", key="search_button"):
        if search_query:
            st.success(f"Searching for: {search_query}")
        else:
            st.warning("Please enter a search term")

    st.markdown(f"""
<div class="search-ti ps">
<h4> <i class="fas  f

- li g h t


ulb"> </i> {get_text('sea r c h _ tips')}</h4>
<ul>
<li>{get_ t e xt (

' us e_k ey w ords')}</li>
<li>{get_text ( ' fi lte r_ c ategory')}</li>
<li>{get_text ( ' ch eck _s p elling')}</li>
</ul>
</div> "" " ,  uns a fe _al l ow_ html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Select Language:</div>', unsafe_allow_html=True)
        language = st.selectbox(
            "Choose Language",
            options=list(TRANSLATIONS.keys()),
            index=list(TRANSLATIONS.keys()).index(st.session_state.language),
=======
# Translation and simplification controls
def render_language_controls():
    """Render language and simplification controls"""
    st.markdown("""
    <div class="translation-bar">
        <h4>🌍 Language & Accessibility Settings</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Language selector
        language_options = [
            f"{lang_info['flag']} {lang_info['native']}" 
            for lang_code, lang_info in SUPPORTED_LANGUAGES.items()
        ]
        
        selected_lang_display = st.selectbox(
            "Select Language",
            language_options,
            index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.current_language),
>>>>>>> fd0f666ea8655d0250a75c9378e7acbbdf0b5a9a
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
    if st.session_state.translation_enabled or st.session_state.simplification_enabled:
        settings_text = []
        if st.session_state.translation_enabled:
            lang_name = SUPPORTED_LANGUAGES[st.session_state.current_language]['native']
            settings_text.append(f"Translating to {lang_name}")
        if st.session_state.simplification_enabled:
            settings_text.append("Simplifying complex terms")
        
        st.info(f"Active: {' | '.join(settings_text)}")

# Main navigation
def render_navigation():
    """Render main navigation sidebar"""
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        # Main pages
        page = st.radio(
            "Choose a page:",
            [
                "🏠 Home",
                "🔍 Explore Campaigns", 
                "🚀 Create Campaign",
                "👤 Profile",
                "🔐 Authentication",
                "🌍 Translation Hub",
                "💡 Simplification Center",
                "📊 Analytics"
            ]
        )
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("## ⚡ Quick Actions")
        
        if st.button("🔄 Translate Page"):
            st.session_state.translation_enabled = not st.session_state.translation_enabled
            st.rerun()
        
        if st.button("💡 Toggle Simplification"):
            st.session_state.simplification_enabled = not st.session_state.simplification_enabled
            st.rerun()
        
        # Service status
        st.markdown("---")
        st.markdown("## 📡 Service Status")
        
        try:
            health = make_api_request("/health")
            if "error" not in health:
                st.success("✅ Backend Connected")
                if health.get("features", {}).get("translation"):
                    st.success("✅ Translation Available")
                if health.get("features", {}).get("simplification"):
                    st.success("✅ Simplification Available")
            else:
                st.error("❌ Backend Unavailable")
        except:
            st.error("❌ Connection Failed")
    
    return page

# Page components
def render_home_page():
    """Render home page"""
    st.markdown("## 🏠 Welcome to HAVEN")
    
    display_text_with_translation("""
    HAVEN is a revolutionary crowdfunding platform that connects innovative projects 
    with passionate supporters. Our platform leverages cutting-edge technology to 
    ensure transparency, security, and accessibility for all users.
    """)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🚀 Launch Your Project</h4>
            <p>Turn your innovative ideas into reality with our easy-to-use campaign creation tools.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🤝 Support Innovation</h4>
            <p>Discover and fund groundbreaking projects that align with your interests and values.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🛡️ Secure & Transparent</h4>
            <p>Advanced fraud detection and blockchain technology ensure your investments are safe.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent campaigns
    st.markdown("## 🔥 Featured Campaigns")
    
    # Mock campaign data
    campaigns = [
        {
            "title": "Smart Agriculture IoT System",
            "description": "Revolutionary IoT sensors for precision farming",
            "goal": "$50,000",
            "raised": "$32,500",
            "progress": 65
        },
        {
            "title": "Eco-Friendly Water Purifier",
            "description": "Solar-powered water purification for rural communities",
            "goal": "$25,000",
            "raised": "$18,750",
            "progress": 75
        },
        {
            "title": "Educational VR Platform",
            "description": "Immersive virtual reality learning experiences",
            "goal": "$75,000",
            "raised": "$45,000",
            "progress": 60
        }
    ]
    
    for campaign in campaigns:
        with st.expander(f"📈 {campaign['title']}"):
            display_text_with_translation(campaign['description'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Goal", campaign['goal'])
            with col2:
                st.metric("Raised", campaign['raised'])
            with col3:
                st.metric("Progress", f"{campaign['progress']}%")
            
            st.progress(campaign['progress'] / 100)

def render_explore_page():
    """Render explore campaigns page"""
    st.markdown("## 🔍 Explore Campaigns")
    
    display_text_with_translation("""
    Discover innovative projects and campaigns from creators around the world. 
    Use our advanced filters to find projects that match your interests.
    """)
    
    # Search and filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search campaigns", placeholder="Enter keywords...")
    
    with col2:
        category = st.selectbox(
            "📂 Category",
            ["All", "Technology", "Health", "Education", "Environment", "Arts"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "📊 Sort by",
            ["Most Recent", "Most Funded", "Ending Soon", "Most Popular"]
        )
    
    # Campaign grid
    st.markdown("### 📋 Campaign Results")
    
    # Mock search results
    if search_query or category != "All":
        st.info(f"Showing results for: {search_query or category}")
    
    # Display campaigns in grid
    campaigns = [
        {"title": "AI-Powered Healthcare Assistant", "category": "Health", "raised": "$45,000", "goal": "$60,000"},
        {"title": "Sustainable Energy Storage", "category": "Technology", "raised": "$78,000", "goal": "$100,000"},
        {"title": "Digital Literacy Program", "category": "Education", "raised": "$23,000", "goal": "$40,000"},
        {"title": "Ocean Cleanup Initiative", "category": "Environment", "raised": "$156,000", "goal": "$200,000"}
    ]
    
    for i in range(0, len(campaigns), 2):
        col1, col2 = st.columns(2)
        
        for j, col in enumerate([col1, col2]):
            if i + j < len(campaigns):
                campaign = campaigns[i + j]
                with col:
                    with st.container():
                        st.markdown(f"**{campaign['title']}**")
                        st.markdown(f"Category: {campaign['category']}")
                        st.markdown(f"Raised: {campaign['raised']} / {campaign['goal']}")
                        
                        progress = int(campaign['raised'].replace('$', '').replace(',', '')) / int(campaign['goal'].replace('$', '').replace(',', ''))
                        st.progress(progress)
                        
                        if st.button(f"View Details", key=f"view_{i+j}"):
                            st.info("Campaign details would open here")

def render_create_campaign_page():
    """Render create campaign page"""
    st.markdown("## 🚀 Create Your Campaign")
    
    display_text_with_translation("""
    Launch your innovative project and connect with supporters who believe in your vision. 
    Our platform provides all the tools you need to create a successful crowdfunding campaign.
    """)
    
    # Campaign creation form
    with st.form("create_campaign"):
        st.markdown("### 📝 Campaign Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Campaign Title*", placeholder="Enter a compelling title")
            category = st.selectbox("Category*", ["Technology", "Health", "Education", "Environment", "Arts", "Other"])
            goal_amount = st.number_input("Funding Goal ($)*", min_value=1000, value=10000, step=1000)
        
        with col2:
            duration = st.number_input("Campaign Duration (days)*", min_value=7, max_value=90, value=30)
            location = st.text_input("Location", placeholder="City, Country")
            website = st.text_input("Website/Social Media", placeholder="https://...")
        
        description = st.text_area(
            "Campaign Description*", 
            placeholder="Describe your project, its impact, and why people should support it...",
            height=150
        )
        
        # File uploads
        st.markdown("### 📸 Media")
        
        col1, col2 = st.columns(2)
        with col1:
            main_image = st.file_uploader("Main Campaign Image", type=['jpg', 'jpeg', 'png'])
        with col2:
            additional_images = st.file_uploader("Additional Images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
        
        video_url = st.text_input("Video URL (optional)", placeholder="YouTube, Vimeo, etc.")
        
        # Rewards/perks
        st.markdown("### 🎁 Rewards & Perks")
        
        num_rewards = st.number_input("Number of reward tiers", min_value=0, max_value=10, value=3)
        
        for i in range(num_rewards):
            with st.expander(f"Reward Tier {i+1}"):
                col1, col2 = st.columns(2)
                with col1:
                    reward_amount = st.number_input(f"Minimum Contribution ($)", min_value=1, value=25, key=f"reward_amount_{i}")
                with col2:
                    reward_title = st.text_input(f"Reward Title", placeholder="Early Bird Special", key=f"reward_title_{i}")
                
                reward_description = st.text_area(f"Reward Description", placeholder="What backers will receive...", key=f"reward_desc_{i}")
        
        # Terms and conditions
        st.markdown("### ⚖️ Terms & Conditions")
        
        col1, col2 = st.columns(2)
        with col1:
            agree_terms = st.checkbox("I agree to the Terms of Service*")
        with col2:
            agree_fraud = st.checkbox("I confirm this campaign is legitimate*")
        
        # Submit button
        submitted = st.form_submit_button("🚀 Launch Campaign", type="primary")
        
        if submitted:
            if not all([title, category, description, agree_terms, agree_fraud]):
                st.error("Please fill in all required fields and agree to the terms.")
            else:
                # Here you would normally submit to the backend
                st.success("🎉 Campaign created successfully! It will be reviewed before going live.")
                
                # Show campaign preview
                with st.expander("📋 Campaign Preview"):
                    st.markdown(f"**{title}**")
                    st.markdown(f"Category: {category}")
                    st.markdown(f"Goal: ${goal_amount:,}")
                    st.markdown(f"Duration: {duration} days")
                    st.markdown(description)

def render_translation_hub():
    """Render translation hub page"""
    st.markdown("## 🌍 Translation Hub")
    
    display_text_with_translation("""
    Translate content between English, Hindi, Tamil, and Telugu. 
    Our AI-powered translation service ensures accurate and contextual translations.
    """)
    
    # Translation interface
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Input Text")
        
        source_lang = st.selectbox(
            "Source Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]['flag']} {SUPPORTED_LANGUAGES[x]['native']}",
            key="trans_source"
        )
        
        input_text = st.text_area(
            "Text to translate",
            placeholder="Enter text to translate...",
            height=200
        )
    
    with col2:
        st.markdown("### 🔄 Translation")
        
        target_lang = st.selectbox(
            "Target Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]['flag']} {SUPPORTED_LANGUAGES[x]['native']}",
            index=1,
            key="trans_target"
        )
        
        if st.button("🔄 Translate", type="primary"):
            if input_text:
                with st.spinner("Translating..."):
                    translated = translate_text(input_text, target_lang, source_lang)
                    st.text_area("Translation result", value=translated, height=200, disabled=True)
            else:
                st.warning("Please enter text to translate")
    
    # Batch translation
    st.markdown("### 📚 Batch Translation")
    
    uploaded_file = st.file_uploader("Upload text file for batch translation", type=['txt'])
    
    if uploaded_file:
        content = uploaded_file.read().decode('utf-8')
        lines = content.split('\n')
        
        if st.button("🔄 Translate All Lines"):
            with st.spinner(f"Translating {len(lines)} lines..."):
                translated_lines = []
                for line in lines:
                    if line.strip():
                        translated = translate_text(line, target_lang, source_lang)
                        translated_lines.append(translated)
                    else:
                        translated_lines.append("")
                
                # Display results
                st.markdown("### 📋 Translation Results")
                for i, (original, translated) in enumerate(zip(lines, translated_lines)):
                    if original.strip():
                        st.markdown(f"**Line {i+1}:**")
                        st.markdown(f"Original: {original}")
                        st.markdown(f"Translated: {translated}")
                        st.markdown("---")

def render_simplification_center():
    """Render simplification center page"""
    st.markdown("## 💡 Simplification Center")
    
    display_text_with_translation("""
    Make complex financial and technical terms easier to understand. 
    Our AI analyzes text complexity and provides simplified explanations.
    """)
    
    # Text simplification
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Complex Text")
        
        complexity_level = st.selectbox(
            "Target Complexity Level",
            ["very_simple", "simple", "moderate"],
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        complex_text = st.text_area(
            "Enter complex text",
            placeholder="Enter text with complex terms...",
            height=200
        )
    
    with col2:
        st.markdown("### 💡 Simplified Text")
        
        if st.button("💡 Simplify", type="primary"):
            if complex_text:
                with st.spinner("Simplifying..."):
                    simplified = simplify_text(complex_text, complexity_level)
                    st.text_area("Simplified result", value=simplified, height=200, disabled=True)
            else:
                st.warning("Please enter text to simplify")
    
    # Term lookup
    st.markdown("### 🔍 Term Lookup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("Search for a term", placeholder="e.g., crowdfunding, equity, ROI")
        
        if st.button("🔍 Search Term"):
            if search_term:
                definition = get_term_definition(search_term)
                if definition:
                    st.success(f"**{search_term}**: {definition}")
                else:
                    st.warning(f"Definition not found for '{search_term}'")
    
    with col2:
        # Popular terms
        st.markdown("#### 🔥 Popular Terms")
        popular_terms = ["crowdfunding", "equity", "roi", "valuation", "angel_investor"]
        
        for term in popular_terms:
            if st.button(f"📖 {term.replace('_', ' ').title()}", key=f"popular_{term}"):
                definition = get_term_definition(term)
                if definition:
                    st.info(f"**{term.replace('_', ' ').title()}**: {definition}")
    
    # Complexity analysis
    st.markdown("### 📊 Text Complexity Analysis")
    
    analysis_text = st.text_area("Text to analyze", placeholder="Enter text for complexity analysis...")
    
    if st.button("📊 Analyze Complexity"):
        if analysis_text:
            try:
                data = {"text": analysis_text}
                result = make_api_request("/api/simplify/analyze", "POST", data)
                
                if "error" not in result:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Complexity Score", f"{result['complexity_score']:.1f}/100")
                    with col2:
                        st.metric("Complexity Level", result['complexity_level'])
                    with col3:
                        st.metric("Word Count", result['word_count'])
                    
                    if result.get('complex_terms'):
                        st.markdown("#### 🔍 Complex Terms Found:")
                        for term_info in result['complex_terms']:
                            st.markdown(f"- **{term_info['term']}**: {term_info['definition']}")
                    
                    if result.get('recommendations'):
                        st.markdown("#### 💡 Recommendations:")
                        for rec in result['recommendations']:
                            st.markdown(f"- {rec}")
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

<<<<<<< HEAD
            if st.session_state.current_page != 'explore':
                if st.button(get_text("explore"), key="nav_explore"):
                    st.session_state.current_page = 'explore'
                    st.rerun()

            if st.session_state.current_page != 'search':
                if st.button(get_text("search"), key="nav_search"):
                    st.session_state.current_page = 'search'
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

            render_create_campaign_button()

def handle_js_messages():
    """Handles messages pos
ted from JavaScr
pt to
Streamlit."""
    i

 "js_messa
ge" in st.session_state:
        message = st.session_state.js_message
        if message and isinstance(message, dict):
            action = message.get("action")
            id_token = message.get("id_token")
            error = message.get("error")

            if action == "login":
                if id_token:
                    login_user_backend(id_token)
                else:
                    st.error("Firebase login failed: No ID token received.")
            elif action == "login_error":
                st.error(f"Firebase login error: {error}")
            elif action == "register":
                if id_token and 'temp_registration_data' in st.session_state:
                    temp_data = st.session_state.temp_registration_data
                    register_user_backend(
                        id_token,
                        temp_data.get('user_type'),
                        temp_data.get('individual_data'),
                        temp_data.get('organization_data')
                    )
                    del st.session_state.temp_registration_data # Clear temp data
                else:
                    st.error("Firebase registration failed: No ID token or temporary data received.")
            elif action == "register_error":
                st.error(f"Firebase registration error: {error}")
            elif action == "logout_success":
                st.session_state.user_token = None
                st.session_state.user_info = None
                st.session_state.current_page = 'login'
                st.success("Successfully logged out!")
                st.rerun()
            elif action == "logout_error":
                st.error(f"Logout failed: {error}")
        # Clear the message after processing
        st.session_state.js_message = None


def main():
    st.set_page_config(
        page_title="HAVEN - Crowdfunding Platform",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    apply_custom_css()

    # This component listens for messages from the embedded JavaScript
st.components.v1.html("""
<script>
window.addEv entLis tener('message', event => {
if (event.data. streamlit) {
                          //
Forward the message to Python
session state
window.parent.postMessage(event.data, '*'); } });
</script>
""", height=0, width=0, key="js_listener")

# Handle messages from JavaScript
if "streamlit" in st.query_params:
    # This is how Streamlit receives messages from custom components/JS
    # We need to parse it and store it in session_state for handle_js_messages
    try:
        message_payload = json.loads(st.query_params["streamlit"])
        if message_payload.get("type") == "SET_PAGE_STATE":
            st.session_state.js_message = message_payload.get("payload")
        # Clear the query param to avoid re-processing on rerun
        st.query_params.clear()
        st.rerun() # Rerun to process the message
    except json.JSONDecodeError:
        pass # Ignore malformed messages

handle_js_messages() # Process any messages received

# Updated banner rendering with new classes for better control
st.markdown(f'<div class="welcome-banner-main-title">{get_text("welcome_banner_text")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="welcome-banner-tagline">{get_text("welcome_banner_tagline")}</div>', unsafe_allow_html=True)


handle_oauth_callback()

query_params = st.query_params
if 'page' in query_params:
    requested_page = query_params['page']
    if requested_page in ['login', 'register', 'home', 'explore', 'search', 'complete_oauth_profile',
                          'create_campaign']:
        st.session_state.current_page = requested_page
        # Clear the page query param after setting state to avoid re-processing on rerun
        st.query_params.clear()
        st.rerun() # Rerun to navigate to the correct page

render_sidebar()

try:
    if st.session_state.current_page == 'login':
        render_login_page()
    elif st.session_state.current_page == 'register':
        render_register_page()
    elif st.session_state.current_page == 'complete_oauth_profile':
        render_complete_oauth_profile_page()
    elif st.session_state.current_page == 'create_campaign':
        render_create_campaign_page()
    elif st.session_state.current_page == 'home':
        render_home_page()
    elif st.session_state.current_page == 'explore':
        render_explore_page()
    elif st.session_state.current_page == 'search':
        render_search_page()
    else:
        st.session_state.current_page = 'login'
        render_login_page()
except Exception as e:
    st.error(f"An unexpected error occurred in the main application flow: {e}")
    st.exception(e)
=======
def render_analytics_page():
    """Render analytics page"""
    st.markdown("## 📊 Platform Analytics")
    
    display_text_with_translation("""
    Monitor platform performance, translation usage, and user engagement metrics.
    """)
    
    # Service statistics
    try:
        stats = make_api_request("/api/stats")
        
        if "error" not in stats:
            st.markdown("### 🔧 Service Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Supported Languages", stats.get('combined_stats', {}).get('total_supported_languages', 4))
            with col2:
                st.metric("Available Terms", stats.get('combined_stats', {}).get('total_terms_available', 0))
            with col3:
                st.metric("Services Status", "Healthy" if stats.get('combined_stats', {}).get('services_healthy') else "Issues")
            with col4:
                st.metric("Last Updated", "Now")
            
            # Translation statistics
            if 'translation' in stats:
                st.markdown("### 🌍 Translation Service")
                trans_stats = stats['translation']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Language Pairs", trans_stats.get('supported_language_pairs', 12))
                with col2:
                    st.metric("Cache Memory", trans_stats.get('cache_memory_usage', 'N/A'))
            
            # Simplification statistics
            if 'simplification' in stats:
                st.markdown("### 💡 Simplification Service")
                simp_stats = stats['simplification']
                
                if 'categories' in simp_stats:
                    st.markdown("#### 📚 Term Categories")
                    categories_df = pd.DataFrame(
                        list(simp_stats['categories'].items()),
                        columns=['Category', 'Term Count']
                    )
                    st.bar_chart(categories_df.set_index('Category'))
    
    except Exception as e:
        st.error(f"Failed to load analytics: {str(e)}")
    
    # Mock usage analytics
    st.markdown("### 📈 Usage Analytics")
    
    # Generate mock data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    usage_data = pd.DataFrame({
        'Date': dates,
        'Translations': [50 + i*2 + (i%7)*10 for i in range(len(dates))],
        'Simplifications': [30 + i*1.5 + (i%5)*8 for i in range(len(dates))],
        'New Users': [10 + i*0.5 + (i%3)*5 for i in range(len(dates))]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔄 Daily Translations")
        st.line_chart(usage_data.set_index('Date')['Translations'])
    
    with col2:
        st.markdown("#### 💡 Daily Simplifications")
        st.line_chart(usage_data.set_index('Date')['Simplifications'])
    
    st.markdown("#### 👥 New User Registrations")
    st.area_chart(usage_data.set_index('Date')['New Users'])
>>>>>>> fd0f666ea8655d0250a75c9378e7acbbdf0b5a9a

def render_authentication_page():
    """Render authentication page"""
    st.markdown("## 🔐 Authentication")
    
    if not st.session_state.user_authenticated:
        display_text_with_translation("""
        Sign in to access all features of the HAVEN platform. 
        Create campaigns, support projects, and manage your profile.
        """)
        
        tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])
        
        with tab1:
            st.markdown("### 🔑 Sign In to Your Account")
            
            with st.form("signin_form"):
                email = st.text_input("Email Address", placeholder="your@email.com")
                password = st.text_input("Password", type="password")
                remember_me = st.checkbox("Remember me")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("🔑 Sign In", type="primary"):
                        if email and password:
                            # Mock authentication
                            st.session_state.user_authenticated = True
                            st.success("✅ Successfully signed in!")
                            st.rerun()
                        else:
                            st.error("Please enter both email and password")
                
                with col2:
                    if st.form_submit_button("🔗 Forgot Password"):
                        st.info("Password reset link would be sent to your email")
            
            st.markdown("---")
            st.markdown("### 🌐 Social Sign In")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔴 Sign in with Google", key="google_signin"):
                    # Redirect to Google OAuth
                    google_oauth_url = f"{BACKEND_URL}/auth/google/login"
                    st.markdown(f"[Click here to sign in with Google]({google_oauth_url})")
            
            with col2:
                if st.button("🔵 Sign in with Facebook", key="facebook_signin"):
                    # Redirect to Facebook OAuth
                    facebook_oauth_url = f"{BACKEND_URL}/auth/facebook/login"
                    st.markdown(f"[Click here to sign in with Facebook]({facebook_oauth_url})")
        
        with tab2:
            st.markdown("### 📝 Create New Account")
            
            with st.form("signup_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name")
                    email = st.text_input("Email Address")
                    password = st.text_input("Password", type="password")
                
                with col2:
                    last_name = st.text_input("Last Name")
                    phone = st.text_input("Phone Number (optional)")
                    confirm_password = st.text_input("Confirm Password", type="password")
                
                country = st.selectbox("Country", ["India", "United States", "United Kingdom", "Canada", "Other"])
                
                agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
                newsletter = st.checkbox("Subscribe to newsletter for updates")
                
                if st.form_submit_button("📝 Create Account", type="primary"):
                    if not all([first_name, last_name, email, password, confirm_password]):
                        st.error("Please fill in all required fields")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    elif not agree_terms:
                        st.error("Please agree to the Terms of Service")
                    else:
                        # Mock account creation
                        st.success("✅ Account created successfully! Please check your email for verification.")
    
    else:
        # User is authenticated
        st.markdown("### 👤 User Profile")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image("https://via.placeholder.com/150", caption="Profile Picture")
            
            if st.button("🚪 Sign Out"):
                st.session_state.user_authenticated = False
                st.rerun()
        
        with col2:
            st.markdown("**John Doe**")
            st.markdown("📧 john.doe@email.com")
            st.markdown("📱 +1 (555) 123-4567")
            st.markdown("🌍 United States")
            st.markdown("📅 Member since: January 2024")
        
        # User statistics
        st.markdown("### 📊 Your Activity")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Campaigns Created", "3")
        with col2:
            st.metric("Projects Supported", "12")
        with col3:
            st.metric("Total Contributed", "$2,450")
        with col4:
            st.metric("Total Raised", "$8,750")

# Main application
def main():
    """Main application function"""
    # Render header
    render_header()
    
    # Render language controls
    render_language_controls()
    
    # Render navigation and get selected page
    selected_page = render_navigation()
    
    # Render selected page
    if selected_page == "🏠 Home":
        render_home_page()
    elif selected_page == "🔍 Explore Campaigns":
        render_explore_page()
    elif selected_page == "🚀 Create Campaign":
        render_create_campaign_page()
    elif selected_page == "👤 Profile":
        render_authentication_page()
    elif selected_page == "🔐 Authentication":
        render_authentication_page()
    elif selected_page == "🌍 Translation Hub":
        render_translation_hub()
    elif selected_page == "💡 Simplification Center":
        render_simplification_center()
    elif selected_page == "📊 Analytics":
        render_analytics_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🏠 HAVEN Crowdfunding Platform | Empowering Innovation Through Community</p>
        <p>🌍 Supporting 4 languages | 💡 AI-powered simplification | 🛡️ Secure & transparent</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
main()

