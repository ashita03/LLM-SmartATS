# utils/pdf_handler.py
import pdfplumber
import io
import streamlit as st
import logging
from typing import Optional, Tuple, Union
from db_utils import save_resume, get_active_resume

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFHandler:
    @staticmethod
    def extract_text(file_or_bytes: Union[bytes, io.BytesIO]) -> str:
        """
        Extract text from a PDF file with robust error handling and logging
        
        Args:
            file_or_bytes (Union[bytes, io.BytesIO]): PDF content to extract text from
        
        Returns:
            str: Extracted text from PDF, empty string if extraction fails
        """
        try:
            # Ensure we have a BytesIO object
            if isinstance(file_or_bytes, bytes):
                pdf_file = io.BytesIO(file_or_bytes)
            else:
                pdf_file = file_or_bytes
            
            with pdfplumber.open(pdf_file) as pdf:
                # Extract text with error checking
                extracted_pages = [
                    page.extract_text() for page in pdf.pages 
                    if page.extract_text() is not None
                ]
                
                # Join non-empty pages
                text = "\n".join(extracted_pages)
                
                if not text:
                    logger.warning("No text extracted from PDF")
                    return ""
                
                return text
        
        except Exception as e:
            logger.error(f"PDF text extraction error: {e}")
            st.error(f"Error extracting PDF text: {str(e)}")
            return ""

    @staticmethod
    def validate_pdf(file_content: bytes) -> bool:
        """
        Validate PDF file content
        
        Args:
            file_content (bytes): PDF file content to validate
        
        Returns:
            bool: True if valid PDF, False otherwise
        """
        try:
            with io.BytesIO(file_content) as pdf_file:
                with pdfplumber.open(pdf_file) as pdf:
                    # Check if PDF has pages
                    return len(pdf.pages) > 0
        except Exception as e:
            logger.error(f"PDF validation error: {e}")
            return False

    @staticmethod
    def handle_resume_upload(current_resume: Optional[bytes] = None) -> Tuple[Optional[str], Optional[bytes]]:
        """
        Handle resume upload with enhanced validation and error handling
        
        Args:
            current_resume (Optional[bytes]): Currently active resume content
        
        Returns:
            Tuple[Optional[str], Optional[bytes]]: Extracted text and file content
        """
        uploaded_file = st.file_uploader(
            "Upload new resume (PDF)", 
            type="pdf",
            help="Upload a PDF to use as your resume. Maximum file size: 10MB"
        )
        
        if uploaded_file:
            try:
                # Validate file size (optional)
                if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
                    st.error("File too large. Maximum file size is 10MB.")
                    return None, None
                
                file_content = uploaded_file.read()
                
                # Validate PDF
                if not PDFHandler.validate_pdf(file_content):
                    st.error("Invalid PDF file. Please upload a valid PDF.")
                    return None, None
                
                # Extract text
                text = PDFHandler.extract_text(io.BytesIO(file_content))
                
                if not text.strip():
                    st.warning("No readable text found in the PDF. Please check the document.")
                    return None, None
                
                # Store filename in session state
                st.session_state['uploaded_file_name'] = uploaded_file.name
                
                return text, file_content
            
            except Exception as e:
                logger.error(f"Resume upload processing error: {e}")
                st.error(f"Error processing PDF: {str(e)}")
                return None, None
        
        return None, None

# components/resume_manager.py
class ResumeManager:
    @staticmethod

    def display_resume_section(user_email: str) -> Optional[str]:
        """
        Display resume management section with comprehensive debugging
        
        Args:
            user_email (str): User's email for resume retrieval
        
        Returns:
            Optional[str]: Extracted resume text
        """
        st.markdown("### 📄 Resume Management")
        
        try:
            # Log entry point
            logger.info(f"Displaying resume section for user: {user_email}")
            
            current_resume = get_active_resume(user_email)
            resume_text = None

            if current_resume:
                # Detailed logging of current resume
                logger.info(f"Current resume found - Filename: {current_resume.file_name}")
                logger.info(f"Resume content size: {len(current_resume.content)} bytes")
                
                st.success(f"Current active resume: {current_resume.file_name}")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("View Current Resume"):
                        # Enhanced text extraction with more detailed logging
                        resume_text = PDFHandler.extract_text(current_resume.content)
                        
                        # Log text extraction results
                        logger.info(f"Resume text extraction result - Length: {len(resume_text)} characters")
                        
                        if resume_text:
                            # Truncate very long text for display
                            display_text = resume_text[:5000] + (
                                "...\n\n[Text truncated for display]" 
                                if len(resume_text) > 5000 else ""
                            )
                            st.text_area("Resume Content", display_text, height=300, disabled=True)
                            
                            # Debug information
                            st.info(f"Total resume text length: {len(resume_text)} characters")
                        else:
                            st.warning("Unable to extract text from current resume")
                            logger.warning("Resume text extraction failed")
                
                with col2:
                    if st.button("Replace Resume"):
                        st.session_state.replace_resume = True

            if not current_resume or st.session_state.get("replace_resume"):
                text, content = PDFHandler.handle_resume_upload(
                    current_resume.content if current_resume else None
                )
                
                # Log upload results
                logger.info(f"Resume upload - Text length: {len(text) if text else 0}")
                logger.info(f"Resume upload - Content size: {len(content) if content else 0} bytes")
                
                if content:
                    try:
                        save_resume(
                            user_email, 
                            content, 
                            st.session_state.get('uploaded_file_name', 'resume.pdf')
                        )
                        st.success("Resume updated successfully!")
                        st.session_state.replace_resume = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to save resume: {e}")
                        logger.error(f"Resume save error: {e}", exc_info=True)
                
                resume_text = text

            # Final logging of resume text
            if resume_text:
                logger.info(f"Final resume text length: {len(resume_text)} characters")
            else:
                logger.warning("No resume text available")

            return resume_text
        
        except Exception as e:
            logger.error(f"Comprehensive resume section error: {e}", exc_info=True)
            st.error("An unexpected error occurred while managing your resume")
            return None
    
# components/job_form.py
class JobApplicationForm:
    @staticmethod
    def display() -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Display and handle job application form inputs with enhanced validation
        
        Returns:
            Tuple[Optional[str], Optional[str], Optional[str]]: Company name, role, job description
        """
        with st.form("job_application_form"):
            st.markdown("### 🏢 Job Application Details")
            
            # Input fields with placeholders and help text
            company_name = st.text_input(
                "Company Name", 
                placeholder="e.g., Google, Microsoft",
                help="Enter the name of the company you're applying to"
            )
            
            role = st.text_input(
                "Job Role", 
                placeholder="e.g., Software Engineer, Data Scientist",
                help="Specify the exact role you're applying for"
            )
            
            job_desc = st.text_area(
                "Job Description", 
                placeholder="Paste the full job description here",
                help="Copy and paste the complete job description from the listing"
            )
            
            submitted = st.form_submit_button("Submit Job Details")
            
            if submitted:
                # Enhanced validation
                errors = []
                if not company_name:
                    errors.append("Company name is required")
                if not role:
                    errors.append("Job role is required")
                if not job_desc:
                    errors.append("Job description is required")
                
                if errors:
                    for error in errors:
                        st.error(error)
                    return None, None, None
                
                return company_name.strip(), role.strip(), job_desc.strip()
            
            return None, None, None

# services/ai_service.py
import time
import streamlit as st
import logging
from typing import Dict, Any, Optional

from gemini import get_gemini_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    @staticmethod
    def generate_content(
        prompt_template: str, 
        **kwargs
    ) -> Optional[str]:
        """
        Generate content using AI with comprehensive error handling and logging
        
        Args:
            prompt_template (str): Template for generating prompt
            **kwargs: Dynamic arguments for prompt formatting
        
        Returns:
            Optional[str]: Generated content or None
        """
        max_retries = 3
        base_retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                # Validate prompt formatting
                try:
                    prompt = prompt_template.format(**kwargs)
                except KeyError as e:
                    logger.error(f"Missing required key for prompt: {e}")
                    st.error(f"Invalid prompt configuration: {e}")
                    return None
                
                # Generate response
                response = get_gemini_response(prompt)
                
                if not response:
                    raise ValueError("Empty response from AI")
                
                return response
            
            except Exception as e:
                logger.error(f"Content generation attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    # Exponential backoff
                    retry_delay = base_retry_delay * (2 ** attempt)
                    time.sleep(retry_delay)
                else:
                    st.error(f"Failed to generate content after {max_retries} attempts")
                    return None