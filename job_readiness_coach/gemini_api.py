import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import re

# Load env + configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash-latest')  # Or pro-latest if you have quota

def search_and_generate_jobs(role):
    prompt = f"""
    You are a career coach. Suggest 5 realistic job roles for '{role}'.
    For each, include the following details in JSON format:
    [
      {{
        "title": "Job Title",
        "description": "Short description.",
        "skills": ["Skill1", "Skill2"]
        "pay_range": "Salary range (e.g. $50,000 - $70,000)"
        "location": "City, Country"
        "company": "Company Name"
        "url": "https://example.com/job-link"
        "date_posted": "YYYY-MM-DD"
        "date_expires": "YYYY-MM-DD"
      }},
      ...
    ]

    Respond ONLY with valid JSON. Do not wrap in code fences or add extra text.
    """

    response = model.generate_content(prompt)
    print("\n🔍 Raw Gemini output:\n", response.text)

    # ✅ Remove ```json ... ``` if present
    cleaned_text = response.text.strip()
    if cleaned_text.startswith("```"):
        cleaned_text = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned_text)
        cleaned_text = re.sub(r"```$", "", cleaned_text).strip()

    print("\n✅ Cleaned text:\n", cleaned_text)

    try:
        jobs_data = json.loads(cleaned_text)
        return jobs_data
    except json.JSONDecodeError:
        print("❌ JSON parse failed! Cleaned text above 👆")
        return []
