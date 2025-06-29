import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

def generate_task(company, role):
    prompt = (
        f"You are a manager at {company}. Generate a realistic work email assigning a new task to a {role}. "
        "The email should include a subject line, greeting, context, detailed instructions, expected deliverables, and a sign-off. "
        "Make the email sound professional, with proper formatting. Do not include attachments unless explicitly asked."
    )
    response = model.generate_content(prompt)
    return response.text

def generate_feedback(user_response, task_email):
    prompt = (
        f"Here is a task email:\n\n{task_email}\n\n"
        f"Here is the employee's response:\n\n{user_response}\n\n"
        "Please provide structured, constructive feedback. Mention strengths, weaknesses, and a suggested XP score out of 100."
    )
    response = model.generate_content(prompt)
    return response.text

def generate_job_postings(role, location, filters=None, pay_range=None):
    filter_text = ""
    if filters:
        if isinstance(filters, list):
            filter_text = ", ".join(filters)
        elif isinstance(filters, dict):
            filter_text = ", ".join([key for key, value in filters.items() if value])

    prompt = (
        f"Generate a JSON array of 5 job postings for the role '{role}' in {location}. "
        f"Each job must include: title, location, pay, description, apply_url, "
        f"date_posted, last_date_to_apply. "
        f"{'Apply filters: ' + filter_text + '.' if filter_text else ''} "
        f"{'Pay range: ' + pay_range + '.' if pay_range else ''} "
        "Respond with valid JSON only. No markdown, no explanation. For the apply_url, make sure the url is real. no exmaple url otherwise do not return the job."
    )

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Remove markdown block if present
        if raw.startswith("```"):
            raw = "\n".join(line for line in raw.splitlines() if not line.strip().startswith("```"))

        print("Cleaned Gemini output:\n", raw)

        try:
            jobs = json.loads(raw)
            return jobs if isinstance(jobs, list) else []
        except json.JSONDecodeError:
            print("Failed to parse cleaned output as JSON.")
            return []
    except Exception as e:
        print("Gemini API job generation error:", e)
        return []

