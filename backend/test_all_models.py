import google.generativeai as genai
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Load API Key
current_file = Path(__file__).resolve()
env_path = current_file.parent / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print(f"🕵️  Deep Scanning all models for Key ending in ...{api_key[-5:]}")
print("--------------------------------------------------")

working_models = []

try:
    # Get all models
    all_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    for m in all_models:
        model_name = m.name.replace("models/", "")
        print(f"👉 Testing: {model_name.ljust(30)}", end="")
        
        try:
            # Try to generate actual content
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello")
            
            if response.text:
                print("✅ WORKS!")
                working_models.append(model_name)
        except Exception as e:
            if "429" in str(e):
                print("❌ Quota Full (429)")
            elif "404" in str(e):
                print("❌ Not Found (404)")
            else:
                print(f"❌ Error")
        
        # Brief pause to avoid triggering spam filters
        time.sleep(1)

    print("\n--------------------------------------------------")
    if working_models:
        print(f"🎉 FOUND {len(working_models)} WORKING MODELS:")
        for wm in working_models:
            print(f"   model = genai.GenerativeModel('{wm}')")
    else:
        print("⛔ NO MODELS WORKING. You must create a new API Key with a different Google Account.")

except Exception as e:
    print(f"Critical Error: {e}")