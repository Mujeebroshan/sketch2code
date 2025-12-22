import google.generativeai as genai
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Load your API Key
current_file = Path(__file__).resolve()
env_path = current_file.parent / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print(f"🔎 Testing models with Key: {api_key[:5]}...\n")

# Get all models that support generating content
all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

working_model = None

for model_name in all_models:
    # Clean the name (remove 'models/' prefix if present)
    clean_name = model_name.replace("models/", "")
    print(f"👉 Testing: {clean_name}...", end=" ")
    
    try:
        # Try a tiny request
        model = genai.GenerativeModel(clean_name)
        response = model.generate_content("Hi")
        
        if response.text:
            print("✅ WORKS!")
            working_model = clean_name
            break # Stop at the first working one
            
    except Exception as e:
        if "429" in str(e):
            print("❌ Rate Limited (429)")
        elif "404" in str(e):
            print("❌ Not Found (404)")
        else:
            print(f"❌ Error: {str(e)[:50]}...")
            
    # Small pause to be nice to the API
    time.sleep(1)

print("\n------------------------------------------------")
if working_model:
    print(f"🎉 FOUND WORKING MODEL: '{working_model}'")
    print(f"PLEASE UPDATE gemini_service.py TO USE THIS NAME.")
else:
    print("❌ No working models found. Your IP or Key might be temporarily blocked.")
print("------------------------------------------------")