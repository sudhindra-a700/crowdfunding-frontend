import streamlit as st
from utils import (
    submit_campaign_for_review, 
    get_individual_profile_data, 
    get_organization_profile_data
)
from streamlit_notify import notify

def display_individual_profile():
    st.subheader("Your Personal Information")
    profile_data = get_individual_profile_data()
    with st.form("individual_profile_form", border=True):
        st.text_input("Full Name", value=profile_data["full_name"])
        st.text_input("Email Address", value=profile_data["email"], disabled=True)
        st.text_input("Phone Number", value=profile_data["phone"])
        st.text_area("Address", value=profile_data["address"])
        if st.form_submit_button("Update Profile"):
            notify("Profile updated successfully!", "success")
    st.subheader("Your Donation History")
    for campaign in profile_data["donated_to"]:
        st.info(f"You donated to: **{campaign['title']}**")

def display_organization_profile():
    st.subheader("Your Organization's Information")
    profile_data = get_organization_profile_data()
    with st.form("organization_profile_form", border=True):
        st.text_input("Organization Name", value=profile_data["org_name"])
        st.text_input("Contact Person", value=profile_data["contact_person"])
        st.text_input("Contact Email", value=profile_data["contact_email"], disabled=True)
        st.text_input("Organization Phone", value=profile_data["org_phone"])
        st.selectbox("Organization Type", ["NGO", "Non-Profit", "Social Enterprise"], index=0)
        st.text_area("Organization Description", value=profile_data["org_description"])
        if st.form_submit_button("Update Profile"):
            notify("Organization profile updated successfully!", "success")
    st.subheader("Campaigns You Created")
    for campaign in profile_data["created_campaigns"]:
        st.info(f"You created the campaign: **{campaign['title']}**")

def show_profile_details():
    st.title("Your Profile")
    user_type = st.session_state.get("user_type")
    if user_type == "individual":
        display_individual_profile()
    elif user_type == "organization":
        display_organization_profile()
    else:
        st.error("Could not determine user type. Please log in again.")

def show_creation_form():
    st.title("Create a New Campaign")
    st.info("Submit your project details below. It will be reviewed by our AI and Admin team.")
    with st.form("new_campaign_form", border=True):
        title = st.text_input("Campaign Title")
        description = st.text_area("Campaign Description")
        category = st.selectbox("Category", ["Education", "Health", "Community"])
        target_amount = st.number_input("Target Amount ($)", min_value=100.0)
        if st.form_submit_button("Submit for Moderation"):
            data = {"title": title, "description": description, "category": category, "target_amount": target_amount}
            response = submit_campaign_for_review(data)
            notify(response['message'], "success")
