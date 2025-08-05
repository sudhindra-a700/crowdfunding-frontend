import streamlit as st
from utils import get_all_campaigns, simplify_text
from streamlit_extras.stoggle import stoggle
from streamlit_notify import notify

def show():
    st.header("Campaign Details")
    campaigns = get_all_campaigns()
    campaign_titles = {c['title']: c['id'] for c in campaigns}
    selected_title = st.selectbox("Select a Campaign to View", campaign_titles.keys())
    
    campaign_id = campaign_titles[selected_title]
    campaign = next((c for c in campaigns if c['id'] == campaign_id), None)
    lang = st.session_state.get('language', 'en')

    if campaign:
        st.image(campaign['image'], use_column_width=True)
        st.title(campaign['title'])
        
        simplified_desc = simplify_text(campaign['description'], lang)
        stoggle("Read Campaign Description", simplified_desc)
        
        st.progress(campaign['current_amount'] / campaign['target_amount'])
        st.markdown(f"**${campaign['current_amount']:,}** raised of **${campaign['target_amount']:,}** goal")
        
        if campaign['verified']:
            st.success("This project is verified and open for funding.")
            with st.form("contribution_form"):
                amount = st.number_input("Enter your contribution amount", min_value=5)
                if st.form_submit_button("Contribute Now"):
                    notify(f"Thank you for your ${amount} contribution!", "success")
        else:
            st.warning("This project is under review and not accepting funding.")
