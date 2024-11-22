import streamlit as st
from db_utils import get_active_resume, save_resume
from gemini import get_gemini_response, input_prompt_resume_match
import pdfplumber
import io


# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def display_resume_options():
    """Display options to view, use, or replace the uploaded resume."""
    st.markdown("### Uploaded Resume")
    current_resume = get_active_resume(st.session_state.user_id)

    input_resume_text = None  # Initialize the resume text variable

    if current_resume:
        st.success(f"Current active resume: {current_resume.file_name}")

        if st.button("View Current Resume"):
            try:
                with pdfplumber.open(io.BytesIO(current_resume.content)) as pdf:
                    pdf_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                    st.text_area("Resume Content", pdf_text, height=300, disabled=True)
                    input_resume_text = pdf_text  # Set input_resume_text to current resume text
            except Exception as e:
                st.error("Error displaying PDF. Please try uploading again.")

        if st.button("Use Existing Resume for Cover Letter"):
            st.session_state.use_existing_resume = True
            st.success("Using the existing resume for cover letter generation.")
            input_resume_text = pdf_text  # Set input_resume_text to current resume text

        if st.button("Replace Resume"):
            st.session_state.replace_resume = True
    else:
        st.info("No resume found. Please upload your resume.")

    # Handle new resume upload or replacement
    if not current_resume or st.session_state.get("replace_resume"):
        uploaded_file = st.file_uploader("Upload new resume (PDF)", type="pdf", help="Upload a PDF to use as your resume")
        
        if uploaded_file:
            try:
                file_content = uploaded_file.read()
                input_resume_text = input_pdf_text(uploaded_file)  # Extract text from the newly uploaded file
                save_resume(st.session_state.user_id, file_content, uploaded_file.name)
                st.success("Resume uploaded successfully and replaced the old one!")
                st.session_state.replace_resume = False
                st.session_state.use_existing_resume = True
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error saving resume: {str(e)}")
    
    return input_resume_text

def resume_review_main():
    #Page information
    st.header("📄 Resume Review")
    # Display resume options and retrieve the extracted text
    input_resume_text = display_resume_options()
    job_desc = st.text_area("Paste the Job Description")
    uploaded_file = st.file_uploader("Please upload your resume in PDF format", type="pdf", help="Please upload the PDF")

    if uploaded_file is not None:
        input_resume_text = input_pdf_text(uploaded_file)  # Extract resume text from uploaded PDF

    submit = st.button("Review")

    if submit:
        if input_resume_text is not None and job_desc:
            # Extract resume text from uploaded PDF
            jd = job_desc
            
            # Create the input for the Gemini prompt by filling in the template
            prompt = input_prompt_resume_match.format(text=input_resume_text, jd=jd)
            
            # Get the response from Gemini model
            response = get_gemini_response(prompt)
            
            # Display the response in the app
            st.subheader("Resume Review Results")
            st.write(response)
            
        else:
            st.error("Please fill in both the Job Description and upload your resume.")
            
resume_review_main()