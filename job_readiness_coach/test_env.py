from gemini_api import search_and_generate_jobs
from job_db import insert_jobs, get_jobs

role = input("What job role do you want? ")

jobs = search_and_generate_jobs(role)
print("Generated jobs:", jobs)

if jobs:
    insert_jobs(jobs)
    print("✅ Jobs inserted!")

print("\nCurrent jobs in DB:")
print(get_jobs())
