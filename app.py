import streamlit as st
from pdfextractor import text_extractor
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# First lets configure the model
gemini_api_key = os.getenv('Google_API_Key1')
model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    api_key = gemini_api_key,
    temperature = 0.9
)




# Lets create the sidebar to upload the resume

st.sidebar.title(':red[UPLOAD YOUR RESUME(ONLY PDF)]')
file = st.sidebar.file_uploader('Resume',type=['pdf'])
if file:
    file_text = text_extractor(file)
    st.sidebar.success('FILE UPLOADED SUCCESSFULLY')

# Lets create the main page of the Application

st.title(':orange[SKILLMATCH :-] :rainbow[AI Assisted Skill Matching Tool]')
st.markdown('### :green[This Application will match and analyze your resume and the Job Description that you have Provided]')
tips = '''
Follow these steps :-
1. Upload your resume (PDF only) in side bar.
2. Copy and Paste the Job Description below.
3. Click on Submit to run the Application.
'''

st.info(tips)

job_desc = st.text_area(':red[Copy and paste your JOB DESCRIPTION here.]',max_chars=10000)

if st.button('SUBMIT'):
    with st.spinner('Processing....'):
        prompt = f'''
        <Role> You are an expert in analysing resume and matching it with  job description. Also you have an experience in data science and generative aI for about 15+ years
        <Goal> Match the resume and the Job description provided by the applicant
        <Context> The following content has been provided by the applicant
        * Resume : {file_text}
        * Job Description : {job_desc}
        <Format>  The report should follow these steps : 
        * Give a breif description of the applicant in 3-5 lines.
        * Describe in percentage what our the chances of this Resume of getting selected.
        * Need not to be exact percentage, your can give interval of percentage based close approximation. 
        * Give the expected ATS score along witht the list of matching an dnon matching keywords
        * Perform SWAT Analysis and explain each parameter, that is, Strength , Weakness, Opportunity and Threat.
        * Give what all Sections in the current resume that are required to be changed in order to improve the ATS Score and selection percentage.
        * Show both current vesion and improve version of the section in resume with proper clarity and easy to be accessible
        * Create two sample resume which can maximize the ats score and selection percentage and make the resume stand out from others
        <Instructions> 
        * Use bullet points for explanantion where ever possible.
        * Create tables for description where ever required
        * strictly do not add any new skill in sample resume.
        * the format of sample resumes must be according to the current market requirement. the format should be in such a way that it can be copy-pasted directly in word file.


        '''
        response = model.invoke(prompt)
        st.write(response.content)
