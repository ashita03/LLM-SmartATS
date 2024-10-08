import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

#Prompt Template to match the resume to the job description

input_prompt_resume_match="""
Hey, act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of tech field, software engineering, data science , data analyst and big data engineer. 
You must keep in mind that the market is extremely competitive, and therefore would require a great resume to match the jd. 
You must evaluate the resume and the job description to provide recommendations on how the resume can be improved based on the jd, what needs to be added, what percent of the skills match with the jd.
Assign the percentage Matching based on Job description and the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response structured as a conversational output which should include the percentage of match between the resume and the jd, the missing skills based on the jd, and the summary of the profile for the jd
"""

#Prompt Template to get a cover letter

input_prompt_cover_letter_request = """
Imagine yourself as a skilled cover letter writer who provides unqiue cover letters for different roles and responsibilities. Based on the jd and resume, write a cover letter which would highlight the skills needed for the role.
resume:{text}
description:{jd}
I want the response to be in a letter format and very professionally formatted. Include work experience and projects from the resume and compare how well it fits the jd.
"""
