import streamlit as st
from utils import get_all_campaigns
from streamlit_card import card

def show():
    st.header("Explore All Campaigns")
    # This section can be expanded in the future with filters for category, location, etc.
    
    all_campaigns = get_all_campaigns()
    if not all_campaigns:
        st.info("No campaigns are available at the moment.")
        return
    
    # Create a responsive 3-column grid for displaying campaigns
    cols = st.columns(3)
    for i, campaign in enumerate(all_campaigns):
        with cols[i % 3]:
            card(
                title=campaign['title'], 
                text=f"Goal: ${campaign['target_amount']:,}", 
                image=campaign['image'], 
                url="#" # This would link to the campaign detail page
            )
