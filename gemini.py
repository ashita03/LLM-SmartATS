import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

#Prompt Template to match the resume to the job description

input_prompt_resume_match="""
Hey, act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of tech field. You must keep in mind that the market is extremely competitive, and therefore would require a great resume to match the jd. 
Please evaluate the resume and the description to provide recommendations on how the resume can be improved based on the description, what needs to be added, what percent of the skills match with the description.
Please assign the percentage matching based on Job description and the missing keywords with high accuracy. Please thoroughly go through the description and the resume to match it perfectly and accordingly please provide good recommendations. Please do not add extra keywords that do not align with the role being applied to.

Please only use the resume uploaded and the description provided as a context.

Context:
resume:{text}
description:{jd}

I want the response structured as a conversational output which should include the percentage of match between the resume and the jd, the missing skills based on the jd, and the summary of the profile for the jd
"""

#Prompt Template to get a cover letter

input_prompt_cover_letter_request = """
Hey, imagine yourself as a professional cover letter writer who is working towards helping applicants stand out during job applications. For this you are expected to write a cover letter that highlights the skills relevant from the resume that matches with the description or the jd. Please ensure that the cover letter is professional and is unique so it could stand out

Context: 
resume:{text}
Company: {company_name}
Role applied for: {role}
description:{jd}

Make the cover letter interactive yet professional.
"""
