import google.generativeai as genai

# Set your API key
genai.configure(api_key="AIzaSyAPmbij4xd4EUpa0dxIj4CTkqj3jRtRWME")

# Use a valid model name from the list you saw earlier
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Generate content
try:
    response = model.generate_content("Say hello in a funny way!")
    print("✅ Success! Gemini says:")
    print(response.text)
except Exception as e:
    print("❌ Error occurred:")
    print(e)
