import streamlit as st
from dotenv import load_dotenv
from db_utils import (
    init_session_state, 
    save_resume, 
    get_active_resume,
    get_user_applications,
)
from db_schema import SessionLocal, User
import pdfplumber
import io

# Load environment variables and initialize session state
load_dotenv()
init_session_state()

# Initialize session state for user login details
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

def prompt_email():
    """Prompt user to log in or register"""
    if st.session_state.user_email is None:
        st.write("### User Login / Registration")
        email = st.text_input("📧 Enter your email to login or register:")
        
        if email:
            db = SessionLocal()
            try:
                # Check if user already exists
                user = db.query(User).filter_by(email=email).first()
                if user:
                    # Existing user, set session state
                    st.session_state.user_email = user.email
                    st.session_state.user_id = user.id
                    st.success("Logged in successfully!")
                else:
                    # New user - registration flow
                    st.write("New user detected. Please register.")
                    first_name = st.text_input("First Name:")
                    last_name = st.text_input("Last Name:")
                    
                    if first_name and last_name:
                        # Register new user in the database
                        new_user = User(email=email, first_name=first_name, last_name=last_name)
                        db.add(new_user)
                        db.commit()
                        st.session_state.user_email = new_user.email
                        st.session_state.user_id = new_user.id
                        st.success("Registered and logged in successfully!")
            finally:
                db.close()

def handle_resume_upload():
    """Handle resume upload and display"""
    st.markdown("### 📄 Resume Management")
    current_resume = get_active_resume(st.session_state.user_id)
    
    if current_resume:
        st.success(f"Current active resume: {current_resume.file_name}")
        if st.button("View Current Resume"):
            try:
                with pdfplumber.open(io.BytesIO(current_resume.content)) as pdf:
                    pdf_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                    st.text_area("Resume Content", pdf_text, height=300, disabled=True)
            except Exception as e:
                st.error("Error displaying PDF. Please try uploading again.")
    
    uploaded_file = st.file_uploader(
        "Upload new resume (PDF)", 
        type="pdf",
        help="This resume will be used across all features"
    )
    
    if uploaded_file:
        try:
            file_content = uploaded_file.read()
            save_resume(st.session_state.user_id, file_content, uploaded_file.name)
            st.success("Resume updated successfully!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error saving resume: {str(e)}")

def display_about():
    """Display about section"""
    st.markdown("### 🎯 About")
    st.text_area(
        "Purpose of the application",
        "The main aim of this product is to support students in ensuring their application "
        "is up to the mark in this competitive market. The product provides multiple AI "
        "generated features that could support the student in the entire journey.",
        disabled=True
    )

def display_application_history():
    """Display user's application history"""
    st.markdown("### 📊 Your Application History")
    try:
        applications = get_user_applications(st.session_state.user_id)
        if applications:
            for app in applications:
                with st.expander(f"{app.company_name} - {app.role}"):
                    st.write(f"Status: {app.status}")
                    st.write(f"Applied: {app.created_at.strftime('%Y-%m-%d %H:%M')}")
                    
                    sections = {
                        "Resume Review": app.resume_review,
                        "Cover Letter": app.cover_letter,
                        "Networking Email": app.networking_email
                    }
                    
                    for title, content in sections.items():
                        if content:
                            st.markdown(f"#### {title}")
                            st.write(content)
        else:
            st.info("No applications found. Start applying to see your history here!")
    except Exception as e:
        st.error(f"Error loading application history: {str(e)}")

def main():
    """Main application logic"""
    # Run email prompt first and stop if user is not logged in
    prompt_email()
    if st.session_state.user_email is None:
        st.stop()  # Stops execution to ensure only login/registration prompt is shown

    # Sidebar for logged-in users
    st.sidebar.success(f"Logged in as {st.session_state.user_email}")
    if st.sidebar.button("Logout"):
        st.session_state.user_email = None
        st.session_state.user_id = None
        st.rerun()

    # Main content
    st.title("👋🏻 AI - Smart Applications")
    st.subheader("Your one-stop place for applications help!")
    
    handle_resume_upload()
    display_about()
    display_application_history()

main()

# if __name__ == "__main__":
#     main()
