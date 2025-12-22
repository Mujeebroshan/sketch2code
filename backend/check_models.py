import google.generativeai as genai
import os
from pathlib import Path
from dotenv import load_dotenv

# Load env safely
current_file = Path(__file__).resolve()
env_path = current_file.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print(f"Checking models for Key starting with: {api_key[:5]}...\n")

try:
    print("--- AVAILABLE MODELS ---")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
    print("------------------------")
except Exception as e:
    print(f"Error: {e}")