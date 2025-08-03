"""
HAVEN Crowdfunding Platform - Complete Streamlit Frontend
Enhanced with 4-language translation and term simplification
"""

import streamlit as st
import requests
import json
import asyncio
import time
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="HAVEN Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
BACKEND_URL = st.secrets.get("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")
DEFAULT_LANGUAGE = "en"

# Language configuration
SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "flag": "🇺🇸", "native": "English"},
    "hi": {"name": "Hindi", "flag": "🇮🇳", "native": "हिन्दी"},
    "ta": {"name": "Tamil", "flag": "🇮🇳", "native": "தமிழ்"},
    "te": {"name": "Telugu", "flag": "🇮🇳", "native": "తెలుగు"}
}

# Custom CSS for light green theme
st.markdown("""
<style>
    /* Main theme colors */
    .main {
        background-color: #f1f8e9;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #e8f5e8;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #4caf50, #66bb6a);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Translation bar styling */
    .translation-bar {
        background-color: #c8e6c9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin-bottom: 1rem;
    }
    
    /* Feature card styling */
    .feature-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #4caf50;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #45a049;
    }
    
    /* Success message styling */
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    /* Term tooltip styling */
    .term-tooltip {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 4px;
        padding: 0.5rem;
        margin: 0.25rem 0;
        font-size: 0.9em;
    }
    
    /* Language selector styling */
    .language-selector {
        background-color: #e8f5e8;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_language' not in st.session_state:
    st.session_state.current_language = DEFAULT_LANGUAGE
if 'translation_enabled' not in st.session_state:
    st.session_state.translation_enabled = False
if 'simplification_enabled' not in st.session_state:
    st.session_state.simplification_enabled = False
if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False

# Utility functions
def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API request to backend"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return {"error": str(e)}
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return {"error": str(e)}

def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    """Translate text using backend API"""
    if not text or source_language == target_language:
        return text
    
    try:
        data = {
            "text": text,
            "source_language": source_language,
            "target_language": target_language
        }
        
        result = make_api_request("/api/translate", "POST", data)
        
        if "error" not in result:
            return result.get("translated_text", text)
        else:
            return text
    
    except Exception:
        return text

def simplify_text(text: str, level: str = "simple") -> str:
    """Simplify text using backend API"""
    if not text:
        return text
    
    try:
        data = {
            "text": text,
            "target_level": level
        }
        
        result = make_api_request("/api/simplify", "POST", data)
        
        if "error" not in result:
            return result.get("simplified_text", text)
        else:
            return text
    
    except Exception:
        return text

def get_term_definition(term: str) -> Optional[str]:
    """Get simple definition for a term"""
    try:
        result = make_api_request(f"/api/simplify/define/{term}")
        
        if "error" not in result:
            return result.get("simple_definition")
        else:
            return None
    
    except Exception:
        return None

def display_text_with_translation(text: str, key: str = None):
    """Display text with optional translation and simplification"""
    if not text:
        return
    
    # Apply translation if enabled
    if st.session_state.translation_enabled and st.session_state.current_language != "en":
        translated_text = translate_text(text, st.session_state.current_language, "en")
    else:
        translated_text = text
    
    # Apply simplification if enabled
    if st.session_state.simplification_enabled:
        simplified_text = simplify_text(translated_text)
    else:
        simplified_text = translated_text
    
    # Display the text
    st.markdown(simplified_text)

# Header component
def render_header():
    """Render main header with branding"""
    st.markdown("""
    <div class="main-header">
        <h1>🏠 HAVEN Crowdfunding Platform</h1>
        <p>Empowering Innovation Through Community Funding</p>
    </div>
    """, unsafe_allow_html=True)

# Translation and simplification controls
def render_language_controls():
    """Render language and simplification controls"""
    st.markdown("""
    <div class="translation-bar">
        <h4>🌍 Language & Accessibility Settings</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Language selector
        language_options = [
            f"{lang_info['flag']} {lang_info['native']}" 
            for lang_code, lang_info in SUPPORTED_LANGUAGES.items()
        ]
        
        selected_lang_display = st.selectbox(
            "Select Language",
            language_options,
            index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.current_language),
            key="language_selector"
        )
        
        # Extract language code from selection
        for lang_code, lang_info in SUPPORTED_LANGUAGES.items():
            if f"{lang_info['flag']} {lang_info['native']}" == selected_lang_display:
                if st.session_state.current_language != lang_code:
                    st.session_state.current_language = lang_code
                    st.rerun()
                break
    
    with col2:
        # Translation toggle
        translation_enabled = st.checkbox(
            "🔄 Enable Translation",
            value=st.session_state.translation_enabled,
            help="Translate content to your selected language"
        )
        
        if translation_enabled != st.session_state.translation_enabled:
            st.session_state.translation_enabled = translation_enabled
            st.rerun()
    
    with col3:
        # Simplification toggle
        simplification_enabled = st.checkbox(
            "💡 Simplify Complex Terms",
            value=st.session_state.simplification_enabled,
            help="Make complex financial and technical terms easier to understand"
        )
        
        if simplification_enabled != st.session_state.simplification_enabled:
            st.session_state.simplification_enabled = simplification_enabled
            st.rerun()
    
    # Show current settings
    if st.session_state.translation_enabled or st.session_state.simplification_enabled:
        settings_text = []
        if st.session_state.translation_enabled:
            lang_name = SUPPORTED_LANGUAGES[st.session_state.current_language]['native']
            settings_text.append(f"Translating to {lang_name}")
        if st.session_state.simplification_enabled:
            settings_text.append("Simplifying complex terms")
        
        st.info(f"Active: {' | '.join(settings_text)}")

# Main navigation
def render_navigation():
    """Render main navigation sidebar"""
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        # Main pages
        page = st.radio(
            "Choose a page:",
            [
                "🏠 Home",
                "🔍 Explore Campaigns", 
                "🚀 Create Campaign",
                "👤 Profile",
                "🔐 Authentication",
                "🌍 Translation Hub",
                "💡 Simplification Center",
                "📊 Analytics"
            ]
        )
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("## ⚡ Quick Actions")
        
        if st.button("🔄 Translate Page"):
            st.session_state.translation_enabled = not st.session_state.translation_enabled
            st.rerun()
        
        if st.button("💡 Toggle Simplification"):
            st.session_state.simplification_enabled = not st.session_state.simplification_enabled
            st.rerun()
        
        # Service status
        st.markdown("---")
        st.markdown("## 📡 Service Status")
        
        try:
            health = make_api_request("/health")
            if "error" not in health:
                st.success("✅ Backend Connected")
                if health.get("features", {}).get("translation"):
                    st.success("✅ Translation Available")
                if health.get("features", {}).get("simplification"):
                    st.success("✅ Simplification Available")
            else:
                st.error("❌ Backend Unavailable")
        except:
            st.error("❌ Connection Failed")
    
    return page

# Page components
def render_home_page():
    """Render home page"""
    st.markdown("## 🏠 Welcome to HAVEN")
    
    display_text_with_translation("""
    HAVEN is a revolutionary crowdfunding platform that connects innovative projects 
    with passionate supporters. Our platform leverages cutting-edge technology to 
    ensure transparency, security, and accessibility for all users.
    """)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🚀 Launch Your Project</h4>
            <p>Turn your innovative ideas into reality with our easy-to-use campaign creation tools.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🤝 Support Innovation</h4>
            <p>Discover and fund groundbreaking projects that align with your interests and values.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🛡️ Secure & Transparent</h4>
            <p>Advanced fraud detection and blockchain technology ensure your investments are safe.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent campaigns
    st.markdown("## 🔥 Featured Campaigns")
    
    # Mock campaign data
    campaigns = [
        {
            "title": "Smart Agriculture IoT System",
            "description": "Revolutionary IoT sensors for precision farming",
            "goal": "$50,000",
            "raised": "$32,500",
            "progress": 65
        },
        {
            "title": "Eco-Friendly Water Purifier",
            "description": "Solar-powered water purification for rural communities",
            "goal": "$25,000",
            "raised": "$18,750",
            "progress": 75
        },
        {
            "title": "Educational VR Platform",
            "description": "Immersive virtual reality learning experiences",
            "goal": "$75,000",
            "raised": "$45,000",
            "progress": 60
        }
    ]
    
    for campaign in campaigns:
        with st.expander(f"📈 {campaign['title']}"):
            display_text_with_translation(campaign['description'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Goal", campaign['goal'])
            with col2:
                st.metric("Raised", campaign['raised'])
            with col3:
                st.metric("Progress", f"{campaign['progress']}%")
            
            st.progress(campaign['progress'] / 100)

def render_explore_page():
    """Render explore campaigns page"""
    st.markdown("## 🔍 Explore Campaigns")
    
    display_text_with_translation("""
    Discover innovative projects and campaigns from creators around the world. 
    Use our advanced filters to find projects that match your interests.
    """)
    
    # Search and filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search campaigns", placeholder="Enter keywords...")
    
    with col2:
        category = st.selectbox(
            "📂 Category",
            ["All", "Technology", "Health", "Education", "Environment", "Arts"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "📊 Sort by",
            ["Most Recent", "Most Funded", "Ending Soon", "Most Popular"]
        )
    
    # Campaign grid
    st.markdown("### 📋 Campaign Results")
    
    # Mock search results
    if search_query or category != "All":
        st.info(f"Showing results for: {search_query or category}")
    
    # Display campaigns in grid
    campaigns = [
        {"title": "AI-Powered Healthcare Assistant", "category": "Health", "raised": "$45,000", "goal": "$60,000"},
        {"title": "Sustainable Energy Storage", "category": "Technology", "raised": "$78,000", "goal": "$100,000"},
        {"title": "Digital Literacy Program", "category": "Education", "raised": "$23,000", "goal": "$40,000"},
        {"title": "Ocean Cleanup Initiative", "category": "Environment", "raised": "$156,000", "goal": "$200,000"}
    ]
    
    for i in range(0, len(campaigns), 2):
        col1, col2 = st.columns(2)
        
        for j, col in enumerate([col1, col2]):
            if i + j < len(campaigns):
                campaign = campaigns[i + j]
                with col:
                    with st.container():
                        st.markdown(f"**{campaign['title']}**")
                        st.markdown(f"Category: {campaign['category']}")
                        st.markdown(f"Raised: {campaign['raised']} / {campaign['goal']}")
                        
                        progress = int(campaign['raised'].replace('$', '').replace(',', '')) / int(campaign['goal'].replace('$', '').replace(',', ''))
                        st.progress(progress)
                        
                        if st.button(f"View Details", key=f"view_{i+j}"):
                            st.info("Campaign details would open here")

def render_create_campaign_page():
    """Render create campaign page"""
    st.markdown("## 🚀 Create Your Campaign")
    
    display_text_with_translation("""
    Launch your innovative project and connect with supporters who believe in your vision. 
    Our platform provides all the tools you need to create a successful crowdfunding campaign.
    """)
    
    # Campaign creation form
    with st.form("create_campaign"):
        st.markdown("### 📝 Campaign Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Campaign Title*", placeholder="Enter a compelling title")
            category = st.selectbox("Category*", ["Technology", "Health", "Education", "Environment", "Arts", "Other"])
            goal_amount = st.number_input("Funding Goal ($)*", min_value=1000, value=10000, step=1000)
        
        with col2:
            duration = st.number_input("Campaign Duration (days)*", min_value=7, max_value=90, value=30)
            location = st.text_input("Location", placeholder="City, Country")
            website = st.text_input("Website/Social Media", placeholder="https://...")
        
        description = st.text_area(
            "Campaign Description*", 
            placeholder="Describe your project, its impact, and why people should support it...",
            height=150
        )
        
        # File uploads
        st.markdown("### 📸 Media")
        
        col1, col2 = st.columns(2)
        with col1:
            main_image = st.file_uploader("Main Campaign Image", type=['jpg', 'jpeg', 'png'])
        with col2:
            additional_images = st.file_uploader("Additional Images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
        
        video_url = st.text_input("Video URL (optional)", placeholder="YouTube, Vimeo, etc.")
        
        # Rewards/perks
        st.markdown("### 🎁 Rewards & Perks")
        
        num_rewards = st.number_input("Number of reward tiers", min_value=0, max_value=10, value=3)
        
        for i in range(num_rewards):
            with st.expander(f"Reward Tier {i+1}"):
                col1, col2 = st.columns(2)
                with col1:
                    reward_amount = st.number_input(f"Minimum Contribution ($)", min_value=1, value=25, key=f"reward_amount_{i}")
                with col2:
                    reward_title = st.text_input(f"Reward Title", placeholder="Early Bird Special", key=f"reward_title_{i}")
                
                reward_description = st.text_area(f"Reward Description", placeholder="What backers will receive...", key=f"reward_desc_{i}")
        
        # Terms and conditions
        st.markdown("### ⚖️ Terms & Conditions")
        
        col1, col2 = st.columns(2)
        with col1:
            agree_terms = st.checkbox("I agree to the Terms of Service*")
        with col2:
            agree_fraud = st.checkbox("I confirm this campaign is legitimate*")
        
        # Submit button
        submitted = st.form_submit_button("🚀 Launch Campaign", type="primary")
        
        if submitted:
            if not all([title, category, description, agree_terms, agree_fraud]):
                st.error("Please fill in all required fields and agree to the terms.")
            else:
                # Here you would normally submit to the backend
                st.success("🎉 Campaign created successfully! It will be reviewed before going live.")
                
                # Show campaign preview
                with st.expander("📋 Campaign Preview"):
                    st.markdown(f"**{title}**")
                    st.markdown(f"Category: {category}")
                    st.markdown(f"Goal: ${goal_amount:,}")
                    st.markdown(f"Duration: {duration} days")
                    st.markdown(description)

def render_translation_hub():
    """Render translation hub page"""
    st.markdown("## 🌍 Translation Hub")
    
    display_text_with_translation("""
    Translate content between English, Hindi, Tamil, and Telugu. 
    Our AI-powered translation service ensures accurate and contextual translations.
    """)
    
    # Translation interface
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Input Text")
        
        source_lang = st.selectbox(
            "Source Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]['flag']} {SUPPORTED_LANGUAGES[x]['native']}",
            key="trans_source"
        )
        
        input_text = st.text_area(
            "Text to translate",
            placeholder="Enter text to translate...",
            height=200
        )
    
    with col2:
        st.markdown("### 🔄 Translation")
        
        target_lang = st.selectbox(
            "Target Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]['flag']} {SUPPORTED_LANGUAGES[x]['native']}",
            index=1,
            key="trans_target"
        )
        
        if st.button("🔄 Translate", type="primary"):
            if input_text:
                with st.spinner("Translating..."):
                    translated = translate_text(input_text, target_lang, source_lang)
                    st.text_area("Translation result", value=translated, height=200, disabled=True)
            else:
                st.warning("Please enter text to translate")
    
    # Batch translation
    st.markdown("### 📚 Batch Translation")
    
    uploaded_file = st.file_uploader("Upload text file for batch translation", type=['txt'])
    
    if uploaded_file:
        content = uploaded_file.read().decode('utf-8')
        lines = content.split('\n')
        
        if st.button("🔄 Translate All Lines"):
            with st.spinner(f"Translating {len(lines)} lines..."):
                translated_lines = []
                for line in lines:
                    if line.strip():
                        translated = translate_text(line, target_lang, source_lang)
                        translated_lines.append(translated)
                    else:
                        translated_lines.append("")
                
                # Display results
                st.markdown("### 📋 Translation Results")
                for i, (original, translated) in enumerate(zip(lines, translated_lines)):
                    if original.strip():
                        st.markdown(f"**Line {i+1}:**")
                        st.markdown(f"Original: {original}")
                        st.markdown(f"Translated: {translated}")
                        st.markdown("---")

def render_simplification_center():
    """Render simplification center page"""
    st.markdown("## 💡 Simplification Center")
    
    display_text_with_translation("""
    Make complex financial and technical terms easier to understand. 
    Our AI analyzes text complexity and provides simplified explanations.
    """)
    
    # Text simplification
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Complex Text")
        
        complexity_level = st.selectbox(
            "Target Complexity Level",
            ["very_simple", "simple", "moderate"],
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        complex_text = st.text_area(
            "Enter complex text",
            placeholder="Enter text with complex terms...",
            height=200
        )
    
    with col2:
        st.markdown("### 💡 Simplified Text")
        
        if st.button("💡 Simplify", type="primary"):
            if complex_text:
                with st.spinner("Simplifying..."):
                    simplified = simplify_text(complex_text, complexity_level)
                    st.text_area("Simplified result", value=simplified, height=200, disabled=True)
            else:
                st.warning("Please enter text to simplify")
    
    # Term lookup
    st.markdown("### 🔍 Term Lookup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("Search for a term", placeholder="e.g., crowdfunding, equity, ROI")
        
        if st.button("🔍 Search Term"):
            if search_term:
                definition = get_term_definition(search_term)
                if definition:
                    st.success(f"**{search_term}**: {definition}")
                else:
                    st.warning(f"Definition not found for '{search_term}'")
    
    with col2:
        # Popular terms
        st.markdown("#### 🔥 Popular Terms")
        popular_terms = ["crowdfunding", "equity", "roi", "valuation", "angel_investor"]
        
        for term in popular_terms:
            if st.button(f"📖 {term.replace('_', ' ').title()}", key=f"popular_{term}"):
                definition = get_term_definition(term)
                if definition:
                    st.info(f"**{term.replace('_', ' ').title()}**: {definition}")
    
    # Complexity analysis
    st.markdown("### 📊 Text Complexity Analysis")
    
    analysis_text = st.text_area("Text to analyze", placeholder="Enter text for complexity analysis...")
    
    if st.button("📊 Analyze Complexity"):
        if analysis_text:
            try:
                data = {"text": analysis_text}
                result = make_api_request("/api/simplify/analyze", "POST", data)
                
                if "error" not in result:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Complexity Score", f"{result['complexity_score']:.1f}/100")
                    with col2:
                        st.metric("Complexity Level", result['complexity_level'])
                    with col3:
                        st.metric("Word Count", result['word_count'])
                    
                    if result.get('complex_terms'):
                        st.markdown("#### 🔍 Complex Terms Found:")
                        for term_info in result['complex_terms']:
                            st.markdown(f"- **{term_info['term']}**: {term_info['definition']}")
                    
                    if result.get('recommendations'):
                        st.markdown("#### 💡 Recommendations:")
                        for rec in result['recommendations']:
                            st.markdown(f"- {rec}")
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

def render_analytics_page():
    """Render analytics page"""
    st.markdown("## 📊 Platform Analytics")
    
    display_text_with_translation("""
    Monitor platform performance, translation usage, and user engagement metrics.
    """)
    
    # Service statistics
    try:
        stats = make_api_request("/api/stats")
        
        if "error" not in stats:
            st.markdown("### 🔧 Service Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Supported Languages", stats.get('combined_stats', {}).get('total_supported_languages', 4))
            with col2:
                st.metric("Available Terms", stats.get('combined_stats', {}).get('total_terms_available', 0))
            with col3:
                st.metric("Services Status", "Healthy" if stats.get('combined_stats', {}).get('services_healthy') else "Issues")
            with col4:
                st.metric("Last Updated", "Now")
            
            # Translation statistics
            if 'translation' in stats:
                st.markdown("### 🌍 Translation Service")
                trans_stats = stats['translation']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Language Pairs", trans_stats.get('supported_language_pairs', 12))
                with col2:
                    st.metric("Cache Memory", trans_stats.get('cache_memory_usage', 'N/A'))
            
            # Simplification statistics
            if 'simplification' in stats:
                st.markdown("### 💡 Simplification Service")
                simp_stats = stats['simplification']
                
                if 'categories' in simp_stats:
                    st.markdown("#### 📚 Term Categories")
                    categories_df = pd.DataFrame(
                        list(simp_stats['categories'].items()),
                        columns=['Category', 'Term Count']
                    )
                    st.bar_chart(categories_df.set_index('Category'))
    
    except Exception as e:
        st.error(f"Failed to load analytics: {str(e)}")
    
    # Mock usage analytics
    st.markdown("### 📈 Usage Analytics")
    
    # Generate mock data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    usage_data = pd.DataFrame({
        'Date': dates,
        'Translations': [50 + i*2 + (i%7)*10 for i in range(len(dates))],
        'Simplifications': [30 + i*1.5 + (i%5)*8 for i in range(len(dates))],
        'New Users': [10 + i*0.5 + (i%3)*5 for i in range(len(dates))]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔄 Daily Translations")
        st.line_chart(usage_data.set_index('Date')['Translations'])
    
    with col2:
        st.markdown("#### 💡 Daily Simplifications")
        st.line_chart(usage_data.set_index('Date')['Simplifications'])
    
    st.markdown("#### 👥 New User Registrations")
    st.area_chart(usage_data.set_index('Date')['New Users'])

def render_authentication_page():
    """Render authentication page"""
    st.markdown("## 🔐 Authentication")
    
    if not st.session_state.user_authenticated:
        display_text_with_translation("""
        Sign in to access all features of the HAVEN platform. 
        Create campaigns, support projects, and manage your profile.
        """)
        
        tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])
        
        with tab1:
            st.markdown("### 🔑 Sign In to Your Account")
            
            with st.form("signin_form"):
                email = st.text_input("Email Address", placeholder="your@email.com")
                password = st.text_input("Password", type="password")
                remember_me = st.checkbox("Remember me")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("🔑 Sign In", type="primary"):
                        if email and password:
                            # Mock authentication
                            st.session_state.user_authenticated = True
                            st.success("✅ Successfully signed in!")
                            st.rerun()
                        else:
                            st.error("Please enter both email and password")
                
                with col2:
                    if st.form_submit_button("🔗 Forgot Password"):
                        st.info("Password reset link would be sent to your email")
            
            st.markdown("---")
            st.markdown("### 🌐 Social Sign In")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔴 Sign in with Google", key="google_signin"):
                    # Redirect to Google OAuth
                    google_oauth_url = f"{BACKEND_URL}/auth/google/login"
                    st.markdown(f"[Click here to sign in with Google]({google_oauth_url})")
            
            with col2:
                if st.button("🔵 Sign in with Facebook", key="facebook_signin"):
                    # Redirect to Facebook OAuth
                    facebook_oauth_url = f"{BACKEND_URL}/auth/facebook/login"
                    st.markdown(f"[Click here to sign in with Facebook]({facebook_oauth_url})")
        
        with tab2:
            st.markdown("### 📝 Create New Account")
            
            with st.form("signup_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name")
                    email = st.text_input("Email Address")
                    password = st.text_input("Password", type="password")
                
                with col2:
                    last_name = st.text_input("Last Name")
                    phone = st.text_input("Phone Number (optional)")
                    confirm_password = st.text_input("Confirm Password", type="password")
                
                country = st.selectbox("Country", ["India", "United States", "United Kingdom", "Canada", "Other"])
                
                agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
                newsletter = st.checkbox("Subscribe to newsletter for updates")
                
                if st.form_submit_button("📝 Create Account", type="primary"):
                    if not all([first_name, last_name, email, password, confirm_password]):
                        st.error("Please fill in all required fields")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    elif not agree_terms:
                        st.error("Please agree to the Terms of Service")
                    else:
                        # Mock account creation
                        st.success("✅ Account created successfully! Please check your email for verification.")
    
    else:
        # User is authenticated
        st.markdown("### 👤 User Profile")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image("https://via.placeholder.com/150", caption="Profile Picture")
            
            if st.button("🚪 Sign Out"):
                st.session_state.user_authenticated = False
                st.rerun()
        
        with col2:
            st.markdown("**John Doe**")
            st.markdown("📧 john.doe@email.com")
            st.markdown("📱 +1 (555) 123-4567")
            st.markdown("🌍 United States")
            st.markdown("📅 Member since: January 2024")
        
        # User statistics
        st.markdown("### 📊 Your Activity")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Campaigns Created", "3")
        with col2:
            st.metric("Projects Supported", "12")
        with col3:
            st.metric("Total Contributed", "$2,450")
        with col4:
            st.metric("Total Raised", "$8,750")

# Main application
def main():
    """Main application function"""
    # Render header
    render_header()
    
    # Render language controls
    render_language_controls()
    
    # Render navigation and get selected page
    selected_page = render_navigation()
    
    # Render selected page
    if selected_page == "🏠 Home":
        render_home_page()
    elif selected_page == "🔍 Explore Campaigns":
        render_explore_page()
    elif selected_page == "🚀 Create Campaign":
        render_create_campaign_page()
    elif selected_page == "👤 Profile":
        render_authentication_page()
    elif selected_page == "🔐 Authentication":
        render_authentication_page()
    elif selected_page == "🌍 Translation Hub":
        render_translation_hub()
    elif selected_page == "💡 Simplification Center":
        render_simplification_center()
    elif selected_page == "📊 Analytics":
        render_analytics_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🏠 HAVEN Crowdfunding Platform | Empowering Innovation Through Community</p>
        <p>🌍 Supporting 4 languages | 💡 AI-powered simplification | 🛡️ Secure & transparent</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

