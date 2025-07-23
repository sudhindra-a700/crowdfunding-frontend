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
        # Get URL parameters
        query_params = st.experimental_get_query_params()

        access_token = query_params.get('access_token', [None])[0]
        error = query_params.get('error', [None])[0]

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
                    st.experimental_set_query_params()

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

# --- Custom CSS for global styling --- #
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

    /* OAuth Styling */
    .oauth-container {
        background: #f0f8f0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
        text-align: center;
    }

    .oauth-title {
        color: #2d5a2d;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 20px;
    }

    .oauth-divider {
        margin: 20px 0;
        text-align: center;
        position: relative;
    }

    .oauth-divider::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background: #ddd;
    }

    .oauth-divider span {
        background: #f0f8f0;
        padding: 0 15px;
        color: #666;
        font-size: 14px;
    }

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
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Backend Connection Configuration --- #
BACKEND_SERVICE_NAME = os.environ.get("BACKEND_SERVICE_NAME", "haven-fastapi-backend")
BACKEND_PORT = os.environ.get("BACKEND_PORT", "8000")
BACKEND_URL = "https://srv-d1sq8ser433s73eke7v0.onrender.com"  # Your Render backend URL

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
        "enter_otp": "Enter OTP",
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
    # ... (other language translations remain the same)
}

# Get current language from session state or set default
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'


# Function to get translated text
def t(key):
    english_text = translations["en"].get(key, key)
    if st.session_state.lang == "en":
        return english_text
    # Add translation logic for other languages if needed
    return english_text


# --- Page Navigation State --- #
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
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


def login_user_with_oauth(email, password):
    """Enhanced login function that supports both traditional and OAuth login"""
    try:
        response = requests.post(f"{BACKEND_URL}/login", json={"email": email, "password": password})
        response.raise_for_status()
        token_data = response.json()

        # Store traditional auth data
        st.session_state.auth_token = token_data.get("access_token")
        st.session_state.user_role = token_data.get("role", "user")
        st.session_state.logged_in = True
        st.session_state.username = email
        st.session_state.current_page = "home"

        st.success(f"Welcome, {email}!")
        st.rerun()
    except requests.exceptions.HTTPError as e:
        st.error(f"Login failed: {e.response.json().get('detail', 'Incorrect email or password')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Login failed: Could not connect to backend. Is it running? {e}")


def logout_user_enhanced():
    """Enhanced logout function that handles both traditional and OAuth logout"""
    if oauth_service.is_authenticated():
        oauth_service.logout()
    else:
        # Traditional logout
        st.session_state.logged_in = False
        st.session_state.auth_token = None
        st.session_state.username = None
        st.session_state.user_role = "user"
        st.session_state.current_page = "login"
        st.success("Logged out successfully.")
        st.rerun()


def render_oauth_buttons():
    """Render OAuth login buttons with proper styling"""

    # Check OAuth provider status
    oauth_status = oauth_service.check_oauth_status()

    st.markdown("""
    <div class="oauth-container">
        <div class="oauth-title">Sign in with your social account</div>
    """, unsafe_allow_html=True)

    # Create columns for buttons
    col1, col2 = st.columns(2)

    with col1:
        if oauth_status.get('google_available', False):
            if st.button("🔍 Sign in with Google", key="google_oauth", help="Sign in using your Google account"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={oauth_service.get_google_auth_url()}">',
                            unsafe_allow_html=True)
                st.write("Redirecting to Google...")
        else:
            st.button("🔍 Google (Not Available)", disabled=True, help="Google OAuth is not configured")

    with col2:
        if oauth_status.get('facebook_available', False):
            if st.button("📘 Sign in with Facebook", key="facebook_oauth", help="Sign in using your Facebook account"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={oauth_service.get_facebook_auth_url()}">',
                            unsafe_allow_html=True)
                st.write("Redirecting to Facebook...")
        else:
            st.button("📘 Facebook (Not Available)", disabled=True, help="Facebook OAuth is not configured")

    st.markdown("</div>", unsafe_allow_html=True)

    # Add divider
    st.markdown("""
    <div class="oauth-divider">
        <span>or continue with email</span>
    </div>
    """, unsafe_allow_html=True)


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


def check_oauth_callback():
    """Check for OAuth callback and handle it"""
    query_params = st.experimental_get_query_params()

    if 'access_token' in query_params or 'error' in query_params:
        return oauth_service.handle_oauth_callback()

    return False


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
        st.error(f"HTTP error fetching campaigns: {e.response.status_code} - {e.response.text}")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return []


def register_user_backend(user_data):
    """Registers a new user with the backend."""
    try:
        response = requests.post(f"{BACKEND_URL}/register", json=user_data)
        response.raise_for_status()
        st.success("Registration successful! Please log in.")
        st.session_state.current_page = "login"
        st.rerun()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"Registration failed: {e.response.json().get('detail', 'Unknown error')}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Registration failed: Could not connect to backend. Is it running? {e}")
        return None


# --- Render Pages based on current_page --- #

def render_login_page():
    with st.form(key='login_form'):
        st.markdown(f"""
        <div class="container">
          <div class="title">{t("login_title")}</div>
        """, unsafe_allow_html=True)

        # Add OAuth buttons at the top
        st.markdown("</div>", unsafe_allow_html=True)
        render_oauth_buttons()
        st.markdown('<div class="container">', unsafe_allow_html=True)

        email = st.text_input(t("email_id"), key="login_email")
        password = st.text_input(t("enter_otp"), type="password", key="login_password")

        submit_button = st.form_submit_button(t("continue_btn"))

        st.markdown(f"""
          <div class="option">
            {t("not_registered")}
            <a href="#" id="create_account_link">{t("create_account")}</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if submit_button:
            login_user_with_oauth(email, password)

    # Handle navigation to register page from login
    st.markdown("""
    <script>
        document.getElementById("create_account_link").onclick = function() {
            const streamlitButton = document.getElementById("hidden_register_button");
            if (streamlitButton) {
                streamlitButton.click();
            }
        };
    </script>
    """, unsafe_allow_html=True)
    if st.button("", key="hidden_register_button", help="Go to registration", disabled=True):
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
            otp = st.text_input(t("enter_otp"), key="reg_otp")
            user_data = {"full_name": full_name, "email": email, "phone_number": phone_number, "otp": otp,
                         "type": "individual"}

        elif st.session_state.registration_type == 'organization':
            org_name = st.text_input(t("organization_name"), key="reg_org_name")
            org_phone = st.text_input(t("organization_phone"), key="reg_org_phone")
            org_type = st.selectbox(t("select_org_type"), ["", "NGO", "Startup", "Charity"], key="reg_org_type")
            brief_description = st.text_area(t("brief_description"), max_chars=100, key="reg_brief_desc")
            email = st.text_input(t("email_id"), key="reg_email_org")
            otp = st.text_input(t("enter_otp"), key="reg_otp_org")
            user_data = {"organization_name": org_name, "organization_phone": org_phone, "organization_type": org_type,
                         "brief_description": brief_description, "email": email, "otp": otp, "type": "organization"}

        st.markdown(f"""
            </div>

            <div class="input-box button">
              <input type="submit" value="{t("register_btn")}" />
            </div>
          </div>
        """, unsafe_allow_html=True)

        submit_button = st.form_submit_button(t("register_btn"))

        if submit_button:
            register_user_backend(user_data)


def render_home_page():
    st.markdown(f"""
    <div class="container">
        <h1>{t("welcome_haven")}</h1>
        <p>{t("support_popular_projects")}</p>
        <div class="campaign-card">
            <img src="https://via.placeholder.com/600x400" alt="Campaign Image">
            <h3>Sustainable Farming Initiative</h3>
            <p>By Green Earth Foundation</p>
            <p>Support local farmers in adopting sustainable practices.</p>
            <p>₹75,000 raised of ₹100,000 goal</p>
            <p>30 days left</p>
        </div>
        <div class="campaign-card">
            <img src="https://via.placeholder.com/600x400" alt="Campaign Image">
            <h3>Clean Water Project</h3>
            <p>By Water for All</p>
            <p>Provide access to clean and safe drinking water.</p>
            <p>₹50,000 raised of ₹80,000 goal</p>
            <p>45 days left</p>
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
        logout_user_enhanced()
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

# You can add a button to test backend connectivity (for debugging)
if st.sidebar.button("Test Backend Connection"):
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            st.success(f"✅ Backend connected successfully!")
            health_data = response.json()
            if 'oauth' in health_data:
                oauth_info = health_data['oauth']
                st.info(
                    f"OAuth Status: Google: {'✅' if oauth_info.get('google_configured') else '❌'}, Facebook: {'✅' if oauth_info.get('facebook_configured') else '❌'}")
        else:
            st.error(f"❌ Backend connection failed. Status: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Failed to connect to backend: {str(e)}")

# Add Font Awesome for icons
st.markdown(
    "<link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css\">",
    unsafe_allow_html=True)

