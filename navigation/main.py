import streamlit as st
from dotenv import load_dotenv


# Load environment variables
load_dotenv() 

# Streamlit App
st.title("👋🏻 Smart Applications ")
st.subheader("Your one stop place for applications help!")
st.info("Use this page to upload your resume, company and the respective role being applied to, the job description. Based on these, you can choose whether you would you to get a 'Resume Review' or a 'Cover Letter'", icon="ℹ️",)

st.markdown("### 🎯 About")
st.text_area(
             " Purpose of the application",
             "The main aim of this product is to support students in ensuring their application is to up to the mark in this competitive market. The product provides multiple AI generated features that could support the student in the entire journey.")

st.markdown("### ⏯️ How to Use")
st.text_area("There are navigation pages to the left wherein you can choose what feature you would like to access.",
        "Upload your resume at the bottom so the app can use it across different features and choose the service you are interested in")

st.markdown("### Features Available ")
st.markdown("""
            - Resume Review: This feature helps you assess your resume against a specific job description. It provides you with a detailed score and actionable feedback.
            - Resume Analysis: This feature analyzes your resume to identify any potential areas for improvement.
            - Cover Letter Generator: This feature generates a cover letter based on your resume and the company you are applying to. It includes the company name, role, and job description.
            - Networking: This feature provides you with a well-drafted email to shoot to the hiring manager
            """)


    