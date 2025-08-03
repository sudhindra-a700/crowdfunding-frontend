"""
HAVEN Crowdfunding Platform - Enhanced Streamlit OAuth Integration
OAuth integration with translation and simplification support
"""

import streamlit as st
import requests
import json
import time
from typing import Dict, Optional
from urllib.parse import urlencode, parse_qs, urlparse
import hashlib
import secrets

# Configuration
BACKEND_URL = st.secrets.get("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")

# Language support
SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "flag": "🇺🇸", "native": "English"},
    "hi": {"name": "Hindi", "flag": "🇮🇳", "native": "हिन्दी"},
    "ta": {"name": "Tamil", "flag": "🇮🇳", "native": "தமிழ்"},
    "te": {"name": "Telugu", "flag": "🇮🇳", "native": "తెలుగు"}
}

class EnhancedOAuthManager:
    """Enhanced OAuth manager with translation support"""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.session_key = "oauth_session"
        self.user_key = "user_data"
        self.language_key = "user_language"
        
        # Initialize session state
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {}
        
        if self.user_key not in st.session_state:
            st.session_state[self.user_key] = None
        
        if self.language_key not in st.session_state:
            st.session_state[self.language_key] = "en"
    
    def translate_text(self, text: str, target_language: str = None) -> str:
        """Translate text using backend API"""
        if not target_language:
            target_language = st.session_state.get(self.language_key, "en")
        
        if not text or target_language == "en":
            return text
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/translate/quick",
                params={
                    "text": text,
                    "target_language": target_language,
                    "source_language": "en"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("translated_text", text)
            else:
                return text
        
        except Exception:
            return text
    
    def display_translated_text(self, text: str, markdown: bool = True):
        """Display text with translation if needed"""
        translated = self.translate_text(text)
        
        if markdown:
            st.markdown(translated)
        else:
            st.text(translated)
    
    def generate_state_token(self) -> str:
        """Generate secure state token for OAuth"""
        return secrets.token_urlsafe(32)
    
    def get_oauth_url(self, provider: str) -> str:
        """Get OAuth URL for provider"""
        if provider.lower() == "google":
            return f"{self.backend_url}/auth/google/login"
        elif provider.lower() == "facebook":
            return f"{self.backend_url}/auth/facebook/login"
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def handle_oauth_callback(self, provider: str, code: str, state: str) -> Dict:
        """Handle OAuth callback"""
        try:
            # Verify state token
            stored_state = st.session_state[self.session_key].get(f"{provider}_state")
            if not stored_state or stored_state != state:
                return {"error": "Invalid state token"}
            
            # Exchange code for tokens
            callback_url = f"{self.backend_url}/auth/{provider}/callback"
            response = requests.get(
                callback_url,
                params={"code": code, "state": state},
                timeout=30
            )
            
            if response.status_code == 200:
                user_data = response.json()
                
                # Store user data
                st.session_state[self.user_key] = user_data
                
                # Clear OAuth session
                if f"{provider}_state" in st.session_state[self.session_key]:
                    del st.session_state[self.session_key][f"{provider}_state"]
                
                return {"success": True, "user": user_data}
            else:
                return {"error": f"OAuth callback failed: {response.status_code}"}
        
        except Exception as e:
            return {"error": f"OAuth callback error: {str(e)}"}
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state[self.user_key] is not None
    
    def get_user_data(self) -> Optional[Dict]:
        """Get current user data"""
        return st.session_state[self.user_key]
    
    def logout(self):
        """Logout user"""
        st.session_state[self.user_key] = None
        st.session_state[self.session_key] = {}
        
        # Clear any cached data
        for key in list(st.session_state.keys()):
            if key.startswith("oauth_") or key.startswith("user_"):
                del st.session_state[key]
    
    def render_language_selector(self):
        """Render language selector"""
        st.markdown("### 🌍 Language Settings")
        
        current_lang = st.session_state.get(self.language_key, "en")
        
        language_options = [
            f"{lang_info['flag']} {lang_info['native']}" 
            for lang_code, lang_info in SUPPORTED_LANGUAGES.items()
        ]
        
        selected_lang_display = st.selectbox(
            "Select your preferred language:",
            language_options,
            index=list(SUPPORTED_LANGUAGES.keys()).index(current_lang),
            key="oauth_language_selector"
        )
        
        # Extract language code from selection
        for lang_code, lang_info in SUPPORTED_LANGUAGES.items():
            if f"{lang_info['flag']} {lang_info['native']}" == selected_lang_display:
                if st.session_state[self.language_key] != lang_code:
                    st.session_state[self.language_key] = lang_code
                    st.rerun()
                break
    
    def render_oauth_buttons(self):
        """Render OAuth login buttons"""
        st.markdown("### 🔐 Sign In Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔴 Sign in with Google", key="google_oauth", type="primary"):
                self.initiate_oauth("google")
        
        with col2:
            if st.button("🔵 Sign in with Facebook", key="facebook_oauth", type="primary"):
                self.initiate_oauth("facebook")
    
    def initiate_oauth(self, provider: str):
        """Initiate OAuth flow"""
        try:
            # Generate and store state token
            state_token = self.generate_state_token()
            st.session_state[self.session_key][f"{provider}_state"] = state_token
            
            # Get OAuth URL
            oauth_url = self.get_oauth_url(provider)
            
            # Add state parameter if needed
            if "?" in oauth_url:
                oauth_url += f"&state={state_token}"
            else:
                oauth_url += f"?state={state_token}"
            
            # Redirect user
            st.markdown(f"""
            <script>
                window.open('{oauth_url}', '_blank');
            </script>
            """, unsafe_allow_html=True)
            
            st.info(f"🔄 Redirecting to {provider.title()} for authentication...")
            st.markdown(f"[Click here if redirect doesn't work]({oauth_url})")
            
        except Exception as e:
            st.error(f"OAuth initiation failed: {str(e)}")
    
    def render_user_profile(self):
        """Render user profile section"""
        user_data = self.get_user_data()
        
        if not user_data:
            return
        
        st.markdown("### 👤 User Profile")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Profile picture
            profile_pic = user_data.get("picture", "https://via.placeholder.com/150")
            st.image(profile_pic, width=150, caption="Profile Picture")
        
        with col2:
            # User information
            name = user_data.get("name", "Unknown User")
            email = user_data.get("email", "No email")
            provider = user_data.get("provider", "Unknown")
            
            self.display_translated_text(f"**Name:** {name}")
            self.display_translated_text(f"**Email:** {email}")
            self.display_translated_text(f"**Provider:** {provider.title()}")
            
            if "locale" in user_data:
                self.display_translated_text(f"**Locale:** {user_data['locale']}")
            
            # Logout button
            if st.button("🚪 Sign Out", key="logout_button"):
                self.logout()
                st.rerun()
    
    def render_authentication_page(self):
        """Render complete authentication page"""
        st.markdown("## 🔐 Authentication")
        
        # Language selector
        self.render_language_selector()
        
        st.markdown("---")
        
        if self.is_authenticated():
            # Show user profile
            self.render_user_profile()
            
            # Show user statistics
            st.markdown("---")
            st.markdown("### 📊 Your Activity")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Campaigns Created", "0")
            with col2:
                st.metric("Projects Supported", "0")
            with col3:
                st.metric("Total Contributed", "$0")
            
            self.display_translated_text("""
            **Welcome to HAVEN!** You can now create campaigns, support projects, 
            and access all platform features. Your profile information is securely 
            stored and can be updated at any time.
            """)
        
        else:
            # Show login options
            self.display_translated_text("""
            **Welcome to HAVEN Crowdfunding Platform!** 
            
            Sign in to access all features including:
            - Create and manage crowdfunding campaigns
            - Support innovative projects
            - Track your contributions and rewards
            - Access multilingual content
            - Get simplified explanations of complex terms
            """)
            
            st.markdown("---")
            
            # OAuth buttons
            self.render_oauth_buttons()
            
            st.markdown("---")
            
            # Manual login form
            self.render_manual_login_form()
    
    def render_manual_login_form(self):
        """Render manual login form"""
        st.markdown("### 📝 Manual Sign In")
        
        with st.form("manual_login"):
            email = st.text_input("Email Address", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("🔑 Sign In", type="primary"):
                    if email and password:
                        # Mock authentication for demo
                        mock_user_data = {
                            "name": "Demo User",
                            "email": email,
                            "provider": "manual",
                            "picture": "https://via.placeholder.com/150",
                            "locale": st.session_state[self.language_key]
                        }
                        
                        st.session_state[self.user_key] = mock_user_data
                        st.success("✅ Successfully signed in!")
                        st.rerun()
                    else:
                        st.error("Please enter both email and password")
            
            with col2:
                if st.form_submit_button("📝 Create Account"):
                    st.info("Account creation would be handled here")
    
    def handle_oauth_redirect(self):
        """Handle OAuth redirect from URL parameters"""
        # Get URL parameters
        query_params = st.experimental_get_query_params()
        
        if "code" in query_params and "state" in query_params:
            code = query_params["code"][0]
            state = query_params["state"][0]
            
            # Determine provider from state or URL
            provider = None
            if "google" in str(query_params):
                provider = "google"
            elif "facebook" in str(query_params):
                provider = "facebook"
            
            if provider:
                with st.spinner(f"Completing {provider.title()} authentication..."):
                    result = self.handle_oauth_callback(provider, code, state)
                    
                    if "success" in result:
                        st.success(f"✅ Successfully signed in with {provider.title()}!")
                        
                        # Clear URL parameters
                        st.experimental_set_query_params()
                        st.rerun()
                    else:
                        st.error(f"❌ Authentication failed: {result.get('error', 'Unknown error')}")
    
    def render_protected_content(self, content_func):
        """Render content only if user is authenticated"""
        if self.is_authenticated():
            content_func()
        else:
            st.warning("🔒 Please sign in to access this content")
            
            with st.expander("🔐 Sign In"):
                self.render_oauth_buttons()
    
    def get_user_language(self) -> str:
        """Get user's preferred language"""
        user_data = self.get_user_data()
        
        if user_data and "locale" in user_data:
            # Try to map locale to supported language
            locale = user_data["locale"].lower()
            if locale.startswith("hi"):
                return "hi"
            elif locale.startswith("ta"):
                return "ta"
            elif locale.startswith("te"):
                return "te"
        
        return st.session_state.get(self.language_key, "en")
    
    def update_user_language(self, language: str):
        """Update user's language preference"""
        st.session_state[self.language_key] = language
        
        # Update user data if authenticated
        if self.is_authenticated():
            user_data = st.session_state[self.user_key]
            user_data["locale"] = language
            st.session_state[self.user_key] = user_data

# Global OAuth manager instance
oauth_manager = None

def get_oauth_manager() -> EnhancedOAuthManager:
    """Get or create OAuth manager instance"""
    global oauth_manager
    if oauth_manager is None:
        oauth_manager = EnhancedOAuthManager()
    return oauth_manager

# Utility functions for easy integration
def require_authentication(func):
    """Decorator to require authentication for a function"""
    def wrapper(*args, **kwargs):
        oauth_mgr = get_oauth_manager()
        if oauth_mgr.is_authenticated():
            return func(*args, **kwargs)
        else:
            st.warning("🔒 Authentication required")
            oauth_mgr.render_oauth_buttons()
            return None
    return wrapper

def translate_for_user(text: str) -> str:
    """Translate text for current user's language"""
    oauth_mgr = get_oauth_manager()
    return oauth_mgr.translate_text(text)

def display_user_text(text: str, markdown: bool = True):
    """Display text translated for user"""
    oauth_mgr = get_oauth_manager()
    oauth_mgr.display_translated_text(text, markdown)

# Example usage and testing
if __name__ == "__main__":
    st.title("🔐 OAuth Integration Test")
    
    oauth_mgr = get_oauth_manager()
    
    # Handle OAuth redirects
    oauth_mgr.handle_oauth_redirect()
    
    # Render authentication page
    oauth_mgr.render_authentication_page()
    
    # Test protected content
    st.markdown("---")
    st.markdown("## 🔒 Protected Content Test")
    
    def protected_content():
        st.success("🎉 You have access to protected content!")
        display_user_text("This content is only available to authenticated users.")
    
    oauth_mgr.render_protected_content(protected_content)

