import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import base64
from io import BytesIO
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="HAVEN - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with MaterializeCSS and proper logo integration
st.markdown("""
<head>
    <!-- MaterializeCSS -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
    <!-- Material Icons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <!-- Custom fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
</head>

<style>
    /* Hide Streamlit elements */
    .stApp > header {visibility: hidden;}
    .stApp > div[data-testid="stDecoration"] {visibility: hidden;}
    .stApp > div[data-testid="stToolbar"] {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Full page styling */
    .stApp {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
        font-family: 'Roboto', sans-serif;
    }
    
    /* MaterializeCSS custom colors */
    .btn-haven {
        background: linear-gradient(45deg, #4caf50, #66bb6a) !important;
        border: none;
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
    }
    
    .btn-haven:hover {
        background: linear-gradient(45deg, #388e3c, #4caf50) !important;
        box-shadow: 0 6px 12px rgba(76, 175, 80, 0.4);
    }
    
    /* OAuth buttons */
    .google-btn {
        background: #db4437 !important;
        color: white !important;
    }
    
    .facebook-btn {
        background: #3b5998 !important;
        color: white !important;
    }
    
    .oauth-btn.pulse {
        animation: pulse 2s infinite;
    }
    
    /* Floating Action Button */
    .fixed-action-btn {
        position: fixed;
        right: 23px;
        bottom: 23px;
        z-index: 1000;
    }
    
    .btn-floating.btn-large {
        width: 56px;
        height: 56px;
        background: linear-gradient(45deg, #f44336, #e57373);
        box-shadow: 0 8px 16px rgba(244, 67, 54, 0.3);
    }
    
    .btn-floating.btn-large:hover {
        background: linear-gradient(45deg, #d32f2f, #f44336);
        box-shadow: 0 12px 20px rgba(244, 67, 54, 0.4);
        transform: scale(1.1);
    }
    
    /* Vertical navbar */
    .vertical-navbar {
        position: fixed;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 15px 8px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        z-index: 999;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    
    .nav-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #4caf50;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
    }
    
    .nav-icon:hover {
        background: #4caf50;
        color: white;
        transform: scale(1.1);
    }
    
    /* Tooltips */
    .nav-icon::before {
        content: attr(data-tooltip);
        position: absolute;
        right: 50px;
        background: #333;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .nav-icon:hover::before {
        opacity: 1;
        visibility: visible;
    }
    
    /* Card panels */
    .card-panel {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .card-panel:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* Logo styling */
    .haven-logo {
        max-width: 200px;
        height: auto;
        margin: 20px auto;
        display: block;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .vertical-navbar {
            position: fixed;
            bottom: 0;
            right: 0;
            left: 0;
            top: auto;
            transform: none;
            border-radius: 0;
            flex-direction: row;
            justify-content: space-around;
            padding: 10px;
        }
        
        .fixed-action-btn {
            bottom: 80px;
        }
        
        .haven-logo {
            max-width: 150px;
        }
    }
    
    /* Form styling */
    .input-field input:focus + label {
        color: #4caf50 !important;
    }
    
    .input-field input:focus {
        border-bottom: 1px solid #4caf50 !important;
        box-shadow: 0 1px 0 0 #4caf50 !important;
    }
    
    /* Animation classes */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
</style>

<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'auth'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'

# Backend API URL
BACKEND_URL = "https://haven-fastapi-backend.onrender.com"

# Helper functions
def load_logo():
    """Load and encode the HAVEN logo"""
    try:
        # Try to load the uploaded logo
        with open("/home/ubuntu/upload/haven_logo.png", "rb") as f:
            logo_bytes = f.read()
        return base64.b64encode(logo_bytes).decode()
    except:
        # Fallback to a placeholder if logo not found
        return None

def display_logo():
    """Display the HAVEN logo"""
    logo_base64 = load_logo()
    if logo_base64:
        st.markdown(f"""
        <div class="center-align">
            <img src="data:image/png;base64,{logo_base64}" class="haven-logo" alt="HAVEN Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="center-align">
            <h2 style="color: #4caf50; font-weight: 300; margin: 30px 0;">
                🏠 HAVEN
            </h2>
            <p style="color: #666; margin-bottom: 30px;">Crowdfunding Platform</p>
        </div>
        """, unsafe_allow_html=True)

# Vertical Navigation Bar
def display_navbar():
    if st.session_state.user:
        st.markdown("""
        <div class="vertical-navbar">
            <div class="nav-icon" data-tooltip="Home" onclick="setPage('home')">
                <i class="material-icons">home</i>
            </div>
            <div class="nav-icon" data-tooltip="Explore" onclick="setPage('explore')">
                <i class="material-icons">explore</i>
            </div>
            <div class="nav-icon" data-tooltip="Search" onclick="setPage('search')">
                <i class="material-icons">search</i>
            </div>
            <div class="nav-icon" data-tooltip="Profile" onclick="setPage('profile')">
                <i class="material-icons">person</i>
            </div>
            <div class="nav-icon" data-tooltip="Logout" onclick="logout()">
                <i class="material-icons">logout</i>
            </div>
        </div>
        
        <script>
            function setPage(page) {
                // This would be handled by Streamlit in a real implementation
                console.log('Navigate to:', page);
            }
            
            function logout() {
                // This would be handled by Streamlit in a real implementation
                console.log('Logout');
            }
        </script>
        """, unsafe_allow_html=True)

# Floating Action Button
def display_fab():
    if st.session_state.user:
        st.markdown("""
        <div class="fixed-action-btn">
            <a class="btn-floating btn-large waves-effect waves-light red" onclick="createCampaign()">
                <i class="material-icons">add</i>
            </a>
        </div>
        
        <script>
            function createCampaign() {
                // This would be handled by Streamlit in a real implementation
                console.log('Create campaign');
            }
        </script>
        """, unsafe_allow_html=True)

# OAuth popup functionality
def oauth_popup_script():
    st.markdown("""
    <script>
        let oauthWindow = null;
        
        function openOAuthPopup(provider) {
            // Show loading state
            const button = event.target.closest('button');
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="material-icons left">hourglass_empty</i>Loading...';
            button.disabled = true;
            
            // Get OAuth URL from backend
            fetch(`${window.location.protocol}//${window.location.hostname.replace('haven-streamlit-frontend', 'haven-fastapi-backend')}/api/auth/oauth/${provider}/url`)
                .then(response => response.json())
                .then(data => {
                    if (data.oauth_url) {
                        // Open popup window
                        oauthWindow = window.open(
                            data.oauth_url,
                            'oauth',
                            'width=500,height=600,scrollbars=yes,resizable=yes'
                        );
                        
                        // Monitor popup
                        const checkClosed = setInterval(() => {
                            if (oauthWindow.closed) {
                                clearInterval(checkClosed);
                                button.innerHTML = originalText;
                                button.disabled = false;
                                
                                // Check for authentication success
                                // In a real implementation, this would check for tokens
                                console.log('OAuth popup closed');
                            }
                        }, 1000);
                    }
                })
                .catch(error => {
                    console.error('OAuth error:', error);
                    button.innerHTML = originalText;
                    button.disabled = false;
                    M.toast({html: 'Authentication failed. Please try again.', classes: 'red'});
                });
        }
        
        // Initialize Materialize components
        document.addEventListener('DOMContentLoaded', function() {
            M.AutoInit();
        });
    </script>
    """, unsafe_allow_html=True)

# Authentication page
def show_auth_page():
    display_logo()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.auth_mode == 'login':
            st.markdown("""
            <div class="card-panel white fade-in-up" style="padding: 40px;">
                <div class="center-align">
                    <h4 style="color: #4caf50; margin-bottom: 30px;">Welcome Back</h4>
                    <p style="color: #666; margin-bottom: 30px;">Sign in to your HAVEN account</p>
                </div>
                
                <form id="loginForm">
                    <div class="row">
                        <div class="input-field col s12">
                            <i class="material-icons prefix">email</i>
                            <input id="email" type="email" class="validate" required>
                            <label for="email">Email</label>
                            <span class="helper-text" data-error="Please enter a valid email" data-success="Valid email"></span>
                        </div>
                    </div>

                    <div class="row">
                        <div class="input-field col s12">
                            <i class="material-icons prefix">lock</i>
                            <input id="password" type="password" class="validate" required minlength="6">
                            <label for="password">Password</label>
                            <span class="helper-text" data-error="Password must be at least 6 characters" data-success="Valid password"></span>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col s12">
                            <label>
                                <input type="checkbox" id="remember" />
                                <span>Remember me</span>
                            </label>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col s6">
                            <button class="btn waves-effect waves-light btn-haven" type="submit" style="width: 100%;">
                                Sign In
                                <i class="material-icons right">send</i>
                            </button>
                        </div>
                        <div class="col s6">
                            <button class="btn waves-effect waves-light grey" type="button" onclick="showRegister()" style="width: 100%;">
                                Register
                                <i class="material-icons right">person_add</i>
                            </button>
                        </div>
                    </div>
                </form>

                <div class="divider" style="margin: 30px 0;"></div>

                <div class="row">
                    <div class="col s12 center-align">
                        <p style="color: #666; margin-bottom: 20px;">Or continue with:</p>
                    </div>
                </div>

                <div class="row">
                    <div class="col s6">
                        <button class="btn waves-effect waves-light google-btn oauth-btn pulse" style="width: 100%;" onclick="openOAuthPopup('google')">
                            <i class="material-icons left">search</i>Google
                        </button>
                    </div>
                    <div class="col s6">
                        <button class="btn waves-effect waves-light facebook-btn oauth-btn pulse" style="width: 100%;" onclick="openOAuthPopup('facebook')">
                            <i class="material-icons left">facebook</i>Facebook
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        else:  # Register mode
            st.markdown("""
            <div class="card-panel white fade-in-up" style="padding: 40px;">
                <div class="center-align">
                    <h4 style="color: #4caf50; margin-bottom: 30px;">Join HAVEN</h4>
                    <p style="color: #666; margin-bottom: 30px;">Create your crowdfunding account</p>
                </div>
                
                <form id="registerForm">
                    <div class="row">
                        <div class="input-field col s12">
                            <select id="userType" required>
                                <option value="" disabled selected>Choose account type</option>
                                <option value="individual">Individual</option>
                                <option value="organization">Organization</option>
                                <option value="ngo">NGO</option>
                            </select>
                            <label>Account Type</label>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="input-field col s6">
                            <i class="material-icons prefix">person</i>
                            <input id="firstName" type="text" class="validate" required>
                            <label for="firstName">First Name</label>
                        </div>
                        <div class="input-field col s6">
                            <input id="lastName" type="text" class="validate" required>
                            <label for="lastName">Last Name</label>
                        </div>
                    </div>

                    <div class="row">
                        <div class="input-field col s12">
                            <i class="material-icons prefix">email</i>
                            <input id="regEmail" type="email" class="validate" required>
                            <label for="regEmail">Email</label>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="input-field col s12">
                            <i class="material-icons prefix">phone</i>
                            <input id="phone" type="tel" class="validate">
                            <label for="phone">Phone Number</label>
                        </div>
                    </div>

                    <div class="row">
                        <div class="input-field col s6">
                            <i class="material-icons prefix">lock</i>
                            <input id="regPassword" type="password" class="validate" required minlength="6">
                            <label for="regPassword">Password</label>
                        </div>
                        <div class="input-field col s6">
                            <input id="confirmPassword" type="password" class="validate" required minlength="6">
                            <label for="confirmPassword">Confirm Password</label>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="input-field col s12">
                            <i class="material-icons prefix">location_on</i>
                            <textarea id="address" class="materialize-textarea" data-length="200"></textarea>
                            <label for="address">Address</label>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col s12">
                            <label>
                                <input type="checkbox" id="terms" required />
                                <span>I agree to the <a href="#" style="color: #4caf50;">Terms and Conditions</a></span>
                            </label>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col s12">
                            <label>
                                <input type="checkbox" id="newsletter" />
                                <span>Subscribe to newsletter for updates</span>
                            </label>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col s6">
                            <button class="btn waves-effect waves-light btn-haven" type="submit" style="width: 100%;">
                                Create Account
                                <i class="material-icons right">person_add</i>
                            </button>
                        </div>
                        <div class="col s6">
                            <button class="btn waves-effect waves-light grey" type="button" onclick="showLogin()" style="width: 100%;">
                                Back to Login
                                <i class="material-icons right">arrow_back</i>
                            </button>
                        </div>
                    </div>
                </form>

                <div class="divider" style="margin: 30px 0;"></div>

                <div class="row">
                    <div class="col s12 center-align">
                        <p style="color: #666; margin-bottom: 20px;">Or register with:</p>
                    </div>
                </div>

                <div class="row">
                    <div class="col s6">
                        <button class="btn waves-effect waves-light google-btn oauth-btn pulse" style="width: 100%;" onclick="openOAuthPopup('google')">
                            <i class="material-icons left">search</i>Google
                        </button>
                    </div>
                    <div class="col s6">
                        <button class="btn waves-effect waves-light facebook-btn oauth-btn pulse" style="width: 100%;" onclick="openOAuthPopup('facebook')">
                            <i class="material-icons left">facebook</i>Facebook
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # JavaScript for form handling
    st.markdown("""
    <script>
        function showRegister() {
            // This would be handled by Streamlit in a real implementation
            console.log('Show register form');
        }
        
        function showLogin() {
            // This would be handled by Streamlit in a real implementation
            console.log('Show login form');
        }
        
        // Form submission handlers
        document.addEventListener('DOMContentLoaded', function() {
            // Initialize Materialize components
            M.AutoInit();
            
            // Login form handler
            const loginForm = document.getElementById('loginForm');
            if (loginForm) {
                loginForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    const email = document.getElementById('email').value;
                    const password = document.getElementById('password').value;
                    
                    // Show loading toast
                    M.toast({html: 'Signing in...', classes: 'blue'});
                    
                    // In a real implementation, this would call the backend
                    console.log('Login:', {email, password});
                });
            }
            
            // Register form handler
            const registerForm = document.getElementById('registerForm');
            if (registerForm) {
                registerForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    const password = document.getElementById('regPassword').value;
                    const confirmPassword = document.getElementById('confirmPassword').value;
                    
                    if (password !== confirmPassword) {
                        M.toast({html: 'Passwords do not match!', classes: 'red'});
                        return;
                    }
                    
                    // Show loading toast
                    M.toast({html: 'Creating account...', classes: 'blue'});
                    
                    // In a real implementation, this would call the backend
                    console.log('Register form submitted');
                });
            }
        });
    </script>
    """, unsafe_allow_html=True)

# Home page with campaigns
def show_home_page():
    display_navbar()
    display_fab()
    
    st.markdown("""
    <div class="container" style="margin-top: 20px;">
        <div class="row">
            <div class="col s12">
                <div class="card-panel teal lighten-2 white-text center-align">
                    <h4>Welcome to HAVEN</h4>
                    <p>Discover amazing crowdfunding campaigns and make a difference in the world.</p>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col s12">
                <h5 style="color: #4caf50;">Trending Campaigns</h5>
            </div>
        </div>
        
        <div class="row">
            <div class="col s12 m6 l4">
                <div class="card">
                    <div class="card-image">
                        <img src="https://images.unsplash.com/photo-1541919329513-35f7af297129?w=400&h=250&fit=crop" alt="Clean Water">
                        <span class="card-title">Clean Water Project</span>
                    </div>
                    <div class="card-content">
                        <p>Providing clean drinking water to rural communities.</p>
                        <div class="progress" style="margin: 10px 0;">
                            <div class="determinate" style="width: 75%; background-color: #4caf50;"></div>
                        </div>
                        <p><strong>₹3,75,000</strong> raised of ₹5,00,000 goal</p>
                    </div>
                    <div class="card-action">
                        <a href="#" class="btn-small btn-haven">Donate Now</a>
                        <a href="#" style="color: #4caf50;">Learn More</a>
                    </div>
                </div>
            </div>
            
            <div class="col s12 m6 l4">
                <div class="card">
                    <div class="card-image">
                        <img src="https://images.unsplash.com/photo-1497486751825-1233686d5d80?w=400&h=250&fit=crop" alt="Education">
                        <span class="card-title">Education Support</span>
                    </div>
                    <div class="card-content">
                        <p>Supporting underprivileged children's education.</p>
                        <div class="progress" style="margin: 10px 0;">
                            <div class="determinate" style="width: 60%; background-color: #4caf50;"></div>
                        </div>
                        <p><strong>₹4,50,000</strong> raised of ₹7,50,000 goal</p>
                    </div>
                    <div class="card-action">
                        <a href="#" class="btn-small btn-haven">Donate Now</a>
                        <a href="#" style="color: #4caf50;">Learn More</a>
                    </div>
                </div>
            </div>
            
            <div class="col s12 m6 l4">
                <div class="card">
                    <div class="card-image">
                        <img src="https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&h=250&fit=crop" alt="Healthcare">
                        <span class="card-title">Healthcare Initiative</span>
                    </div>
                    <div class="card-content">
                        <p>Medical support for cancer patients.</p>
                        <div class="progress" style="margin: 10px 0;">
                            <div class="determinate" style="width: 80%; background-color: #4caf50;"></div>
                        </div>
                        <p><strong>₹1,20,000</strong> raised of ₹1,50,000 goal</p>
                    </div>
                    <div class="card-action">
                        <a href="#" class="btn-small btn-haven">Donate Now</a>
                        <a href="#" style="color: #4caf50;">Learn More</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main app logic
def main():
    oauth_popup_script()
    
    if st.session_state.user is None:
        show_auth_page()
    else:
        if st.session_state.page == 'home':
            show_home_page()
        # Add other pages here

if __name__ == "__main__":
    main()

