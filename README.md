# Smart Applications - using Google Gemini

Smart Applications is a Streamlit-based web application designed to help job seekers improve their resumes, generate professional cover letters using AI and draft emails to get their profiles noticed. This project allows users to upload resumes and receive actionable feedback for resume improvement or generate a customized cover letter for specific job applications or generate email that can be shot to anybody in the company you are looking to apply to.

## Features

* 📄 Resume Review: Upload a PDF resume and receive AI-based feedback on how to improve it.
* ✍🏻 Cover Letter Generator: Automatically generate a customized cover letter tailored to a specific job description.
* 👩‍💻 Networking (Email Generator): Drafts an email that elaborates skills and experience relevant to the role applying to. This can be used to reach out to recruiters or other organization members.
* 🔄 Multipage App: Navigate between different features (Resume Review, Cover Letter Generator) easily using the sidebar.
* 🛠 AI-Powered: Uses state-of-the-art AI to analyze resumes and generate cover letters.

## Tech Stack

* Python: Programming language
* Streamlit: Web application framework
* Google's Gemini AI: AI models for generating content (requires API key)

## Usage

#### Resume Review:

* Navigate to "Resume Review" in the sidebar.
* Upload your resume (PDF format).
* The app will extract the text from your resume and provide feedback on how to improve it.

#### Cover Letter Generator:

* Navigate to "Cover Letter" in the sidebar.
* Enter the company name, the role you’re applying for, and paste the job description.
* Upload a new resume (PDF format) or use the previous one
* The app will generate a professional cover letter based on the input provided.

#### Cold Email drafting:

* Choose 'Networking' and provide the necessary details as the app requests.
* As an output of this feature, you'll have an email drafted per the job description, role, and company applied to with alignement to your work experience

## Application Link
https://llm-smartats.streamlit.app/

## Application Interface
![App main page](images/LLM-SmartATS-Screenshot.png)

