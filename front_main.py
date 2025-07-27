import streamlit as st
import requests
import json
import base64
import time
import os
import re
from urllib.parse import urlencode, parse_qs, urlparse

BACKEND_URL = "https://haven-fastapi-backend.onrender.com"
FRONTEND_BASE_URL = "https://haven-streamlit-frontend.onrender.com"  # <<< IMPORTANT: REPLACE THIS WITH YOUR ACTUAL DEPLOYED STREAMLIT FRONTEND URL

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
        'update_profile': 'Update Profile'
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
        'update_profile': 'प्रोफ़ाइल अपडेट करें'
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
        'update_profile': 'சுயவிவரத்தை புதுப்பிக்கவும்'
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
        'provide_details': 'మీ ప్రొఫైల్‌ను పూర్తి చేయడానికి దయచేసి అదనపు వివరాలను అందించండి.',
        'update_profile': 'ప్రొఫైల్‌ను అప్‌డేట్ చేయండి'
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


def get_text(key):
    return TRANSLATIONS[st.session_state.language].get(key, key)


def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

    .stApp {
        background-color: #f0f2e6 !important;
        font-family: 'Poppins', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .html-container {
        background: #fff;
        width: 100%;
        max-width: 400px;
        padding: 20px 20px;
        border-radius: 5px;
        box-shadow: 0 10px 10px rgba(0, 0, 0, 0.15);
        margin: 20px auto;
        color: #000;
    }

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
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid #ccc !important;
        border-radius: 0 !important;
        padding: 5px !important;
        font-size: 16px !important;
        color: #333 !important; /* Slightly darker input text for contrast */
        font-family: 'Poppins', sans-serif !important;
        height: 45px !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-bottom: 2px solid #4CAF50 !important;
        box-shadow: none !important;
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
        text-decoration: underline;
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
        border-radius: 5px;
        transition: all 0.3s ease;
        margin-bottom: 15px;
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
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
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

    .stTextInput label, .stSelectbox label, .stTextArea label {
        display: none !important;
    }

    .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: #333 !important; /* Ensure all markdown text is dark for contrast */
    }

    .app-title {
        background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
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
        color: #333; /* Darker subtitle for contrast */
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

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
        border-color: #4CAF50;
    }

    .category-icon {
        font-size: 2.5rem;
        color: #4CAF50;
        margin-bottom: 1rem;
    }

    .category-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #333; /* Darker category title for contrast */
        margin-bottom: 0.5rem;
    }

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
        background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
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
        color: #333; /* Darker campaign title for contrast */
        margin-bottom: 0.5rem;
    }

    .campaign-description {
        color: #666; /* Darker campaign description for contrast */
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
        background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }

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
        border-left: 4px solid #4CAF50;
    }

    .search-tips h4 {
        color: #4CAF50;
        margin-bottom: 1rem;
        font-weight: 600;
    }

    .search-tips ul {
        color: #666; /* Darker search tips list for contrast */
        margin: 0;
        padding-left: 1.5rem;
    }

    .search-tips li {
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }

    .welcome-banner {
        background-color: #e6ffe6; /* Light green background */
        padding: 15px 20px;
        margin-bottom: 20px;
        border-radius: 8px;
        text-align: center;
        font-size: 24px;
        font-weight: 600;
        color: #2d5a2d; /* Dark green text for contrast */
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)


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
        return False, f"Connection error: {str(e)}"


def safe_json_parse(response):
    try:
        return response.json()
    except:
        return {"detail": f"Server error (Status: {response.status_code})"}


def handle_oauth_callback():
    try:
        query_params = st.query_params

        access_token = query_params.get('access_token')
        if access_token:
            st.session_state.user_token = access_token

            user_info_str = query_params.get('user_info')
            if user_info_str:
                try:
                    st.session_state.user_info = json.loads(user_info_str)
                except json.JSONDecodeError:
                    st.session_state.user_info = {"name": "OAuth User", "email": "user@oauth.com"}
            else:
                st.session_state.user_info = {"name": "OAuth User", "email": "user@oauth.com"}

            if query_params.get('register_oauth') == 'true':
                st.session_state.current_page = 'complete_oauth_profile'
                st.success("Please complete your profile details.")
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
            google_available = status.get('google_oauth', {}).get('available', False)
            facebook_available = status.get('facebook_oauth', {}).get('available', False)
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
        <a href="{google_url}" class="html-oauth-google">
            <i class="fab fa-google"></i>{get_text('sign_in_google')}
        </a>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="html-oauth-google" style="background: #ccc; color: #666; cursor: not-allowed;">
            <i class="fab fa-google"></i>{get_text('sign_in_google')}
        </div>
        """, unsafe_allow_html=True)

    if facebook_available:
        st.markdown(f"""
        <a href="{facebook_url}" class="html-oauth-facebook">
            <i class="fab fa-facebook-f"></i>{get_text('sign_in_facebook')}
        </a>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="html-oauth-facebook" style="background: #ccc; color: #666; cursor: not-allowed;">
            <i class="fab fa-facebook-f"></i>{get_text('sign_in_facebook')}
        </div>
        """, unsafe_allow_html=True)


def login_user_backend(email, password):
    try:
        response = requests.post(
            f"{BACKEND_URL}/login",
            json={"email": email, "password": password},
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


def register_user_backend(user_data):
    try:
        response = requests.post(
            f"{BACKEND_URL}/register",
            json=user_data,
            timeout=15
        )

        if response.status_code == 200:
            st.success("Registration successful! Please login with your credentials.")
            st.session_state.current_page = 'login'
            st.rerun()
        else:
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
            st.success("Profile updated successfully!")
            st.session_state.user_info.update(user_data)
            st.session_state.current_page = 'home'
            st.rerun()
        else:
            error_data = safe_json_parse(response)
            st.error(f"Profile update failed: {error_data.get('detail', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
    except Exception as e:
        st.error(f"Profile update error: {str(e)}")


def render_user_profile():
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
    st.markdown('<div class="html-container">', unsafe_allow_html=True)

    st.markdown(f'<div class="html-title">{get_text("login")}</div>', unsafe_allow_html=True)

    with st.form(key='login_form'):
        email = st.text_input("", placeholder="Enter Your Email", key="login_email")
        password = st.text_input("", type="password", placeholder="Enter Your Password", key="login_password")

        submit_button = st.form_submit_button(get_text('continue'))

        if submit_button:
            if email and password:
                login_user_backend(email, password)
            else:
                st.error("Please fill in all fields")

    st.markdown(f"""
    <div class="html-option">
        {get_text('not_registered')}
        <a href="{FRONTEND_BASE_URL}?page=register" target="_blank">{get_text('create_account')}</a>
    </div>
    """, unsafe_allow_html=True)

    render_oauth_buttons(is_register_page=False)

    st.markdown('</div>', unsafe_allow_html=True)


def render_register_page():
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)

    st.markdown(f'<div class="html-title-register">{get_text("register")}</div>', unsafe_allow_html=True)

    with st.form(key='register_form'):

        registration_type = st.selectbox(
            "Select Registration Type",
            options=[get_text('individual'), get_text('organization')],
            key="reg_type_select"
        )

        if registration_type == get_text('individual'):
            # Changed back to f-string for simplicity and common usage, assuming previous error was transient or due to other factors.
            st.markdown(f"""<div class="html-form-box"><h3>{get_text("register_individual")}</h3></div>""",
                        unsafe_allow_html=True)

            full_name = st.text_input("", placeholder="Full Name", key="reg_full_name")
            email = st.text_input("", placeholder="Email ID", key="reg_email")
            phone = st.text_input("", placeholder="Phone Number", key="reg_phone")
            password = st.text_input("", type="password", placeholder="Password", key="reg_password")
            confirm_password = st.text_input("", type="password", placeholder="Confirm Password",
                                             key="reg_confirm_password")

            # This div closing tag was missing in the previous version, potentially causing rendering issues.
            # It should close the html-form-box opened above.
            # st.markdown('</div>', unsafe_allow_html=True) # This was commented out in previous version's thought process. Re-adding it.

            user_data_for_backend = {
                "email": email,
                "password": password,
                "user_type": "individual",
                "full_name": full_name,
                "phone": phone,
                "address": ""
            }
            is_valid_input = bool(full_name and email and phone and password and confirm_password)

        elif registration_type == get_text('organization'):
            # Changed back to f-string for simplicity and common usage.
            st.markdown(f"""<div class="html-form-box"><h3>{get_text("register_organization")}</h3></div>""",
                        unsafe_allow_html=True)

            org_name = st.text_input("", placeholder="Organization Name", key="reg_org_name")
            org_phone = st.text_input("", placeholder="Organization Phone Number", key="reg_org_phone")
            org_type = st.selectbox("",
                                    options=["", get_text('ngo'), get_text('startup'), get_text('charity')],
                                    key="reg_org_type_select")
            org_description = st.text_input("", placeholder=get_text('description'), key="reg_org_description")
            email = st.text_input("", placeholder="Email ID", key="reg_email_org")
            password = st.text_input("", type="password", placeholder="Password", key="reg_password_org")
            confirm_password = st.text_input("", type="password", placeholder="Confirm Password",
                                             key="reg_confirm_password_org")

            # This div closing tag was missing in the previous version, potentially causing rendering issues.
            # It should close the html-form-box opened above.
            # st.markdown('</div>', unsafe_allow_html=True) # This was commented out in previous version's thought process. Re-adding it.

            user_data_for_backend = {
                "email": email,
                "password": password,
                "user_type": "organization",
                "organization_name": org_name,
                "phone": org_phone,
                "organization_type": org_type,
                "description": org_description,
                "address": ""
            }
            is_valid_input = bool(org_name and org_phone and org_type and email and password and confirm_password)
        else:
            user_data_for_backend = {}
            is_valid_input = False

        submit_button = st.form_submit_button(get_text('register'))

        if submit_button:
            if not is_valid_input:
                st.error("Please fill in all required fields for the selected registration type.")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                register_user_backend(user_data_for_backend)

    st.markdown(f"""
    <div class="html-option">
        {get_text('already_have_account')}
        <a href="{FRONTEND_BASE_URL}?page=login" target="_blank">{get_text('sign_in_here')}</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="oauth-divider">
        <span>or sign up with social account</span>
    </div>
    """, unsafe_allow_html=True)

    render_oauth_buttons(is_register_page=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_complete_oauth_profile_page():
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)
    st.markdown(f'<div class="html-title-register">{get_text("complete_profile_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #333; text-align: center; margin-bottom: 20px;">{get_text("provide_details")}</p>',
                unsafe_allow_html=True)

    user_info = st.session_state.get('user_info', {})
    oauth_email = user_info.get('email', '')
    oauth_name = user_info.get('name', '')

    with st.form(key='complete_profile_form'):
        st.markdown(f"""<div class="html-form-wrapper">""", unsafe_allow_html=True)

        st.markdown(f"""<div class="html-form-box"><h3>OAuth Details</h3></div>""", unsafe_allow_html=True)
        st.text_input("Email", value=oauth_email, disabled=True, key="oauth_email_display")
        st.text_input("Name", value=oauth_name, disabled=True, key="oauth_name_display")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""<div class="html-form-box"><h3>Additional Details</h3></div>""", unsafe_allow_html=True)

        registration_type = st.selectbox(
            "Select Your User Type",
            options=[get_text('individual'), get_text('organization')],
            key="complete_reg_type_select"
        )

        if registration_type == get_text('individual'):
            phone = st.text_input("", placeholder="Phone Number", key="complete_phone")
            address = st.text_area("", placeholder="Address", key="complete_address")

            user_data_to_send = {
                "user_type": "individual",
                "phone": phone,
                "address": address,
                "email": oauth_email,
                "full_name": oauth_name
            }
            is_valid_input = bool(phone and address)

        elif registration_type == get_text('organization'):
            org_name = st.text_input("", placeholder="Organization Name", key="complete_org_name")
            org_phone = st.text_input("", placeholder="Organization Phone Number", key="complete_org_phone")
            org_type = st.selectbox("",
                                    options=["", get_text('ngo'), get_text('startup'), get_text('charity')],
                                    key="complete_org_type_select")
            org_description = st.text_input("", placeholder=get_text('description'), key="complete_org_description")
            address = st.text_area("", placeholder="Address", key="complete_address_org")

            user_data_to_send = {
                "user_type": "organization",
                "organization_name": org_name,
                "phone": org_phone,
                "organization_type": org_type,
                "description": org_description,
                "address": address,
                "email": oauth_email,
                "full_name": oauth_name
            }
            is_valid_input = bool(org_name and org_phone and org_type and org_description and address)

        else:
            user_data_to_send = {}
            is_valid_input = False

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        submit_button = st.form_submit_button(get_text('update_profile'))

        if submit_button:
            if not is_valid_input:
                st.error("Please fill in all required fields for your selected user type.")
            else:
                update_user_profile_backend(user_data_to_send, st.session_state.user_token)

    st.markdown('</div>', unsafe_allow_html=True)


def render_home_page():
    st.markdown(f'<h1 class="app-title">{get_text("welcome")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="app-subtitle">{get_text("platform_description")}</p>', unsafe_allow_html=True)

    st.markdown(f"## {get_text('trending_campaigns')}")

    campaigns = [
        {"title": "Clean Water Initiative", "description": "Providing clean water access to rural communities",
         "progress": 75, "raised": "$15,000", "goal": "$20,000"},
        {"title": "Education for All", "description": "Building schools in underserved areas", "progress": 60,
         "raised": "$30,000", "goal": "$50,000"},
        {"title": "Green Energy Project", "description": "Solar panel installation for villages", "progress": 40,
         "raised": "$8,000", "goal": "$20,000"}
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
            <div class="category-card">
                <div class="category-icon">
                    <i class="{category['icon']}"></i>
                </div>
                <div class="category-title">{category['name']}</div>
            </div>
            """, unsafe_allow_html=True)


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
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Select Language:</div>', unsafe_allow_html=True)
        language = st.selectbox(
            "Choose Language",
            options=list(TRANSLATIONS.keys()),
            index=list(TRANSLATIONS.keys()).index(st.session_state.language),
            key="language_selector"
        )

        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Backend Status:</div>', unsafe_allow_html=True)

        is_connected, status_message = check_backend_connection()
        if is_connected:
            st.markdown(f'<div class="status-connected">✅ {status_message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-disconnected">❌ {status_message}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.user_token:
            render_user_profile()

            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-title">Navigation:</div>', unsafe_allow_html=True)

            if st.session_state.current_page != 'home':
                if st.button(get_text("home"), key="nav_home"):
                    st.session_state.current_page = 'home'
                    st.rerun()

            if st.session_state.current_page != 'explore':
                if st.button(get_text("explore"), key="nav_explore"):
                    st.session_state.current_page = 'explore'
                    st.rerun()

            if st.session_state.current_page != 'search':
                if st.button(get_text("search"), key="nav_search"):
                    st.session_state.current_page = 'search'
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-title">Account:</div>', unsafe_allow_html=True)

            if st.session_state.current_page != 'login':
                if st.button(get_text('sign_in_here'), key="sidebar_login_btn"):
                    st.session_state.current_page = 'login'
                    st.rerun()

            if st.session_state.current_page != 'register':
                if st.button(get_text('create_account'), key="sidebar_register_btn"):
                    st.session_state.current_page = 'register'
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="HAVEN - Crowdfunding Platform",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    apply_custom_css()

    st.markdown('<div class="welcome-banner">Welcome to HAVEN Crowdfunding!</div>', unsafe_allow_html=True)

    handle_oauth_callback()

    query_params = st.query_params
    if 'page' in query_params:
        requested_page = query_params['page']
        if requested_page in ['login', 'register', 'home', 'explore', 'search', 'complete_oauth_profile']:
            st.session_state.current_page = requested_page

    render_sidebar()

    if st.session_state.current_page == 'login':
        render_login_page()
    elif st.session_state.current_page == 'register':
        render_register_page()
    elif st.session_state.current_page == 'complete_oauth_profile':
        render_complete_oauth_profile_page()
    elif st.session_state.current_page == 'home':
        render_home_page()
    elif st.session_state.current_page == 'explore':
        render_explore_page()
    elif st.session_state.current_page == 'search':
        render_search_page()
    else:
        st.session_state.current_page = 'login'
        render_login_page()


if __name__ == "__main__":
    main()