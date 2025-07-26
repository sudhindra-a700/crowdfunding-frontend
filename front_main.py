import streamlit as st
import requests
import os
import json
import re
import time
from urllib.parse import urlencode, parse_qs
import base64

# Set page config for wide layout and initial title
st.set_page_config(layout="wide", page_title="HAVEN Crowdfunding")


# --- OAuth Service Integration --- #
class StreamlitOAuthService:
    """OAuth service specifically designed for Streamlit applications"""

    def __init__(self):
        self.backend_url = "https://srv-d1sq8ser433s73eke7v0.onrender.com"  # Your Render backend URL
        self.token_key = 'oauth_access_token'
        self.user_key = 'oauth_user_profile'

    def is_authenticated(self):
        """Check if user is authenticated"""
        token = st.session_state.get(self.token_key)
        if not token:
            return False

        try:
            # Simple JWT expiration check
            payload = json.loads(base64.b64decode(token.split('.')[1] + '=='))
            return payload.get('exp', 0) > time.time()
        except:
            return False

    def get_access_token(self):
        """Get stored access token"""
        return st.session_state.get(self.token_key)

    def get_user_profile(self):
        """Get stored user profile"""
        return st.session_state.get(self.user_key)

    def store_auth_data(self, token, user_profile):
        """Store authentication data in session state"""
        st.session_state[self.token_key] = token
        st.session_state[self.user_key] = user_profile
        st.session_state.logged_in = True
        st.session_state.username = user_profile.get('email', 'User')
        st.session_state.user_role = user_profile.get('role', 'user')

    def clear_auth_data(self):
        """Clear authentication data"""
        keys_to_remove = [self.token_key, self.user_key]
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]

        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_role = "user"

    def get_google_auth_url(self):
        """Get Google OAuth authorization URL"""
        return f"{self.backend_url}/auth/google"

    def get_facebook_auth_url(self):
        """Get Facebook OAuth authorization URL"""
        return f"{self.backend_url}/auth/facebook"

    def handle_oauth_callback(self):
        """Handle OAuth callback from URL parameters"""
        # FIXED: Use st.query_params instead of st.experimental_get_query_params
        query_params = st.query_params

        access_token = query_params.get('access_token')
        error = query_params.get('error')

        if error:
            st.error(f"OAuth authentication failed: {error}")
            return False

        if access_token:
            try:
                # Fetch user profile with the token
                user_profile = self.fetch_user_profile(access_token)
                if user_profile:
                    self.store_auth_data(access_token, user_profile)
                    st.success(f"Welcome, {user_profile.get('name', 'User')}!")

                    # Clear URL parameters
                    st.query_params.clear()

                    # Navigate to home page
                    st.session_state.current_page = 'home'
                    st.rerun()
                    return True
            except Exception as e:
                st.error(f"Failed to complete authentication: {str(e)}")
                return False

        return False

    def fetch_user_profile(self, token):
        """Fetch user profile using access token"""
        try:
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            response = requests.get(f"{self.backend_url}/auth/profile", headers=headers)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch user profile: {str(e)}")
            return None

    def logout(self):
        """Logout user"""
        token = self.get_access_token()

        if token:
            try:
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
                requests.post(f"{self.backend_url}/auth/logout", headers=headers)
            except:
                pass  # Ignore logout request failures

        self.clear_auth_data()
        st.session_state.current_page = 'login'
        st.success("Logged out successfully!")
        st.rerun()

    def check_oauth_status(self):
        """Check which OAuth providers are available"""
        try:
            response = requests.get(f"{self.backend_url}/auth/status")
            response.raise_for_status()
            return response.json()
        except:
            return {"google_available": False, "facebook_available": False}


# Create global OAuth service instance
oauth_service = StreamlitOAuthService()

# --- Custom CSS for global styling (matching front(2).py exactly) --- #
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

    .container {
        background: #fff;
        width: 100%;
        max-width: 900px;
        padding: 25px 30px;
        border-radius: 5px;
        box-shadow: 0 10px 10px rgba(0, 0, 0, 0.15);
        margin: 20px auto;
    }

    h1 {
        color: #4CAF50; /* Example color for main titles */
    }

    .title {
        font-size: 30px;
        font-weight: 600;
        margin-bottom: 30px;
        position: relative;
    }

    .title::before {
        content: "";
        position: absolute;
        height: 4px;
        width: 33px;
        left: 0;
        bottom: -5px;
        border-radius: 5px;
        background: linear-gradient(to right, #ed4599 0%, #ff0080 100%);
    }

    .form-wrapper {
        display: flex;
        flex-direction: column;
        gap: 30px;
    }

    .form-box {
        background: #fafafa;
        padding: 20px;
        border-radius: 8px;
        flex: 1;
    }

    .form-box h3 {
        margin-bottom: 10px;
        font-size: 18px;
        font-weight: 600;
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
    }

    .input-box {
        width: 100%;
        height: 45px;
        margin-top: 15px;
        position: relative;
    }

    .input-box input,
    .input-box select {
        width: 100%;
        height: 100%;
        outline: none;
        font-size: 16px;
        border: none;
        background: transparent;
        color: #000;
        border-bottom: 2px solid #ccc;
        padding-left: 5px;
    }

    .input-box input::placeholder {
        color: #aaa;
    }

    .button {
        margin-top: 30px;
    }

    .button input[type="submit"] {
        background: linear-gradient(to right, #99004d 0%, #ff0080 100%);
        font-size: 17px;
        color: #fff;
        border-radius: 5px;
        cursor: pointer;
        padding: 10px 0;
        transition: all 0.3s ease;
        width: 100%;
        border: none;
    }

    .button input[type="submit"]:hover {
        letter-spacing: 1px;
        background: linear-gradient(to left, #99004d 0%, #ff0080 100%);
    }

    .option {
        font-size: 14px;
        text-align: center;
        margin: 20px 0;
    }

    .option a {
        color: #ed4599;
        text-decoration: none;
        font-weight: 500;
        cursor: pointer;
    }

    .google a,
    .facebook a {
        display: block;
        height: 45px;
        width: 100%;
        font-size: 15px;
        text-decoration: none;
        padding-left: 20px;
        line-height: 45px;
        color: #fff;
        border-radius: 5px;
        transition: all 0.3s ease;
        margin-bottom: 15px;
    }

    .google a {
        background: linear-gradient(to right, #db4437 0%, #e57373 100%);
    }

    .google a:hover {
        background: linear-gradient(to left, #db4437 0%, #e57373 100%);
    }

    .facebook a {
        background: linear-gradient(to right, #3b5998 0%, #476bb8 100%);
    }

    .facebook a:hover {
        background: linear-gradient(to left, #3b5998 0%, #476bb8 100%);
    }

    .google i,
    .facebook i {
        padding-right: 12px;
        font-size: 20px;
    }

    /* Side-by-side only on larger screens */
    @media (min-width: 768px) {
        .form-wrapper {
            flex-direction: row;
        }

        .form-box {
            width: 48%;
        }
    }

    /* Improve spacing on very small phones */
    @media (max-width: 480px) {
        .container {
            padding: 20px 15px;
        }

        .title {
            font-size: 24px;
        }

        .input-box {
            height: 40px;
        }

        .input-box input,
        .input-box select {
            font-size: 14px;
        }

        .button input[type="submit"] {
            font-size: 15px;
            padding: 8px 0;
        }
    }

    /* Styles for Explore and Search pages */
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }

    .category-card {
        background-color: #f5f5f5;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        cursor: pointer;
        transition: transform 0.2s;
    }

    .category-card:hover {
        transform: translateY(-5px);
    }

    .category-card i {
        font-size: 40px;
        margin-bottom: 10px;
        color: #4CAF50;
    }

    .campaign-card {
        background-color: #f5f5f5;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }

    .campaign-card img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 4px;
        margin-bottom: 15px;
    }

    .campaign-card h3 {
        margin-top: 0;
        color: #333;
    }

    .campaign-card p {
        color: #666;
        font-size: 14px;
    }

    .search-bar {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }

    .search-bar input {
        flex-grow: 1;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    .search-bar button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
    }

    /* OAuth User Profile Widget */
    .user-profile-widget {
        background: #f0f8f0;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 2px solid #4CAF50;
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 15px;
    }

    .user-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 2px solid #4CAF50;
    }

    .user-details h4 {
        margin: 0;
        color: #2d5a2d;
        font-size: 16px;
    }

    .user-details p {
        margin: 2px 0;
        color: #666;
        font-size: 12px;
    }

    /* Term highlighting styles */
    .highlight-legal { background-color: #ffeb3b; color: #000; position: relative; cursor: help; }
    .highlight-financial { background-color: #4caf50; color: #fff; position: relative; cursor: help; }
    .highlight-tech { background-color: #2196f3; color: #fff; position: relative; cursor: help; }
    .highlight-social { background-color: #ff9800; color: #fff; position: relative; cursor: help; }
    .highlight-marketing { background-color: #9c27b0; color: #fff; position: relative; cursor: help; }
    .highlight-general { background-color: #607d8b; color: #fff; position: relative; cursor: help; }

    .tooltip-box {
        visibility: hidden;
        width: 200px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
    }

    .highlight-legal:hover .tooltip-box,
    .highlight-financial:hover .tooltip-box,
    .highlight-tech:hover .tooltip-box,
    .highlight-social:hover .tooltip-box,
    .highlight-marketing:hover .tooltip-box,
    .highlight-general:hover .tooltip-box {
        visibility: visible;
        opacity: 1;
    }

    /* Success and error message styling */
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 5px;
        margin: 10px 0;
    }

    .error-message {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Backend Connection Configuration --- #
BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME", "haven-fastapi-backend")
BACKEND_PORT = os.environ.get("BACKEND_PORT", "8000")
BACKEND_URL = "https://srv-d1sq8ser433s73eke7v0.onrender.com"  # Your Render backend URL

# --- API Key Environment Variables --- #
FIREBASE_SERVICE_ACCOUNT_KEY_JSON_BASE64 = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_JSON_BASE64")
ALGOLIA_API_KEY = os.environ.get("ALGOLIA_API_KEY")
ALGOLIA_APP_ID = os.environ.get("ALGOLIA_APP_ID")
BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
INSTAMOJO_API_KEY = os.environ.get("INSTAMOJO_API_KEY")
INSTAMOJO_AUTH_TOKEN = os.environ.get("INSTAMOJO_AUTH_TOKEN")

# --- Language Selection and Term Simplification --- #

translations = {
    "en": {
        "welcome_title": "Welcome to HAVEN Crowdfunding!",
        "app_loading": "Your application is loading...",
        "contact_support": "If you see this message for a long time, please contact support.",
        "select_language": "Select Language:",
        "simplify_terms": "Simplify Terms",
        "campaigns_title": "Our Campaigns",
        "campaign_detail": "Details for Campaign ",
        "back_to_campaigns": "Back to Campaigns",
        "login_title": "Login",
        "register_title": "Register",
        "full_name": "Full Name",
        "email_id": "Email ID",
        "phone_number": "Phone Number",
        "password": "Password",
        "confirm_password": "Confirm Password",
        "continue_btn": "Continue",
        "not_registered": "Not registered?",
        "create_account": "Create an account",
        "sign_in_google": "Sign in With Google",
        "sign_in_facebook": "Sign in With Facebook",
        "register_individual": "Register as an Individual",
        "register_organization": "Register as an Organization",
        "organization_name": "Organization Name",
        "organization_phone": "Organization Phone Number",
        "select_org_type": "Select Organization Type",
        "brief_description": "Brief Description (max 100 chars)",
        "register_btn": "Register",
        "campaign_1_title": "Sustainable Farming Initiative",
        "campaign_1_desc": "Support local farmers in adopting sustainable practices.",
        "campaign_3_title": "Education for All",
        "campaign_3_desc": "Fund educational resources for underprivileged children.",
        "campaign_2_title": "Clean Water Project",
        "campaign_2_desc": "Provide access to clean and safe drinking water.",
        "explore_categories": "Explore Categories",
        "discover_campaigns": "Discover campaigns by interest.",
        "art_design": "Art & Design",
        "technology": "Technology",
        "community": "Community",
        "film_video": "Film & Video",
        "music": "Music",
        "publishing": "Publishing",
        "search_campaigns": "Search Campaigns",
        "search_placeholder": "Search by keyword, category.",
        "enter_term_search": "Enter a term above to search for campaigns.",
        "search_tip": "You can search by title, description, or category.",
        "trending_campaigns": "Trending Campaigns",
        "support_popular_projects": "Support the most popular projects on HAVEN.",
        "home_button": "Home",
        "explore_button": "Explore",
        "search_button": "Search",
        "welcome_haven": "Welcome to HAVEN"
    },
    "hi": {
        "welcome_title": "हैवन क्राउडफंडिंग में आपका स्वागत है!",
        "app_loading": "आपका एप्लिकेशन लोड हो रहा है...",
        "contact_support": "यदि आप इस संदेश को लंबे समय तक देखते हैं, तो कृपया सहायता से संपर्क करें।",
        "select_language": "भाषा चुनें:",
        "simplify_terms": "शब्दों को सरल बनाएं",
        "campaigns_title": "हमारे अभियान",
        "campaign_detail": "अभियान के विवरण ",
        "back_to_campaigns": "अभियानों पर वापस जाएं",
        "login_title": "लॉगिन",
        "register_title": "पंजीकरण",
        "full_name": "पूरा नाम",
        "email_id": "ईमेल आईडी",
        "phone_number": "फोन नंबर",
        "password": "पासवर्ड",
        "confirm_password": "पासवर्ड की पुष्टि करें",
        "continue_btn": "जारी रखें",
        "not_registered": "पंजीकृत नहीं हैं?",
        "create_account": "खाता बनाएं",
        "sign_in_google": "गूगल से साइन इन करें",
        "sign_in_facebook": "फेसबुक से साइन इन करें",
        "register_individual": "व्यक्तिगत के रूप में पंजीकरण करें",
        "register_organization": "संगठन के रूप में पंजीकरण करें",
        "organization_name": "संगठन का नाम",
        "organization_phone": "संगठन का फोन नंबर",
        "select_org_type": "संगठन का प्रकार चुनें",
        "brief_description": "संक्षिप्त विवरण (अधिकतम 100 अक्षर)",
        "register_btn": "पंजीकरण करें",
        "campaign_1_title": "टिकाऊ कृषि पहल",
        "campaign_1_desc": "स्थानीय किसानों को टिकाऊ प्रथाओं को अपनाने में सहायता करें।",
        "campaign_3_title": "सभी के लिए शिक्षा",
        "campaign_3_desc": "वंचित बच्चों के लिए शैक्षिक संसाधनों को फंड करें।",
        "campaign_2_title": "स्वच्छ पानी परियोजना",
        "campaign_2_desc": "स्वच्छ और सुरक्षित पेयजल तक पहुंच प्रदान करें।",
        "explore_categories": "श्रेणियों का अन्वेषण करें",
        "discover_campaigns": "रुचि के अनुसार अभियान खोजें।",
        "art_design": "कला और डिज़ाइन",
        "technology": "प्रौद्योगिकी",
        "community": "समुदाय",
        "film_video": "फिल्म और वीडियो",
        "music": "संगीत",
        "publishing": "प्रकाशन",
        "search_campaigns": "अभियान खोजें",
        "search_placeholder": "कीवर्ड, श्रेणी से खोजें।",
        "enter_term_search": "अभियान खोजने के लिए ऊपर एक शब्द दर्ज करें।",
        "search_tip": "आप शीर्षक, विवरण, या श्रेणी से खोज सकते हैं।",
        "trending_campaigns": "ट्रेंडिंग अभियान",
        "support_popular_projects": "हैवन पर सबसे लोकप्रिय परियोजनाओं का समर्थन करें।",
        "home_button": "होम",
        "explore_button": "अन्वेषण करें",
        "search_button": "खोजें",
        "welcome_haven": "हैवन में आपका स्वागत है"
    },
    "ta": {
        "welcome_title": "ஹேவன் க்ரவுட்ஃபண்டிங்கிற்கு வரவேற்கிறோம்!",
        "app_loading": "உங்கள் பயன்பாடு ஏற்றப்படுகிறது...",
        "contact_support": "இந்த செய்தியை நீண்ட நேரம் பார்த்தால், தயவுசெய்து ஆதரவைத் தொடர்பு கொள்ளுங்கள்।",
        "select_language": "மொழியைத் தேர்ந்தெடுக்கவும்:",
        "simplify_terms": "சொற்களை எளிதாக்கவும்",
        "campaigns_title": "எங்கள் பிரச்சாரங்கள்",
        "campaign_detail": "பிரச்சாரத்தின் விவரங்கள் ",
        "back_to_campaigns": "பிரச்சாரங்களுக்குத் திரும்பு",
        "login_title": "உள்நுழைவு",
        "register_title": "பதிவு",
        "full_name": "முழு பெயர்",
        "email_id": "மின்னஞ்சல் ஐடி",
        "phone_number": "தொலைபேசி எண்",
        "password": "கடவுச்சொல்",
        "confirm_password": "கடவுச்சொல்லை உறுதிப்படுத்தவும்",
        "continue_btn": "தொடரவும்",
        "not_registered": "பதிவு செய்யப்படவில்லையா?",
        "create_account": "கணக்கை உருவாக்கவும்",
        "sign_in_google": "கூகிள் மூலம் உள்நுழையவும்",
        "sign_in_facebook": "பேஸ்புக் மூலம் உள்நுழையவும்",
        "register_individual": "தனிநபராக பதிவு செய்யவும்",
        "register_organization": "அமைப்பாக பதிவு செய்யவும்",
        "organization_name": "அமைப்பின் பெயர்",
        "organization_phone": "அமைப்பின் தொலைபேசி எண்",
        "select_org_type": "அமைப்பின் வகையைத் தேர்ந்தெடுக்கவும்",
        "brief_description": "சுருக்க விளக்கம் (அதிகபட்சம் 100 எழுத்துக்கள்)",
        "register_btn": "பதிவு செய்யவும்",
        "campaign_1_title": "நிலையான விவசாய முன்முயற்சி",
        "campaign_1_desc": "உள்ளூர் விவசாயிகளை நிலையான நடைமுறைகளை ஏற்க ஆதரிக்கவும்।",
        "campaign_3_title": "அனைவருக்கும் கல்வி",
        "campaign_3_desc": "பின்தங்கிய குழந்தைகளுக்கு கல்வி வளங்களுக்கு நிதி வழங்கவும்।",
        "campaign_2_title": "சுத்தமான நீர் திட்டம்",
        "campaign_2_desc": "சுத்தமான மற்றும் பாதுகாப்பான குடிநீருக்கான அணுகலை வழங்கவும்।",
        "explore_categories": "வகைகளை ஆராயவும்",
        "discover_campaigns": "ஆர்வத்தின் அடிப்படையில் பிரச்சாரங்களைக் கண்டறியவும்।",
        "art_design": "கலை மற்றும் வடிவமைப்பு",
        "technology": "தொழில்நுட்பம்",
        "community": "சமூகம்",
        "film_video": "திரைப்படம் மற்றும் வீடியோ",
        "music": "இசை",
        "publishing": "வெளியீடு",
        "search_campaigns": "பிரச்சாரங்களைத் தேடவும்",
        "search_placeholder": "முக்கிய சொல், வகை மூலம் தேடவும்।",
        "enter_term_search": "பிரச்சாரங்களைத் தேட மேலே ஒரு சொல்லை உள்ளிடவும்।",
        "search_tip": "நீங்கள் தலைப்பு, விளக்கம் அல்லது வகை மூலம் தேடலாம்।",
        "trending_campaigns": "டிரெண்டிங் பிரச்சாரங்கள்",
        "support_popular_projects": "ஹேவனில் மிகவும் பிரபலமான திட்டங்களை ஆதரிக்கவும்।",
        "home_button": "முகப்பு",
        "explore_button": "ஆராயவும்",
        "search_button": "தேடவும்",
        "welcome_haven": "ஹேவனுக்கு வரவேற்கிறோம்"
    },
    "te": {
        "welcome_title": "హేవన్ క్రౌడ్‌ఫండింగ్‌కు స్వాగతం!",
        "app_loading": "మీ అప్లికేషన్ లోడ్ అవుతోంది...",
        "contact_support": "మీరు ఈ సందేశాన్ని చాలా కాలం పాటు చూస్తుంటే, దయచేసి మద్దతును సంప్రదించండి।",
        "select_language": "భాషను ఎంచుకోండి:",
        "simplify_terms": "పదాలను సరళీకరించండి",
        "campaigns_title": "మా ప్రచారాలు",
        "campaign_detail": "ప్రచారం వివరాలు ",
        "back_to_campaigns": "ప్రచారాలకు తిరిగి వెళ్ళండి",
        "login_title": "లాగిన్",
        "register_title": "నమోదు",
        "full_name": "పూర్తి పేరు",
        "email_id": "ఇమెయిల్ ఐడి",
        "phone_number": "ఫోన్ నంబర్",
        "password": "పాస్‌వర్డ్",
        "confirm_password": "పాస్‌వర్డ్‌ను నిర్ధారించండి",
        "continue_btn": "కొనసాగించండి",
        "not_registered": "నమోదు కాలేదా?",
        "create_account": "ఖాతాను సృష్టించండి",
        "sign_in_google": "గూగుల్‌తో సైన్ ఇన్ చేయండి",
        "sign_in_facebook": "ఫేస్‌బుక్‌తో సైన్ ఇన్ చేయండి",
        "register_individual": "వ్యక్తిగతంగా నమోదు చేసుకోండి",
        "register_organization": "సంస్థగా నమోదు చేసుకోండి",
        "organization_name": "సంస్థ పేరు",
        "organization_phone": "సంస్థ ఫోన్ నంబర్",
        "select_org_type": "సంస్థ రకాన్ని ఎంచుకోండి",
        "brief_description": "సంక్షిప్త వివరణ (గరిష్టంగా 100 అక్షరాలు)",
        "register_btn": "నమోదు చేయండి",
        "campaign_1_title": "స్థిరమైన వ్యవసాయ చొరవ",
        "campaign_1_desc": "స్థానిక రైతులను స్థిరమైన పద్ధతులను అనుసరించడంలో మద్దతు ఇవ్వండి।",
        "campaign_3_title": "అందరికీ విద్య",
        "campaign_3_desc": "నిరుపేద పిల్లలకు విద్యా వనరులకు నిధులు అందించండి।",
        "campaign_2_title": "స్వచ్ఛమైన నీటి ప్రాజెక్ట్",
        "campaign_2_desc": "స్వచ్ఛమైన మరియు సురక్షితమైన తాగునీటికి అందుబాటును అందించండి।",
        "explore_categories": "వర్గాలను అన్వేషించండి",
        "discover_campaigns": "ఆసక్తి ఆధారంగా ప్రచారాలను కనుగొనండి।",
        "art_design": "కళ మరియు డిజైన్",
        "technology": "సాంకేతికత",
        "community": "సమాజం",
        "film_video": "చలనచిత్రం మరియు వీడియో",
        "music": "సంగీతం",
        "publishing": "ప్రచురణ",
        "search_campaigns": "ప్రచారాలను వెతకండి",
        "search_placeholder": "కీవర్డ్, వర్గం ద్వారా వెతకండి।",
        "enter_term_search": "ప్రచారాలను వెతకడానికి పైన ఒక పదాన్ని నమోదు చేయండి।",
        "search_tip": "మీరు శీర్షిక, వివరణ లేదా వర్గం ద్వారా వెతకవచ్చు।",
        "trending_campaigns": "ట్రెండింగ్ ప్రచారాలు",
        "support_popular_projects": "హేవన్‌లో అత్యంత ప్రజాదరణ పొందిన ప్రాజెక్టులకు మద్దతు ఇవ్వండి।",
        "home_button": "హోమ్",
        "explore_button": "అన్వేషించండి",
        "search_button": "వెతకండి",
        "welcome_haven": "హేవన్‌కు స్వాగతం"
    }
}

# Get current language from session state or set default
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'


# Function to get translated text
def t(key):
    english_text = translations["en"].get(key, key)  # Always get English text first
    if st.session_state.lang == "en":
        return english_text

    # Check if a direct translation exists for the key in the target language
    if key in translations[st.session_state.lang]:
        return translations[st.session_state.lang][key]
    else:
        # If no direct translation for the key, try to translate word by word via backend
        # This part assumes the backend can handle word-by-word translation or returns original if no translation
        translated_words = []
        words = re.findall(r'\b\w+\b|\W+', english_text)  # Split by words and non-words
        for word in words:
            if word.strip() and word.strip().isalpha():  # Only try to translate actual words
                translated_word = translate_text_backend(word, target_lang=st.session_state.lang)
                translated_words.append(translated_word)
            else:
                translated_words.append(word)  # Keep non-words as is
        return "".join(translated_words)


# --- Term Simplification and Translation (Automatic) --- #
def translate_text_backend(text, target_lang=None):
    """Sends text to backend for translation."""
    try:
        payload = {"text": text, "source_language": "en", "target_language": target_lang}

        response = requests.post(f"{BACKEND_URL}/translate-text", json=payload)
        response.raise_for_status()
        return response.json().get("translated_text", text)
    except requests.exceptions.RequestException as e:
        # st.warning(f"Could not translate text via backend: {e}. Using local translation.")
        return text  # Return original text if backend call fails


def simplify_text_backend(text, target_lang=None):
    """Sends text to backend for simplification/translation."""
    try:
        payload = {"text": text}
        if target_lang:
            payload["target_language"] = target_lang

        response = requests.post(f"{BACKEND_URL}/simplify-text", json=payload)
        response.raise_for_status()
        return response.json().get("simplified_text", text)
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not simplify text via backend: {e}. Using local simplification.")
        return simplify_text_local(text)


def simplify_text_local(text):
    replacements = {
        "sustainable practices": "eco-friendly ways",
        "underprivileged children": "children who need help",
        "holistic development": "all-round growth",
        "socio-economic background": "family's money situation",
        "permaculture": "natural farming methods",
        "resilient food system": "strong food supply",
        "widespread health issues": "many health problems",
        "fundamental human right": "basic right for everyone"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


# --- Page Navigation State --- #
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'  # Start with login page
if 'registration_type' not in st.session_state:
    st.session_state.registration_type = None


# --- Enhanced Authentication Functions --- #
def is_user_authenticated():
    """Check if user is authenticated via OAuth or traditional login"""
    return oauth_service.is_authenticated() or st.session_state.get('logged_in', False)


def get_enhanced_auth_headers():
    """Get authentication headers for API requests"""
    # Try OAuth token first
    oauth_token = oauth_service.get_access_token()
    if oauth_token:
        return {"Authorization": f"Bearer {oauth_token}"}

    # Fall back to traditional auth token
    if st.session_state.get("auth_token"):
        return {"Authorization": f"Bearer {st.session_state.auth_token}"}

    return {}


def check_oauth_callback():
    """Check for OAuth callback and handle it"""
    query_params = st.query_params

    if 'access_token' in query_params or 'error' in query_params:
        return oauth_service.handle_oauth_callback()

    return False


def render_user_profile_widget():
    """Render user profile widget for authenticated users"""
    if not oauth_service.is_authenticated():
        return

    user = oauth_service.get_user_profile()
    if not user:
        return

    with st.sidebar:
        st.markdown(f"""
        <div class="user-profile-widget">
            <div class="user-info">
                <img src="{user.get('picture', 'https://via.placeholder.com/50')}" alt="Profile" class="user-avatar">
                <div class="user-details">
                    <h4>{user.get('name', 'User')}</h4>
                    <p>{user.get('email', '')}</p>
                    <p>via {user.get('provider', 'OAuth')}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Sign Out", key="oauth_logout"):
            oauth_service.logout()


# --- Enhanced Error Handling Functions --- #
def safe_json_response(response):
    """Safely extract JSON from response with fallback error handling"""
    try:
        return response.json()
    except (ValueError, json.JSONDecodeError):
        # If response is not JSON, return a generic error structure
        return {
            "detail": f"Server error (Status: {response.status_code}). Please try again later.",
            "status_code": response.status_code,
            "response_text": response.text[:200] if response.text else "No response content"
        }


def display_error_message(error_msg):
    """Display error message with consistent styling"""
    st.markdown(f"""
    <div class="error-message">
        <strong>Error:</strong> {error_msg}
    </div>
    """, unsafe_allow_html=True)


def display_success_message(success_msg):
    """Display success message with consistent styling"""
    st.markdown(f"""
    <div class="success-message">
        <strong>Success:</strong> {success_msg}
    </div>
    """, unsafe_allow_html=True)


# --- API Interaction Functions ---
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def fetch_all_campaigns():
    """Fetches all campaigns from the backend."""
    if not is_user_authenticated():
        return []  # Don't fetch if not logged in

    try:
        response = requests.get(f"{BACKEND_URL}/campaigns", headers=get_enhanced_auth_headers())
        response.raise_for_status()  # Raise an exception for HTTP errors
        all_campaigns = response.json()
        return [c for c in all_campaigns if c.get('verification_status') != 'Rejected']
    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to backend at {BACKEND_URL}. Please ensure the backend is running.")
        return []
    except requests.exceptions.HTTPError as e:
        error_data = safe_json_response(e.response)
        st.error(
            f"HTTP error fetching campaigns: {e.response.status_code} - {error_data.get('detail', 'Unknown error')}")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return []


def search_campaigns_backend(query):
    """Searches campaigns via the backend."""
    try:
        response = requests.post(f"{BACKEND_URL}/search", json={"query": query}, headers=get_enhanced_auth_headers())
        response.raise_for_status()
        search_results = response.json()
        return [c for c in search_results if c.get('verification_status') != 'Rejected']
    except requests.exceptions.RequestException as e:
        st.error(f"Error searching campaigns: {e}")
        return []


def create_campaign_backend(campaign_data):
    """Sends request to create a new campaign."""
    try:
        response = requests.post(f"{BACKEND_URL}/create-campaign", json=campaign_data,
                                 headers=get_enhanced_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_data = safe_json_response(e.response)
        st.error(f"Error creating campaign: {error_data.get('detail', 'Unknown error')}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating campaign: {e}")
        return None


def login_user(email, password):
    """Authenticates user with the backend using JWT."""
    try:
        response = requests.post(f"{BACKEND_URL}/login", json={"email": email, "password": password})
        response.raise_for_status()
        token_data = response.json()
        st.session_state.auth_token = token_data.get("access_token")
        st.session_state.user_role = token_data.get("role", "user")
        st.session_state.logged_in = True
        st.session_state.username = email  # Or fetch username from token_data
        st.session_state.current_page = "home"
        display_success_message(f"Welcome, {email}!")
        st.rerun()
    except requests.exceptions.HTTPError as e:
        error_data = safe_json_response(e.response)
        display_error_message(f"Login failed: {error_data.get('detail', 'Incorrect email or password')}")
    except requests.exceptions.RequestException as e:
        display_error_message(f"Login failed: Could not connect to backend. Is it running? {e}")


def register_user_backend(user_data):
    """Registers a new user with the backend using JWT authentication."""
    try:
        # Validate required fields
        if user_data.get("type") == "individual":
            required_fields = ["full_name", "email", "phone_number", "password"]
        else:
            required_fields = ["organization_name", "email", "organization_phone", "organization_type", "password"]

        missing_fields = [field for field in required_fields if not user_data.get(field)]
        if missing_fields:
            display_error_message(f"Please fill in all required fields: {', '.join(missing_fields)}")
            return None

        # Validate password confirmation
        if user_data.get("password") != user_data.get("confirm_password"):
            display_error_message("Passwords do not match. Please try again.")
            return None

        # Remove confirm_password from data sent to backend
        registration_data = {k: v for k, v in user_data.items() if k != "confirm_password"}

        response = requests.post(f"{BACKEND_URL}/register", json=registration_data)
        response.raise_for_status()

        result = response.json()
        display_success_message("Registration successful! You can now log in with your credentials.")
        st.session_state.current_page = "login"
        st.rerun()
        return result

    except requests.exceptions.HTTPError as e:
        error_data = safe_json_response(e.response)
        display_error_message(f"Registration failed: {error_data.get('detail', 'Unknown error')}")
        return None
    except requests.exceptions.RequestException as e:
        display_error_message(f"Registration failed: Could not connect to backend. Is it running? {e}")
        return None


def logout_user():
    """Logs out the user."""
    if oauth_service.is_authenticated():
        oauth_service.logout()
    else:
        st.session_state.logged_in = False
        st.session_state.auth_token = None
        st.session_state.username = None
        st.session_state.user_role = "user"
        st.session_state.current_page = "login"
        display_success_message("Logged out successfully.")
        st.rerun()


# --- Term Definitions for Simplification ---
TERM_DEFINITIONS = {
    "legal": {
        "Intellectual Property Rights": "Legal rights to creations of the mind, like inventions or designs.",
        "Terms of Service": "The rules and conditions users must agree to when using a service.",
        "Accredited Investor": "An investor recognized by financial regulators as sophisticated enough to invest in certain complex securities.",
        "SEC regulations": "Rules set by the U.S. Securities and Exchange Commission to protect investors.",
        "KYC (Know Your Customer)": "A process to verify the identity of clients to prevent fraud and illegal activities.",
        "AML (Anti-Money Laundering)": "Laws and procedures to prevent criminals from disguising illegally obtained funds as legitimate income.",
        "Equity Crowdfunding": "Raising capital by offering shares of a company to a large number of small investors.",
        "Convertible Note": "A type of short-term debt that converts into equity at a later stage, usually during a future funding round.",
        "Arbitration": "A legal technique for resolving disputes outside the courts, where a neutral third party makes a decision.",
        "Jurisdiction": "The official power to make legal decisions and judgments."
    },
    "financial": {
        "Return on Investment (ROI)": "A measure of the profitability of an investment, calculated as profit divided by cost.",
        "Valuation": "The process of determining the current worth of a company or asset.",
        "Seed Funding": "The earliest stage of fundraising for a startup, used to get the business off the ground.",
        "Venture Capital": "Funding provided by investors to startup companies and small businesses with perceived long-term growth potential.",
        "Dilution": "The reduction in the ownership percentage of a company's existing shareholders when new shares are issued.",
        "Capital": "Wealth in the form of money or other assets owned by a person or organization.",
        "Liquidity": "The ease with which an asset or security can be converted into ready cash without affecting its market price.",
        "Escrow Account": "A temporary pass-through account held by a third party during the process of a transaction.",
        "Payment Gateway Fees": "Charges imposed by payment processing services for handling online transactions.",
        "Funding Threshold": "The minimum amount of money a crowdfunding campaign must raise to be successful.",
        "All-or-Nothing Model": "A crowdfunding model where funds are only collected if the campaign reaches its full funding goal.",
        "Tax Implications": "The consequences that a financial transaction or investment has on an individual's or company's tax liability."
    },
    "tech": {
        "Minimum Viable Product (MVP)": "A version of a new product with just enough features to satisfy early customers and provide feedback for future product development.",
        "Proof of Concept (POC)": "A realization of a certain method or idea to demonstrate its feasibility.",
        "Scalability": "The ability of a system to handle a growing amount of work by adding resources.",
        "Blockchain": "A decentralized, distributed ledger technology that records transactions across many computers.",
        "Artificial Intelligence (AI)": "The simulation of human intelligence processes by machines.",
        "Machine Learning (ML)": "A subset of AI that allows systems to learn from data without being explicitly programmed.",
        "API (Application Programming Interface)": "A set of rules and protocols for building and interacting with software applications.",
        "User Interface (UI)": "The visual part of a computer application or website that a user interacts with.",
        "User Experience (UX)": "The overall experience of a person using a product, encompassing their feelings and attitudes.",
        "Open Source": "Software with source code that anyone can inspect, modify, and enhance.",
        "Proprietary Technology": "Technology owned exclusively by a company, often protected by patents or copyrights."
    },
    "social": {
        "Sustainable Development Goals (SDGs)": "A collection of 17 global goals set by the United Nations for a sustainable future.",
        "Impact Investing": "Investments made with the intention to generate positive, measurable social and environmental impact alongside a financial return.",
        "Social Enterprise": "A business that has specific social objectives as its primary purpose.",
        "Carbon Footprint": "The total amount of greenhouse gases produced to directly and indirectly support human activities.",
        "Renewable Energy": "Energy from sources that are naturally replenishing but flow-limited, such as solar, wind, geothermal, and hydro.",
        "Circular Economy": "An economic system aimed at eliminating waste and the continual use of resources.",
        "Biodiversity": "The variety of life on Earth at all its levels, from genes to ecosystems.",
        "Community Empowerment": "The process of enabling communities to increase control over their lives.",
        "Philanthropy": "The desire to promote the welfare of others, expressed especially by the generous donation of money to good causes."
    },
    "marketing": {
        "Market Penetration": "The successful selling of a product or service in a specific market.",
        "Target Audience": "The specific group of consumers most likely to want your product or service.",
        "Value Proposition": "A statement that explains what benefit a company provides to customers.",
        "Unique Selling Proposition (USP)": "The unique benefit a company offers that helps it stand out from competitors.",
        "SEO (Search Engine Optimization)": "The process of improving the visibility of a website or a web page in a web search engine's unpaid results.",
        "Content Strategy": "The planning, development, and management of content.",
        "Customer Acquisition Cost (CAC)": "The cost associated with convincing a consumer to buy a product/service.",
        "Business Model Canvas": "A strategic management template used for developing new or documenting existing business models."
    },
    "general": {
        "Milestone": "A significant stage or event in the development of something.",
        "Deliverable": "A tangible or intangible good or service produced as a result of a project that is intended to be delivered to a customer.",
        "Timeline": "A schedule of events; a chronological record.",
        "Budget Allocation": "The process of assigning available financial resources for specific purposes.",
        "Risk Assessment": "The process of identifying potential hazards and analyzing what could happen if a hazard occurs."
    }
}


# --- JavaScript for Term Highlighting and Tooltips ---
def inject_term_simplification_js():
    js_code = """
    <script>
    const termDefinitions = %s; // Will be replaced by Python with JSON data

    function applyTermSimplification() {
        const campaignDescriptionElement = document.getElementById(\'campaign-description-text\');
        if (!campaignDescriptionElement) {
            return;
        }

        let originalText = campaignDescriptionElement.innerHTML;
        let newHtml = originalText;

        for (const category in termDefinitions) {
            const terms = termDefinitions[category];
            const className = `highlight-${category}`; // e.g., highlight-legal

            for (const term in terms) {
                const definition = terms[term];
                // Create a regex to match the whole word, case-insensitive
                const regex = new RegExp(`\\b${term.replace(/[.*+?^${}()|[\]\\\\]/g, '\\$&')}\\b`, 'gi');
                newHtml = newHtml.replace(regex, (match) => {
                    // Avoid re-wrapping already wrapped terms
                    if (match.includes('<span class="highlight-"')) {
                        return match;
                    }
                    return `<span class="${className}" data-definition="${definition}">${match}<span class="tooltip-box">${definition}</span></span>`;
                });
            }
        }
        campaignDescriptionElement.innerHTML = newHtml;
    }

    const observer = new MutationObserver((mutationsList, observer) => {
        for(const mutation of mutationsList) {
            if (mutation.type === \'childList\' && mutation.addedNodes.length > 0) {
                const campaignDetailContainer = document.querySelector(\".campaign-detail-container\");
                if (campaignDetailContainer && campaignDetailContainer.contains(document.getElementById(\'campaign-description-text\'))) {
                    applyTermSimplification();
                    return;
                }
            }
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
    document.addEventListener(\'DOMContentLoaded\', applyTermSimplification);
    </script>
    """ % json.dumps(TERM_DEFINITIONS)
    st.markdown(js_code, unsafe_allow_html=True)


# --- Render Pages based on current_page --- #

def render_login_page():
    # OAuth buttons OUTSIDE the form - FIXED
    oauth_status = oauth_service.check_oauth_status()

    # OAuth buttons with the exact styling from front(2).py
    st.markdown(f"""
    <div class="container">
      <div class="title">{t("login_title")}</div>

      <div class="google">
        <a href="{oauth_service.get_google_auth_url() if oauth_status.get('google_available', False) else '#'}" 
           {'onclick="window.location.href=this.href"' if oauth_status.get('google_available', False) else 'onclick="return false;" style="opacity:0.5; cursor:not-allowed;"'}>
          <i class="fab fa-google"></i>{t("sign_in_google")}
        </a>
      </div>

      <div class="facebook">
        <a href="{oauth_service.get_facebook_auth_url() if oauth_status.get('facebook_available', False) else '#'}" 
           {'onclick="window.location.href=this.href"' if oauth_status.get('facebook_available', False) else 'onclick="return false;" style="opacity:0.5; cursor:not-allowed;"'}>
          <i class="fab fa-facebook-f"></i>{t("sign_in_facebook")}
        </a>
      </div>
    """, unsafe_allow_html=True)

    # Traditional login form - FIXED with submit button
    with st.form(key='login_form'):
        email = st.text_input(t("email_id"), key="login_email")
        password = st.text_input(t("password"), type="password", key="login_password")

        # FIXED: Added submit button inside the form
        submit_button = st.form_submit_button(t("continue_btn"))

        st.markdown(f"""
          <div class="option">
            {t("not_registered")}
            <a href="#" onclick="document.getElementById('nav_to_register').click()">{t("create_account")}</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if submit_button:
            if email and password:
                login_user(email, password)
            else:
                display_error_message("Please enter both email and password.")

    # Navigation to register page
    if st.button("Create Account", key="nav_to_register"):
        st.session_state.current_page = 'register'
        st.rerun()


def render_register_page():
    st.markdown(f"""
    <div class="container">
      <div class="title">{t("register_title")}</div>
    """, unsafe_allow_html=True)

    reg_type_options = {"Individual": "individual", "Organization": "organization"}
    selected_reg_type_display = st.selectbox(
        "Register as a:",
        list(reg_type_options.keys()),
        key="reg_type_select"
    )
    st.session_state.registration_type = reg_type_options[selected_reg_type_display]

    with st.form(key='register_form'):
        st.markdown(f"""
          <div class="form-wrapper">
        """, unsafe_allow_html=True)

        if st.session_state.registration_type == 'individual':
            full_name = st.text_input(t("full_name"), key="reg_full_name")
            email = st.text_input(t("email_id"), key="reg_email")
            phone_number = st.text_input(t("phone_number"), key="reg_phone_number")
            password = st.text_input(t("password"), type="password", key="reg_password")
            confirm_password = st.text_input(t("confirm_password"), type="password", key="reg_confirm_password")
            user_data = {
                "full_name": full_name,
                "email": email,
                "phone_number": phone_number,
                "password": password,
                "confirm_password": confirm_password,
                "type": "individual"
            }

        elif st.session_state.registration_type == 'organization':
            org_name = st.text_input(t("organization_name"), key="reg_org_name")
            org_phone = st.text_input(t("organization_phone"), key="reg_org_phone")
            org_type = st.selectbox(t("select_org_type"), ["", "NGO", "Startup", "Charity"], key="reg_org_type")
            brief_description = st.text_area(t("brief_description"), max_chars=100, key="reg_brief_desc")
            email = st.text_input(t("email_id"), key="reg_email_org")
            password = st.text_input(t("password"), type="password", key="reg_password_org")
            confirm_password = st.text_input(t("confirm_password"), type="password", key="reg_confirm_password_org")
            user_data = {
                "organization_name": org_name,
                "organization_phone": org_phone,
                "organization_type": org_type,
                "brief_description": brief_description,
                "email": email,
                "password": password,
                "confirm_password": confirm_password,
                "type": "organization"
            }

        st.markdown(f"""
            </div>

            <div class="input-box button">
              <input type="submit" value="{t("register_btn")}" />
            </div>
          </div>
        """, unsafe_allow_html=True)

        # FIXED: Added submit button inside the form
        submit_button = st.form_submit_button(t("register_btn"))

        if submit_button:
            register_user_backend(user_data)

    # Navigation back to login
    if st.button("Back to Login", key="nav_to_login"):
        st.session_state.current_page = 'login'
        st.rerun()


def render_home_page():
    st.markdown(f"""
    <div class="container">
        <h1>{t("welcome_haven")}</h1>
        <p>{t("support_popular_projects")}</p>
        <div class="campaign-card">
            <img src="https://via.placeholder.com/600x400" alt="Campaign Image">
            <h3>ABC</h3>
            <p>By XYZ</p>
            <p>CAMPAIGNS DESCRIPTION</p>
            <p>P1,000 raised 100%</p>
            <p>30 days left</p>
        </div>
        <div class="campaign-card">
            <img src="https://via.placeholder.com/600x400" alt="Campaign Image">
            <h3>ABC</h3>
            <p>By XYZ</p>
            <p>CAMPAIGNS DESCRIPTION</p>
            <p>P1,000 raised 100%</p>
            <p>30 days left</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_explore_page():
    st.markdown(f"""
    <div class="container">
        <h1>{t("explore_categories")}</h1>
        <p>{t("discover_campaigns")}</p>
        <div class="category-grid">
            <div class="category-card">
                <i class="fas fa-paint-brush"></i>
                <p>{t("art_design")}</p>
            </div>
            <div class="category-card">
                <i class="fas fa-microchip"></i>
                <p>{t("technology")}</p>
            </div>
            <div class="category-card">
                <i class="fas fa-users"></i>
                <p>{t("community")}</p>
            </div>
            <div class="category-card">
                <i class="fas fa-film"></i>
                <p>{t("film_video")}</p>
            </div>
            <div class="category-card">
                <i class="fas fa-music"></i>
                <p>{t("music")}</p>
            </div>
            <div class="category-card">
                <i class="fas fa-book"></i>
                <p>{t("publishing")}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_search_page():
    st.markdown(f"""
    <div class="container">
        <h1>{t("search_campaigns")}</h1>
        <div class="search-bar">
            <input type="text" placeholder="{t("search_placeholder")}">
            <button><i class="fas fa-search"></i></button>
        </div>
        <p>{t("enter_term_search")}</p>
        <p>{t("search_tip")}</p>
    </div>
    """, unsafe_allow_html=True)


# --- Main App Logic --- #

# Check for OAuth callback first
if check_oauth_callback():
    st.rerun()

# Language selection dropdown (moved to sidebar for consistency)
lang_options = [
    ("en", "English"),
    ("hi", "हिन्दी"),
    ("ta", "தமிழ்"),
    ("te", "తెలుగు")
]
lang_codes = [code for code, _ in lang_options]
lang_names = [name for _, name in lang_options]

current_index = 0
if st.session_state.lang in lang_codes:
    current_index = lang_codes.index(st.session_state.lang)

selected_lang_index = st.sidebar.selectbox(
    t("select_language"),
    range(len(lang_options)),
    index=current_index,
    format_func=lambda x: lang_names[x],
    key="lang_selector"
)

selected_lang = lang_codes[selected_lang_index]

if selected_lang != st.session_state.lang:
    st.session_state.lang = selected_lang
    st.rerun()

# Sidebar navigation (updated buttons)
st.sidebar.title("Navigation")

# Show user profile widget if authenticated via OAuth
render_user_profile_widget()

if is_user_authenticated():
    if st.sidebar.button(t("home_button")):
        st.session_state.current_page = 'home'
        st.rerun()
    if st.sidebar.button(t("explore_button")):
        st.session_state.current_page = 'explore'
        st.rerun()
    if st.sidebar.button(t("search_button")):
        st.session_state.current_page = 'search'
        st.rerun()
    if st.sidebar.button("🚪 Logout"):
        logout_user()
else:
    # Only show login/register if not logged in
    if st.session_state.current_page != 'login' and st.session_state.current_page != 'register':
        st.session_state.current_page = 'login'  # Force login page if not logged in

# Render current page
if st.session_state.current_page == 'login':
    render_login_page()
elif st.session_state.current_page == 'register':
    render_register_page()
elif is_user_authenticated():
    if st.session_state.current_page == 'home':
        render_home_page()
    elif st.session_state.current_page == 'explore':
        render_explore_page()
    elif st.session_state.current_page == 'search':
        render_search_page()
    # Add more pages here as needed

# Placeholder for automatic term simplification
# This would ideally be integrated into the content rendering functions
# For example, when displaying campaign details, run them through simplify_text()

# Example usage of simplify_text (for demonstration)
# st.write(simplify_text("This campaign aims to provide resources and training to local farmers to transition to organic and sustainable farming methods."))

# You can add a button to test backend connectivity (for debugging)
if st.sidebar.button("Test Backend Connection"):
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            display_success_message("Backend connected successfully!")
            health_data = response.json()
            if 'oauth' in health_data:
                oauth_info = health_data['oauth']
                st.info(
                    f"OAuth Status: Google: {'✅' if oauth_info.get('google_configured') else '❌'}, Facebook: {'✅' if oauth_info.get('facebook_configured') else '❌'}")
        else:
            display_error_message(f"Backend connection failed. Status: {response.status_code}")
    except Exception as e:
        display_error_message(f"Failed to connect to backend: {str(e)}")

# Add Font Awesome for icons
st.markdown(
    "<link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css\">",
    unsafe_allow_html=True)


