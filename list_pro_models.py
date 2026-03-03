import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Available Pro models:")
for m in genai.list_models():
  if 'pro' in m.name.lower() and 'generateContent' in m.supported_generation_methods:
    print(m.name)
