import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey, act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of tech field, software engineering, data science , data analyst and big data engineer. 
You must keep in mind that the market is extremely competitive, and therefore would require a great resume to match the jd. 
You must evaluate the resume and the job description to provide recommendations on how the resume can be improved based on the jd, what needs to be added, what percent of the skills match with the jd.
Assign the percentage Matching based on Job description and the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response structured as a conversational output which should include the percentage of match between the resume and the jd, the missing skills based on the jd, and the summary of the profile for the jd
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)