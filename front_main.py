"""
HAVEN Crowdfunding Platform - Complete Frontend with Automatic Term Simplification
Features: Left sidebar navigation, language selection, backend testing, and hover tooltips
"""

import streamlit as st
import requests
import json
import base64
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import time

# ========================================
# CONFIGURATION
# ========================================

# Backend configuration
BACKEND_URL = os.getenv("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")

# Feature flags
TRANSLATION_ENABLED = os.getenv("FEATURES_TRANSLATION_ENABLED", "true").lower() == "true"
SIMPLIFICATION_ENABLED = os.getenv("FEATURES_SIMPLIFICATION_ENABLED", "true").lower() == "true"
OAUTH_ENABLED = os.getenv("FEATURES_OAUTH_ENABLED", "true").lower() == "true"

# OAuth configuration
GOOGLE_CLIENT_ID = os.getenv("OAUTH_GOOGLE_CLIENT_ID", "")
FACEBOOK_APP_ID = os.getenv("OAUTH_FACEBOOK_APP_ID", "")

# ========================================
# TERM DEFINITIONS FOR AUTOMATIC TOOLTIPS
# ========================================

# Comprehensive term definitions for automatic simplification
TERM_DEFINITIONS = {
    # Financial Terms
    "crowdfunding": "A way to raise money by asking many people to contribute small amounts online",
    "investment": "Money put into a project or business to make more money later",
    "equity": "Ownership share in a company",
    "revenue": "Total money earned from sales",
    "profit": "Money left after paying all costs",
    "roi": "Return on Investment - how much money you make compared to what you invested",
    "valuation": "How much a company is worth",
    "venture capital": "Money invested in new businesses with high growth potential",
    "angel investor": "Wealthy person who invests in startups",
    "seed funding": "Early money given to start a business",
    "series a": "First major round of investment funding",
    "ipo": "Initial Public Offering - when a company first sells shares to the public",
    "dividend": "Money paid to shareholders from company profits",
    "market cap": "Total value of all company shares",
    "cash flow": "Money coming in and going out of a business",
    
    # Technology Terms
    "api": "Application Programming Interface - a way for different software to communicate",
    "platform": "A system that allows people to build or use services",
    "algorithm": "A set of rules or instructions for solving a problem",
    "blockchain": "A secure digital ledger that records transactions",
    "cryptocurrency": "Digital money secured by cryptography",
    "saas": "Software as a Service - software delivered over the internet",
    "cloud computing": "Using internet-based computing services instead of local servers",
    "ai": "Artificial Intelligence - computer systems that can perform tasks requiring human intelligence",
    "machine learning": "Type of AI where computers learn from data without being explicitly programmed",
    "big data": "Extremely large datasets that require special tools to analyze",
    "iot": "Internet of Things - everyday objects connected to the internet",
    "cybersecurity": "Protection of computer systems and data from digital attacks",
    
    # Business Terms
    "startup": "A new company trying to grow quickly",
    "entrepreneur": "Person who starts and runs a business",
    "scalability": "Ability to grow and handle more customers or work",
    "market research": "Studying customers and competitors to understand demand",
    "business model": "How a company makes money",
    "prototype": "Early version of a product used for testing",
    "milestone": "Important goal or achievement in a project",
    "pivot": "Changing business direction based on what you learn",
    "mvp": "Minimum Viable Product - simplest version that customers will use",
    "b2b": "Business to Business - companies selling to other companies",
    "b2c": "Business to Consumer - companies selling directly to customers",
    "kpi": "Key Performance Indicator - important metric to measure success",
    "burn rate": "How fast a company spends money",
    "runway": "How long money will last at current spending rate",
    "exit strategy": "Plan for how investors will get their money back",
    
    # Legal Terms
    "intellectual property": "Legal rights to ideas, inventions, or creative works",
    "patent": "Legal protection for an invention",
    "trademark": "Legal protection for a brand name or logo",
    "copyright": "Legal protection for creative works like books, music, or art",
    "liability": "Legal responsibility for damages or debts",
    "nda": "Non-Disclosure Agreement - legal contract to keep information secret",
    "terms of service": "Legal agreement between a service provider and user",
    "privacy policy": "Document explaining how personal data is collected and used",
    "compliance": "Following laws and regulations that apply to your business",
    "due diligence": "Careful investigation before making a business decision",
    
    # Marketing Terms
    "target audience": "Specific group of people you want to reach",
    "conversion rate": "Percentage of visitors who take a desired action",
    "brand awareness": "How well people know and recognize your brand",
    "viral marketing": "Marketing that spreads quickly through social sharing",
    "seo": "Search Engine Optimization - making websites easier to find on Google",
    "ctr": "Click-Through Rate - percentage of people who click on an ad or link",
    "cac": "Customer Acquisition Cost - how much it costs to get a new customer",
    "ltv": "Lifetime Value - total money a customer will spend over time",
    "funnel": "Process that guides potential customers toward making a purchase",
    "lead": "Potential customer who has shown interest in your product",
    "crm": "Customer Relationship Management - system for managing customer interactions",
    "a/b testing": "Comparing two versions to see which performs better"
}

# ========================================
# UTILITY FUNCTIONS
# ========================================

def get_logo_base64():
    """Convert logo image to base64 with error handling"""
    try:
        logo_paths = [
            "/home/ubuntu/haven_logo.png",
            "/home/ubuntu/assets/haven_logo.png",
            "./assets/haven_logo.png",
            "./haven_logo.png"
        ]
        
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        
        return None
    except Exception as e:
        return None

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API request with comprehensive error handling"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://haven-streamlit-frontend.onrender.com"
        }
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to backend server"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def get_supported_languages() -> List[Dict[str, str]]:
    """Get supported languages from backend or return default"""
    try:
        result = make_api_request("/api/supported-languages")
        if "error" not in result and "languages" in result:
            return result["languages"]
    except Exception:
        pass
    
    return [
        {"code": "en", "name": "English", "native": "English"},
        {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
        {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
        {"code": "te", "name": "Telugu", "native": "తెలుగు"}
    ]

def add_tooltips_to_text(text: str) -> str:
    """Add automatic tooltips to complex terms in text"""
    if not text:
        return text
    
    # Create a copy of the text to modify
    modified_text = text
    
    # Sort terms by length (longest first) to avoid partial matches
    sorted_terms = sorted(TERM_DEFINITIONS.keys(), key=len, reverse=True)
    
    for term in sorted_terms:
        # Create case-insensitive pattern that matches whole words
        pattern = r'\b' + re.escape(term) + r'\b'
        
        # Find all matches
        matches = list(re.finditer(pattern, modified_text, re.IGNORECASE))
        
        # Replace matches from right to left to preserve positions
        for match in reversed(matches):
            start, end = match.span()
            original_term = modified_text[start:end]
            definition = TERM_DEFINITIONS[term]
            
            # Create tooltip HTML
            tooltip_html = f'''
            <span class="tooltip-term" title="{definition}">
                {original_term}
                <span class="tooltip-icon">ℹ️</span>
                <span class="tooltip-text">{definition}</span>
            </span>
            '''
            
            # Replace the term with tooltip version
            modified_text = modified_text[:start] + tooltip_html + modified_text[end:]
    
    return modified_text

# ========================================
# CSS STYLING WITH TOOLTIPS
# ========================================

def load_css():
    """Load custom CSS for the application including tooltip styles"""
    logo_base64 = get_logo_base64()
    
    css = f"""
    <style>
    /* Hide Streamlit default elements */
    .stDeployButton {{display: none !important;}}
    footer {{visibility: hidden !important;}}
    .stApp > header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    
    /* Main app styling */
    .stApp {{
        background: linear-gradient(135deg, 
            #f0f8ff 0%,     /* Light blue */
            #e6e6fa 50%,    /* Lavender */
            #f0fff0 100%    /* Light green */
        );
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background: linear-gradient(180deg, 
            #2d3748 0%,     /* Dark gray */
            #1a202c 100%   /* Dark blue-gray */
        );
        padding: 1rem;
    }}
    
    /* Sidebar content */
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stMarkdown,
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {{
        color: #ffffff !important;
        font-weight: 500;
    }}
    
    /* Language selector styling */
    .css-1d391kg .stSelectbox > div > div {{
        background-color: #4a5568 !important;
        color: #ffffff !important;
        border: 1px solid #718096 !important;
        border-radius: 8px !important;
    }}
    
    /* Navigation buttons */
    .nav-button {{
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white !important;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
        display: block;
        margin: 0.5rem 0;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
    }}
    
    .nav-button:hover {{
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3);
    }}
    
    /* Main content area */
    .main-content {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    /* Logo styling */
    .logo-container {{
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
    }}
    
    .logo-image {{
        max-width: 250px;
        height: auto;
        margin: 0 auto;
        display: block;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
        animation: pulse 3s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.02); }}
    }}
    
    /* Tagline styling */
    .tagline {{
        text-align: center;
        font-size: 1.2rem;
        color: #2d3748;
        font-style: italic;
        margin-bottom: 2rem;
        font-weight: 500;
    }}
    
    /* TOOLTIP STYLES - AUTOMATIC TERM SIMPLIFICATION */
    .tooltip-term {{
        position: relative;
        display: inline;
        color: #2b6cb0;
        font-weight: 600;
        cursor: help;
        border-bottom: 2px dotted #2b6cb0;
        text-decoration: none;
    }}
    
    .tooltip-icon {{
        display: inline-block;
        margin-left: 2px;
        font-size: 0.8em;
        color: #2b6cb0;
        opacity: 0.7;
    }}
    
    .tooltip-text {{
        visibility: hidden;
        opacity: 0;
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        color: #ffffff;
        text-align: center;
        border-radius: 8px;
        padding: 12px 16px;
        z-index: 1000;
        width: 280px;
        font-size: 0.9rem;
        font-weight: 400;
        line-height: 1.4;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        pointer-events: none;
    }}
    
    .tooltip-text::after {{
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -8px;
        border-width: 8px;
        border-style: solid;
        border-color: #1a202c transparent transparent transparent;
    }}
    
    .tooltip-term:hover .tooltip-text {{
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(-5px);
    }}
    
    .tooltip-term:hover .tooltip-icon {{
        opacity: 1;
        transform: scale(1.2);
    }}
    
    /* Responsive tooltip positioning */
    @media (max-width: 768px) {{
        .tooltip-text {{
            width: 240px;
            font-size: 0.8rem;
            padding: 10px 12px;
        }}
    }}
    
    @media (max-width: 480px) {{
        .tooltip-text {{
            width: 200px;
            font-size: 0.75rem;
            padding: 8px 10px;
        }}
    }}
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {{
        background-color: #ffffff !important;
        color: #1a202c !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {{
        border-color: #48bb78 !important;
        box-shadow: 0 0 0 3px rgba(72, 187, 120, 0.1) !important;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3) !important;
    }}
    
    /* OAuth buttons */
    .oauth-button {{
        background: #ffffff;
        color: #1a202c;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        margin: 0.5rem 0;
        font-weight: 600;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .oauth-button:hover {{
        border-color: #48bb78;
        box-shadow: 0 2px 8px rgba(72, 187, 120, 0.2);
        transform: translateY(-1px);
    }}
    
    .oauth-button.google {{
        border-color: #4285f4;
    }}
    
    .oauth-button.google:hover {{
        border-color: #3367d6;
        box-shadow: 0 2px 8px rgba(66, 133, 244, 0.2);
    }}
    
    .oauth-button.facebook {{
        border-color: #1877f2;
    }}
    
    .oauth-button.facebook:hover {{
        border-color: #166fe5;
        box-shadow: 0 2px 8px rgba(24, 119, 242, 0.2);
    }}
    
    /* Status indicators */
    .status-success {{
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 600;
    }}
    
    .status-error {{
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 600;
    }}
    
    .status-warning {{
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 600;
    }}
    
    /* Content with tooltips */
    .content-with-tooltips {{
        line-height: 1.8;
        font-size: 1.1rem;
        color: #2d3748;
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .logo-image {{
            max-width: 200px;
        }}
        
        .main-content {{
            margin: 0.5rem;
            padding: 1rem;
        }}
        
        .tagline {{
            font-size: 1rem;
        }}
    }}
    
    @media (max-width: 480px) {{
        .logo-image {{
            max-width: 180px;
        }}
        
        .main-content {{
            margin: 0.25rem;
            padding: 0.75rem;
        }}
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

# ========================================
# SIDEBAR NAVIGATION
# ========================================

def render_sidebar():
    """Render the left sidebar with navigation and language selection"""
    with st.sidebar:
        # Language Selection
        st.markdown("### 🌍 Select Language:")
        
        languages = get_supported_languages()
        language_options = {lang["native"]: lang["code"] for lang in languages}
        
        selected_language_name = st.selectbox(
            "Choose your language",
            options=list(language_options.keys()),
            index=0,
            key="language_selector"
        )
        
        selected_language = language_options[selected_language_name]
        st.session_state.selected_language = selected_language
        
        st.markdown("---")
        
        # Navigation Section
        st.markdown("### 🧭 Navigation")
        
        # Backend Test Button
        if st.button("🔧 Test Backend Connection", key="test_backend", help="Test connection to backend API"):
            st.session_state.show_backend_test = True
            st.session_state.show_translation_test = False
            st.session_state.show_simplification_test = False
            st.session_state.show_demo_content = False
        
        # Translation Test Button
        if TRANSLATION_ENABLED:
            if st.button("🌐 Test Translation", key="test_translation", help="Test translation service"):
                st.session_state.show_translation_test = True
                st.session_state.show_backend_test = False
                st.session_state.show_simplification_test = False
                st.session_state.show_demo_content = False
        
        # Simplification Test Button
        if SIMPLIFICATION_ENABLED:
            if st.button("📝 Test Simplification", key="test_simplification", help="Test term simplification"):
                st.session_state.show_simplification_test = True
                st.session_state.show_backend_test = False
                st.session_state.show_translation_test = False
                st.session_state.show_demo_content = False
        
        # Demo Content Button
        if st.button("📚 Demo Content with Tooltips", key="demo_content", help="See automatic term simplification in action"):
            st.session_state.show_demo_content = True
            st.session_state.show_backend_test = False
            st.session_state.show_translation_test = False
            st.session_state.show_simplification_test = False
        
        st.markdown("---")
        
        # Feature Status
        st.markdown("### 📊 Feature Status")
        
        # Backend status
        backend_status = "🟢 Online" if check_backend_health() else "🔴 Offline"
        st.markdown(f"**Backend:** {backend_status}")
        
        # Feature status
        translation_status = "🟢 Enabled" if TRANSLATION_ENABLED else "🔴 Disabled"
        st.markdown(f"**Translation:** {translation_status}")
        
        simplification_status = "🟢 Enabled" if SIMPLIFICATION_ENABLED else "🔴 Disabled"
        st.markdown(f"**Simplification:** {simplification_status}")
        
        oauth_status = "🟢 Configured" if (GOOGLE_CLIENT_ID or FACEBOOK_APP_ID) else "🔴 Not Configured"
        st.markdown(f"**OAuth:** {oauth_status}")

def check_backend_health() -> bool:
    """Check if backend is healthy"""
    try:
        result = make_api_request("/health")
        return "error" not in result and result.get("status") == "healthy"
    except Exception:
        return False

# ========================================
# MAIN CONTENT SECTIONS
# ========================================

def render_header():
    """Render the main header with logo and tagline"""
    logo_base64 = get_logo_base64()
    
    if logo_base64:
        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" class="logo-image" alt="HAVEN Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="logo-container">
            <h1 style="color: #2d3748; font-size: 3rem; margin: 0;">HAVEN</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tagline">
        Help not just some people, but Help Humanity.
    </div>
    """, unsafe_allow_html=True)

def render_demo_content():
    """Render demo content with automatic term simplification tooltips"""
    st.markdown("## 📚 Demo: Automatic Term Simplification")
    
    st.markdown("""
    <div class="content-with-tooltips">
    <p>Hover over the blue terms below to see automatic definitions:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample content with complex terms
    demo_text = """
    Welcome to HAVEN, the revolutionary crowdfunding platform that's transforming how startups and entrepreneurs raise capital. Our innovative approach combines traditional investment strategies with cutting-edge blockchain technology to create unprecedented opportunities for both investors and project creators.

    Whether you're an angel investor looking for the next unicorn startup, or an entrepreneur seeking seed funding for your MVP, HAVEN provides the tools and community you need. Our platform supports various funding models including equity crowdfunding, revenue-based financing, and traditional donation-based campaigns.

    Key features include:
    • Advanced due diligence tools powered by AI and machine learning
    • Comprehensive market research and analytics dashboard  
    • Automated compliance monitoring for regulatory requirements
    • Smart contract integration for transparent and secure transactions
    • Real-time ROI tracking and portfolio management
    • Social proof mechanisms including viral marketing tools

    Our scalable platform architecture ensures high performance even during peak funding periods, while our robust cybersecurity measures protect both investor funds and intellectual property. With built-in KPI tracking and detailed analytics, project creators can monitor their burn rate, extend their runway, and optimize their conversion rates.

    Join thousands of successful entrepreneurs who have already leveraged our platform to achieve their funding milestones and execute their exit strategies. From B2B SaaS solutions to B2C consumer products, HAVEN supports diverse business models across all industries.
    """
    
    # Add tooltips to the demo text
    demo_with_tooltips = add_tooltips_to_text(demo_text)
    
    st.markdown(f"""
    <div class="content-with-tooltips">
    {demo_with_tooltips}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 How It Works")
    st.markdown("""
    1. **Automatic Detection**: Complex terms are automatically identified in all content
    2. **Visual Indicators**: Terms appear in blue with a dotted underline and info icon (ℹ️)
    3. **Hover Tooltips**: Simply hover your mouse over any term to see its definition
    4. **No Clicking Required**: Definitions appear instantly without interrupting your reading
    5. **Mobile Friendly**: Tooltips work on touch devices too
    """)

def render_backend_test():
    """Render backend connection test"""
    st.markdown("## 🔧 Backend Connection Test")
    
    with st.spinner("Testing backend connection..."):
        result = make_api_request("/api/backend-test")
    
    if "error" in result:
        st.markdown(f"""
        <div class="status-error">
            ❌ Backend Connection Failed<br>
            Error: {result['error']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-success">
            ✅ Backend Connection Successful<br>
            Status: {result.get('backend_status', 'Unknown')}<br>
            Response Time: {result.get('response_time_ms', 0):.2f}ms
        </div>
        """, unsafe_allow_html=True)
        
        # Show detailed test results
        st.markdown("### 📊 Detailed Test Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("CORS Enabled", "✅ Yes" if result.get('cors_enabled') else "❌ No")
            st.metric("Translation Available", "✅ Yes" if result.get('translation_available') else "❌ No")
        
        with col2:
            st.metric("Simplification Available", "✅ Yes" if result.get('simplification_available') else "❌ No")
            st.metric("OAuth Configured", "✅ Yes" if result.get('oauth_configured') else "❌ No")

def render_translation_test():
    """Render translation test interface"""
    st.markdown("## 🌐 Translation Test")
    
    # Input form
    with st.form("translation_form"):
        text_to_translate = st.text_area(
            "Enter text to translate:",
            placeholder="Type your text here...",
            height=100
        )
        
        languages = get_supported_languages()
        target_language = st.selectbox(
            "Target Language:",
            options=[lang["code"] for lang in languages],
            format_func=lambda x: next(lang["native"] for lang in languages if lang["code"] == x)
        )
        
        submit_button = st.form_submit_button("🔄 Translate")
    
    if submit_button and text_to_translate:
        with st.spinner("Translating..."):
            result = make_api_request("/api/translate", "POST", {
                "text": text_to_translate,
                "target_language": target_language,
                "source_language": "auto"
            })
        
        if "error" in result:
            st.markdown(f"""
            <div class="status-error">
                ❌ Translation Failed<br>
                Error: {result['error']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("### 📝 Translation Result")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Original Text:**")
                st.info(result.get('original_text', ''))
                st.markdown(f"**Language:** {result.get('source_language', 'Unknown')}")
            
            with col2:
                st.markdown("**Translated Text:**")
                st.success(result.get('translated_text', ''))
                st.markdown(f"**Language:** {result.get('target_language', 'Unknown')}")
            
            st.markdown(f"**Confidence:** {result.get('confidence', 0):.2%}")

def render_simplification_test():
    """Render simplification test interface"""
    st.markdown("## 📝 Term Simplification Test")
    
    # Input form
    with st.form("simplification_form"):
        text_to_simplify = st.text_area(
            "Enter text with complex terms:",
            placeholder="Enter text containing financial, technical, or business terms...",
            height=100,
            value="Our startup is seeking crowdfunding to develop a blockchain-based platform for cryptocurrency investment with high ROI potential."
        )
        
        submit_button = st.form_submit_button("🔍 Analyze & Simplify")
    
    if submit_button and text_to_simplify:
        with st.spinner("Analyzing text..."):
            result = make_api_request("/api/simplify", "POST", {
                "text": text_to_simplify,
                "level": "simple"
            })
        
        if "error" in result:
            st.markdown(f"""
            <div class="status-error">
                ❌ Simplification Failed<br>
                Error: {result['error']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("### 📊 Analysis Results")
            
            # Show complexity score
            complexity = result.get('complexity_score', 0)
            st.metric("Complexity Score", f"{complexity:.2f}")
            
            # Show found terms
            terms = result.get('simplified_terms', [])
            if terms:
                st.markdown("### 📚 Complex Terms Found")
                
                for term in terms:
                    with st.expander(f"ℹ️ {term['term'].title()}", expanded=False):
                        st.markdown(f"**Definition:** {term['definition']}")
                        st.markdown(f"**Category:** {term['category'].title()}")
                        st.markdown(f"**Complexity:** {term['complexity_level'].title()}")
            else:
                st.info("No complex terms found in the text.")

def render_login_page():
    """Render the login page"""
    st.markdown("## 🔐 Login to HAVEN")
    
    # Login form
    with st.form("login_form"):
        email = st.text_input("📧 Email Address", placeholder="Enter your email")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        login_button = st.form_submit_button("🚀 Continue")
    
    if login_button:
        if email and password:
            # Mock login for demo
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
        else:
            st.error("Please enter both email and password")
    
    # OAuth buttons
    st.markdown("### 🔗 Or sign in with:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if GOOGLE_CLIENT_ID:
            if st.button("🔍 Sign in with Google", key="google_login"):
                st.info("Google OAuth integration would open here")
    
    with col2:
        if FACEBOOK_APP_ID:
            if st.button("📘 Sign in with Facebook", key="facebook_login"):
                st.info("Facebook OAuth integration would open here")
    
    # Registration link
    st.markdown("---")
    st.markdown("**Not registered?** [Create an account](#)")

# ========================================
# MAIN APPLICATION
# ========================================

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="HAVEN - Crowdfunding Platform",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load CSS
    load_css()
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "en"
    if "show_backend_test" not in st.session_state:
        st.session_state.show_backend_test = False
    if "show_translation_test" not in st.session_state:
        st.session_state.show_translation_test = False
    if "show_simplification_test" not in st.session_state:
        st.session_state.show_simplification_test = False
    if "show_demo_content" not in st.session_state:
        st.session_state.show_demo_content = False
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    with st.container():
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        # Render header
        render_header()
        
        # Check if user is logged in
        if not st.session_state.logged_in:
            render_login_page()
        else:
            # Show main application content
            st.markdown(f"## Welcome back, {st.session_state.get('user_email', 'User')}! 👋")
            
            # Show different sections based on sidebar selection
            if st.session_state.show_backend_test:
                render_backend_test()
                if st.button("🔙 Back to Home"):
                    st.session_state.show_backend_test = False
                    st.rerun()
            
            elif st.session_state.show_translation_test:
                render_translation_test()
                if st.button("🔙 Back to Home"):
                    st.session_state.show_translation_test = False
                    st.rerun()
            
            elif st.session_state.show_simplification_test:
                render_simplification_test()
                if st.button("🔙 Back to Home"):
                    st.session_state.show_simplification_test = False
                    st.rerun()
            
            elif st.session_state.show_demo_content:
                render_demo_content()
                if st.button("🔙 Back to Home"):
                    st.session_state.show_demo_content = False
                    st.rerun()
            
            else:
                # Default home content
                st.markdown("### 🎯 Platform Features")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    **🌐 Multi-language Support**
                    - English, Hindi, Tamil, Telugu
                    - Real-time translation
                    - Localized content
                    """)
                
                with col2:
                    st.markdown("""
                    **📝 Smart Simplification**
                    - Automatic term detection
                    - Hover tooltips
                    - Context-aware definitions
                    """)
                
                with col3:
                    st.markdown("""
                    **🔐 Secure Authentication**
                    - Google OAuth
                    - Facebook OAuth
                    - Secure sessions
                    """)
                
                # Demo content preview
                st.markdown("---")
                st.markdown("### 📚 Try Automatic Term Simplification")
                
                sample_text = "Our startup is seeking crowdfunding for a blockchain-based cryptocurrency platform with high ROI potential."
                sample_with_tooltips = add_tooltips_to_text(sample_text)
                
                st.markdown(f"""
                <div class="content-with-tooltips">
                <p><strong>Sample text with automatic tooltips:</strong></p>
                <p>{sample_with_tooltips}</p>
                <p><em>Hover over the blue terms to see definitions!</em></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Logout button
                if st.button("🚪 Logout"):
                    st.session_state.logged_in = False
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

