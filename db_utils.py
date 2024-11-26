# db_utils.py
from db_schema import SessionLocal, User, Resume, Application
import streamlit as st
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_db_operation(operation):
    """Decorator for database operations with error handling"""
    def wrapper(*args, **kwargs):
        db = SessionLocal(expire_on_commit=False)
        try:
            result = operation(db, *args, **kwargs)
            db.commit()
            return result
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error in {operation.__name__}: {str(e)}")
            st.error("An error occurred while processing your request. Please try again.")
            return None
        finally:
            db.close()
    return wrapper

@handle_db_operation
def get_or_create_user(db, email):
    """Get existing user or create new one with error handling"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email)
        db.add(user)
    user.last_login = datetime.utcnow()
    return user

@handle_db_operation
def save_resume(db, user_id, file_content, file_name):
    """Save or update user's resume with validation"""
    if not file_content:
        raise ValueError("File content cannot be empty")
    
    # Deactivate existing resumes
    existing_resumes = db.query(Resume).filter(
        Resume.user_id == user_id,
        Resume.is_active == True
    ).all()
    for resume in existing_resumes:
        resume.is_active = False
    
    new_resume = Resume(
        user_id=user_id,
        file_name=file_name,
        content=file_content,
        is_active=True
    )
    db.add(new_resume)
    return new_resume

@handle_db_operation
def get_active_resume(db, user_id):
    """Get user's current active resume with caching"""
    cache_key = f"active_resume_{user_id}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]
        
    resume = db.query(Resume).filter(
        Resume.user_id == user_id,
        Resume.is_active == True
    ).first()
    
    if resume:
        st.session_state[cache_key] = resume
    return resume

@handle_db_operation
def save_application(db, user_id, company_name, role, job_description, 
                    cover_letter=None, networking_email=None, resume_review=None):
    """Save application details with validation"""
    if not all([company_name, role, job_description]):
        raise ValueError("Company name, role, and job description are required")
        
    application = Application(
        user_id=user_id,
        company_name=company_name,
        role=role,
        job_description=job_description,
        cover_letter=cover_letter,
        networking_email=networking_email,
        resume_review=resume_review,
        status='Created'
    )
    db.add(application)
    return application

@handle_db_operation
def get_user_applications(db, user_id):
    """Get all applications for a user with caching"""
    cache_key = f"user_applications_{user_id}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]
        
    applications = db.query(Application).filter(
        Application.user_id == user_id
    ).order_by(Application.created_at.desc()).all()
    
    if applications:
        st.session_state[cache_key] = applications
    return applications