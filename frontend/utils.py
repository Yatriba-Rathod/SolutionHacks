def calculate_xp(feedback_text):
    """Crude XP calculator based on sentiment keywords."""
    feedback = feedback_text.lower()
    xp = 10  

    if "great" in feedback or "excellent" in feedback:
        xp += 10
    if "clear" in feedback or "well-written" in feedback:
        xp += 5
    if "creative" in feedback:
        xp += 5
    if "needs improvement" in feedback or "could be better" in feedback:
        xp -= 5

    return max(5, min(xp, 30)) 

def get_task_intro(role, step):
    return f"""
Act like a manager giving task #{step} to a {role}.
Make it realistic, short, and relevant to their responsibilities.
"""
