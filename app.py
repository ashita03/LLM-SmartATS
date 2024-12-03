# app.py improvements
import streamlit as st
import logging
from db_utils import get_or_create_user, get_user_applications
from page_components import resume_review_page, cover_letter_page, networking_page

# Add proper logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_session():
    # Fix session state initialization
    default_session_states = {
        'is_authenticated': False,
        'user_email': None,
        'replace_resume': False
    }
    
    for key, default_value in default_session_states.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def authenticate_user():
    if not st.session_state.is_authenticated:
        st.title("Welcome to Job Application Assistant")
        email = st.text_input("Please enter your email to continue:")
        
        if st.button("Continue"):
            try:
                # Improved email validation
                if not email or '@' not in email or '.' not in email.split('@')[1]:
                    st.error("Please enter a valid email address")
                    return False
                
                user = get_or_create_user(email)
                
                if user:
                    st.session_state.is_authenticated = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error("Could not authenticate user")
            
            except Exception as e:
                logger.error(f"Authentication error: {e}")
                st.error("An error occurred during authentication")
        
        return False
    return True

def main_app():
    try:
        # Create navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio(
            "Go to",
            ["Home", "Resume Review", "Cover Letter", "Networking"]
        )
        
        # Route to appropriate page
        page_routes = {
            "Home": main_page,
            "Resume Review": resume_review_page,
            "Cover Letter": cover_letter_page,
            "Networking": networking_page
        }
        
        page_routes.get(page, main_page)()
    
    except Exception as e:
        logger.error(f"Error in main app: {e}")
        st.error("An unexpected error occurred")

def main_page():
    st.title("🎯 Smart AI - Job Application Dashboard")
    
    if not st.session_state.get('user_email'):
        st.warning("User email not found")
        return
    
    st.write(f"👋🏻 Welcome back, {st.session_state.user_email}!")

    st.markdown("### ⏯️ About")
    st.text_area(
        "Purpose of the application",
        "The main aim of this product is to support students in ensuring their "
        "application is up to the mark in this competitive market. The product "
        "provides multiple AI-generated features that could support the student "
        "in the entire job application journey.",
    )
    
    try:
        applications = get_user_applications(st.session_state.user_email)
        
        if applications:
            st.subheader("Your Recent Application Support")
            for app in applications:
                with st.expander(f"{app['company_name']} - {app['role']}"):
                    st.write(f"Status: {app['status'] or 'Not specified'}")
                    st.write(f"Applied: {app['created_at'].strftime('%Y-%m-%d') if app['created_at'] else 'Date not available'}")
                    st.write(f"Resume Review: {'✓' if app['resume_review'] else '✗'}")
                    st.write(f"Cover Letter: {'✓' if app['cover_letter'] else '✗'}")
                    st.write(f"Networking Email: {'✓' if app['networking_email'] else '✗'}")
        else:
            st.info("No recent job applications found")
    
    except Exception as e:
        logger.error(f"Error retrieving applications: {e}")
        st.error("Could not retrieve job applications")

if __name__ == "__main__":
    init_session()
    if authenticate_user():
        main_app()