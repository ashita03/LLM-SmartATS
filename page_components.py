# pages/resume_review.py
import streamlit as st
from utils.pdf_handler import ResumeManager, JobApplicationForm, AIService
from gemini import input_prompt_cover_letter_request, input_prompt_networking_email, input_prompt_resume_match
from db_utils import save_application

def resume_review_page():
    st.header("📄 Resume Review")
    
    # Get resume text
    resume_text = ResumeManager.display_resume_section(st.session_state.user_email)
    
    if not resume_text:
        st.warning("Please upload your resume to continue")
        return
    
    # Get job details
    company_name, role, job_desc = JobApplicationForm.display()
    
    if all([company_name, role, job_desc]):
        with st.spinner("Analyzing resume..."):
            review = AIService.generate_content(
                input_prompt_resume_match,
                text=resume_text,
                jd=job_desc
            )
            
            if review:
                st.subheader("Resume Review Results")
                st.write(review)
                
                # Save application
                save_application(
                    st.session_state.user_email,
                    company_name,
                    role,
                    job_desc,
                    resume_review=review
                )

# pages/cover_letter.py
def cover_letter_page():
    st.header("✍🏻 Cover Letter Generator")
    
    # Get resume text
    resume_text = ResumeManager.display_resume_section(st.session_state.user_email)
    
    if not resume_text:
        st.warning("Please upload your resume to continue")
        return
    
    # Get job details
    company_name, role, job_desc = JobApplicationForm.display()
    
    if all([company_name, role, job_desc]):
        with st.spinner("Generating cover letter..."):
            cover_letter = AIService.generate_content(
                input_prompt_cover_letter_request,
                text=resume_text,
                company_name=company_name,
                role=role,
                jd=job_desc
            )
            
            if cover_letter:
                st.subheader("Generated Cover Letter")
                st.write(cover_letter)
                
                # Save application
                save_application(
                    st.session_state.user_email,
                    company_name,
                    role,
                    job_desc,
                    cover_letter=cover_letter
                )

# pages/networking.py
def networking_page():
    st.header("👩‍💻 Networking - Cold Emailing")
    
    # Get resume text
    resume_text = ResumeManager.display_resume_section(st.session_state.user_email)
    
    if not resume_text:
        st.warning("Please upload your resume to continue")
        return
    
    # Get job details
    company_name, role, job_desc = JobApplicationForm.display()
    
    if all([company_name, role, job_desc]):
        with st.spinner("Generating networking email..."):
            email = AIService.generate_content(
                input_prompt_networking_email,
                text=resume_text,
                company_name=company_name,
                role=role,
                jd=job_desc
            )
            
            if email:
                st.subheader("Generated Email")
                st.write(email)
                
                # Save application
                save_application(
                    st.session_state.user_email,
                    company_name,
                    role,
                    job_desc,
                    networking_email=email
                )