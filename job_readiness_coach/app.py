# app.py
import streamlit as st
from job_db import get_jobs
from gemini_api import search_and_generate_jobs, tailor_resume

# Any other Streamlit pages go here!
st.title("🎯 Job Readiness Coach")

# Example: show your tailor resume page here or link multiple pages!
