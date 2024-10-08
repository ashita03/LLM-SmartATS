import streamlit as st
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

from gemini import get_gemini_repsonse, input_prompt_cover_letter_request, input_prompt_resume_match

load_dotenv() ## load all our environment variables

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text


## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
company_name = st.text_area("Company applying to")
role = st.text_area("Role applying for")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Resume Review")

cover = st.button("Write a Cover letter")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt_resume_match)
        st.subheader(response)
        
if cover:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt_cover_letter_request)
        st.subheader(response)