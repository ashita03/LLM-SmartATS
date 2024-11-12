from db_schema import SessionLocal, User, Resume, Application
import streamlit as st
from datetime import datetime

def init_session_state():
    """Initialize session state variables"""
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

def get_or_create_user(email):
    """Get existing user or create new one"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(email=email)
            db.add(user)
            db.commit()
            db.refresh(user)
        user.last_login = datetime.utcnow()
        db.commit()
        return user
    finally:
        db.close()

def save_resume(user_id, file_content, file_name):
    """Save or update user's resume"""
    db = SessionLocal()
    try:
        # Deactivate all existing resumes
        existing_resumes = db.query(Resume).filter(
            Resume.user_id == user_id,
            Resume.is_active == True
        ).all()
        for resume in existing_resumes:
            resume.is_active = False
        
        # Create new resume entry
        new_resume = Resume(
            user_id=user_id,
            file_name=file_name,
            content=file_content,
            is_active=True
        )
        db.add(new_resume)
        db.commit()
    finally:
        db.close()

def get_active_resume(user_id):
    """Get user's current active resume"""
    db = SessionLocal()
    try:
        resume = db.query(Resume).filter(
            Resume.user_id == user_id,
            Resume.is_active == True
        ).first()
        return resume
    finally:
        db.close()

def save_application(user_id, company_name, role, job_description, 
                    cover_letter=None, networking_email=None, resume_review=None):
    """Save application details"""
    db = SessionLocal()
    try:
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
        db.commit()
        return application
    finally:
        db.close()

def get_user_applications(user_id):
    """Get all applications for a user"""
    db = SessionLocal()
    try:
        applications = db.query(Application).filter(
            Application.user_id == user_id
        ).order_by(Application.created_at.desc()).all()
        return applications
    finally:
        db.close()
