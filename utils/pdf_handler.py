# utils/pdf_handler.py
import pdfplumber
import io
import streamlit as st
from typing import Optional, Tuple
from db_utils import save_resume, get_active_resume

class PDFHandler:
    @staticmethod
    def extract_text(file_or_bytes) -> str:
        """Extract text from a PDF file"""
        try:
            if isinstance(file_or_bytes, bytes):
                pdf_file = io.BytesIO(file_or_bytes)
            else:
                pdf_file = file_or_bytes
                
            with pdfplumber.open(pdf_file) as pdf:
                return "\n".join(
                    page.extract_text() for page in pdf.pages 
                    if page.extract_text()
                )
        except Exception as e:
            st.error(f"Error extracting PDF text: {str(e)}")
            return ""

    @staticmethod
    def handle_resume_upload(current_resume: Optional[bytes] = None) -> Tuple[Optional[str], Optional[bytes]]:
        """Handle resume upload and return extracted text and file content"""
        uploaded_file = st.file_uploader(
            "Upload new resume (PDF)", 
            type="pdf",
            help="Upload a PDF to use as your resume"
        )
        
        if uploaded_file:
            try:
                file_content = uploaded_file.read()
                text = PDFHandler.extract_text(io.BytesIO(file_content))
                return text, file_content
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
                return None, None
        return None, None

# components/resume_manager.py
class ResumeManager:
    @staticmethod
    def display_resume_section(user_id: int) -> Optional[str]:
        """Display resume management section and return resume text if available"""
        st.markdown("### 📄 Resume Management")
        current_resume = get_active_resume(user_id)
        resume_text = None

        if current_resume:
            st.success(f"Current active resume: {current_resume.file_name}")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("View Current Resume"):
                    resume_text = PDFHandler.extract_text(current_resume.content)
                    if resume_text:
                        st.text_area("Resume Content", resume_text, height=300, disabled=True)
            
            with col2:
                if st.button("Replace Resume"):
                    st.session_state.replace_resume = True

        if not current_resume or st.session_state.get("replace_resume"):
            text, content = PDFHandler.handle_resume_upload(
                current_resume.content if current_resume else None
            )
            if content:
                save_resume(user_id, content, st.session_state.uploaded_file_name)
                st.success("Resume updated successfully!")
                st.experimental_rerun()
            resume_text = text

        return resume_text

# components/job_form.py
class JobApplicationForm:
    @staticmethod
    def display() -> Tuple[str, str, str]:
        """Display and handle job application form inputs"""
        with st.form("job_application_form"):
            company_name = st.text_input("Company applying to")
            role = st.text_input("Role applying for")
            job_desc = st.text_area("Job Description")
            
            submitted = st.form_submit_button("Submit")
            if submitted and all([company_name, role, job_desc]):
                return company_name, role, job_desc
            elif submitted:
                st.error("Please fill in all fields")
            return None, None, None

# services/ai_service.py
from gemini import get_gemini_response
import time

class AIService:
    @staticmethod
    def generate_content(prompt_template: str, **kwargs) -> str:
        """Generate content using AI with retry logic and rate limiting"""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                prompt = prompt_template.format(**kwargs)
                response = get_gemini_response(prompt)
                return response
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    st.error(f"Failed to generate content: {str(e)}")
                    return None