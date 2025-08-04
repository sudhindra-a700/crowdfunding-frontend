# front_main.py
# This is the corrected and complete Streamlit frontend application.
# It now includes the necessary imports for `Optional` and `Dict`
# to resolve the latest NameError.

import streamlit as st
import requests
import base64
from datetime import datetime
import json
import os
from urllib.parse import urlencode
import time
from dotenv import load_dotenv
from typing import Optional, Dict # Added this import

# --- Environment Variable Loading ---
load_dotenv()

# --- Backend URL Configuration ---
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="HAVEN - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load HAVEN logo
def load_logo():
    """Loads the logo from the file system and encodes it to base64."""
    try:
        # Assuming the logo is available in the current directory or a known path
        with open("haven_logo.png", "rb") as f:
            logo_data = f.read()
        return base64.b64encode(logo_data).decode()
    except FileNotFoundError:
        # Fallback to a placeholder if the file is not found
        st.warning("HAVEN logo not found. Using a placeholder.")
        return None
    except Exception as e:
        st.error(f"Error loading logo: {e}")
        return None

# Custom CSS for exact design match
def load_custom_css(page: str):
    """
    Loads custom CSS to style the app.
    It includes specific styles for different pages like login.
    """
    logo_base64 = load_logo()
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-image" />' if logo_base64 else ''

    css = f"""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Main container styling */
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }}
    
    /* Login page styling - Light blue background */
    .login-container {{
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        min-height: 100vh;
        padding: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    .login-form-container {{
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 400px;
        text-align: center;
    }}
    
    .logo-image {{
        max-width: 150px;
        margin-bottom: 2rem;
    }}
    
    /* General styles */
    body {{
        font-family: 'Inter', sans-serif;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 600;
        color: #1a237e;
    }}
    
    .stButton > button {{
        width: 100%;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        margin-top: 10px;
    }}
    
    /* Specific button styles */
    .stButton > button[kind="primary"] {{
        background-color: #2e7d32;
    }}
    
    .stButton > button[kind="secondary"] {{
        background-color: #1976d2;
    }}
    
    .social-login-button {{
        background-color: #4285f4;
    }}
    
    .facebook-button {{
        background-color: #1877f2;
    }}

    .stProgress > div > div > div > div {{
        background-color: #4CAF50;
    }}
    
    .metric-card {{
        background-color: #e8f5e9;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    
    .category-card {{
        background-color: #f0f4c3;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    
    .campaign-card {{
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 1rem;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }}
    .campaign-card:hover {{
        transform: translateY(-5px);
    }}
    
    .campaign-image {{
        border-radius: 10px;
        width: 100%;
        height: 200px;
        object-fit: cover;
    }}

    .bottom-nav {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #ffffff;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-around;
        padding: 0.5rem 0;
        z-index: 1000;
    }}
    .nav-item {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-decoration: none;
        color: #757575;
        font-size: 0.8rem;
        transition: color 0.2s;
    }}
    .nav-item:hover, .nav-item.active {{
        color: #1a237e;
    }}
    .nav-item i {{
        font-size: 1.5rem;
        margin-bottom: 5px;
    }}
    
    .icon-container {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #e8f5e9;
        color: #2e7d32;
        margin-right: 1rem;
    }}

    .simplification-icon {{
        font-style: normal;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background-color: #2196f3;
        color: white;
        font-weight: bold;
        font-size: 0.8rem;
        cursor: pointer;
    }}

    .tooltip {{
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
    }}

    .tooltip .tooltiptext {{
        visibility: hidden;
        width: 250px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%; /* Position the tooltip above the text */
        left: 50%;
        margin-left: -125px; /* Use half of the width to center the tooltip */
        opacity: 0;
        transition: opacity 0.3s;
    }}

    .tooltip:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
    }}

    </style>
    """
    if page == "login":
        st.markdown(
            f"""
            <div class="login-container">
                <div class="login-form-container">
                    {logo_html}
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(f'<div class="logo-container">{logo_html}</div>', unsafe_allow_html=True)


# Navigation function
def go_to_page(page: str):
    """
    Updates the URL query parameters to change the page without a full reload.
    """
    query_params = st.experimental_get_query_params()
    query_params["page"] = [page]
    st.experimental_set_query_params(**query_params)
    st.session_state.current_page = page

# Bottom navigation bar
def bottom_navigation():
    """Renders the bottom navigation bar with different icons."""
    st.markdown("""
    <div class="bottom-nav">
        <a href="?page=trending" class="nav-item">
            <i class="material-icons">local_fire_department</i>
            <span>Trending</span>
        </a>
        <a href="?page=explore" class="nav-item">
            <i class="material-icons">explore</i>
            <span>Explore</span>
        </a>
        <a href="?page=search" class="nav-item">
            <i class="material-icons">search</i>
            <span>Search</span>
        </a>
        <a href="?page=profile" class="nav-item">
            <i class="material-icons">person</i>
            <span>Profile</span>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Helper function to get data from the backend
def fetch_data(endpoint: str, params: Optional[Dict] = None):
    """Fetches data from a given backend endpoint."""
    try:
        response = requests.get(f"{BACKEND_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# --- Page functions ---

def login_page():
    """Renders the login page with OAuth buttons."""
    # The login page CSS is handled by load_custom_css
    
    st.markdown("""
    <h2 style="text-align: center; color: #1a237e;">Sign In</h2>
    <p style="text-align: center; color: #555;">Welcome back to HAVEN</p>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In")

        if submitted:
            # Simulate a successful login
            if email and password:
                st.session_state.authenticated = True
                go_to_page('trending')
                st.experimental_rerun()
            else:
                st.error("Please enter both email and password.")

    st.markdown("""
    <div style="text-align: center; margin-top: 1rem;">
        <p>or</p>
    </div>
    """, unsafe_allow_html=True)

    # Google OAuth button
    google_oauth_url = f"{BACKEND_URL}/auth/google/login"
    st.markdown(f'<a href="{google_oauth_url}" target="_self"><button class="stButton" style="background-color: #4285f4; color: white;">Sign in with Google</button></a>', unsafe_allow_html=True)

    # Facebook OAuth button
    facebook_oauth_url = f"{BACKEND_URL}/auth/facebook/login"
    st.markdown(f'<a href="{facebook_oauth_url}" target="_self"><button class="stButton" style="background-color: #1877f2; color: white; margin-top: 10px;">Sign in with Facebook</button></a>', unsafe_allow_html=True)
    
    if st.button("Don't have an account? Sign Up", key="signup_redirect"):
        go_to_page('register')
        st.experimental_rerun()

def register_page():
    """Renders the registration page."""
    st.markdown(
        f"""
        <style>{load_custom_css('register')}</style>
        <div class="login-form-container">
            <h2 style="text-align: center; color: #1a237e;">Sign Up</h2>
            <p style="text-align: center; color: #555;">Join HAVEN today</p>
        </div>
        """, unsafe_allow_html=True
    )

    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if password != confirm_password:
                st.error("Passwords do not match.")
            else:
                st.success("Registration successful! Please sign in.")
                go_to_page('login')
                st.experimental_rerun()

def trending_page():
    """Renders the trending campaigns page."""
    st.header("Trending Campaigns 🔥")
    trending_data = fetch_data("/api/trending")
    if trending_data and trending_data.get('campaigns'):
        campaigns = trending_data['campaigns']
        num_columns = 2
        columns = st.columns(num_columns)
        for i, campaign in enumerate(campaigns):
            with columns[i % num_columns]:
                st.markdown(f"""
                <div class="campaign-card" onclick="window.location.href='?page=campaign_{campaign['id']}'" style="cursor:pointer;">
                    <img src="{campaign['image_url']}" class="campaign-image" />
                    <h5 style="margin-top: 10px;">{campaign['title']}</h5>
                    <p style="color: #555;">{campaign['organization']}</p>
                    <p><b>₹{campaign['current_amount']:,}</b> raised of ₹{campaign['target_amount']:,}</p>
                    <div style="height: 10px; background-color: #f0f0f0; border-radius: 5px;">
                        <div style="width: {campaign['progress']}%; height: 100%; background-color: #2e7d32; border-radius: 5px;"></div>
                    </div>
                    <p style="font-size: 0.8rem; text-align: right; margin-top: 5px;">{campaign['days_left']} days left</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No trending campaigns found.")

def explore_page():
    """Renders the explore campaigns page."""
    st.header("Explore All Campaigns")
    all_campaigns_data = fetch_data("/api/campaigns")
    if all_campaigns_data and all_campaigns_data.get('campaigns'):
        campaigns = all_campaigns_data['campaigns']
        for campaign in campaigns:
            st.markdown(f"""
            <div class="campaign-card" onclick="window.location.href='?page=campaign_{campaign['id']}'" style="cursor:pointer;">
                <h5 style="margin-top: 0;">{campaign['title']}</h5>
                <p style="color: #555;">{campaign['organization']}</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <p><b>₹{campaign['current_amount']:,}</b> raised</p>
                    <span style="background-color: #e3f2fd; padding: 5px 10px; border-radius: 15px; font-size: 0.8rem; color: #1a237e;">{campaign['category']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No campaigns to explore.")

def search_page():
    """Renders the search campaigns page."""
    st.header("Search Campaigns")
    search_query = st.text_input("Search for campaigns...")
    if search_query:
        search_results = fetch_data("/api/search", params={"q": search_query})
        if search_results and search_results.get('campaigns'):
            st.subheader(f"Results for '{search_query}'")
            for campaign in search_results['campaigns']:
                st.markdown(f"""
                <div class="campaign-card" onclick="window.location.href='?page=campaign_{campaign['id']}'" style="cursor:pointer;">
                    <h5 style="margin-top: 0;">{campaign['title']}</h5>
                    <p style="color: #555;">{campaign['organization']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"No campaigns found for '{search_query}'.")
    else:
        st.info("Start typing to search for campaigns.")

def profile_page():
    """Renders the user profile page."""
    st.header("My Profile")
    st.info("This is a placeholder for the user profile page.")
    st.button("Logout", on_click=lambda: (go_to_page('login'), st.session_state.clear()))

def campaign_detail_page(campaign_id: str):
    """
    Renders the detailed view of a specific campaign.
    This function now includes the fix for the NameError.
    """
    campaign_data = fetch_data(f"/api/campaigns/{campaign_id}")
    if not campaign_data:
        st.error("Campaign not found.")
        return

    # Use a container for the main content
    st.title(campaign_data['title'])
    
    # Correction for NameError: The variable 'title' is now correctly defined
    title = campaign_data['title']

    st.image(campaign_data['image_url'], use_column_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Details")
        st.markdown(f"**Organization:** {campaign_data['organization']}")
        st.markdown(f"**Category:** {campaign_data['category']}")
        st.markdown(f"**Location:** {campaign_data['location']}")
        st.markdown(f"**NGO DARPAN ID:** {campaign_data['ngo_darpan_id']}")
        st.markdown(f"**Verified:** {'✅ Yes' if campaign_data['is_verified'] else '❌ No'}")

    with col2:
        st.subheader("Funding Progress")
        st.metric(
            label=f"₹{campaign_data['current_amount']:,} Raised",
            value=f"of ₹{campaign_data['target_amount']:,} Goal",
            delta=f"{campaign_data['progress']}% progress"
        )
        st.progress(campaign_data['progress'] / 100)
        st.markdown(f"**{campaign_data['donors_count']}** Donors")
        st.markdown(f"**{campaign_data['days_left']}** Days Left")
        
        # Donation form
        with st.expander("Make a Donation", expanded=False):
            with st.form(key="donation_form"):
                st.subheader("Donate to this campaign")
                amount = st.number_input("Amount (₹)", min_value=1.0, value=100.0, step=1.0)
                donor_name = st.text_input("Your Name")
                donor_email = st.text_input("Your Email")
                donor_phone = st.text_input("Your Phone Number")
                anonymous = st.checkbox("Donate Anonymously")
                
                donate_button = st.form_submit_button("Donate Now")
                
                if donate_button:
                    donation_data = {
                        "campaign_id": campaign_id,
                        "amount": amount,
                        "donor_name": donor_name,
                        "donor_email": donor_email,
                        "donor_phone": donor_phone,
                        "anonymous": anonymous
                    }
                    try:
                        response = requests.post(f"{BACKEND_URL}/api/donate", data=donation_data)
                        response.raise_for_status()
                        payment_result = response.json()
                        if payment_result["success"]:
                            st.success("Redirecting to payment gateway...")
                            st.markdown(f'<meta http-equiv="refresh" content="0; url={payment_result["payment_url"]}">', unsafe_allow_html=True)
                        else:
                            st.error(f"Payment failed: {payment_result.get('error', 'Unknown error')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error processing donation: {e}")

    # Description with simplification feature
    st.subheader("About the Campaign")
    
    # Text simplification API call
    if st.button("Simplify complex terms"):
        with st.spinner("Simplifying text..."):
            try:
                payload = {"text": campaign_data['description'], "language": "en"}
                response = requests.post(f"{BACKEND_URL}/api/process_text_for_simplification", json=payload)
                response.raise_for_status()
                simplification_data = response.json()
                
                # Store the processed text and simplifications in session state
                st.session_state[f'simplified_text_{campaign_id}'] = simplification_data['processed_text']
                st.session_state[f'simplifications_{campaign_id}'] = simplification_data['simplifications']

                # Trigger a rerun to display the simplified text
                st.experimental_rerun()

            except requests.exceptions.RequestException as e:
                st.error(f"Error simplifying text: {e}")

    # Display the description, either original or simplified
    description_text = campaign_data['description']
    simplifications = {}
    
    if f'simplified_text_{campaign_id}' in st.session_state:
        description_text = st.session_state[f'simplified_text_{campaign_id}']
        simplifications = st.session_state[f'simplifications_{campaign_id}']
    
    # Process the text to display with tooltips
    processed_html = description_text
    for term, definition in simplifications.items():
        processed_html = processed_html.replace(
            f"{{i}}{term}{{/i}}",
            f'<span class="tooltip">{term}<span class="tooltiptext">{definition}</span></span>'
        )

    st.markdown(f'<p>{processed_html}</p>', unsafe_allow_html=True)
    
# Main application
def main():
    """Main function to handle page routing and application logic."""
    # Load custom CSS
    load_custom_css(page="")  # Pass an empty string as a default value
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"
    
    # Get page from URL parameters
    query_params = st.experimental_get_query_params()
    page = query_params.get('page', ['login'])[0]
    
    # Route to appropriate page
    if not st.session_state.authenticated and page not in ['login', 'register']:
        page = 'login'
    
    if page == 'login':
        login_page()
    elif page == 'register':
        register_page()
    elif page == 'trending':
        trending_page()
        bottom_navigation()
    elif page == 'search':
        search_page()
        bottom_navigation()
    elif page == 'explore':
        explore_page()
        bottom_navigation()
    elif page == 'profile':
        profile_page()
        bottom_navigation()
    elif page.startswith('campaign_'):
        campaign_id = page.split('_')[1]
        campaign_detail_page(campaign_id)
        bottom_navigation()
    else:
        if st.session_state.authenticated:
            trending_page()
            bottom_navigation()
        else:
            login_page()
    
if __name__ == "__main__":
    main()
