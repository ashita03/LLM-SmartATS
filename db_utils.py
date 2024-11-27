# db_utils.py
import logging
from sqlalchemy.exc import SQLAlchemyError
from db_schema import SessionLocal, User, Resume, Application
import streamlit as st
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_db_operation(operation):
    """Decorator for database operations with comprehensive error handling"""
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            # Log the operation details
            logger.info(f"Attempting database operation: {operation.__name__}")
            logger.info(f"Arguments: {args}, Keyword Arguments: {kwargs}")
            
            result = operation(db, *args, **kwargs)
            
            # Commit only if no exception occurred
            db.commit()
            
            logger.info(f"Operation {operation.__name__} completed successfully")
            return result
        
        except SQLAlchemyError as e:
            # Rollback the transaction
            db.rollback()
            
            # Log detailed error information
            logger.error(f"Database error in {operation.__name__}: {str(e)}")
            logger.error(f"Full exception details:", exc_info=True)
            
            # Display user-friendly error
            st.error(f"A database error occurred: {str(e)}")
            return None
        
        except Exception as e:
            # Catch any other unexpected errors
            db.rollback()
            
            logger.error(f"Unexpected error in {operation.__name__}: {str(e)}")
            logger.error(f"Full exception details:", exc_info=True)
            
            st.error(f"An unexpected error occurred: {str(e)}")
            return None
        
        finally:
            # Always close the session
            db.close()
    
    return wrapper

@handle_db_operation
def get_or_create_user(db, email):
    """Get existing user or create new one with improved error handling"""
    try:
        # Attempt to find existing user
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Create new user if not exists
            user = User(email=email)
            db.add(user)
        
        # Update last login timestamp
        user.last_login = datetime.utcnow()
        
        return user
    
    except Exception as e:
        logger.error(f"Error in get_or_create_user: {str(e)}")
        raise

@handle_db_operation
def save_resume(db, user_email:str, file_content, file_name):
    """Save or update user's resume with comprehensive validation"""
    try:
        # Validate inputs
        if not file_content:
            raise ValueError("File content cannot be empty")
        
        # Deactivate existing active resumes for this user
        existing_resumes = db.query(Resume).filter(
            Resume.user_email == user_email,
            Resume.is_active == True
        ).all()
        
        for resume in existing_resumes:
            resume.is_active = False
        
        # Create new resume entry
        new_resume = Resume(
            user_email=user_email,
            file_name=file_name,
            content=file_content,
            is_active=True
        )
        
        db.add(new_resume)
        
        return new_resume
    
    except Exception as e:
        logger.error(f"Error saving resume: {str(e)}")
        raise

@handle_db_operation
def get_active_resume(db, user_email:str):
    """Get user's current active resume"""
    try:
        # Explicitly refresh the session to ensure it's active
        db.expire_on_commit = False
        
        resume = db.query(Resume).filter(
            Resume.user_email == user_email,
            Resume.is_active == True
        ).first()
        
        return resume
    
    except Exception as e:
        logger.error(f"Error retrieving active resume: {str(e)}")
        raise

@handle_db_operation
def save_application(db, user_email, company_name, role, job_description, 
                    cover_letter=None, networking_email=None, resume_review=None):
    """Save application details with validation"""
    if not all([company_name, role, job_description]):
        raise ValueError("Company name, role, and job description are required")
        
    application = Application(
        user_email=user_email,
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
def get_user_applications(db, user_email):
    """Get all applications for a user with improved session handling"""
    cache_key = f"user_applications_{user_email}"
    
    # Check session state cache first
    if cache_key in st.session_state:
        return st.session_state[cache_key]
    
    # Retrieve applications and explicitly load data before session closes
    applications = db.query(Application).filter(
        Application.user_email == user_email
    ).order_by(Application.created_at.desc()).all()
    
    # Convert to a list of dictionaries to detach from session
    application_dicts = [
        {
            'company_name': app.company_name,
            'role': app.role,
            'status': app.status,
            'created_at': app.created_at,
            'resume_review': app.resume_review,
            'cover_letter': app.cover_letter,
            'networking_email': app.networking_email
        } for app in applications
    ]
    
    # Store in session state
    if application_dicts:
        st.session_state[cache_key] = application_dicts
    
    return application_dicts