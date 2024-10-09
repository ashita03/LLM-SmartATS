import os
import google.generativeai as genai

# Configure the Gemini API with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the response from the Gemini model
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Prompt Template to match the resume to the job description
input_prompt_resume_match = """
Task:
You are an experienced ATS (Applicant Tracking System) with a deep understanding of the technology job market. The goal is to evaluate a given resume against a specific job description (JD) and provide actionable feedback. Please ensure that the evaluation is accurate and detailed, as the market is highly competitive and requires an excellent resume to align with the JD.

Instructions:
Using the provided resume and job description as context, follow these steps:

Matching Percentage: Calculate the percentage match between the resume and the job description. This percentage should reflect how closely the resume aligns with the required skills, qualifications, and experience mentioned in the JD.

Missing Skills: Identify the key skills or qualifications mentioned in the JD that are missing or underrepresented in the resume. Focus only on the relevant skills and avoid adding extra keywords or qualifications that do not align with the specific role.

Profile Summary: Provide a brief summary of how well the candidate’s profile fits the job based on the resume. Mention strengths and areas for improvement, focusing on how the candidate can better match the JD.

Recommendations for Improvement: Suggest concrete ways the resume can be improved to increase the match with the JD. This could include rephrasing existing content, adding missing qualifications, or emphasizing certain skills that are currently understated in the resume.

Output Structure:

Matching Percentage:
Provide a percentage that reflects how well the resume matches the JD.

Missing Skills/Qualifications:
List the skills or qualifications required by the JD but missing from the resume.

Profile Summary for the JD:
Write a short summary that explains the strengths of the profile in relation to the JD and areas where it falls short.

Recommendations for Improvement:
Offer concrete suggestions on how the candidate can improve the resume to better align with the JD.

Context:
Resume: {text}
Job Description: {jd}
"""

# Prompt Template to generate a cover letter
input_prompt_cover_letter_request = """
Task:
You are a professional cover letter writer focused on helping job applicants stand out. Based on the provided resume and job description, write a cover letter that highlights the applicant's relevant skills and experiences, ensuring a close alignment with the role. The cover letter should be professional, engaging, and tailored to the company and job position to make the application stand out.

Instructions:
Using the resume and job description provided, follow these steps to craft an effective cover letter:

Introduction: Start with a professional and engaging introduction that addresses the hiring manager (or use a general greeting if the name is unavailable) and expresses the applicant’s excitement about the role and the company. Briefly mention why the applicant is interested in the position.

Key Skills and Experiences:
Identify and highlight the skills, qualifications, and experiences from the resume that closely align with the job description. Ensure the cover letter emphasizes these skills in a way that resonates with the role and company. Use specific examples where possible to demonstrate how the applicant’s experience matches the key responsibilities outlined in the job description.

Tailored Fit for the Role and Company:
Explain why the applicant is a great fit for the company’s culture and the specific role. Demonstrate knowledge of the company’s mission or values and how the applicant’s background aligns with these.

Closing: End with a professional closing, thanking the hiring manager for their time and expressing enthusiasm for the opportunity. Politely suggest next steps, such as scheduling an interview.

Tone:
Ensure the tone is interactive, engaging, and professional throughout the letter, while keeping the content unique to the applicant and the specific role.

Output Structure:

Introduction:
Professional greeting, mention of the role and company, expression of interest.

Key Skills and Experiences:
Highlight key relevant skills from the resume that match the job description, with specific examples or achievements.

Tailored Fit for Role and Company:
Demonstrate why the applicant is a good fit for the company's culture and values, aligning with the job description.

Closing:
Thank the reader, express excitement, and suggest next steps (e.g., interview or further discussion).

Context: 
resume: {text}
Company: {company_name}
Role applied for: {role}
description: {jd}
"""
