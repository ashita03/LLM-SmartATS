import streamlit as st
from gemini import get_gemini_response, input_prompt_resume_match
import pdfplumber

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

#Page information
st.header("📄 Resume Review")
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