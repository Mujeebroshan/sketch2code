import google.generativeai as genai
import os
import re
from pathlib import Path
from dotenv import load_dotenv

# --- SETUP ---
current_file = Path(__file__).resolve()
backend_folder = current_file.parent.parent
env_path = backend_folder / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ API Key NOT Found! Check your .env file.")
else:
    print(f"✅ API Key Loaded: {api_key[:5]}...")

genai.configure(api_key=api_key)

# --- MODEL LIST ---
MODEL_LIST = [
    "gemini-3-flash-preview", 
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-2.5-flash-preview-09-2025",
    "gemma-3-27b-it",
    "gemini-3-pro-preview",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro"
]

# --- SYSTEM PROMPT (DEPLOY-READY MODE) ---
SYSTEM_PROMPT = """
You are an expert Full-Stack Web Developer.
Goal: Convert the design into a SINGLE, DEPLOY-READY HTML file.

CRITICAL RULES:
1. **Single File Output:** Return ONLY the raw HTML code. Do not use markdown backticks.
2. **Structure:** Use a complete HTML5 boilerplate (`<!DOCTYPE html>`).
3. **Styling:** Use Tailwind CSS via CDN: `<script src="https://cdn.tailwindcss.com"></script>`.
4. **Icons:** Use FontAwesome via CDN: `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">`.
5. **Images:** Use 'https://placehold.co/600x400' for placeholders.
6. **INTERACTIVITY (MANDATORY):** - You MUST write actual, working JavaScript inside `<script>` tags at the bottom of the `<body>`.
   - **Mobile Menu:** If there is a navigation bar, implement a working hamburger menu toggle.
   - **Sliders/Carousels:** Write the JS logic to make them slide.
   - **Modals:** Write the JS to open/close them.
   - **Do not use placeholders** like "// add js here". Write the real code.
"""

# --- HELPER FUNCTIONS ---

def clean_code(text):
    """Removes markdown backticks."""
    if not text: return ""
    text = text.strip()
    text = re.sub(r'^```html\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return text.strip()

def generate_with_fallback(inputs):
    """Tries models one by one."""
    last_error = None
    for model_name in MODEL_LIST:
        try:
            print(f"🔄 Trying model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(inputs)
            print(f"✅ Success with {model_name}!")
            return response.text
        except Exception as e:
            last_error = e
            continue 
    raise Exception(f"All models failed. Last Error: {str(last_error)}")

# --- MAIN FUNCTIONS ---

def analyze_image(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    image_payload = {'mime_type': mime_type, 'data': image_bytes}
    inputs = [SYSTEM_PROMPT, image_payload]
    generated_code = generate_with_fallback(inputs)
    return clean_code(generated_code)

def refine_code(current_code: str, instruction: str) -> str:
    prompt = f"""
    {SYSTEM_PROMPT}
    
    CURRENT CODE:
    {current_code}
    
    USER INSTRUCTION:
    {instruction}
    
    Return the FULL UPDATED code.
    """
    generated_code = generate_with_fallback(prompt)
    return clean_code(generated_code)