# Streamlit OAuth Integration for HAVEN Crowdfunding Platform
# Add this to your existing front_main.py file

import streamlit as st
import requests
import json
import time
from urllib.parse import urlencode, parse_qs

# OAuth Configuration for your Render backend
BACKEND_URL = "https://srv-d1sq8ser433s73eke7v0.onrender.com"

class StreamlitOAuthService:
    """OAuth service specifically designed for Streamlit applications"""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.token_key = 'oauth_access_token'
        self.user_key = 'oauth_user_profile'
        
    def is_authenticated(self):
        """Check if user is authenticated"""
        token = st.session_state.get(self.token_key)
        if not token:
            return False
        
        try:
            # Simple JWT expiration check
            import base64
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

def render_oauth_buttons():
    """Render OAuth login buttons with proper styling"""
    
    # Check OAuth provider status
    oauth_status = oauth_service.check_oauth_status()
    
    st.markdown("""
    <style>
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
    
    .oauth-button {
        display: inline-block;
        width: 100%;
        max-width: 300px;
        padding: 12px 24px;
        margin: 8px;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        text-decoration: none;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .google-oauth {
        background-color: #4285f4;
        color: white;
    }
    
    .google-oauth:hover {
        background-color: #357ae8;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(66, 133, 244, 0.3);
    }
    
    .facebook-oauth {
        background-color: #1877f2;
        color: white;
    }
    
    .facebook-oauth:hover {
        background-color: #166fe5;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(24, 119, 242, 0.3);
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
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="oauth-container">
        <div class="oauth-title">Sign in with your social account</div>
    """, unsafe_allow_html=True)
    
    # Create columns for buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if oauth_status.get('google_available', False):
            if st.button("🔍 Sign in with Google", key="google_oauth", help="Sign in using your Google account"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={oauth_service.get_google_auth_url()}">', unsafe_allow_html=True)
                st.write("Redirecting to Google...")
        else:
            st.button("🔍 Google (Not Available)", disabled=True, help="Google OAuth is not configured")
    
    with col2:
        if oauth_status.get('facebook_available', False):
            if st.button("📘 Sign in with Facebook", key="facebook_oauth", help="Sign in using your Facebook account"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={oauth_service.get_facebook_auth_url()}">', unsafe_allow_html=True)
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
    
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)
    
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
    query_params = st.query_params
    
    if 'access_token' in query_params or 'error' in query_params:
        return oauth_service.handle_oauth_callback()
    
    return False

# Modified login function to include OAuth
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

# Enhanced authentication check
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

# Usage instructions for integration:
"""
To integrate OAuth into your existing front_main.py:

1. Add the imports at the top:
   from streamlit_oauth_integration import (
       oauth_service, render_oauth_buttons, render_user_profile_widget,
       check_oauth_callback, login_user_with_oauth, logout_user_enhanced,
       is_user_authenticated, get_enhanced_auth_headers
   )

2. Replace your existing login_user function with login_user_with_oauth

3. Replace your existing logout_user function with logout_user_enhanced

4. Replace your existing get_auth_headers function with get_enhanced_auth_headers

5. Replace st.session_state.logged_in checks with is_user_authenticated()

6. In your render_login_page function, add OAuth buttons:
   render_oauth_buttons()

7. Add user profile widget to sidebar:
   render_user_profile_widget()

8. Add OAuth callback check at the start of your main app:
   if check_oauth_callback():
       st.rerun()

9. Update your BACKEND_URL to point to your Render service:
   BACKEND_URL = "https://srv-d1sq8ser433s73eke7v0.onrender.com"
"""

