import streamlit as st
import requests
import base64
import json
import os
from urllib.parse import urlencode
from datetime import datetime, timedelta

# --- Page configuration ---
st.set_page_config(
    page_title="HAVEN - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Environment variables for OAuth and Backend URL ---
BACKEND_URL = os.getenv("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "your-google-client-id")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", f"{BACKEND_URL}/auth/google/callback")
FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID", "your-facebook-app-id")
FACEBOOK_REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI", f"{BACKEND_URL}/auth/facebook/callback")
FRONTEND_BASE_URI = os.getenv("FRONTEND_BASE_URI", "https://haven-streamlit-frontend.onrender.com")

# --- Translation Dictionary ---
TRANSLATIONS = {
    'en': {
        'page_title': "HAVEN - Crowdfunding Platform",
        'tagline': "Help not just some people, but Help Humanity.",
        'trending_title': "Trending Campaigns",
        'search_title': "Search Campaigns",
        'explore_title': "Explore Categories",
        'profile_title': "User Profile",
        'login_title': "Login",
        'register_title': "Register",
        'login_prompt': "Enter Your Email",
        'password_prompt': "Enter Your Password",
        'not_registered': "Not registered?",
        'create_account': "Create an account",
        'or_signin_with': "or you can sign in with",
        'trending_nav': "Trending",
        'search_nav': "Search",
        'explore_nav': "Explore",
        'profile_nav': "Profile",
        'select_language': "Select Language",
        'search_placeholder': "Search by keyword, category...",
        'simplification_label': "i"
    },
    'hi': {
        'page_title': "हेवन - क्राउडफंडिंग प्लेटफ़ॉर्म",
        'tagline': "केवल कुछ लोगों की नहीं, बल्कि मानवता की मदद करें।",
        'trending_title': "ट्रेंडिंग अभियान",
        'search_title': "अभियान खोजें",
        'explore_title': "श्रेणियाँ खोजें",
        'profile_title': "उपयोगकर्ता प्रोफ़ाइल",
        'login_title': "लॉग इन करें",
        'register_title': "पंजीकरण करें",
        'login_prompt': "अपना ईमेल दर्ज करें",
        'password_prompt': "अपना पासवर्ड दर्ज करें",
        'not_registered': "पंजीकृत नहीं हैं?",
        'create_account': "एक खाता बनाएँ",
        'or_signin_with': "या आप इसके साथ साइन इन कर सकते हैं",
        'trending_nav': "ट्रेंडिंग",
        'search_nav': "खोज",
        'explore_nav': "खोज",
        'profile_nav': "प्रोफ़ाइल",
        'select_language': "भाषा चुनें",
        'search_placeholder': "कीवर्ड, श्रेणी द्वारा खोजें...",
        'simplification_label': "i"
    },
    'ta': {
        'page_title': "ஹெவன் - கிரவுட்ஃபண்டிங் பிளாட்ஃபார்ம்",
        'tagline': "சிலருக்கு மட்டுமல்ல, மனிதகுலத்திற்கே உதவுங்கள்.",
        'trending_title': "பிரபலமான பிரச்சாரங்கள்",
        'search_title': "பிரச்சாரங்களைத் தேடு",
        'explore_title': "பிரிவுகளை ஆராயுங்கள்",
        'profile_title': "பயனர் சுயவிவரம்",
        'login_title': "உள்நுழை",
        'register_title': "பதிவுசெய்",
        'login_prompt': "உங்கள் மின்னஞ்சலை உள்ளிடவும்",
        'password_prompt': "உங்கள் கடவுச்சொல்லை உள்ளிடவும்",
        'not_registered': "பதிவு செய்யவில்லையா?",
        'create_account': "ஒரு கணக்கை உருவாக்கவும்",
        'or_signin_with': "அல்லது நீங்கள் இவற்றுடன் உள்நுழையலாம்",
        'trending_nav': "பிரபலம்",
        'search_nav': "தேடல்",
        'explore_nav': "ஆராய்",
        'profile_nav': "சுயவிவரம்",
        'select_language': "மொழியைத் தேர்ந்தெடுக்கவும்",
        'search_placeholder': "முக்கிய வார்த்தை, வகைப்படி தேடு...",
        'simplification_label': "i"
    },
    'te': {
        'page_title': "హేవెన్ - క్రౌడ్‌ఫండింగ్ ప్లాట్‌ఫారమ్",
        'tagline': "కొంతమందికి మాత్రమే కాకుండా, మానవత్వానికి సహాయం చేయండి.",
        'trending_title': "ట్రెండింగ్ ప్రచారాలు",
        'search_title': "ప్రచారాలను శోధించండి",
        'explore_title': "వర్గాలను అన్వేషించండి",
        'profile_title': "వినియోగదారు ప్రొఫైల్",
        'login_title': "లాగిన్",
        'register_title': "నమోదు చేయండి",
        'login_prompt': "మీ ఇమెయిల్ నమోదు చేయండి",
        'password_prompt': "మీ పాస్‌వర్డ్‌ను నమోదు చేయండి",
        'not_registered': "నమోదు చేసుకోలేదా?",
        'create_account': "ఒక ఖాతాను సృష్టించండి",
        'or_signin_with': "లేదా మీరు దీనితో సైన్ ఇన్ చేయవచ్చు",
        'trending_nav': "ట్రెండింగ్",
        'search_nav': "శోధన",
        'explore_nav': "అన్వేషణ",
        'profile_nav': "ప్రొఫైల్",
        'select_language': "భాషను ఎంచుకోండి",
        'search_placeholder': "కీలకపదం, వర్గం ద్వారా శోధించండి...",
        'simplification_label': "i"
    }
}

def get_translated_text(key, lang):
    """Retrieves translated text from the dictionary."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, f"Translation missing for '{key}'")

# --- Utility functions ---
def load_logo():
    """
    Loads the HAVEN logo from the local file system and encodes it as base64.
    """
    try:
        with open("haven_logo.png", "rb") as f:
            logo_data = f.read()
        return base64.b64encode(logo_data).decode()
    except FileNotFoundError:
        return None

def load_custom_css(page):
    """
    Loads custom CSS and a JavaScript snippet to apply the correct background
    color to the page body and to handle the simplification popup.
    """
    st.markdown(f"""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Global styling for main container */
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
        min-height: 100vh;
    }}
    
    /* Page-specific body background styles */
    .login-page-bg {{ background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); color: #1a237e; }}
    .register-page-bg {{ background: linear-gradient(135deg, #ffcdd2 0%, #f8bbd9 100%); color: #263238; }}
    .trending-page-bg {{ background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); color: #1a237e; }}
    .search-page-bg {{ background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); color: #212121; }}
    .explore-page-bg {{ background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); color: #212121; }}
    .profile-page-bg {{ background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); color: #212121; }}
    .campaign-page-bg {{ background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 100%); color: #263238; }}
    
    /* Top navigation bar styling */
    .top-nav {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background: white;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }}
    .top-nav .stSelectbox {{ width: 150px; }}

    /* Simplification popup styling */
    .simplification-popup {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 1001;
        max-width: 400px;
        width: 90%;
    }}
    .popup-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }}
    .popup-header h4 {{ margin: 0; }}
    .close-btn {{
        font-size: 1.5rem;
        cursor: pointer;
        background: none;
        border: none;
    }}
    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        z-index: 1000;
    }}
    .simplification-icon {{
        font-style: normal;
        background: #4caf50;
        color: white;
        border-radius: 50%;
        width: 18px;
        height: 18px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: bold;
        cursor: pointer;
        margin-right: 5px;
        vertical-align: top;
        line-height: 1;
    }}
    
    /* Other existing CSS remains the same... */
    
    .login-card {{ background: white; border-radius: 15px; padding: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); max-width: 400px; margin: 0 auto; }}
    .register-card {{ background: white; border-radius: 15px; padding: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }}
    .oauth-button {{ width: 100%; padding: 12px; border: none; border-radius: 8px; font-size: 16px; font-weight: 500; margin: 8px 0; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.3s ease; }}
    .google-btn {{ background: #4285f4; color: white; }}
    .google-btn:hover {{ background: #357ae8; transform: translateY(-2px); }}
    .facebook-btn {{ background: #1877f2; color: white; }}
    .facebook-btn:hover {{ background: #166fe5; transform: translateY(-2px); }}
    .campaign-card {{ background: white; border-radius: 15px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 16px rgba(0,0,0,0.1); transition: transform 0.3s ease; }}
    .campaign-card:hover {{ transform: translateY(-5px); }}
    .category-card {{ background: white; border-radius: 15px; padding: 2rem; text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.1); transition: transform 0.3s ease; cursor: pointer; }}
    .category-card:hover {{ transform: translateY(-5px); }}
    .category-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
    .progress-container {{ background: #f0f0f0; border-radius: 10px; height: 8px; margin: 10px 0; }}
    .progress-bar {{ background: linear-gradient(90deg, #4caf50, #8bc34a); height: 100%; border-radius: 10px; transition: width 0.3s ease; }}
    .bottom-nav {{ position: fixed; bottom: 0; left: 0; right: 0; background: white; border-top: 1px solid #e0e0e0; padding: 10px 0; display: flex; justify-content: space-around; z-index: 1000; }}
    .nav-item {{ text-align: center; cursor: pointer; padding: 5px; transition: color 0.3s ease; }}
    .nav-item:hover {{ color: #4caf50; }}
    h1 {{ font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; }}
    h2 {{ font-size: 2rem; font-weight: 600; margin-bottom: 1rem; }}
    h3 {{ font-size: 1.5rem; font-weight: 500; margin-bottom: 0.5rem; }}
    p {{ font-size: 1.1rem; line-height: 1.6; margin-bottom: 1rem; }}
    .stTextInput > div > div > input {{ border-radius: 8px; border: 2px solid #e0e0e0; padding: 12px; font-size: 16px; }}
    .stSelectbox > div > div > select {{ border-radius: 8px; border: 2px solid #e0e0e0; padding: 12px; font-size: 16px; }}
    .stTextArea > div > div > textarea {{ border-radius: 8px; border: 2px solid #e0e0e0; padding: 12px; font-size: 16px; }}
    .stButton > button {{ border-radius: 8px; padding: 12px 24px; font-size: 16px; font-weight: 500; border: none; transition: all 0.3s ease; }}
    .stButton > button:hover {{ transform: translateY(-2px); }}
    .search-box {{ background: white; border-radius: 25px; padding: 15px 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.1); margin: 2rem 0; }}
    @media (max-width: 768px) {{ .login-card, .register-card {{ margin: 1rem; padding: 1.5rem; }} h1 {{ font-size: 2rem; }} h2 {{ font-size: 1.5rem; }} .haven-logo img {{ max-width: 150px; }} }}
    </style>
    <script>
        const urlParams = new URLSearchParams(window.location.search);
        const page = urlParams.get('page');
        const body = document.querySelector('body');
        if (body) {{
            if (page) {{ body.classList.add(page + '-page-bg'); }}
            else {{ body.classList.add('login-page-bg'); }}
        }}

        function showSimplificationPopup(title, definition) {{
            const existingPopup = document.querySelector('.simplification-popup');
            if (existingPopup) existingPopup.remove();

            const existingOverlay = document.querySelector('.overlay');
            if (existingOverlay) existingOverlay.remove();

            const overlay = document.createElement('div');
            overlay.className = 'overlay';
            overlay.onclick = () => {{
                document.body.removeChild(popup);
                document.body.removeChild(overlay);
            }};

            const popup = document.createElement('div');
            popup.className = 'simplification-popup';
            popup.innerHTML = `
                <div class="popup-header">
                    <h4><i class="simplification-icon">i</i> ${title}</h4>
                    <button class="close-btn" onclick="document.body.removeChild(popup); document.body.removeChild(overlay);">×</button>
                </div>
                <p>${definition}</p>
            `;

            document.body.appendChild(overlay);
            document.body.appendChild(popup);
        }}
    </script>
    """, unsafe_allow_html=True)

def get_oauth_url(provider):
    """Generate OAuth URL for Google or Facebook"""
    if provider == "google":
        params = {
            "client_id": GOOGLE_CLIENT_ID, "redirect_uri": GOOGLE_REDIRECT_URI, "scope": "openid email profile",
            "response_type": "code", "state": "google"
        }
        return f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
    elif provider == "facebook":
        params = {
            "client_id": FACEBOOK_CLIENT_ID, "redirect_uri": FACEBOOK_REDIRECT_URI, "scope": "email,public_profile",
            "response_type": "code", "state": "facebook"
        }
        return f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode(params)}"

def oauth_login_button(provider, text, icon):
    """Create OAuth login button with popup functionality"""
    button_class = f"{provider}-btn oauth-button"
    oauth_url = get_oauth_url(provider)
    button_html = f"""
    <button class="{button_class}" onclick="openOAuthPopup('{oauth_url}', '{provider}')">
        {icon} {text}
    </button>
    <script>
    function openOAuthPopup(url, provider) {{
        const popup = window.open(
            url, 'oauth_' + provider,
            'width=500,height=600,scrollbars=yes,resizable=yes,status=yes,location=yes,toolbar=no,menubar=no'
        );
        const checkClosed = setInterval(() => {{
            if (popup.closed) {{ clearInterval(checkClosed); window.location.reload(); }}
        }}, 1000);
    }}
    </script>
    """
    st.markdown(button_html, unsafe_allow_html=True)

def fetch_campaigns():
    """Fetch campaigns from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaigns", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching campaigns: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Network error while fetching campaigns: {e}")
        return []

def fetch_categories():
    """Fetch categories from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/categories", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching categories: {response.status_code}")
            return {"categories": []}
    except requests.exceptions.RequestException as e:
        st.error(f"Network error while fetching categories: {e}")
        return {"categories": []}

def search_campaigns(query):
    """Search campaigns from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/search", params={"q": query}, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error searching campaigns: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Network error while searching campaigns: {e}")
        return []

def process_text_for_simplification(text, lang):
    """
    Calls the backend to process text for simplification.
    This function will automatically add the clickable 'i' to complex terms.
    """
    try:
        # Pass the language code to the backend for potential future use with translation
        response = requests.post(f"{BACKEND_URL}/api/process_text_for_simplification", 
                                 json={"text": text, "language": lang}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Replace the marked terms with a clickable icon
            processed_text = data["processed_text"]
            simplifications = data["simplifications"]
            
            for term, definition in simplifications.items():
                simplified_html = f"""
                <span style="white-space: nowrap;">
                    <i class="simplification-icon" onclick="showSimplificationPopup('{term}', '{definition}')">i</i>
                    <span style="font-style: italic;">{term}</span>
                </span>
                """
                # This is a simplified replacement for demonstration.
                processed_text = processed_text.replace(f"{{i}}{term}{{/i}}", simplified_html)
            
            return processed_text
        else:
            st.error(f"Error processing text: {response.status_code}")
            return text
    except requests.exceptions.RequestException as e:
        st.error(f"Network error while processing text: {e}")
        return text

# --- Page components ---
def render_logo():
    """Renders the HAVEN logo from a base64 encoded string or a fallback H1 tag."""
    logo_base64 = load_logo()
    if logo_base64:
        st.markdown(f"""<div class="haven-logo" style="text-align: center;">
            <img src="data:image/png;base64,{logo_base64}" alt="HAVEN Logo" style="max-width: 200px; margin-bottom: 1rem;">
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="haven-logo" style="text-align: center;">
            <h1 style="font-size: 3rem; margin: 0; color: #4caf50;">HAVEN</h1>
        </div>""", unsafe_allow_html=True)

def render_tagline(lang):
    """Renders the application's tagline."""
    st.markdown(f"""
    <div style="text-align: center; color: #333; font-size: 1.2rem; margin-bottom: 2rem;">
        {get_translated_text('tagline', lang)}
    </div>
    """, unsafe_allow_html=True)

def top_navigation():
    """Renders the top navigation bar with a language selection dropdown."""
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("<div class='haven-logo'><h1 style='font-size: 2rem; margin: 0;'>HAVEN</h1></div>", unsafe_allow_html=True)
    with col3:
        language_options = { 'English': 'en', 'Hindi': 'hi', 'Tamil': 'ta', 'Telugu': 'te' }
        default_lang_key = 'English'
        if 'language' in st.session_state:
            for key, value in language_options.items():
                if value == st.session_state.language:
                    default_lang_key = key
                    break
        selected_lang_key = st.selectbox(
            label=get_translated_text('select_language', st.session_state.language),
            options=list(language_options.keys()),
            index=list(language_options.keys()).index(default_lang_key),
            key="language_selector",
            label_visibility="collapsed"
        )
        st.session_state.language = language_options[selected_lang_key]
    st.markdown("</div>", unsafe_allow_html=True)

def login_page():
    """Renders the login page with a form and OAuth buttons."""
    lang = st.session_state.get('language', 'en')
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        render_logo()
        render_tagline(lang)
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"### {get_translated_text('login_title', lang)}")
        
        with st.form("login_form"):
            email = st.text_input(get_translated_text('login_prompt', lang), placeholder=get_translated_text('login_prompt', lang))
            password = st.text_input(get_translated_text('password_prompt', lang), type="password", placeholder=get_translated_text('password_prompt', lang))
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1: login_btn = st.form_submit_button("Continue", use_container_width=True)
            with col_btn2:
                if st.form_submit_button("Forgot Password?", use_container_width=True):
                    st.info("Password reset functionality coming soon!")
        
        if login_btn and email and password:
            st.success("Login successful! Redirecting...")
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.session_state.user_type = "individual"
            st.rerun()
        
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            {get_translated_text('not_registered', lang)} <a href="?page=register" style="color: #4caf50; text-decoration: none;">{get_translated_text('create_account', lang)}</a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"### {get_translated_text('or_signin_with', lang)}")
        col_oauth1, col_oauth2 = st.columns(2)
        with col_oauth1: oauth_login_button("google", "Google", "🔍")
        with col_oauth2: oauth_login_button("facebook", "Facebook", "📘")
        st.markdown('</div>', unsafe_allow_html=True)

def register_page():
    """Renders the registration page with forms for individuals and organizations."""
    lang = st.session_state.get('language', 'en')
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        render_logo()
        st.markdown('<div class="register-card">', unsafe_allow_html=True)
        st.markdown(f"## {get_translated_text('register_title', lang)}")
        account_type = st.selectbox("Select Account Type", ["Individual", "Organization"])
        if account_type == "Individual":
            st.markdown("### Register as an Individual")
            with st.form("individual_register"):
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    full_name = st.text_input("Full Name", placeholder="R PRAKASH")
                    email = st.text_input("Email ID", placeholder="prakashr00@rediffmail.com")
                    phone = st.text_input("Phone Number", placeholder="09936528585")
                    otp = st.text_input("Enter OTP", placeholder="Enter OTP")
                with col_i2:
                    password = st.text_input("Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    address = st.text_area("Address", placeholder="Enter your address")
                    st.markdown("**Identity Verification (Upload any one):**")
                    document_type = st.selectbox("Document Type", ["Aadhar Card", "PAN Card", "Passport", "Driving License", "Voter ID"])
                    document_file = st.file_uploader("Upload Document", type=['pdf', 'jpg', 'png'])
                register_btn = st.form_submit_button("Register", use_container_width=True)
                if register_btn:
                    if password == confirm_password:
                        st.success("Individual registration successful! You can now log in.")
                        st.session_state.current_page = "login"
                        st.rerun()
                    else: st.error("Passwords do not match!")
        else: # Organization
            st.markdown("### Register as an Organization")
            with st.form("organization_register"):
                col_o1, col_o2 = st.columns(2)
                with col_o1:
                    org_name = st.text_input("Organization Name", placeholder="Organization Name")
                    org_phone = st.text_input("Organization Phone Number", placeholder="Organization Phone Number")
                    org_type = st.selectbox("Select Organization Type", ["NGO", "Non-Profit", "Social Enterprise", "Charity", "Foundation"])
                    org_description = st.text_area("Brief Description (max 100 chars)", placeholder="Brief Description (max 100 chars)", max_chars=100)
                with col_o2:
                    contact_person = st.text_input("Contact Person Name")
                    contact_email = st.text_input("Contact Email")
                    password = st.text_input("Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    st.markdown("**Organization Verification (Required):**")
                    cert_type = st.selectbox("Certificate Type", ["Certificate of Incorporation", "GST Certificate", "12A Certificate", "80G Certificate", "FCRA Certificate"])
                    cert_file = st.file_uploader("Upload Certificate", type=['pdf', 'jpg', 'png'])
                register_btn = st.form_submit_button("Register", use_container_width=True)
                if register_btn:
                    if password == confirm_password:
                        st.success("Organization registration successful! You can now log in.")
                        st.session_state.current_page = "login"
                        st.rerun()
                    else: st.error("Passwords do not match!")
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            {get_translated_text('not_registered', lang)} <a href="?page=login" style="color: #4caf50; text-decoration: none;">{get_translated_text('login_title', lang)}</a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def trending_page():
    """Renders the trending campaigns page with a list of campaigns."""
    lang = st.session_state.get('language', 'en')
    render_logo()
    st.markdown(f"# {get_translated_text('trending_title', lang)}")
    st.markdown("Support the most popular projects on HAVEN.")
    st.markdown("""<div style="text-align: right; margin: 20px 0;">
        <span style="background: black; color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold;">
            ⚡ Trending
        </span>
    </div>""", unsafe_allow_html=True)
    campaigns = fetch_campaigns()
    if campaigns:
        for campaign in campaigns.get('campaigns', [])[:5]:
            st.markdown('<div class="campaign-card">', unsafe_allow_html=True)
            st.image(campaign.get('image_url', 'https://picsum.photos/400/300?random=10'), use_column_width=True)
            st.markdown(f"### <a href='?page=campaign_{campaign.get('id', '')}'>{campaign.get('title', 'Campaign Title')}</a>", unsafe_allow_html=True)
            st.markdown(f"By {campaign.get('organization', 'Organization')}")
            
            # Process and render the description with the simplification feature
            processed_description = process_text_for_simplification(
                campaign.get('description', 'Campaign description'), lang
            )
            st.markdown(processed_description, unsafe_allow_html=True)
            
            raised = campaign.get('current_amount', 0)
            goal = campaign.get('target_amount', 100000)
            progress = min((raised / goal) * 100, 100) if goal > 0 else 0
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress}%"></div>
            </div>
            <p>₹{raised:,} raised • {progress:.0f}%</p>
            <p>⏰ {campaign.get('days_left', 0)} days left</p>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else: st.info("No trending campaigns available at the moment.")

def search_page():
    """Renders the search page with a search box and displays results."""
    lang = st.session_state.get('language', 'en')
    render_logo()
    st.markdown(f"# {get_translated_text('search_title', lang)}")
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    search_query = st.text_input("", placeholder=get_translated_text('search_placeholder', lang), label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""<div style="text-align: center; margin: 40px 0;">
        <p style="font-size: 1.2rem; color: #666;">Enter a term above to search for campaigns.</p>
        <p style="color: #888;">You can search by title, description, or category.</p>
    </div>""", unsafe_allow_html=True)
    if search_query:
        results = search_campaigns(search_query)
        if results and results.get('campaigns'):
            st.markdown(f"### Found {len(results['campaigns'])} campaigns")
            for campaign in results['campaigns']:
                st.markdown('<div class="campaign-card">', unsafe_allow_html=True)
                st.markdown(f"**{campaign.get('title', 'Campaign')}**")
                st.markdown(f"By {campaign.get('organization', 'Organization')}")
                processed_description = process_text_for_simplification(
                    campaign.get('description', 'Description'), lang
                )
                st.markdown(processed_description, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else: st.info("No campaigns found. Try different keywords.")

def explore_page():
    """Renders the explore page with a grid of categories."""
    lang = st.session_state.get('language', 'en')
    render_logo()
    st.markdown(f"# {get_translated_text('explore_title', lang)}")
    st.markdown("Discover campaigns by interest.")
    categories_data = fetch_categories()
    categories = categories_data.get('categories', [])
    for i in range(0, len(categories), 2):
        col1, col2 = st.columns(2)
        with col1:
            if i < len(categories):
                cat = categories[i]
                st.markdown(f"""
                <div class="category-card" onclick="setPage('search?q={cat['name']}')">
                    <div class="category-icon">{cat.get('icon', '📁')}</div>
                    <h3>{cat['name']}</h3>
                    <p>{cat.get('count', 0)} campaigns</p>
                </div>
                """, unsafe_allow_html=True)
        with col2:
            if i + 1 < len(categories):
                cat = categories[i + 1]
                st.markdown(f"""
                <div class="category-card" onclick="setPage('search?q={cat['name']}')">
                    <div class="category-icon">{cat.get('icon', '📁')}</div>
                    <h3>{cat['name']}</h3>
                    <p>{cat.get('count', 0)} campaigns</p>
                </div>
                """, unsafe_allow_html=True)

def campaign_detail_page(campaign_id):
    """Renders a detailed view of a specific campaign."""
    lang = st.session_state.get('language', 'en')
    render_logo()
    campaign_data = {
        "id": campaign_id,
        "title": "Clean Water Initiative in Rural Areas",
        "organization": "Water for All Foundation",
        "is_verified": True,
        "image_url": "https://picsum.photos/800/400?random=1",
        "description": "This campaign aims to provide clean and safe drinking water to remote villages. Your donation will help us install water purification systems and educate the community on hygiene. This project focuses on poverty alleviation.",
        "top_donors": [
            {"name": "Anonymous Donor", "amount": 10000},
            {"name": "Jane Doe", "amount": 5000},
            {"name": "John Smith", "amount": 2500}
        ],
        "fraud_detection_message": "This campaign has been verified through our fraud detection system. All documents have been authenticated and the organization is legitimate.",
        "reviews": ["Great cause!", "Proud to support this."],
        "current_amount": 75000,
        "target_amount": 100000
    }
    st.markdown("""<div style="background: #f0f0f0; border-radius: 15px; overflow: hidden; margin-bottom: 20px;">
        <img src="https://picsum.photos/800/400?random=1" style="width: 100%; height: auto; object-fit: cover;">
    </div>""", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1: st.markdown(f"### {campaign_data['organization']}")
    with col2: st.markdown(f"""
        <div style="text-align: right;">
            <span style="color: {'green' if campaign_data['is_verified'] else 'red'};">
                ● {'Verified' if campaign_data['is_verified'] else 'Unverified'}
            </span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f"## {campaign_data['title']}")
    processed_description = process_text_for_simplification(campaign_data['description'], lang)
    st.markdown(processed_description, unsafe_allow_html=True)
    st.markdown("### Donate to this campaign")
    donation_amount = st.number_input("Enter donation amount (₹)", min_value=1, value=100)
    if st.button("Donate Now", use_container_width=True):
        st.success(f"You are donating ₹{donation_amount:,} to {campaign_data['organization']}. A UPI payment page will open shortly.")
    raised = campaign_data['current_amount']
    goal = campaign_data['target_amount']
    progress = min((raised / goal) * 100, 100) if goal > 0 else 0
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%"></div>
    </div>
    <p><b>₹{raised:,} raised</b> of ₹{goal:,}</p>
    """, unsafe_allow_html=True)
    st.markdown("### Top Donators")
    for i, donor in enumerate(campaign_data['top_donors']): st.markdown(f"**{i+1}.** {donor['name']} - ₹{donor['amount']:,}")
    st.markdown("### Reviews and Verification")
    st.markdown(f"""
    <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <p><strong>Fraud Detection Explanation:</strong></p>
        <p>{campaign_data['fraud_detection_message']}</p>
    </div>
    """, unsafe_allow_html=True)

def profile_page():
    """Renders the user profile page with tabs for different sections."""
    lang = st.session_state.get('language', 'en')
    render_logo()
    st.markdown(f"# {get_translated_text('profile_title', lang)}")
    if st.session_state.get('authenticated'):
        st.markdown(f"### Welcome, {st.session_state.get('user_email', 'User')}!")
        tab1, tab2, tab3 = st.tabs(["Profile Info", "My Donations", "My Campaigns"])
        with tab1:
            st.markdown("#### Profile Information")
            st.text_input("Name", value="John Doe")
            st.text_input("Email", value=st.session_state.get('user_email', ''))
            st.text_input("Phone", value="+91 9876543210")
            if st.button("Update Profile"): st.success("Profile updated successfully!")
        with tab2:
            st.markdown("#### My Donations")
            st.markdown("**Recent Donations:**")
            donations = [
                {"campaign": "Clean Water Project", "amount": 5000, "date": "2024-01-15"},
                {"campaign": "Education Support", "amount": 2000, "date": "2024-01-10"}
            ]
            for donation in donations:
                st.markdown(f"- **{donation['campaign']}**: ₹{donation['amount']:,} on {donation['date']}")
        with tab3:
            st.markdown("#### My Campaigns")
            if st.session_state.get('user_type') == 'organization':
                st.markdown("**Active Campaigns:**")
                st.markdown("- Education for All: ₹45,000 raised (75% of goal)")
                st.markdown("- Clean Water Initiative: ₹32,000 raised (64% of goal)")
            else: st.info("Only organizations can create and manage campaigns.")
    else:
        st.warning("Please log in to view your profile.")
        if st.button("Go to Login"):
            st.session_state.authenticated = False
            st.rerun()

def bottom_navigation():
    """Renders the fixed bottom navigation bar with links to different pages."""
    lang = st.session_state.get('language', 'en')
    st.markdown(f"""
    <div class="bottom-nav">
        <div class="nav-item" onclick="setPage('trending')">
            <div style="font-size: 1.5rem;">📈</div>
            <div style="font-size: 0.8rem;">{get_translated_text('trending_nav', lang)}</div>
        </div>
        <div class="nav-item" onclick="setPage('search')">
            <div style="font-size: 1.5rem;">🔍</div>
            <div style="font-size: 0.8rem;">{get_translated_text('search_nav', lang)}</div>
        </div>
        <div class="nav-item" onclick="setPage('explore')">
            <div style="font-size: 1.5rem;">📱</div>
            <div style="font-size: 0.8rem;">{get_translated_text('explore_nav', lang)}</div>
        </div>
        <div class="nav-item" onclick="setPage('profile')">
            <div style="font-size: 1.5rem;">👤</div>
            <div style="font-size: 0.8rem;">{get_translated_text('profile_nav', lang)}</div>
        </div>
    </div>
    
    <script>
    function setPage(page) {{ window.location.href = '?page=' + page; }}
    </script>
    """, unsafe_allow_html=True)

# --- Main application logic ---
def main():
    """
    Main function to handle page routing based on URL parameters and session state.
    """
    query_params = st.experimental_get_query_params()
    page = query_params.get('page', ['login'])[0]
    load_custom_css(page)
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False
    if 'user_type' not in st.session_state: st.session_state.user_type = None
    if 'language' not in st.session_state: st.session_state.language = 'en'
    if not st.session_state.authenticated and page not in ['login', 'register']: page = 'login'
    
    if page not in ['login', 'register']: top_navigation()

    if page == 'login': login_page()
    elif page == 'register': register_page()
    elif page == 'trending': trending_page(); bottom_navigation()
    elif page == 'search': search_page(); bottom_navigation()
    elif page == 'explore': explore_page(); bottom_navigation()
    elif page == 'profile': profile_page(); bottom_navigation()
    elif page.startswith('campaign_'):
        campaign_id = page.split('_')[1]
        campaign_detail_page(campaign_id); bottom_navigation()
    else:
        if st.session_state.authenticated: trending_page(); bottom_navigation()
        else: login_page()

if __name__ == "__main__":
    main()
