import streamlit as st
from utils import get_all_campaigns
from streamlit_card import card

def show():
    st.header("Search for a Campaign")
    query = st.text_input("Enter keywords")
    if query:
        all_campaigns = get_all_campaigns()
        results = [c for c in all_campaigns if query.lower() in c['title'].lower()]
        if results:
            st.subheader(f"Found {len(results)} results:")
            cols = st.columns(3)
            for i, campaign in enumerate(results):
                with cols[i % 3]:
                    card(title=campaign['title'], text=f"Goal: ${campaign['target_amount']:,}", image=campaign['image'], url="#")
        else:
            st.warning("No campaigns found for your query.")
