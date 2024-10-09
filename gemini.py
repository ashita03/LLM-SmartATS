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
input_prompt_cover_letter_request = input_prompt_cover_letter_request = """
Task:
You are a professional cover letter writer focused on helping job applicants stand out. Based on the provided resume, job description, and company details, write a highly customized cover letter. This letter should highlight the applicant's most relevant skills and experiences, ensuring alignment with the specific job role. Additionally, the letter should reflect enthusiasm for the company and the job opportunity.

Instructions:
Using the resume and job description provided, follow these steps to craft an effective, engaging, and professional cover letter:

### 1. Introduction:
- Start with a professional greeting, ideally addressing the hiring manager if a name is available, or use a general greeting like "Dear Hiring Manager".
- Include the company name and the specific role the candidate is applying for.
- Express enthusiasm for the role and briefly mention why the candidate is interested in this position and the company.

### 2. Relevant Work Experience and Skills:
- Identify key skills and experiences from the resume that closely align with the job description.
- For each key responsibility or requirement in the job description, highlight the applicant's relevant experiences or achievements from the resume.
- Provide specific examples of work experience or achievements where the candidate used these skills, emphasizing measurable outcomes where possible.

### 3. Tailored Fit for the Role and Company:
- Explain why the applicant is a strong fit for the role and the company’s culture.
- Demonstrate knowledge of the company’s mission, products, or values, and how the applicant's background aligns with these aspects.
- Mention how the applicant can contribute to the company’s success and growth.

### 4. Closing:
- End with a professional closing, thanking the hiring manager for their time and consideration.
- Express enthusiasm for the opportunity and mention potential next steps, such as scheduling an interview or a further discussion.

### Tone:
- The tone should be professional, positive, and engaging throughout the letter.
- Make sure the content is personalized and unique to the applicant, the role, and the company.

Output Structure:

**Introduction**: 
Professional greeting, mention of the role and company, and expression of interest in the position.

**Relevant Work Experience and Skills**: 
Highlight key skills and experiences from the resume that match the job description, with specific examples or achievements.

**Tailored Fit for Role and Company**: 
Explain why the applicant is a good fit for the company’s culture and values, and align with the job description.

**Closing**: 
Thank the reader, express excitement, and suggest next steps.

Context:
Resume: {text}
Company: {company_name}
Role applied for: {role}
Job Description: {jd}
"""
