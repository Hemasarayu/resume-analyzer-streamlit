import streamlit as st
from resume_parser import extract_resume_data
from job_matcher import match_resume_to_job

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and job description to see how well they match!")

# Upload resume
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Upload job description
job_file = st.file_uploader("Upload Job Description (TXT)", type=["txt"])

if resume_file and job_file:
    with st.spinner("Extracting resume data..."):
        resume_data = extract_resume_data(resume_file)
    
    job_description = job_file.read().decode("utf-8")

    st.subheader("📋 Extracted Resume Info")
    st.json(resume_data)

    with st.spinner("Analyzing match with job description..."):
        match_score, missing_skills = match_resume_to_job(resume_data, job_description)

    st.subheader("📊 Match Score")
    st.success(f"✅ Match Score: {match_score}%")

    if missing_skills:
        st.warning("⚠️ Missing Skills:")
        st.write(", ".join(missing_skills))
