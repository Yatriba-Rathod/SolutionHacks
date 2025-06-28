def get_intro_prompt(role, step):
    return f"""
You are simulating a manager assigning a task to a junior {role}.
This is task #{step} at the beginning of their day.
Give a clear, realistic, and useful task that requires creativity or practical effort.
Do not mention it's a simulation.
"""

def get_next_task_prompt(role, step, previous_answer):
    return f"""
You're acting as a {role} manager supervising a junior employee.

Their previous response was:
\"\"\"{previous_answer}\"\"\"

Now create task #{step} based on their progress so far. 
Make sure the next task builds on or complements what they just did.
Keep it short, action-oriented, and job-relevant.
"""

def get_feedback_prompt(user_response, role, file=None):
    file_note = ""
    if file:
        file_note = f" The user also uploaded a file named '{file.name}'. Consider that in your feedback."

    return f"""
You're a senior {role} reviewing the work of a junior teammate.

Here is their submission:
\"\"\"{user_response}\"\"\"
{file_note}

Give helpful, honest feedback in 3-4 sentences. Be specific and supportive.
End with one clear improvement tip.
Do not summarize the task; focus on evaluating the work.
"""
