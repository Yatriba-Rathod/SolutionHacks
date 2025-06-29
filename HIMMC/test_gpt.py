import openai
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Correct syntax for v1.0+
client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Hello, what is your name?"}
    ]
)

print(response.choices[0].message.content)
