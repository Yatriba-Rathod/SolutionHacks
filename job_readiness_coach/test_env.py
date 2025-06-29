import streamlit as st
from gemini_api import search_and_generate_jobs, tailor_resume
from job_db import insert_jobs, get_jobs
import PyPDF2

st.title("🚀 Job Readiness Coach")

# === SEARCH & ADD JOBS ===
st.header("🔍 Search & Add Jobs")

role = st.text_input("Enter a job role:")
if st.button("Search & Add Jobs"):
    jobs = search_and_generate_jobs(role)
    st.write("✅ Generated Jobs:", jobs)

    if jobs:
        insert_jobs(jobs)
        st.success("✅ Jobs inserted!")

# === SHOW JOBS IN DB ===
if st.checkbox("Show current jobs in DB"):
    jobs = get_jobs()
    st.write(jobs)

# === TAILOR RESUME ===
st.header("🎯 Tailor My Resume (PDF Upload)")

jobs = get_jobs()
if jobs:
    selected_job = st.selectbox(
        "Select a job to tailor for:",
        jobs,
        format_func=lambda job: job['title']
    )

    uploaded_file = st.file_uploader("Upload your current resume (PDF)", type=["pdf"])

    resume_text = ""
    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text() + "\n"

        st.write("✅ PDF uploaded. Preview of extracted text:")
        st.write(resume_text[:500] + "...")

    if st.button("Tailor Resume"):
        if resume_text.strip() == "":
            st.error("Please upload a PDF with text.")
        else:
            tailored = tailor_resume(selected_job, resume_text)
            st.subheader("📄 Your tailored resume draft:")
            st.write(tailored)

            st.download_button(
                label="Download Tailored Resume",
                data=tailored,
                file_name="tailored_resume.txt",
                mime="text/plain"
            )
else:
    st.info("⚠️ No jobs in DB yet. Please run 'Search & Add Jobs' first!")

    