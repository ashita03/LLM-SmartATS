import streamlit as st
from dotenv import load_dotenv
import json
from gemini import get_gemini_response, input_prompt_cover_letter_request, input_prompt_resume_match
import pdfplumber


# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Load environment variables
load_dotenv()

# Streamlit App
st.title("👋🏻 Smart Applications ")
st.subheader("Your one stop place for applications help!")
st.info("Use this page to upload your resume, company and the respective role being applied to, the job description. Based on these, you can choose whether you would you to get a 'Resume Review' or a 'Cover Letter'", icon="ℹ️",)

# Input fields
company_name_entry = st.text_area("Company applying to")
role_entry = st.text_area("Role applying for")
job_desc = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

# Buttons
submit = st.button("Resume Review")
cover = st.button("Write a Cover letter")

# When 'Resume Review' button is pressed
if submit:
    if uploaded_file is not None and job_desc:
        text = input_pdf_text(uploaded_file)  # Extract resume text from uploaded PDF
        jd = job_desc
        
        # Create the input for the Gemini prompt by filling in the template
        prompt = input_prompt_resume_match.format(text=text, jd=jd)
        
        # Get the response from Gemini model
        response = get_gemini_response(prompt)
        
        # Display the response in the app
        st.subheader("Resume Review Results")
        st.write(response)

# When 'Write a Cover letter' button is pressed
if cover:
    if uploaded_file is not None and company_name_entry and role_entry and job_desc:
        text = input_pdf_text(uploaded_file)  # Extract resume text from uploaded PDF
        company_name = company_name_entry
        role = role_entry
        jd = job_desc
        
        # Create the input for the Gemini prompt by filling in the template
        prompt = input_prompt_cover_letter_request.format(text=text, company_name=company_name, role=role, jd=jd)
        
        # Get the response from Gemini model
        response = get_gemini_response(prompt)
        
        # Display the cover letter in the app
        st.subheader("Generated Cover Letter")
        st.write(response)
