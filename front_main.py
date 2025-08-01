import streamlit as st
import requests
import json
import base64
import time
import os
import re
from urllib.parse import urlencode, parse_qs, urlparse

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
        'provide_details': 'మీ పతిவను పూర్తి చేయడానికి దయచేసి అదనపు వివరాలను అందించండి.',
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
        padding: 0 15px;
        border-radius: 5px;
        border-bottom: 2px solid #ccc;
        background: #f9f9f9;
        transition: all 0.3s ease;
    }

    .html-input-box input:focus, .html-input-box select:focus {
        border-bottom-color: #4CAF50;
        background: #fff;
    }

    .html-input-box label {
        position: absolute;
        top: 50%;
        left: 15px;
        color: #999;
        font-weight: 400;
        font-size: 16px;
        pointer-events: none;
        transform: translateY(-50%);
        transition: all 0.3s ease;
    }

    .html-input-box input:focus ~ label,
    .html-input-box input:valid ~ label,
    .html-input-box select:focus ~ label,
    .html-input-box select:valid ~ label {
        top: 0px;
        left: 15px;
        color: #4CAF50;
        font-size: 12px;
        font-weight: 500;
        background: #fff;
        padding: 0 5px;
    }

    .html-button {
        width: 100%;
        height: 45px;
        background: linear-gradient(135deg, #4CAF50, #388E3C);
        border: none;
        outline: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        color: #fff;
        font-weight: 500;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        margin-top: 20px;
    }

    .html-button:hover {
        background: linear-gradient(135deg, #388E3C, #2E7D32);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
    }

    .html-link {
        color: #4CAF50;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .html-link:hover {
        color: #388E3C;
        text-decoration: underline;
    }

    .html-text {
        text-align: center;
        margin: 20px 0 10px 0;
        color: #666;
    }

    .html-or {
        text-align: center;
        margin: 20px 0;
        position: relative;
        color: #999;
    }

    .html-or:before {
        content: "";
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background: #ddd;
    }

    .html-or span {
        background: #fff;
        padding: 0 15px;
        position: relative;
    }

    .social-button {
        width: 100%;
        height: 45px;
        border: 2px solid #ddd;
        background: #fff;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        color: #333;
        font-weight: 500;
        margin-top: 10px;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    .social-button:hover {
        border-color: #4CAF50;
        background: #f8f8f8;
    }

    .google-button:hover {
        border-color: #db4437;
        color: #db4437;
    }

    .facebook-button:hover {
        border-color: #3b5998;
        color: #3b5998;
    }

    .registration-type-selector {
        display: flex;
        gap: 10px;
        margin: 20px 0;
    }

    .registration-type-option {
        flex: 1;
        padding: 15px;
        border: 2px solid #ddd;
        border-radius: 5px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        background: #fff;
    }

    .registration-type-option:hover {
        border-color: #4CAF50;
        background: #f8f8f8;
    }

    .registration-type-option.selected {
        border-color: #4CAF50;
        background: #e8f5e8;
        color: #2d5a2d;
        font-weight: 600;
    }

    .welcome-banner-main-title {
        font-family: 'Great Vibes', cursive;
        font-size: 4rem;
        font-weight: 400;
        text-align: center;
        color: #2d5a2d;
        margin: 20px 0 10px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .welcome-banner-tagline {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        font-weight: 300;
        text-align: center;
        color: #555;
        margin: 0 0 30px 0;
        font-style: italic;
    }

    .sidebar-section {
        margin-bottom: 20px;
        padding: 15px;
        background: #fff;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .sidebar-title {
        font-weight: 600;
        color: #2d5a2d;
        margin-bottom: 10px;
        font-size: 16px;
    }

    .status-connected {
        color: #4CAF50;
        font-weight: 500;
    }

    .status-disconnected {
        color: #f44336;
        font-weight: 500;
    }

    .user-profile {
        padding: 15px;
        background: linear-gradient(135deg, #4CAF50, #388E3C);
        border-radius: 5px;
        color: white;
        margin-bottom: 20px;
    }

    .user-profile h3 {
        margin: 0 0 5px 0;
        font-size: 18px;
    }

    .user-profile p {
        margin: 0;
        opacity: 0.9;
        font-size: 14px;
    }

    .campaign-card {
        background: #fff;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }

    .campaign-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    .campaign-title {
        font-size: 20px;
        font-weight: 600;
        color: #2d5a2d;
        margin-bottom: 10px;
    }

    .campaign-description {
        color: #666;
        margin-bottom: 15px;
        line-height: 1.5;
    }

    .campaign-progress {
        background: #f0f0f0;
        border-radius: 10px;
        height: 8px;
        margin: 10px 0;
        overflow: hidden;
    }

    .campaign-progress-bar {
        background: linear-gradient(90deg, #4CAF50, #388E3C);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }

    .campaign-stats {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
        font-size: 14px;
    }

    .campaign-stat {
        text-align: center;
    }

    .campaign-stat-value {
        font-weight: 600;
        color: #2d5a2d;
        display: block;
    }

    .campaign-stat-label {
        color: #666;
        font-size: 12px;
    }

    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }

    .category-card {
        background: #fff;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
    }

    .category-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        border-color: #4CAF50;
    }

    .category-icon {
        font-size: 2rem;
        margin-bottom: 10px;
        color: #4CAF50;
    }

    .category-name {
        font-weight: 600;
        color: #2d5a2d;
    }

    .search-container {
        background: #fff;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .search-input {
        width: 100%;
        padding: 15px;
        border: 2px solid #ddd;
        border-radius: 5px;
        font-size: 16px;
        transition: border-color 0.3s ease;
    }

    .search-input:focus {
        outline: none;
        border-color: #4CAF50;
    }

    .search-tips {
        margin-top: 20px;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 5px;
        border-left: 4px solid #4CAF50;
    }

    .search-tips h4 {
        margin: 0 0 10px 0;
        color: #2d5a2d;
        font-size: 16px;
    }

    .search-tips ul {
        margin: 0;
        padding-left: 20px;
    }

    .search-tips li {
        margin: 5px 0;
        color: #666;
    }

    .create-campaign-button {
        width: 100%;
        background: linear-gradient(135deg, #FF6B35, #F7931E);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 5px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 10px;
    }

    .create-campaign-button:hover {
        background: linear-gradient(135deg, #F7931E, #FF6B35);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 53, 0.4);
    }

    .file-upload-area {
        border: 2px dashed #ddd;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        transition: border-color 0.3s ease;
        cursor: pointer;
    }

    .file-upload-area:hover {
        border-color: #4CAF50;
        background: #f8f9fa;
    }

    .file-upload-area.dragover {
        border-color: #4CAF50;
        background: #e8f5e8;
    }

    .error-message {
        background: #ffebee;
        color: #c62828;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #c62828;
    }

    .success-message {
        background: #e8f5e8;
        color: #2e7d32;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #4CAF50;
    }

    .info-message {
        background: #e3f2fd;
        color: #1565c0;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #2196f3;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .html-container {
            margin: 10px;
            padding: 15px;
        }

        .html-container-wide {
            margin: 10px;
            padding: 20px;
        }

        .welcome-banner-main-title {
            font-size: 2.5rem;
        }

        .welcome-banner-tagline {
            font-size: 1rem;
        }

        .category-grid {
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
        }

        .registration-type-selector {
            flex-direction: column;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def check_backend_connection():
    """Check if the backend is accessible"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, "Connected"
        else:
            return False, f"Error {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, "Disconnected"


def login_user_backend(id_token):
    """Login user using Firebase ID token"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json={"id_token": id_token},
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.user_token = data.get("access_token")
            st.session_state.user_info = data.get("user")
            st.session_state.current_page = 'home'
            st.success("Login successful!")
            st.rerun()
        else:
            error_data = response.json()
            st.error(f"Login failed: {error_data.get('detail', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Network error during login: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error during login: {str(e)}")


def register_user_backend(id_token, user_type, individual_data=None, organization_data=None):
    """Register user using Firebase ID token and additional data"""
    try:
        payload = {
            "id_token": id_token,
            "user_type": user_type
        }

        if user_type == "individual" and individual_data:
            payload["individual_data"] = individual_data
        elif user_type == "organization" and organization_data:
            payload["organization_data"] = organization_data

        response = requests.post(
            f"{BACKEND_URL}/auth/register",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 201:
            data = response.json()
            st.session_state.user_token = data.get("access_token")
            st.session_state.user_info = data.get("user")
            st.session_state.current_page = 'home'
            st.success("Registration successful!")
            st.rerun()
        else:
            error_data = response.json()
            st.error(f"Registration failed: {error_data.get('detail', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Network error during registration: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error during registration: {str(e)}")


def get_firebase_auth_html(action="login"):
    """Generate Firebase authentication HTML"""
    config_json = json.dumps(FIREBASE_CONFIG)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
        <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"></script>
    </head>
    <body>
        <div id="firebaseui-auth-container"></div>
        <script>
            const firebaseConfig = {config_json};
            firebase.initializeApp(firebaseConfig);

            const auth = firebase.auth();
            const googleProvider = new firebase.auth.GoogleAuthProvider();
            const facebookProvider = new firebase.auth.FacebookAuthProvider();

            function sendMessageToStreamlit(message) {{
                window.parent.postMessage({{
                    streamlit: true,
                    type: "SET_PAGE_STATE",
                    payload: message
                }}, "*");
            }}

            function signInWithGoogle() {{
                auth.signInWithPopup(googleProvider)
                    .then((result) => {{
                        return result.user.getIdToken();
                    }})
                    .then((idToken) => {{
                        sendMessageToStreamlit({{
                            action: "{action}",
                            id_token: idToken
                        }});
                    }})
                    .catch((error) => {{
                        console.error("Google sign-in error:", error);
                        sendMessageToStreamlit({{
                            action: "{action}_error",
                            error: error.message
                        }});
                    }});
            }}

            function signInWithFacebook() {{
                auth.signInWithPopup(facebookProvider)
                    .then((result) => {{
                        return result.user.getIdToken();
                    }})
                    .then((idToken) => {{
                        sendMessageToStreamlit({{
                            action: "{action}",
                            id_token: idToken
                        }});
                    }})
                    .catch((error) => {{
                        console.error("Facebook sign-in error:", error);
                        sendMessageToStreamlit({{
                            action: "{action}_error",
                            error: error.message
                        }});
                    }});
            }}

            function signOut() {{
                auth.signOut()
                    .then(() => {{
                        sendMessageToStreamlit({{
                            action: "logout_success"
                        }});
                    }})
                    .catch((error) => {{
                        console.error("Sign-out error:", error);
                        sendMessageToStreamlit({{
                            action: "logout_error",
                            error: error.message
                        }});
                    }});
            }}

            // Make functions globally available
            window.signInWithGoogle = signInWithGoogle;
            window.signInWithFacebook = signInWithFacebook;
            window.signOut = signOut;
        </script>
    </body>
    </html>
    """


def render_login_page():
    st.markdown('<div class="html-container">', unsafe_allow_html=True)

    st.markdown(f'<div class="html-title">{get_text("login")}</div>', unsafe_allow_html=True)

    # Email/Password Login Form
    with st.form("login_form"):
        email = st.text_input(get_text("email"), key="login_email")
        password = st.text_input(get_text("password"), type="password", key="login_password")

        if st.form_submit_button(get_text("continue"), use_container_width=True):
            if email and password:
                # Here you would typically validate credentials
                # For now, we'll show a placeholder message
                st.info("Email/password login not implemented yet. Please use social login.")
            else:
                st.error("Please fill in all fields.")

    st.markdown(f'<div class="html-or"><span>OR</span></div>', unsafe_allow_html=True)

    # Social Login Buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 " + get_text("sign_in_google"), key="google_login", use_container_width=True):
            # Embed Firebase auth component
            firebase_html = get_firebase_auth_html("login")
            st.components.v1.html(f"""
                {firebase_html}
                <script>
                    setTimeout(() => {{
                        signInWithGoogle();
                    }}, 100);
                </script>
            """, height=0, width=0)

    with col2:
        if st.button("📘 " + get_text("sign_in_facebook"), key="facebook_login", use_container_width=True):
            # Embed Firebase auth component
            firebase_html = get_firebase_auth_html("login")
            st.components.v1.html(f"""
                {firebase_html}
                <script>
                    setTimeout(() => {{
                        signInWithFacebook();
                    }}, 100);
                </script>
            """, height=0, width=0)

    st.markdown(f'''
        <div class="html-text">
            {get_text("not_registered")} 
            <a href="?page=register" class="html-link">{get_text("create_account")}</a>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_register_page():
    st.markdown('<div class="html-container">', unsafe_allow_html=True)

    st.markdown(f'<div class="html-title-register">{get_text("register")}</div>', unsafe_allow_html=True)

    # Registration Type Selection
    st.markdown(f'<div style="margin-bottom: 20px; font-weight: 500;">{get_text("registration_type")}:</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("individual"), key="reg_individual", use_container_width=True):
            st.session_state.selected_reg_type_register = get_text("individual")
            st.rerun()

    with col2:
        if st.button(get_text("organization"), key="reg_organization", use_container_width=True):
            st.session_state.selected_reg_type_register = get_text("organization")
            st.rerun()

    # Show selected type
    if st.session_state.selected_reg_type_register:
        st.markdown(f'<div style="text-align: center; margin: 10px 0; color: #4CAF50; font-weight: 500;">Selected: {st.session_state.selected_reg_type_register}</div>',
                    unsafe_allow_html=True)

    # Registration Form
    if st.session_state.selected_reg_type_register == get_text("individual"):
        with st.form("individual_register_form"):
            st.subheader(get_text("register_individual"))
            full_name = st.text_input(get_text("full_name"), key="reg_full_name")
            email = st.text_input(get_text("email"), key="reg_email")
            password = st.text_input(get_text("password"), type="password", key="reg_password")
            confirm_password = st.text_input(get_text("confirm_password"), type="password", key="reg_confirm_password")
            phone = st.text_input(get_text("phone"), key="reg_phone")
            address = st.text_area(get_text("address"), key="reg_address")

            if st.form_submit_button(get_text("continue"), use_container_width=True):
                if all([full_name, email, password, confirm_password, phone, address]):
                    if password == confirm_password:
                        # Store temporary registration data
                        st.session_state.temp_registration_data = {
                            'user_type': 'individual',
                            'individual_data': {
                                'full_name': full_name,
                                'email': email,
                                'phone': phone,
                                'address': address
                            }
                        }
                        st.info("Please complete registration using social login below.")
                    else:
                        st.error("Passwords do not match.")
                else:
                    st.error("Please fill in all fields.")

    elif st.session_state.selected_reg_type_register == get_text("organization"):
        with st.form("organization_register_form"):
            st.subheader(get_text("register_organization"))
            org_name = st.text_input(get_text("organization_name"), key="reg_org_name")
            org_type = st.selectbox(get_text("organization_type"),
                                    [get_text("ngo"), get_text("startup"), get_text("charity")], key="reg_org_type")
            contact_name = st.text_input(get_text("full_name"), key="reg_contact_name")
            email = st.text_input(get_text("email"), key="reg_org_email")
            password = st.text_input(get_text("password"), type="password", key="reg_org_password")
            confirm_password = st.text_input(get_text("confirm_password"), type="password",
                                             key="reg_org_confirm_password")
            phone = st.text_input(get_text("phone"), key="reg_org_phone")
            address = st.text_area(get_text("address"), key="reg_org_address")
            description = st.text_area(get_text("description"), max_chars=100, key="reg_org_description")

            if st.form_submit_button(get_text("continue"), use_container_width=True):
                if all([org_name, org_type, contact_name, email, password, confirm_password, phone, address, description]):
                    if password == confirm_password:
                        # Store temporary registration data
                        st.session_state.temp_registration_data = {
                            'user_type': 'organization',
                            'organization_data': {
                                'organization_name': org_name,
                                'organization_type': org_type,
                                'contact_person_name': contact_name,
                                'email': email,
                                'phone': phone,
                                'address': address,
                                'description': description
                            }
                        }
                        st.info("Please complete registration using social login below.")
                    else:
                        st.error("Passwords do not match.")
                else:
                    st.error("Please fill in all fields.")

    # Social Registration Buttons (only show if registration type is selected and temp data exists)
    if st.session_state.selected_reg_type_register and 'temp_registration_data' in st.session_state:
        st.markdown(f'<div class="html-or"><span>Complete with Social Login</span></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 " + get_text("sign_in_google"), key="google_register", use_container_width=True):
                firebase_html = get_firebase_auth_html("register")
                st.components.v1.html(f"""
                    {firebase_html}
                    <script>
                        setTimeout(() => {{
                            signInWithGoogle();
                        }}, 100);
                    </script>
                """, height=0, width=0)

        with col2:
            if st.button("📘 " + get_text("sign_in_facebook"), key="facebook_register", use_container_width=True):
                firebase_html = get_firebase_auth_html("register")
                st.components.v1.html(f"""
                    {firebase_html}
                    <script>
                        setTimeout(() => {{
                            signInWithFacebook();
                        }}, 100);
                    </script>
                """, height=0, width=0)

    st.markdown(f'''
        <div class="html-text">
            {get_text("already_have_account")} 
            <a href="?page=login" class="html-link">{get_text("sign_in_here")}</a>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def handle_oauth_callback():
    """Handle OAuth callback and redirect to profile completion if needed"""
    query_params = st.query_params
    if 'oauth_complete' in query_params and query_params['oauth_complete'] == 'true':
        # User completed OAuth but needs to complete profile
        st.session_state.current_page = 'complete_oauth_profile'
        # Clear the query param to avoid re-processing
        st.query_params.clear()
        st.rerun()


def render_complete_oauth_profile_page():
    """Render page for completing profile after OAuth login"""
    st.markdown('<div class="html-container">', unsafe_allow_html=True)

    st.markdown(f'<div class="html-title">{get_text("complete_profile_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<p>{get_text("provide_details")}</p>', unsafe_allow_html=True)

    # Registration Type Selection for OAuth completion
    st.markdown(f'<div style="margin-bottom: 20px; font-weight: 500;">{get_text("registration_type")}:</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("individual"), key="oauth_individual", use_container_width=True):
            st.session_state.selected_reg_type_oauth = get_text("individual")
            st.rerun()

    with col2:
        if st.button(get_text("organization"), key="oauth_organization", use_container_width=True):
            st.session_state.selected_reg_type_oauth = get_text("organization")
            st.rerun()

    # Show selected type
    if st.session_state.selected_reg_type_oauth:
        st.markdown(f'<div style="text-align: center; margin: 10px 0; color: #4CAF50; font-weight: 500;">Selected: {st.session_state.selected_reg_type_oauth}</div>',
                    unsafe_allow_html=True)

    # Profile completion forms
    if st.session_state.selected_reg_type_oauth == get_text("individual"):
        with st.form("complete_individual_profile"):
            st.subheader(get_text("contact_person_details"))
            phone = st.text_input(get_text("phone"), key="complete_phone")
            address = st.text_area(get_text("address"), key="complete_address")

            if st.form_submit_button(get_text("update_profile"), use_container_width=True):
                if phone and address:
                    # Here you would update the user profile via API
                    st.success("Profile completed successfully!")
                    st.session_state.current_page = 'home'
                    st.rerun()
                else:
                    st.error("Please fill in all fields.")

    elif st.session_state.selected_reg_type_oauth == get_text("organization"):
        with st.form("complete_organization_profile"):
            col1, col2 = st.columns(2)

            with col1:
                st.subheader(get_text("contact_person_details"))
                contact_phone = st.text_input(get_text("phone"), key="complete_contact_phone")
                contact_address = st.text_area(get_text("address"), key="complete_contact_address")

            with col2:
                st.subheader(get_text("organization_details"))
                org_name = st.text_input(get_text("organization_name"), key="complete_org_name")
                org_type = st.selectbox(get_text("organization_type"),
                                        [get_text("ngo"), get_text("startup"), get_text("charity")],
                                        key="complete_org_type")
                org_description = st.text_area(get_text("description"), max_chars=100, key="complete_org_description")

            if st.form_submit_button(get_text("update_profile"), use_container_width=True):
                if all([contact_phone, contact_address, org_name, org_type, org_description]):
                    # Here you would update the user profile via API
                    st.success("Profile completed successfully!")
                    st.session_state.current_page = 'home'
                    st.rerun()
                else:
                    st.error("Please fill in all fields.")

    st.markdown('</div>', unsafe_allow_html=True)


def render_home_page():
    """Render the home page with trending campaigns"""
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)

    st.markdown(f'<h2 style="color: #2d5a2d; margin-bottom: 20px;">{get_text("trending_campaigns")}</h2>',
                unsafe_allow_html=True)

    # Mock campaign data
    campaigns = [
        {
            "title": "Clean Water for Rural Communities",
            "description": "Providing clean drinking water access to remote villages through sustainable well construction and water purification systems.",
            "goal": 50000,
            "raised": 32500,
            "backers": 245,
            "days_left": 15,
            "category": "Environment"
        },
        {
            "title": "Education for Underprivileged Children",
            "description": "Supporting education initiatives by providing school supplies, books, and learning materials to children in need.",
            "goal": 25000,
            "raised": 18750,
            "backers": 156,
            "days_left": 22,
            "category": "Education"
        },
        {
            "title": "Medical Equipment for Local Hospital",
            "description": "Fundraising for essential medical equipment to improve healthcare services in our community hospital.",
            "goal": 75000,
            "raised": 45000,
            "backers": 189,
            "days_left": 8,
            "category": "Health"
        }
    ]

    for campaign in campaigns:
        progress_percentage = (campaign["raised"] / campaign["goal"]) * 100

        st.markdown(f'''
            <div class="campaign-card">
                <div class="campaign-title">{campaign["title"]}</div>
                <div class="campaign-description">{campaign["description"]}</div>
                <div class="campaign-progress">
                    <div class="campaign-progress-bar" style="width: {progress_percentage}%"></div>
                </div>
                <div class="campaign-stats">
                    <div class="campaign-stat">
                        <span class="campaign-stat-value">${campaign["raised"]:,}</span>
                        <span class="campaign-stat-label">Raised</span>
                    </div>
                    <div class="campaign-stat">
                        <span class="campaign-stat-value">{progress_percentage:.1f}%</span>
                        <span class="campaign-stat-label">of ${campaign["goal"]:,}</span>
                    </div>
                    <div class="campaign-stat">
                        <span class="campaign-stat-value">{campaign["backers"]}</span>
                        <span class="campaign-stat-label">Backers</span>
                    </div>
                    <div class="campaign-stat">
                        <span class="campaign-stat-value">{campaign["days_left"]}</span>
                        <span class="campaign-stat-label">Days Left</span>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_explore_page():
    """Render the explore page with categories"""
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)

    st.markdown(f'<h2 style="color: #2d5a2d; margin-bottom: 20px;">{get_text("categories")}</h2>',
                unsafe_allow_html=True)

    # Categories with icons
    categories = [
        {"name": get_text("technology"), "icon": "💻"},
        {"name": get_text("health"), "icon": "🏥"},
        {"name": get_text("education"), "icon": "📚"},
        {"name": get_text("environment"), "icon": "🌱"},
        {"name": get_text("arts"), "icon": "🎨"},
        {"name": get_text("community"), "icon": "🤝"}
    ]

    # Create category grid
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            st.markdown(f'''
                <div class="category-card">
                    <div class="category-icon">{category["icon"]}</div>
                    <div class="category-name">{category["name"]}</div>
                </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_search_page():
    """Render the search page"""
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)

    st.markdown(f'<h2 style="color: #2d5a2d; margin-bottom: 20px;">{get_text("search_campaigns")}</h2>',
                unsafe_allow_html=True)

    # Search input
    search_query = st.text_input(
        "",
        placeholder=get_text("search_placeholder"),
        key="search_input"
    )

    if search_query:
        st.markdown(f'<p>Searching for: <strong>{search_query}</strong></p>', unsafe_allow_html=True)
        st.info("Search functionality will be implemented with backend integration.")

    # Search tips
    st.markdown(f'''
        <div class="search-tips">
            <h4><i class="fas fa-lightbulb"></i> {get_text("search_tips")}</h4>
            <ul>
                <li>{get_text("use_keywords")}</li>
                <li>{get_text("filter_category")}</li>
                <li>{get_text("check_spelling")}</li>
            </ul>
        </div>
    ''', unsafe_allow_html=True)

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

            render_create_campaign_button()


def handle_js_messages():
    """Handles messages posted from JavaScript to Streamlit."""
    if "js_message" in st.session_state:
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
                    del st.session_state.temp_registration_data  # Clear temp data
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


def render_user_profile():
    """Render user profile in sidebar"""
    if st.session_state.user_info:
        user = st.session_state.user_info
        st.markdown(f'''
            <div class="user-profile">
                <h3>{user.get("name", "User")}</h3>
                <p>{user.get("email", "")}</p>
            </div>
        ''', unsafe_allow_html=True)

        if st.button(get_text("logout"), key="logout_button", use_container_width=True):
            firebase_html = get_firebase_auth_html("logout")
            st.components.v1.html(f"""
                {firebase_html}
                <script>
                    setTimeout(() => {{
                        signOut();
                    }}, 100);
                </script>
            """, height=0, width=0)


def render_create_campaign_button():
    """Render create campaign button in sidebar"""
    if st.session_state.user_info:
        user = st.session_state.user_info
        # Check if user is an organization
        if user.get("user_type") == "organization":
            if st.button(get_text("create_campaign"), key="create_campaign_nav", use_container_width=True):
                st.session_state.current_page = 'create_campaign'
                st.rerun()
        else:
            st.markdown(f'<div style="text-align: center; color: #666; font-size: 12px; margin-top: 10px;">{get_text("only_org_can_create_campaign")}</div>',
                        unsafe_allow_html=True)


def render_create_campaign_page():
    """Render the create campaign page"""
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)

    st.markdown(f'<h2 style="color: #2d5a2d; margin-bottom: 20px;">{get_text("create_campaign")}</h2>',
                unsafe_allow_html=True)

    # Check if user is authorized to create campaigns
    if not st.session_state.user_info or st.session_state.user_info.get("user_type") != "organization":
        st.error(get_text("only_org_can_create_campaign"))
        st.markdown('</div>', unsafe_allow_html=True)
        return

    with st.form("create_campaign_form"):
        campaign_name = st.text_input(get_text("campaign_name"), key="campaign_name")
        campaign_description = st.text_area(get_text("campaign_description_full"), key="campaign_description", height=150)
        goal_amount = st.number_input(get_text("goal_amount"), min_value=1, step=1, key="goal_amount")

        category = st.selectbox(
            get_text("campaign_category"),
            [get_text("technology"), get_text("health"), get_text("education"),
             get_text("environment"), get_text("arts"), get_text("community")],
            key="campaign_category"
        )

        # File upload for campaign image
        st.markdown(f'<div style="margin: 20px 0; font-weight: 500;">{get_text("upload_image")}:</div>',
                    unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key="campaign_image")

        if st.form_submit_button(get_text("submit_campaign"), use_container_width=True):
            if all([campaign_name, campaign_description, goal_amount, category]):
                # Here you would create the campaign via API
                try:
                    # Mock campaign creation
                    st.success(get_text("campaign_creation_success"))
                    st.session_state.current_page = 'home'
                    st.rerun()
                except Exception as e:
                    st.error(f'{get_text("campaign_creation_failed")} {str(e)}')
            else:
                st.error("Please fill in all required fields.")

    st.markdown('</div>', unsafe_allow_html=True)


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
window.addEventListener('message', event => {
    if (event.data.streamlit) {
        // Forward the message to Python session state
        window.parent.postMessage(event.data, '*');
    }
});
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
            st.rerun()  # Rerun to process the message
        except json.JSONDecodeError:
            pass  # Ignore malformed messages

    handle_js_messages()  # Process any messages received

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
            st.rerun()  # Rerun to navigate to the correct page

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


if __name__ == "__main__":
    main()

