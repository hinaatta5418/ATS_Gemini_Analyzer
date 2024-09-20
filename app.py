from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PyPDF2 import PdfReader  # Importing PdfReader for reading PDF text
import google.generativeai as genai

# Configure the generative model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to interact with Gemini model
def get_gemini_response(input_text, pdf_text, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_text, prompt])
    return response.text  # Ensure it returns response as text

# Function to extract text from uploaded PDF
def pdf_input_setup(uploaded_file):
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        pdf_text = ""
        
        # Extract text from all pages of the PDF
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
        
        return pdf_text
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit interface setup
st.set_page_config(page_title='ATS RESUME EXPERT')
st.header('ATS TRACKING SYSTEM')

# Text input for job description
input_text = st.text_area('Job Description:', key='input')

# File uploader for PDF
uploaded_file = st.file_uploader("Upload your Resume (PDF format)", type=['pdf'])

# Submit buttons
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

# Input prompts for the generative model
input_prompt1 = """
You are an experienced Technical Human Resource Manager with expertise in evaluating candidates across diverse industries. Your task is to review the provided resume and compare it to the specified job description, assessing the candidate's qualifications, experience, and skills. 
Please provide a detailed evaluation addressing the following points:
1. How well the candidate's experience, education, and skills align with the job requirements.
2. Key strengths and standout qualifications that make the candidate suitable for the role.
3. Any gaps or areas where the candidate does not fully meet the job criteria.
4. Additional observations that may impact the hiring decision, such as certifications, projects, or soft skills.
Conclude by giving an overall assessment on whether the candidate is a strong match for the role, and provide any recommendations for improvement if applicable.
"""

input_prompt3 = """
You are an advanced Applicant Tracking System (ATS) scanner with expertise in analyzing resumes against job descriptions for various roles. Your task is to assess the resume based on the provided job description. Perform a detailed evaluation and provide the following outputs:
1. **Match Percentage:** Calculate how well the resume matches the job description based on keywords, skills, and qualifications.
2. **Missing Keywords:** List any critical keywords, skills, or qualifications from the job description that are missing from the resume.
3. **Final Thoughts:** Provide an overall summary of the candidate’s suitability for the role. Highlight any areas where the resume excels or lacks in comparison to the job requirements, and suggest any improvements that could increase the match percentage.
Ensure your evaluation is adaptable to different industries, roles, and technical or non-technical job descriptions.
"""

# Logic for submitting the form
if submit1:
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        pdf_text = pdf_input_setup(uploaded_file)
        # Get response from Gemini model
        response = get_gemini_response(input_text, pdf_text, input_prompt1)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        pdf_text = pdf_input_setup(uploaded_file)
        # Get response from Gemini model
        response = get_gemini_response(input_text, pdf_text, input_prompt3)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
