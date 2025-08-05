# -*- coding: utf-8 -*-
"""
HAVEN Crowdfunding Streamlit App - Final Improved Version

This script is a complete and enhanced version of the frontend, incorporating
a modern layout, advanced CSS styling, and key components from `streamlit-extras`
and `streamlit-card` to create a more professional user interface.
"""

import streamlit as st
import requests
import base64
from datetime import datetime
import json
import os
from urllib.parse import urlencode
import time
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stoggle import stoggle
from streamlit_card import card # Importing the new streamlit-card library
from streamlit_extras.grid import grid # New import for grid layout
from streamlit_extras.badges import badge # New import for badges
from streamlit_avatar import avatar # New import for avatars
from streamlit_extras.image_selector import image_selector # New import for image selector

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

# --- Translation Dictionary and Term Simplification Logic ---
TRANSLATION_DICT = {
    'en': {
        'login': 'Login', 'register': 'Register', 'register_title': 'Register to HAVEN',
        'individual': 'Individual', 'organization': 'Organization', 'full_name': 'Full Name',
        'email_id': 'Email Address', 'phone_number': 'Phone Number', 'otp': 'OTP',
        'password': 'Password', 'confirm_password': 'Confirm Password', 'address': 'Address',
        'identity_verification': 'Identity Verification', 'document_type': 'Document Type',
        'upload_document': 'Upload Document', 'register_button': 'Register',
        'passwords_not_match': 'Passwords do not match!', 'org_name': 'Organization Name',
        'org_phone': 'Organization Phone', 'org_type': 'Organization Type',
        'org_description': 'Organization Description', 'contact_person': 'Contact Person',
        'contact_email': 'Contact Email', 'org_verification': 'Organization Verification',
        'cert_type': 'Certificate Type', 'upload_cert': 'Upload Certificate',
        'not_registered': "Already have an account?"
    },
    'hi': {
        'login': 'लॉग इन', 'register': 'रजिस्टर', 'register_title': 'हैवन से रजिस्टर करें',
        'individual': 'व्यक्तिगत', 'organization': 'संगठन', 'full_name': 'पूरा नाम',
        'email_id': 'ईमेल पता', 'phone_number': 'फ़ोन नंबर', 'otp': 'ओटीपी',
        'password': 'पासवर्ड', 'confirm_password': 'पासवर्ड की पुष्टि करें', 'address': 'पता',
        'identity_verification': 'पहचान सत्यापन', 'document_type': 'दस्तावेज़ का प्रकार',
        'upload_document': 'दस्तावेज़ अपलोड करें', 'register_button': 'रजिस्टर करें',
        'passwords_not_match': 'पासवर्ड मेल नहीं खाते हैं!', 'org_name': 'संगठन का नाम',
        'org_phone': 'संगठन का फ़ोन', 'org_type': 'संगठन का प्रकार',
        'org_description': 'संगठन का विवरण', 'contact_person': 'संपर्क व्यक्ति',
        'contact_email': 'संपर्क ईमेल', 'org_verification': 'संगठन सत्यापन',
        'cert_type': 'प्रमाणपत्र का प्रकार', 'upload_cert': 'प्रमाणपत्र अपलोड करें',
        'not_registered': "पहले से ही एक खाता है?"
    },
    'ta': {
        'login': 'உள்நுழைவு', 'register': 'பதிவு', 'register_title': 'ஹேவனில் பதிவு',
        'individual': 'தனிநபர்', 'organization': 'அமைப்பு', 'full_name': 'முழு பெயர்',
        'email_id': 'மின்னஞ்சல் முகவரி', 'phone_number': 'தொலைபேசி எண்', 'otp': 'OTP',
        'password': 'கடவுச்சொல்', 'confirm_password': 'கடவுச்சொல்லை உறுதிப்படுத்து', 'address': 'முகவரி',
        'identity_verification': 'அடையாள சரிபார்ப்பு', 'document_type': 'ஆவண வகை',
        'upload_document': 'ஆவணத்தைப் பதிவேற்று', 'register_button': 'பதிவு செய்',
        'passwords_not_match': 'கடவுச்சொற்கள் பொருந்தவில்லை!', 'org_name': 'அமைப்பின் பெயர்',
        'org_phone': 'அமைப்பின் தொலைபேசி', 'org_type': 'அமைப்பின் வகை',
        'org_description': 'அமைப்பின் விளக்கம்', 'contact_person': 'தொடர்பு நபர்',
        'contact_email': 'தொடர்பு மின்னஞ்சல்', 'org_verification': 'அமைப்பின் சரிபார்ப்பு',
        'cert_type': 'சான்றிதழ் வகை', 'upload_cert': 'சான்றிதழைப் பதிவேற்று',
        'not_registered': 'ஏற்கனவே கணக்கு உள்ளதா?'
    },
    'te': {
        'login': 'లాగిన్', 'register': 'నమోదు', 'register_title': 'HAVENలో నమోదు చేయండి',
        'individual': 'వ్యక్తిగత', 'organization': 'సంస్థ', 'full_name': 'పూర్తి పేరు',
        'email_id': 'ఇమెయిల్ చిరునామా', 'phone_number': 'ఫోన్ నంబర్', 'otp': 'ఓటిపి',
        'password': 'పాస్వర్డ్', 'confirm_password': 'పాస్వర్డ్‌ను నిర్ధారించండి', 'address': 'చిరునామా',
        'identity_verification': 'గుర్తింపు ధృవీకరణ', 'document_type': 'పత్రం రకం',
        'upload_document': 'పత్రాన్ని అప్‌లోడ్ చేయండి', 'register_button': 'నమోదు చేయండి',
        'passwords_not_match': 'పాస్‌వర్డ్‌లు సరిపోలడం లేదు!', 'org_name': 'సంస్థ పేరు',
        'org_phone': 'సంస్థ ఫోన్', 'org_type': 'సంస్థ రకం',
        'org_description': 'సంస్థ వివరణ', 'contact_person': 'సంప్రదింపు వ్యక్తి',
        'contact_email': 'సంప్రదింపు ఇమెయిల్', 'org_verification': 'సంస్థ ధృవీకరణ',
        'cert_type': 'సర్టిఫికేట్ రకం', 'upload_cert': 'సర్టిఫికేట్‌ను అప్‌లోడ్ చేయండి',
        'not_registered': 'ఇప్పటికే ఖాతా ఉందా?'
    }
}

SIMPLIFICATION_DICT = {
    'philanthropy': 'donating money to help people',
    'sustainability': 'using resources wisely to protect the environment for the future',
}

def get_translated_text(key, lang='en'):
    return TRANSLATION_DICT.get(lang, {}).get(key, key)

def simplify_text(text, lang='en'):
    # Placeholder for advanced simplification logic
    for term, simple_term in SIMPLIFICATION_DICT.items():
        text = text.replace(term, simple_term)
    return text

# --- Custom CSS for improved design ---
def load_custom_css():
    st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Login page styling - Light blue background */
    .login-container {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        min-height: 100vh;
        padding: 2rem;
    }
    .centered-card {
        max-width: 450px;
        margin: 5rem auto;
        padding: 2rem;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Register page styling */
    .register-card {
        max-width: 800px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Style for all buttons */
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .st-emotion-cache-12oz5g7 {
        max-width: 100%;
        padding-top: 0px;
        padding-right: 1rem;
        padding-bottom: 0px;
        padding-left: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Helper functions for API calls ---
def get_all_campaigns():
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaigns")
        response.raise_for_status()
        return response.json().get('campaigns', [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching campaigns: {e}")
        return []

def get_trending_campaigns():
    try:
        response = requests.get(f"{BACKEND_URL}/api/trending")
        response.raise_for_status()
        return response.json().get('trending_campaigns', [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching trending campaigns: {e}")
        return []

def get_campaign_by_id(campaign_id):
    try:
        response = requests.get(f"{BACKEND_URL}/api/campaigns/{campaign_id}")
        response.raise_for_status()
        return response.json().get('campaign')
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching campaign details: {e}")
        return None

def submit_campaign_for_moderation(campaign_data):
    """
    Submits a new campaign to the backend for fraud moderation.
    """
    new_endpoint = f"{BACKEND_URL}/api/campaigns/submit"
    payload = {
        "title": campaign_data["title"],
        "description": campaign_data["description"],
        "organization": campaign_data["organization"],
        "category": campaign_data["category"],
        "ngo_darpan_id": campaign_data.get("ngo_darpan_id"),
        "pan_number": campaign_data.get("pan_number"),
        "has_certificate": campaign_data.get("has_certificate", False),
        "donors_count": campaign_data.get("donors_count", 0),
        "created_at": campaign_data.get("created_at", datetime.now().isoformat())
    }
    try:
        response = requests.post(new_endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to submit campaign: {e}"}

# --- Logo Rendering Function ---
def render_logo():
    logo_path = "haven_logo.png"  # Assumes the logo file is in the same directory
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 2rem;">
                <img src="data:image/png;base64,{logo_data}" alt="HAVEN Logo" style="max-width: 200px;">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(f"<h1 style='text-align: center;'>HAVEN</h1>", unsafe_allow_html=True)

# --- Navigation and Page Functions ---
def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.experimental_set_query_params(page=page_name)

def sidebar_navigation():
    with st.sidebar:
        st.title("HAVEN")
        st.subheader("Crowdfunding Platform")
        
        # Use a single radio button for navigation
        page = st.radio(
            "Navigation",
            ("Trending", "Explore", "Search", "Profile")
        )

        if page == "Trending":
            navigate_to("trending")
        elif page == "Explore":
            navigate_to("explore")
        elif page == "Search":
            navigate_to("search")
        elif page == "Profile":
            navigate_to("profile")

def login_page():
    # Use st.container for a cleaner, centered look
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='centered-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Login to HAVEN</h3>", unsafe_allow_html=True)

        with st.form(key='login_form'):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            login_button = st.form_submit_button("Login")

            if login_button:
                # Placeholder for actual login logic
                if email == "test@example.com" and password == "password":
                    st.session_state.authenticated = True
                    st.success("Login successful!")
                    time.sleep(1)
                    navigate_to("trending")
                else:
                    st.error("Invalid email or password.")
        
        st.markdown("<p style='text-align: center;'>Don't have an account? <a href='?page=register'>Register here</a></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def register_page():
    """Renders the registration page with forms for individuals and organizations."""
    # Ensure a default language is set if not already in session state
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    lang = st.session_state.get('language', 'en')

    # Add a language selector at the top
    st.markdown('<div class="register-card" style="text-align: right; background-color: transparent; box-shadow: none;">', unsafe_allow_html=True)
    st.session_state.language = st.selectbox(
        "Select Language",
        ('English', 'हिन्दी', 'தமிழ்', 'తెలుగు'),
        index=0 if lang=='en' else 1 if lang=='hi' else 2 if lang=='ta' else 3,
        format_func=lambda x: {'English': 'English', 'हिन्दी': 'Hindi', 'தமிழ்': 'Tamil', 'తెలుగు': 'Telugu'}[x],
        key="language_selector"
    )
    # Convert language selection back to code
    lang = 'en' if st.session_state.language == 'English' else 'hi' if st.session_state.language == 'हिन्दी' else 'ta' if st.session_state.language == 'தமிழ்' else 'te'
    st.session_state.language = lang
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        render_logo()
        st.markdown('<div class="register-card">', unsafe_allow_html=True)

        st.markdown(f"## {get_translated_text('register_title', lang)}")

        account_type = st.selectbox("Select Account Type", [get_translated_text('individual', lang), get_translated_text('organization', lang)])

        if account_type == get_translated_text('individual', lang):
            st.markdown(f"### {get_translated_text('register_title', lang)} {get_translated_text('individual', lang)}")
            with st.form("individual_register"):
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    full_name = st.text_input(get_translated_text('full_name', lang), placeholder="R PRAKASH")
                    email = st.text_input(get_translated_text('email_id', lang), placeholder="prakashr00@rediffmail.com")
                    phone = st.text_input(get_translated_text('phone_number', lang), placeholder="09936528585")
                    otp = st.text_input(get_translated_text('otp', lang), placeholder=get_translated_text('otp', lang))

                with col_i2:
                    password = st.text_input(get_translated_text('password', lang), type="password")
                    confirm_password = st.text_input(get_translated_text('confirm_password', lang), type="password")
                    address = st.text_area(get_translated_text('address', lang), placeholder=get_translated_text('address', lang))

                    st.markdown(f"**{get_translated_text('identity_verification', lang)}**")
                    document_type = st.selectbox(get_translated_text('document_type', lang), ["Aadhar Card", "PAN Card", "Passport", "Driving License", "Voter ID"])
                    document_file = st.file_uploader(get_translated_text('upload_document', lang), type=['pdf', 'jpg', 'png'])

                register_btn = st.form_submit_button(get_translated_text('register_button', lang), use_container_width=True)

                if register_btn:
                    if password == confirm_password:
                        st.success(f"{get_translated_text('individual', lang)} {get_translated_text('register_button', lang).lower()} successful! You can now log in.")
                        st.session_state.current_page = "login"
                        st.rerun()
                    else:
                        st.error(get_translated_text('passwords_not_match', lang))

        else: # Organization
            st.markdown(f"### {get_translated_text('register_title', lang)} {get_translated_text('organization', lang)}")
            with st.form("organization_register"):
                col_o1, col_o2 = st.columns(2)
                with col_o1:
                    org_name = st.text_input(get_translated_text('org_name', lang), placeholder=get_translated_text('org_name', lang))
                    org_phone = st.text_input(get_translated_text('org_phone', lang), placeholder=get_translated_text('org_phone', lang))
                    org_type = st.selectbox(get_translated_text('org_type', lang), ["NGO", "Non-Profit", "Social Enterprise", "Charity", "Foundation"])
                    org_description = st.text_area(get_translated_text('org_description', lang), placeholder=get_translated_text('org_description', lang), max_chars=100)

                with col_o2:
                    contact_person = st.text_input(get_translated_text('contact_person', lang))
                    contact_email = st.text_input(get_translated_text('contact_email', lang))
                    password = st.text_input(get_translated_text('password', lang), type="password")
                    confirm_password = st.text_input(get_translated_text('confirm_password', lang), type="password")

                    st.markdown(f"**{get_translated_text('org_verification', lang)}**")
                    cert_type = st.selectbox(get_translated_text('cert_type', lang), ["Certificate of Incorporation", "GST Certificate", "12A Certificate", "80G Certificate", "FCRA Certificate"])
                    cert_file = st.file_uploader(get_translated_text('upload_cert', lang), type=['pdf', 'jpg', 'png'])

                register_btn = st.form_submit_button(get_translated_text('register_button', lang), use_container_width=True)

                if register_btn:
                    if password == confirm_password:
                        st.success(f"{get_translated_text('organization', lang)} {get_translated_text('register_button', lang).lower()} successful! You can now log in.")
                        st.session_state.current_page = "login"
                        st.rerun()
                    else:
                        st.error(get_translated_text('passwords_not_match', lang))

        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            {get_translated_text('not_registered', lang)} <a href="?page=login" style="color: #4caf50; text-decoration: none;">{get_translated_text('login', lang)}</a>
        </div>
        """, unsafe_allow_html=True)


def trending_page():
    st.header("Trending Campaigns")
    trending_campaigns = get_trending_campaigns()
    if trending_campaigns:
        # Use grid layout for a cleaner display
        grid_cols = grid([1, 1, 1], gap="medium")
        for i, campaign in enumerate(trending_campaigns):
            with grid_cols.container():
                # Add a badge for trending campaigns
                badge(type="success", label="Trending")
                # Use streamlit-card to display the campaign
                card(
                    title=campaign['title'],
                    text=f"Raised: ${campaign['current_amount']:,} of ${campaign['target_amount']:,}\nCategory: {campaign['category']}",
                    image="https://placehold.co/600x400/2980b9/ffffff?text=Campaign",
                    url=f"?page=campaign_{campaign['id']}",
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "auto",
                            "border-radius": "10px",
                            "box-shadow": "0 4px 12px rgba(0, 0, 0, 0.05)",
                            "transition": "all 0.3s ease-in-out",
                        },
                        "title": {
                            "font-size": "22px",
                            "font-weight": "bold",
                        },
                        "text": {
                            "font-size": "16px",
                        },
                    }
                )
    else:
        st.info("No trending campaigns found.")

def explore_page():
    st.header("Explore All Campaigns")
    all_campaigns = get_all_campaigns()
    if all_campaigns:
        # Use grid layout for a cleaner display
        grid_cols = grid([1, 1, 1], gap="medium")
        for i, campaign in enumerate(all_campaigns):
            with grid_cols.container():
                # Use streamlit-card to display the campaign
                card(
                    title=campaign['title'],
                    text=f"Raised: ${campaign['current_amount']:,} of ${campaign['target_amount']:,}\nCategory: {campaign['category']}",
                    image="https://placehold.co/600x400/2980b9/ffffff?text=Campaign",
                    url=f"?page=campaign_{campaign['id']}",
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "auto",
                            "border-radius": "10px",
                            "box-shadow": "0 4px 12px rgba(0, 0, 0, 0.05)",
                            "transition": "all 0.3s ease-in-out",
                        },
                        "title": {
                            "font-size": "22px",
                            "font-weight": "bold",
                        },
                        "text": {
                            "font-size": "16px",
                        },
                    }
                )
    else:
        st.info("No campaigns to display.")

def search_page():
    st.header("Search Campaigns")
    query = st.text_input("Enter a keyword to search for campaigns...")
    if st.button("Search"):
        with st.spinner("Searching for campaigns..."):
            time.sleep(2) # Simulate search time
            # Placeholder for search logic
            st.info(f"Search results for '{query}' will be displayed here.")

def profile_page():
    st.header("My Profile")
    st.info("This is a placeholder for the user profile page.")
    
    # Display user avatar
    avatar(name="John Doe", src="https://placehold.co/50x50/3498db/ffffff?text=JD")
    st.markdown("### Welcome, John Doe!")

    st.subheader("Create a New Campaign")
    
    with st.form(key='new_campaign_form'):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Campaign Title")
            organization = st.text_input("Organization Name")
            category = st.selectbox("Category", ["Education", "Health", "Community", "Technology"])
            ngo_darpan_id = st.text_input("NGO Darpan ID (optional)")
            pan_number = st.text_input("PAN Number (optional)")
        
        with col2:
            description = st.text_area("Campaign Description", height=200)
            
            # Use image_selector for a nicer campaign image upload experience
            st.markdown("Select a campaign image:")
            selected_image = image_selector(
                images=[
                    "https://placehold.co/600x400/2980b9/ffffff?text=Education",
                    "https://placehold.co/600x400/27ae60/ffffff?text=Health",
                    "https://placehold.co/600x400/e67e22/ffffff?text=Community",
                    "https://placehold.co/600x400/9b59b6/ffffff?text=Technology",
                ],
                key="campaign_image_selector"
            )

            # Corrected usage of stoggle
            has_certificate = stoggle(
                "Do you have a registration certificate?", 
                "Yes, I have a certificate."
            )
        
        submit_button = st.form_submit_button(label="Submit for Review", use_container_width=True)
        
        if submit_button:
            campaign_data = {
                "title": title,
                "description": description,
                "organization": organization,
                "category": category,
                "ngo_darpan_id": ngo_darpan_id,
                "pan_number": pan_number,
                "has_certificate": has_certificate,
                "image_url": selected_image # Assuming backend can handle this
            }
            with st.spinner("Submitting campaign for fraud moderation..."):
                result = submit_campaign_for_moderation(campaign_data)
                if 'error' in result:
                    st.chat_message("assistant").error(f"Error: {result['error']}")
                else:
                    with st.chat_message("assistant"):
                        st.success("Campaign submitted!")
                        st.info(f"Status: {result['status']}")
                        st.write(f"Fraud Score: {result['fraud_score']:.2f}")
                        st.write(f"Explanation: {result['explanation']}")

def campaign_detail_page(campaign_id):
    st.header(f"Campaign Details for ID: {campaign_id}")
    campaign = get_campaign_by_id(campaign_id)
    if campaign:
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                # Display organization avatar
                avatar(name=campaign['organization'], src="https://placehold.co/50x50/3498db/ffffff?text=Org")
            with col2:
                st.title(campaign['title'])
                st.markdown(f"**Organization:** {campaign['organization']}")
            
            st.markdown(f"**Category:** {campaign['category']}")
            
            # Calculate progress percentage
            progress_percent = (campaign['current_amount'] / campaign['target_amount']) * 100 if campaign['target_amount'] > 0 else 0
            
            col1, col2 = st.columns(2)
            with col1:
                metric_card(
                    title="Amount Raised",
                    value=f"${campaign['current_amount']:,}",
                    delta=f"Target: ${campaign['target_amount']:,}",
                    # You can add a specific icon here if you like
                )
            with col2:
                metric_card(
                    title="Donors",
                    value=f"{campaign.get('donors_count', 0):,}",
                    # You can add an icon for donors here
                )
            
            # Display a larger progress bar
            st.markdown("### Progress")
            st.progress(progress_percent / 100, text=f"{progress_percent:.2f}% of goal reached")

            with st.expander("Read full description"):
                st.write(campaign['description'])

            if st.button("Donate"):
                st.success("Thank you for your donation! (This is a placeholder)")
    else:
        st.error("Campaign not found.")


def main():
    """
    Main application loop.
    """
    # Load custom CSS
    load_custom_css()
    
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
    
    # Render the sidebar for all pages except login/register
    if page not in ['login', 'register']:
        sidebar_navigation()

    if page == 'login':
        login_page()
    elif page == 'register':
        register_page()
    elif page == 'trending':
        trending_page()
    elif page == 'search':
        search_page()
    elif page == 'explore':
        explore_page()
    elif page == 'profile':
        profile_page()
    elif page.startswith('campaign_'):
        campaign_id = page.split('_')[1]
        campaign_detail_page(campaign_id)
    else:
        # Default to trending if authenticated, login if not
        if st.session_state.authenticated:
            trending_page()
        else:
            login_page()

if __name__ == "__main__":
    main()
