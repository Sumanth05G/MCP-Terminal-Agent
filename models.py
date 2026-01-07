# Lists the available models for the api

import google.generativeai as genai

genai.configure(api_key="Gemini API")

print("Fetching available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")