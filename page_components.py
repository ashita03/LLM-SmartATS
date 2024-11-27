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

def process_application(generator_func, prompt_template, save_key):
    """Generic function to process job application tasks with enhanced logging"""
    try:
        # Explicit logging of method entry
        logger.info(f"Starting process_application for {save_key}")
        
        resume_text = ResumeManager.display_resume_section(st.session_state.user_email)
        logger.info(f"Resume text length: {len(resume_text) if resume_text else 0}")
        
        company_name, role, job_desc = JobApplicationForm.display()
        
        # Detailed logging of inputs
        logger.info(f"Job Details - Company: {company_name}, Role: {role}")
        logger.info(f"Job Description length: {len(job_desc) if job_desc else 0}")
        
        if not validate_inputs(resume_text, company_name, role, job_desc):
            logger.warning("Input validation failed")
            return
        
        with st.spinner(f"Processing {save_key.replace('_', ' ').title()}..."):
            # Pass debug parameter to help trace generation
            result = AIService.generate_content(
                prompt_template,
                text=resume_text,
                company_name=company_name,
                role=role,
                jd=job_desc,
                _debug=True  # Additional debugging flag
            )
            
            logger.info(f"Generation result for {save_key}: {bool(result)}")
            
            if result:
                st.subheader(f"Generated {save_key.replace('_', ' ').title()}")
                st.write(result)
                
                # Log before saving application
                logger.info(f"Saving application for {save_key}")
                
                save_application(
                    st.session_state.user_email,
                    company_name,
                    role,
                    job_desc,
                    **{save_key: result}
                )
            else:
                st.error(f"No result generated for {save_key}. Please check your inputs or try again.")
                logger.error(f"Content generation failed for {save_key}")
    
    except Exception as e:
        logger.error(f"Detailed error in {save_key} processing: {e}", exc_info=True)
        st.error(f"An error occurred while processing {save_key}: {str(e)}")
        st.exception(e)  # This will show the full traceback

def validate_inputs(resume_text, company_name, role, job_desc):
    """Enhanced input validation with detailed logging"""
    logger.info("Validating application inputs")
    
    # Detailed input checks with specific warnings
    # if not resume_text:
    #     st.warning("⚠️ No resume text found. Please upload a resume first.")
    #     logger.warning(" ⚠️ Resume text is empty")
    #     return False
    
    if not company_name:
        st.warning("⚠️ Company name is required")
        return False
    
    if not role:
        st.warning("⚠️ Job role is required")
        return False
    
    if not job_desc:
        st.warning("⚠️ Job description is required")
        return False
    
    logger.info("All inputs validated successfully")
    return True

def resume_review_page():
    st.header("📑 Resume Review")
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