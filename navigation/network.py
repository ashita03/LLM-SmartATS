import streamlit as st
from gemini import get_gemini_response, input_prompt_networking_email
import pdfplumber

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

#Page information
st.header("👩‍💻 Networking - Cold Emailing")

# Input fields
company_name_entry = st.text_area("Company applying to")
role_entry = st.text_area("Role applying for")
job_desc = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Please upload your resume in PDF format", type="pdf", help="Please upload the PDF")

if uploaded_file is not None:
    input_resume_text = input_pdf_text(uploaded_file)  # Extract resume text from uploaded PDF

submit = st.button("Generate Email")

if submit:
    if input_resume_text is not None and company_name_entry and role_entry and job_desc:
        company_name = company_name_entry
        role = role_entry
        jd = job_desc
        
        # Create the input for the Gemini prompt by filling in the template
        prompt = input_prompt_networking_email.format(text=input_resume_text, company_name=company_name, role=role, jd=jd)
        
        # Get the response from Gemini model
        response = get_gemini_response(prompt)
        
        # Display the cover letter in the app
        st.subheader("Generated Email")
        st.write(response)