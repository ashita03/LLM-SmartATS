import os
import google.generativeai as genai
import logging
import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure the Gemini API with the API key from environment variables
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
#genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to get the response from the Gemini model
def get_gemini_response(input_text):
    try:
        model = genai.GenerativeModel('models/gemini-1.5-pro')
        response = model.generate_content(input_text)
        
        # Check if the response is successfully generated
        if not response or not response.text:
            raise ValueError("Empty response from Gemini")
        
        return response.text
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return None

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

Introduction: 
Professional greeting, mention of the role and company, and expression of interest in the position.

Relevant Work Experience and Skills: 
Highlight key skills and experiences from the resume that match the job description, with specific examples or achievements.

Tailored Fit for Role and Company: 
Explain why the applicant is a good fit for the company’s culture and values, and align with the job description.

Closing: 
Thank the reader, express excitement, and suggest next steps.

Context:
Resume: {text}
Company: {company_name}
Role applied for: {role}
Job Description: {jd}
"""

# Prompt Template to generate an email to the hiring manager

input_prompt_networking_email = """Task:
Draft a professional and engaging, short yet crisp email to the hiring manager of the company where the applicant is applying. The email should introduce the applicant, briefly highlight relevant experiences and skills from the resume, and express enthusiasm for the opportunity. The email should be tailored to the role and company, with a subject line that captures the hiring manager's attention. The Email should not be too long and should be engaging in a professional manner

Instructions:
Using the provided resume and job description as context, follow these steps to draft the email:

Subject Line:
Create a concise and engaging subject line that highlights the role the applicant is applying for and a key experience or skill that makes them a strong candidate. The subject line should capture the hiring manager’s attention.

Introduction:
Start with a polite and professional greeting. If the hiring manager’s name is known, address them directly; if not, use a general greeting (e.g., “Dear Hiring Manager”). Mention the role the applicant is applying for and how they came across the opportunity.

Key Experiences and Skills:
Briefly introduce the applicant’s background, highlighting key experiences and skills from the resume that align with the job description. Use specific examples to demonstrate relevant achievements or qualifications that would make the applicant a valuable addition to the company.

Interest in the Company and Role:
Explain why the applicant is particularly excited about the opportunity and why they believe they would be a great fit for the company’s culture and the specific role. Reference the company’s mission, values, or any unique aspects of the job that resonate with the applicant’s goals and experience.

Closing:
End the email by expressing enthusiasm for the next steps, such as discussing the role in more detail or scheduling an interview. Thank the hiring manager for their time and consideration, and provide contact information for follow-up.

Tone:
Keep the tone professional, respectful, and enthusiastic throughout the email. Ensure the email is concise and to the point while making the applicant’s value clear.

Output Structure:

Subject Line:
A subject line that highlights the role applied for and a relevant skill/experience (e.g., “Experienced Software Developer Excited to Apply for [Role] at [Company]”).

Introduction:
Greeting, mention of the role, and how the applicant found the opportunity.

Key Experiences and Skills:
A brief introduction to the applicant’s background, with specific experiences and skills relevant to the role.

Interest in the Company and Role:
Explain why the applicant is excited about this particular role and company, aligning their interests with the company’s values or goals.

Closing:
Expression of enthusiasm for next steps, thank the hiring manager, and provide contact information.

Context:
Resume: {text}
Company: {company_name}
Role applied for: {role}
Job Description: {jd}

"""

# Prompt Template to generate bullet points for resume improvement

input_prompt_resume_bullet_points = """
Task:
Imagine yourself as an expert ATS resume viewer, and go through all of the Resume bullet points to ensure it matches with the key skills and words in the Job Description. You have to make sure that most skills and the most important keywords mentioned in the Job Description are ALL present in the Resume and additionally being highlighted. The main aim is to ensure that the Resume stands out as a Top Applicant for the respective Job Description. In order to achieve this, do not force it. Maintain a good balance. Based on the theme of the job description or the main project, align project points to that. Make sure to use all the keywords and skills at least once.

Instructions:
1. Optimize for ATS Compatibility:
   - Begin each bullet point with strong action verbs (e.g., "Led," "Implemented," "Optimized").
   - Incorporate keywords from the Job Description naturally into the bullet points.
   - Use the APR format (Action + Project/Problem + Result) to effectively showcase the candidate’s impact.
   - Ensure bullet points are concise, clear, and results-driven to be easily parsed by ATS.
   - Avoid complex formatting; use standard symbols (• or -) for bullet points.

2. Quantify Achievements Where Possible:
   - Replace vague descriptions with measurable results (e.g., "Increased efficiency by 30%" instead of "Improved processes").
   - Highlight key contributions such as revenue growth, cost savings, efficiency improvements, or customer satisfaction, based on the Job Description’s focus.
   - Include specific figures, percentages, or timeframes to add credibility to achievements.
   
3. Align with the Job Description:
   - Identify key responsibilities and skills from the JD.
   - Tailor each bullet point to directly reflect the requirements and expectations of the role.
   - Emphasize experiences that demonstrate the candidate’s ability to excel in this position by incorporating relevant keywords and skills from the JD where appropriate.

Output Structure:
For each bullet point in the Work Experience section of the resume, provide an improved version that follows the guidelines above.

Context:
- Resume: {text}
- Company: {company_name}
- Role Applied For: {role}
- Job Description: {jd}

Example Before & After:
- Before: Managed social media accounts for the company.
- After: Increased social media engagement by 25% through a targeted content strategy and active community engagement, driving brand visibility and lead generation."""