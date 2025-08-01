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
        'charity': 'Charity',
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
        'welcome_banner_tagline': 'కేవలం కొందరికి కాదు, మానవత్వానికి సహాయం చేయండి।',  # New key for the banner tagline
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
        'provide_details': 'మీ பதிவை முடிக்க கூடுதல் விவரங்களை வழங்கவும்।',
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
            background: transparent;
            color: #333 !important; /* Slightly darker input text for contrast */
            border-bottom: 2px solid #ccc;
            padding-left: 5px;
            font-family: 'Poppins', sans-serif;
        }

        .html-input-box input::placeholder {
            color: #777; /* Darker placeholder for contrast */
        }

        .stTextInput > div > div > input, .stSelectbox > div > div > select, .stTextArea > div > div > textarea {
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

        .stTextInput > div > div > input:focus, .stSelectbox > div > div > select:focus, .stTextArea > div > div > textarea:focus {
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
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .stSelectbox > label, .stTextInput > label, .stTextArea > label {
            font-weight: 500 !important;
            color: #333 !important;
            margin-bottom: 5px !important;
        }

        .st-emotion-cache-16txte5 {
            padding: 2rem 1rem !important;
        }

        .st-emotion-cache-p5m64f {
            font-family: 'Great Vibes', cursive;
            font-weight: 700;
            font-size: 4rem;
            color: #4CAF50;
            text-align: center;
        }

        .st-emotion-cache-1wq0s7a {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .welcome-banner {
            background: url("https://images.unsplash.com/photo-1549880338-65ddcdfd017b?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D") no-repeat center center;
            background-size: cover;
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            border-radius: 15px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .welcome-banner::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1;
        }

        .welcome-banner-content {
            position: relative;
            z-index: 2;
        }

        .welcome-banner-title {
            font-family: 'Poppins', sans-serif;
            font-size: 3rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 0.5rem;
        }

        .welcome-banner-tagline {
            font-size: 1.2rem;
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto;
        }

        .html-flex-container {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 20px;
        }

        .html-flex-item {
            flex: 1;
        }

        .custom-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            transition: all 0.3s ease-in-out;
        }

        .custom-card:hover {
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-5px);
        }

        .card-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2d5a2d;
            margin-bottom: 15px;
            position: relative;
        }

        .card-header::after {
            content: "";
            position: absolute;
            height: 3px;
            width: 50px;
            left: 0;
            bottom: -5px;
            background-color: #4CAF50;
            border-radius: 5px;
        }

        .card-content {
            font-size: 1rem;
            line-height: 1.6;
            color: #555;
        }

        .sidebar-logo {
            font-family: 'Great Vibes', cursive;
            font-weight: 700;
            font-size: 2rem;
            text-align: center;
            color: #4CAF50;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .st-emotion-cache-13sdm9 {
            padding: 1rem;
        }

        .st-emotion-cache-1629p8f {
            margin-top: 1.5rem !important;
        }

        .st-emotion-cache-13k656a {
            font-weight: 600 !important;
        }

        .st-emotion-cache-g18894 {
            flex-direction: row-reverse;
        }
    </style>
    """, unsafe_allow_html=True)


def handle_oauth_callback():
    query_params = st.query_params
    if "token" in query_params:
        try:
            token_json = json.loads(base64.b64decode(query_params["token"]).decode('utf-8'))
            st.session_state.user_token = token_json['access_token']
            st.session_state.user_info = token_json.get('user_info')

            # Determine the next page based on whether profile is complete
            if st.session_state.user_info and not st.session_state.user_info.get('profile_complete', False):
                st.session_state.current_page = 'complete_oauth_profile'
            else:
                st.session_state.current_page = 'home'

        except (json.JSONDecodeError, KeyError):
            st.error("Invalid token received from OAuth provider.")
            st.session_state.user_token = None
            st.session_state.user_info = None

        # Clear the query param to prevent re-processing on rerun
        st.query_params.clear()
        st.rerun()


def render_sidebar():
    st.sidebar.markdown('<div class="sidebar-logo">HAVEN</div>', unsafe_allow_html=True)
    if st.session_state.user_token:
        st.sidebar.page_link("front_main.py", label=get_text('home'), icon="🏠")
        st.sidebar.page_link("front_main.py", label=get_text('explore'), icon="🔍")
        st.sidebar.page_link("front_main.py", label=get_text('search'), icon="🔎")
        st.sidebar.page_link("front_main.py", label=get_text('profile'), icon="👤")
        st.sidebar.page_link("front_main.py", label=get_text('create_campaign'), icon="🚀")
        if st.sidebar.button(get_text('logout'), use_container_width=True):
            st.session_state.user_token = None
            st.session_state.user_info = None
            st.session_state.current_page = 'login'
            st.rerun()
    else:
        st.sidebar.page_link("front_main.py", label=get_text('login'), icon="🔒")
        st.sidebar.page_link("front_main.py", label=get_text('register'), icon="📝")


def render_login_page():
    # Login page UI
    st.markdown(f"""
        <div class="html-container">
            <h1 class="html-title">{get_text('login')}</h1>
            <p style="text-align: center; color: #555; margin-bottom: 20px;">{get_text('login_page_subtitle')}</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input(get_text('email'), key="login_email")
        password = st.text_input(get_text('password'), type="password", key="login_password")
        submitted = st.form_submit_button(get_text('login'))

        if submitted:
            # Mock API call
            login_data = {"email": email, "password": password}
            response = requests.post(f"{BACKEND_URL}/login", json=login_data)
            if response.status_code == 200:
                st.success("Login successful!")
                st.session_state.user_token = response.json().get("access_token")
                st.session_state.user_info = response.json().get("user")
                st.session_state.current_page = 'home'
                time.sleep(1)
                st.rerun()
            else:
                st.error("Login failed: " + response.json().get("detail", "Invalid credentials"))

    st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            {get_text('not_registered')} <a href="#" onclick="window.parent.postMessage('navigate-register', '*')">{get_text('create_account')}</a>
            <div style="margin: 20px 0; font-size: 0.9em; color: #888;">{get_text('oauth_divider')}</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.button(get_text('sign_in_google'), on_click=lambda: st.rerun())
    with col2:
        st.button(get_text('sign_in_facebook'), on_click=lambda: st.rerun())


def render_register_page():
    # Registration page UI
    st.markdown(f"""
        <div class="html-container-wide">
            <h1 class="html-title-register">{get_text('register')}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Use session state to control the selected registration type
    reg_type_options = [get_text('individual'), get_text('organization')]
    selected_reg_type = st.selectbox(
        get_text('registration_type'),
        options=reg_type_options,
        key='selected_reg_type_register',
        index=reg_type_options.index(st.session_state.selected_reg_type_register) if st.session_state.selected_reg_type_register in reg_type_options else 0
    )

    with st.form("register_form", clear_on_submit=True):
        st.session_state.selected_reg_type_register = selected_reg_type
        if selected_reg_type == get_text('individual'):
            st.subheader(get_text('register_individual'))
            full_name = st.text_input(get_text('full_name'), key="reg_ind_full_name")
            email = st.text_input(get_text('email'), key="reg_ind_email")
            phone = st.text_input(get_text('phone'), key="reg_ind_phone")
            password = st.text_input(get_text('password'), type="password", key="reg_ind_password")
            confirm_password = st.text_input(get_text('confirm_password'), type="password", key="reg_ind_confirm_password")
            address = st.text_area(get_text('address'), key="reg_ind_address")
        else:
            st.subheader(get_text('contact_person_details'))
            contact_person_name = st.text_input(get_text('full_name'), key="reg_org_contact_name")
            contact_person_email = st.text_input(get_text('email'), key="reg_org_contact_email")
            contact_person_phone = st.text_input(get_text('phone'), key="reg_org_contact_phone")
            password = st.text_input(get_text('password'), type="password", key="reg_org_password")
            confirm_password = st.text_input(get_text('confirm_password'), type="password", key="reg_org_confirm_password")

            st.subheader(get_text('organization_details'))
            organization_name = st.text_input(get_text('organization_name'), key="reg_org_name")
            organization_type = st.selectbox(
                get_text('organization_type'),
                options=[get_text('ngo'), get_text('startup'), get_text('charity')],
                key="reg_org_type"
            )
            description = st.text_area(get_text('description'), max_chars=100, key="reg_org_description")
            address = st.text_area(get_text('address'), key="reg_org_address")
            ngo_darpan_id = st.text_input("NGO Darpan ID (Optional)", key="reg_org_ngo_darpan")
            pan = st.text_input("PAN (Optional)", key="reg_org_pan")
            fcra_number = st.text_input("FCRA Number (Optional)", key="reg_org_fcra")

        submitted = st.form_submit_button(get_text('register'))

        if submitted:
            # Mock API call
            st.success("Registration successful! Please check your email for verification.")
            st.session_state.current_page = 'login'
            st.rerun()

    st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            {get_text('already_have_account')} <a href="#" onclick="window.parent.postMessage('navigate-login', '*')">{get_text('sign_in_here')}</a>
            <div style="margin: 20px 0; font-size: 0.9em; color: #888;">{get_text('oauth_divider_register')}</div>
        </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.button(get_text('sign_in_google'), on_click=lambda: st.rerun(), key='reg_google')
    with col2:
        st.button(get_text('sign_in_facebook'), on_click=lambda: st.rerun(), key='reg_facebook')


def render_complete_oauth_profile_page():
    st.markdown(f"""
        <div class="html-container-wide">
            <h1 class="html-title-register">{get_text('complete_profile_title')}</h1>
            <p style="text-align: center; color: #555; margin-bottom: 20px;">{get_text('provide_details')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Use session state to control the selected registration type for OAuth
    reg_type_options = [get_text('individual'), get_text('organization')]
    selected_reg_type = st.selectbox(
        get_text('registration_type'),
        options=reg_type_options,
        key='selected_reg_type_oauth',
        index=reg_type_options.index(st.session_state.selected_reg_type_oauth) if st.session_state.selected_reg_type_oauth in reg_type_options else 0
    )

    with st.form("complete_profile_form", clear_on_submit=False):
        st.session_state.selected_reg_type_oauth = selected_reg_type
        if selected_reg_type == get_text('individual'):
            st.subheader(get_text('contact_person_details'))
            full_name = st.text_input(get_text('full_name'), value=st.session_state.user_info.get('full_name', ''), key="oauth_ind_full_name")
            phone = st.text_input(get_text('phone'), key="oauth_ind_phone")
            address = st.text_area(get_text('address'), key="oauth_ind_address")
        else:
            st.subheader(get_text('contact_person_details'))
            contact_person_name = st.text_input(get_text('full_name'), value=st.session_state.user_info.get('full_name', ''), key="oauth_org_contact_name")
            contact_person_phone = st.text_input(get_text('phone'), key="oauth_org_contact_phone")

            st.subheader(get_text('organization_details'))
            organization_name = st.text_input(get_text('organization_name'), key="oauth_org_name")
            organization_type = st.selectbox(
                get_text('organization_type'),
                options=[get_text('ngo'), get_text('startup'), get_text('charity')],
                key="oauth_org_type"
            )
            description = st.text_area(get_text('description'), max_chars=100, key="oauth_org_description")
            address = st.text_area(get_text('address'), key="oauth_org_address")
            ngo_darpan_id = st.text_input("NGO Darpan ID (Optional)", key="oauth_org_ngo_darpan")
            pan = st.text_input("PAN (Optional)", key="oauth_org_pan")
            fcra_number = st.text_input("FCRA Number (Optional)", key="oauth_org_fcra")
        
        submitted = st.form_submit_button(get_text('submit'))

        if submitted:
            st.success("Profile updated successfully!")
            st.session_state.current_page = 'home'
            st.rerun()


def render_home_page():
    # Home page UI
    st.markdown(f"""
    <div class="welcome-banner">
        <div class="welcome-banner-content">
            <div class="welcome-banner-title">{get_text("welcome_banner_text")}</div>
            <div class="welcome-banner-tagline">{get_text("welcome_banner_tagline")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h2 class='card-header'>{get_text('trending_campaigns')}</h2>", unsafe_allow_html=True)
    # The actual campaign data would be fetched from the backend here
    # Example:
    # campaigns_data = requests.get(f"{BACKEND_URL}/campaigns/trending").json()
    st.info("This is where trending campaigns will be displayed after being fetched from the backend.")

    st.markdown(f"<h2 class='card-header'>{get_text('explore_categories')}</h2>", unsafe_allow_html=True)
    # The categories would be listed here
    st.info("This is where categories will be displayed.")


def render_explore_page():
    st.markdown(f"<h1 class='html-title-register'>{get_text('explore')}</h1>", unsafe_allow_html=True)
    st.info("Here you will find a list of all campaigns.")


def render_search_page():
    st.markdown(f"<h1 class='html-title-register'>{get_text('search')}</h1>", unsafe_allow_html=True)
    st.text_input(get_text('search_campaigns'), placeholder=get_text('search_placeholder'))
    st.markdown(f"**{get_text('search_tips')}**")
    st.info(f"""
        - {get_text('use_keywords')}
        - {get_text('filter_category')}
        - {get_text('check_spelling')}
    """)


def render_create_campaign_page():
    st.markdown(f"<h1 class='html-title-register'>{get_text('create_campaign')}</h1>", unsafe_allow_html=True)

    if st.session_state.user_info and st.session_state.user_info.get('account_type') == get_text('organization'):
        with st.form("create_campaign_form", clear_on_submit=True):
            campaign_name = st.text_input(get_text('campaign_name'))
            campaign_description = st.text_area(get_text('campaign_description_full'))
            goal_amount = st.number_input(get_text('goal_amount'), min_value=1)
            campaign_category = st.selectbox(get_text('campaign_category'), options=['Health', 'Education', 'Environment', 'Technology', 'Arts & Culture', 'Community'])
            campaign_image = st.file_uploader(get_text('upload_image'), type=['png', 'jpg', 'jpeg'])

            submitted = st.form_submit_button(get_text('submit_campaign'))

            if submitted:
                if not all([campaign_name, campaign_description, goal_amount, campaign_category, campaign_image]):
                    st.error("Please fill in all the fields.")
                else:
                    # Mock API call
                    st.success(get_text('campaign_creation_success'))
                    # In a real app, you would send the data to your backend
    else:
        st.error(get_text('only_org_can_create_campaign'))


def render_profile_page():
    st.markdown(f"<h1 class='html-title-register'>{get_text('profile')}</h1>", unsafe_allow_html=True)
    st.info("This is the profile page where user details and created campaigns will be shown.")

    if st.session_state.user_info:
        st.subheader("User Information")
        st.json(st.session_state.user_info)

        # Example of fetching user-specific campaigns
        st.subheader("My Campaigns")
        st.info("This section would show campaigns created by the user.")


def render_main_page():
    # main page where we handle the routing
    apply_custom_css()
    
    st.markdown("""<div class="welcome-banner">
                    <div class="welcome-banner-content">
                        <div class="welcome-banner-title">{get_text("welcome_banner_text")}</div>
                        <div class="welcome-banner-tagline">{get_text("welcome_banner_tagline")}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    handle_oauth_callback()

    query_params = st.query_params
    if 'page' in query_params:
        requested_page = query_params['page']
        if requested_page in ['login', 'register', 'home', 'explore', 'search', 'complete_oauth_profile',
                              'create_campaign', 'profile']:
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
        elif st.session_state.current_page == 'profile':
            render_profile_page()
        else:
            st.session_state.current_page = 'login'
            render_login_page()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state.current_page = 'login'
        st.rerun()


if __name__ == "__main__":
    render_main_page()
