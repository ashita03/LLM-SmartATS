import streamlit as st
import logging
from utils.pdf_handler import ResumeManager, JobApplicationForm, AIService
from gemini import (
    input_prompt_cover_letter_request, 
    input_prompt_networking_email, 
    input_prompt_resume_match
)
from db_utils import save_application

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_inputs(resume_text, company_name, role, job_desc):
    """Validate input parameters before processing"""
    if not resume_text:
        st.warning("Please upload your resume to continue")
        return False
    
    if not all([company_name, role, job_desc]):
        st.warning("Please provide complete job details")
        return False
    
    return True

def process_application(generator_func, prompt_template, save_key):
    """Generic function to process job application tasks"""
    try:
        resume_text = ResumeManager.display_resume_section(st.session_state.user_email)
        company_name, role, job_desc = JobApplicationForm.display()
        
        if not validate_inputs(resume_text, company_name, role, job_desc):
            return
        
        with st.spinner(f"Processing {save_key.replace('_', ' ').title()}..."):
            result = AIService.generate_content(
                prompt_template,
                text=resume_text,
                company_name=company_name,
                role=role,
                jd=job_desc
            )
            
            if result:
                st.subheader(f"Generated {save_key.replace('_', ' ').title()}")
                st.write(result)
                
                # Dynamically save application based on the task
                save_application(
                    st.session_state.user_email,
                    company_name,
                    role,
                    job_desc,
                    **{save_key: result}
                )
    
    except Exception as e:
        logger.error(f"Error in {save_key} processing: {e}")
        st.error(f"An error occurred while processing {save_key}")

def resume_review_page():
    st.header("📄 Resume Review")
    process_application(
        AIService.generate_content, 
        input_prompt_resume_match, 
        'resume_review'
    )

def cover_letter_page():
    st.header("✍🏻 Cover Letter Generator")
    process_application(
        AIService.generate_content, 
        input_prompt_cover_letter_request, 
        'cover_letter'
    )

def networking_page():
    st.header("👩‍💻 Networking - Cold Emailing")
    process_application(
        AIService.generate_content, 
        input_prompt_networking_email, 
        'networking_email'
    )