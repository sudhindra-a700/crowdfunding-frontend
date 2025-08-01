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
        'welcome_banner_title': 'Welcome to HAVEN',
        'welcome_banner_tagline': 'Your hub for impactful campaigns and community giving',
        'trending_campaigns': 'Trending Campaigns',
        'ongoing_campaigns': 'Ongoing Campaigns',
        'completed_campaigns': 'Completed Campaigns',
        'ngo': 'NGO',
        'startup': 'Startup',
        'charity': 'Charity',
        'description': 'Description',
        'register_individual': 'Individual Registration',
        'contact_person_details': 'Contact Person Details',
        'organization_details': 'Organization Details',
        'create_campaign': 'Create Campaign',
        'campaign_name': 'Campaign Name',
        'goal_amount': 'Goal Amount ($)',
        'campaign_image': 'Campaign Image',
        'category': 'Category',
        'start_date': 'Start Date',
        'end_date': 'End Date',
        'submit_campaign': 'Submit Campaign',
        'login_page_title': 'Welcome Back!',
        'login_page_subtitle': 'Sign in to continue your journey',
        'oauth_divider': 'or sign in with social account',
        'oauth_divider_register': 'or sign up with social account',
        'complete_profile_title': 'Complete Your Profile',
        'submit': 'Submit'
    }
    # Add other languages here if needed
}

# --- Utility Functions ---

def get_text(key):
    # This function should be defined to retrieve text from the TRANSLATIONS dict.
    # We'll assume a language is selected, e.g., 'English'.
    return TRANSLATIONS.get('English', {}).get(key, key)

def render_sidebar():
    # This function is used to render the sidebar.
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">HAVEN</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)

        nav_pages = [('home', get_text('home')),
                     ('explore', get_text('explore')),
                     ('search', get_text('search'))]

        for page_name, page_title in nav_pages:
            st.markdown(f'<a href="{FRONTEND_BASE_URL}?page={page_name}" class="sidebar-nav-item">{page_title}</a>',
                        unsafe_allow_html=True)

        if st.session_state.get('user_authenticated'):
            st.markdown(f'<a href="{FRONTEND_BASE_URL}?page=profile" class="sidebar-nav-item">{get_text("profile")}</a>',
                        unsafe_allow_html=True)
            st.markdown(f'<a href="{FRONTEND_BASE_URL}?page=logout" class="sidebar-nav-item">{get_text("logout")}</a>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<a href="{FRONTEND_BASE_URL}?page=login" class="sidebar-nav-item">{get_text("login")}</a>',
                        unsafe_allow_html=True)
            st.markdown(f'<a href="{FRONTEND_BASE_URL}?page=register" class="sidebar-nav-item">{get_text("register")}</a>',
                        unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

def render_oauth_buttons(is_register_page=False):
    # Renders the Google and Facebook OAuth buttons.
    st.markdown('<div class="social-login-container">', unsafe_allow_html=True)
    if is_register_page:
        st.markdown(f'<a href="{BACKEND_URL}/auth/google/register" class="social-button google">{get_text("sign_in_google")}</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{BACKEND_URL}/auth/facebook/register" class="social-button facebook">{get_text("sign_in_facebook")}</a>', unsafe_allow_html=True)
    else:
        st.markdown(f'<a href="{BACKEND_URL}/auth/google/login" class="social-button google">{get_text("sign_in_google")}</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{BACKEND_URL}/auth/facebook/login" class="social-button facebook">{get_text("sign_in_facebook")}</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Page Rendering Functions ---

def render_login_page():
    # Renders the login page
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)
    st.markdown(f'<div class="html-title-login">{get_text("login_page_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="html-subtitle-login">{get_text("login_page_subtitle")}</div>', unsafe_allow_html=True)

    with st.form(key='login_form', clear_on_submit=False):
        email = st.text_input("", placeholder=get_text('email'), key="login_email")
        password = st.text_input("", type="password", placeholder=get_text('password'), key="login_password")
        submit_button = st.form_submit_button(label=get_text('login'))
        if submit_button:
            # Placeholder for login logic
            pass
    st.markdown(f"""
<div class="html-option">
{get_text('not_registered')}
<a href="{FRONTEND_BASE_URL}?page=register" target="_self">{get_text('create_account')}</a>
</div>
""", unsafe_allow_html=True)
    st.markdown(f"""
<div class="oauth-divider">
<span>{get_text('oauth_divider')}</span>
</div>
""", unsafe_allow_html=True)
    render_oauth_buttons()
    st.markdown('</div>', unsafe_allow_html=True)

def render_register_page():
    # Renders the register page
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)

    st.markdown(f'<div class="html-title-register">{get_text("register")}</div>', unsafe_allow_html=True)

    registration_type_options = [get_text('individual'), get_text('organization')]

    if 'selected_reg_type_register' not in st.session_state:
        st.session_state.selected_reg_type_register = registration_type_options[0]

    selected_type = st.selectbox(
        "Select Registration Type",
        options=registration_type_options,
        index=registration_type_options.index(st.session_state.selected_reg_type_register),
        key="reg_type_selector_outside_form_register"
    )
    if selected_type != st.session_state.selected_reg_type_register:
        st.session_state.selected_reg_type_register = selected_type
        st.rerun()

    with st.form(key='register_form'):
        email, password, confirm_password = "", "", ""
        full_name, phone, address = "", "", ""
        contact_full_name, contact_phone = "", ""
        org_name, org_type, org_description = "", "", ""
        ngo_darpan_id, pan, fcra_number = "", "", ""

        user_data_for_backend = {}  # Initialize the variable here to prevent NameError

        is_valid_input = False

        if st.session_state.selected_reg_type_register == get_text('individual'):
            st.markdown(f"""<div class="html-form-box"><h3>{get_text("register_individual")}</h3>""",
                        unsafe_allow_html=True)

            full_name = st.text_input("", placeholder="Full Name", key="reg_full_name_ind")
            email = st.text_input("", placeholder="Email ID", key="reg_email_ind")
            phone = st.text_input("", placeholder="Phone Number", key="reg_phone_ind")
            password = st.text_input("", type="password", placeholder="Password", key="reg_password_ind")
            confirm_password = st.text_input("", type="password", placeholder="Confirm Password",
                                             key="reg_confirm_password_ind")
            address = st.text_area("", placeholder="Address", key="reg_address_individual_ind")

            st.markdown('</div>', unsafe_allow_html=True)

            individual_data = {
                "full_name": full_name,
                "phone": phone,
                "address": address
            }
            user_data_for_backend = {"user_type": "individual", "individual_data": individual_data}
            is_valid_input = bool(full_name and email and phone and password and confirm_password and address)

        elif st.session_state.selected_reg_type_register == get_text('organization'):
            st.markdown(f"""<div class="html-form-box"><h3>{get_text("contact_person_details")}</h3>""",
                        unsafe_allow_html=True)

            contact_full_name = st.text_input("", placeholder="Contact Person Full Name",
                                              key="reg_contact_full_name_org")
            email = st.text_input("", placeholder="Contact Person Email ID (for login)",
                                  key="reg_email_org_contact_org")
            contact_phone = st.text_input("", placeholder="Contact Person Phone Number",
                                          key="reg_contact_phone_org")
            password = st.text_input("", type="password", placeholder="Password",
                                     key="reg_password_org_contact_org")
            confirm_password = st.text_input("", type="password", placeholder="Confirm Password",
                                             key="reg_confirm_password_org_contact_org")

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(f"""<div class="html-form-box"><h3>{get_text("organization_details")}</h3>""",
                        unsafe_allow_html=True)

            org_name = st.text_input("", placeholder="Organization Name", key="reg_org_name_org")
            org_type = st.selectbox("",
                                    options=["", get_text('ngo'), get_text('startup'), get_text('charity')],
                                    key="reg_org_type_select_org")
            org_description = st.text_input("", placeholder=get_text('description'), key="reg_org_description_org")
            address = st.text_area("", placeholder="Organization Address", key="reg_address_organization_org")
            ngo_darpan_id = st.text_input("", placeholder="NGO Darpan ID (Optional)", key="reg_ngo_darpan_id_org")
            pan = st.text_input("", placeholder="PAN (Optional)", key="reg_pan_org")
            fcra_number = st.text_input("", placeholder="FCRA Number (Optional)", key="reg_fcra_number_org")

            st.markdown('</div>', unsafe_allow_html=True)

            organization_data = {
                "contact_full_name": contact_full_name,
                "contact_phone": contact_phone,
                "organization_name": org_name,
                "organization_type": org_type,
                "description": org_description,
                "address": address,
                "ngo_darpan_id": ngo_darpan_id,
                "pan": pan,
                "fcra_number": fcra_number
            }
            user_data_for_backend = {"user_type": "organization", "organization_data": organization_data}
            is_valid_input = bool(contact_full_name and email and contact_phone and password and confirm_password and
                                  org_name and org_type and org_description and address)

        submit_button = st.form_submit_button(get_text('register'))

        if submit_button:
            if not is_valid_input:
                st.error("Please fill in all required fields for the selected registration type.")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                # Call JavaScript function to create user with Firebase
                st.components.v1.html(f"""
<script>
window.createUserWithEmailPassword("{email}", "{password}");
</script>
""", height=0, width=0)
                # Store additional data in session state temporarily until Firebase ID token is received
                st.session_state.temp_registration_data = user_data_for_backend
                st.session_state.temp_registration_data['email'] = email # Store email for reference

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
    # Renders the page for completing the profile after OAuth login
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)
    st.markdown(f'<div class="html-title-register">{get_text("complete_profile_title")}</div>', unsafe_allow_html=True)

    with st.form(key='complete_profile_form'):
        full_name = st.text_input("", placeholder=get_text('full_name'))
        phone = st.text_input("", placeholder=get_text('phone'))
        address = st.text_area("", placeholder=get_text('address'))
        submit_button = st.form_submit_button(label=get_text('submit'))
        if submit_button:
            # Placeholder for profile completion logic
            st.success("Profile completed!")
            st.session_state.current_page = 'home'
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def render_create_campaign_page():
    # Renders the page for creating a new campaign
    st.markdown('<div class="html-container-wide">', unsafe_allow_html=True)
    st.markdown(f'<div class="html-title-register">{get_text("create_campaign")}</div>', unsafe_allow_html=True)

    with st.form(key='create_campaign_form'):
        campaign_name = st.text_input("", placeholder=get_text('campaign_name'))
        description = st.text_area("", placeholder=get_text('description'))
        goal_amount = st.number_input("", placeholder=get_text('goal_amount'), min_value=1.00)
        image_url = st.text_input("", placeholder=get_text('campaign_image'))
        category = st.selectbox("", options=["", "Education", "Health", "Environment"])
        start_date = st.date_input(get_text('start_date'))
        end_date = st.date_input(get_text('end_date'))
        submit_button = st.form_submit_button(label=get_text('submit_campaign'))

        if submit_button:
            # Placeholder for campaign creation logic
            st.success(f"Campaign '{campaign_name}' created successfully!")
            st.session_state.current_page = 'home'
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def render_home_page():
    # Renders the home page with trending campaigns.
    st.markdown(f'<h1 class="app-title">{get_text("explore")}</h1>', unsafe_allow_html=True)
    st.markdown(f"## {get_text('trending_campaigns')}")

    try:
        response = requests.get(f"{BACKEND_URL}/campaigns", timeout=10)
        if response.status_code == 200:
            campaigns = response.json()
        else:
            st.error(f"Failed to load campaigns: {response.status_code} - {response.text}")
            campaigns = []
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error fetching campaigns: {str(e)}")
        campaigns = []

    if not campaigns:
        st.info("No campaigns found. Create one if you are an organization!")
    else:
        # Corrected code to iterate through columns without calling the list
        columns = st.columns(2)
        for i, campaign in enumerate(campaigns):
            col = columns[i % 2]
            with col:
                progress_percent = (campaign.get('funded', 0) / campaign.get('goal', 1)) * 100 if campaign.get('goal', 1) > 0 else 0
                progress_percent = min(100, max(0, progress_percent))
                st.markdown(f"""
<div class="campaign-card">
<div class="campaign-image">
<img src="{campaign.get('image_url', 'https://placehold.co/600x400/4CAF50/ffffff?text=Campaign+Image')}"
alt="{campaign['campaign_name']}"
style="width:100%; height: 200px; object-fit:cover; border-radius: 12px 12px 0 0;">
</div>
<div class="campaign-content">
<div class="campaign-title">{campaign['campaign_name']}</div>
<div class="campaign-description">{campaign['description']}</div>
<div style="font-size: 0.9em; color: #777; margin-bottom: 0.5rem;">
By: {campaign.get('author', 'N/A')} | Category: {campaign.get('category', 'N/A')}
</div>
<div class="campaign-progress">
<div class="campaign-progress-bar" style="width: {progress_percent}%"></div>
</div>
<div style="display: flex; justify-content: space-between; color: #666; font-weight: 500;">
<span>Raised: ${campaign.get('funded', 0):,}</span>
<span>Goal: ${campaign.get('goal', 0):,}</span>
</div>
<div style="text-align: right; font-size: 0.8em; color: #999; margin-top: 0.5rem;">
Days Left: {round(campaign.get('days_left', 'N/A'))} | Status: {campaign.get('verification_status', 'N/A')}
</div>
</div>
</div>
""", unsafe_allow_html=True)

def render_explore_page():
    # Placeholder for the explore page.
    st.header(get_text('explore'))
    st.write("This is the explore page. You can see all available campaigns here.")

def render_search_page():
    # Placeholder for the search page.
    st.header(get_text('search'))
    st.write("This is the search page. You can search for campaigns here.")

def handle_oauth_callback():
    # This function handles the OAuth callback from the backend.
    query_params = st.query_params
    if 'oauth_token' in query_params:
        token = query_params['oauth_token']
        # You'd typically store this token and redirect the user.
        st.session_state.oauth_token = token
        st.session_state.user_authenticated = True
        st.session_state.current_page = 'home'
        st.experimental_set_query_params(oauth_token=None) # Clear the query param
        st.rerun()

# --- Main App Logic ---

# Initial setup for session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False

# CSS styling for the app
st.markdown("""
    <style>
    .sidebar-logo { font-size: 2em; font-weight: bold; color: #4CAF50; padding: 1em; }
    .sidebar-nav-item { display: block; padding: 1em; text-decoration: none; color: #fff; }
    .sidebar-nav-item:hover { background-color: #575757; }
    .app-title { font-size: 3em; font-weight: bold; color: #4CAF50; text-align: center; margin-bottom: 1em; }
    .html-container-wide { max-width: 600px; margin: auto; padding: 2rem; background-color: #f9f9f9; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .html-form-box { padding: 1rem; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 1rem; }
    .html-title-register, .html-title-login { font-size: 2.5em; text-align: center; color: #333; margin-bottom: 0.5em; }
    .html-subtitle-login { font-size: 1.2em; text-align: center; color: #666; margin-bottom: 2em; }
    .html-option { text-align: center; margin-top: 1em; color: #666; }
    .html-option a { color: #4CAF50; text-decoration: none; font-weight: bold; }
    .oauth-divider { display: flex; align-items: center; text-align: center; margin: 20px 0; }
    .oauth-divider::before, .oauth-divider::after { content: ''; flex: 1; border-bottom: 1px solid #ccc; }
    .oauth-divider:not(:empty)::before { margin-right: .5em; }
    .oauth-divider:not(:empty)::after { margin-left: .5em; }
    .social-login-container { display: flex; justify-content: space-around; }
    .social-button { padding: 10px 20px; border-radius: 5px; color: white; text-decoration: none; }
    .google { background-color: #DB4437; }
    .facebook { background-color: #4267B2; }
    .campaign-card {
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        margin: 1rem 0.5rem;
        transition: transform 0.2s ease-in-out;
        background-color: #ffffff;
    }
    .campaign-card:hover {
        transform: translateY(-5px);
    }
    .campaign-content {
        padding: 1.5rem;
    }
    .campaign-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .campaign-description {
        font-size: 1rem;
        color: #666;
        margin-bottom: 1rem;
        line-height: 1.4;
    }
    .campaign-progress {
        width: 100%;
        background-color: #e0e0e0;
        border-radius: 50px;
        margin: 1rem 0;
        height: 10px;
    }
    .campaign-progress-bar {
        height: 100%;
        background-color: #4CAF50;
        border-radius: 50px;
        transition: width 0.5s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# Main entry point of the app
def main():
    handle_oauth_callback()

    query_params = st.query_params
    if 'page' in query_params:
        requested_page = query_params['page']
        if requested_page in ['login', 'register', 'home', 'explore', 'search', 'complete_oauth_profile',
                              'create_campaign', 'profile', 'logout']:
            st.session_state.current_page = requested_page
            st.query_params.clear()
            st.rerun()

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
        st.error(f"An unexpected error occurred: {e}")
        st.session_state.current_page = 'login'
        st.rerun()

if __name__ == "__main__":
    main()

