# app.py
import streamlit as st
#from navigation.main import main
#from navigation.cover_letter import cover_main
import db_utils
from page_components import resume_review_page, cover_letter_page, networking_page


# Initialize session state
def init_session():
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

def authenticate_user():
    if not st.session_state.is_authenticated:
        st.title("Welcome to Job Application Assistant")
        email = st.text_input("Please enter your email to continue:")
        if st.button("Continue"):
            if email and '@' in email:
                user = db_utils.get_or_create_user(email)
                st.session_state.is_authenticated = True
                st.session_state.user_email = email
                st.session_state.user_id = user.id
                st.rerun()
            else:
                st.error("Please enter a valid email address")
        return False
    return True

def main_app():
    # Create navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Resume Review", "Cover Letter", "Networking"]
    )
    
    if page == "Home":
        main_page()
    elif page == "Resume Review":
        resume_review_page()
    elif page == "Cover Letter":
        cover_letter_page()
    elif page == "Networking":
        networking_page()

def main_page():
    st.title("🎯 Smart AI - Job Application Dashboard")
    st.write(f"👋🏻 Welcome back, {st.session_state.user_email}!")
    

    st.markdown("### ⏯️ About")
    st.text_area(
        "Purpose of the application",
        "The main aim of this product is to support students in ensuring their application "
        "is up to the mark in this competitive market. The product provides multiple AI "
        "generated features that could support the student in the entire journey.",
    )
    
    # Show user's applications
    applications = db_utils.get_user_applications(st.session_state.user_id)
    if applications:
        st.subheader("Your Recent Applications")
        for app in applications:
            with st.expander(f"{app.company_name} - {app.role}"):
                st.write(f"Status: {app.status}")
                st.write(f"Applied: {app.created_at.strftime('%Y-%m-%d')}")
                if app.resume_review:
                    st.write("Resume Review: ✓")
                if app.cover_letter:
                    st.write("Cover Letter: ✓")
                if app.networking_email:
                    st.write("Networking Email: ✓")

if __name__ == "__main__":
    init_session()
    if authenticate_user():
        main_app()