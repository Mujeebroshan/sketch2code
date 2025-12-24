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

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ API Key NOT Found! Check your .env file.")
else:
    print(f"✅ API Key Loaded: {api_key[:5]}...")

genai.configure(api_key=api_key)

# --- 🛡️ THE POWER-RANKED FALLBACK LIST ---
# Ordered by Intelligence (Smartest -> Fastest)
MODEL_LIST = [
    # Tier 1: The Brainiacs (Complex Logic)
    "gemini-2.5-pro",
    "gemini-3-pro-preview",
    "gemini-exp-1206",
    "gemini-1.5-pro",

    # Tier 2: Heavyweight Open Models
    "gemma-3-27b-it",
    "gemma-3-12b-it",
    
    # Tier 3: Speed & Efficiency
    "gemini-2.5-flash",
    "gemini-3-flash-preview",
    "gemini-1.5-flash",
    "gemini-flash-latest",
    
    # Tier 4: Experimental
    "gemini-2.0-flash-exp",
    "gemini-robotics-er-1.5-preview",
    
    # Tier 5: Safety Net
    "gemini-pro",
    "gemma-3-4b-it"
]

# --- SYSTEM PROMPT ---
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
"""

# --- HELPER FUNCTIONS ---

def clean_code(text):
    """Removes markdown backticks if Gemini adds them."""
    if not text: return ""
    text = re.sub(r'^```html\s*', '', text.strip())
    text = re.sub(r'^```\s*', '', text.strip())
    text = re.sub(r'\s*```$', '', text)
    return text.strip()

def generate_with_fallback(inputs):
    """
    Tries models one by one.
    Returns: Tuple (generated_text, model_name)
    """
    last_error = None
    
    for model_name in MODEL_LIST:
        try:
            print(f"🔄 Trying model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(inputs)
            print(f"✅ Success with {model_name}!")
            
            # ✅ RETURN BOTH TEXT AND MODEL NAME
            return response.text, model_name
            
        except Exception as e:
            print(f"❌ {model_name} Failed.") 
            last_error = e
            continue 
            
    raise Exception(f"All models failed. Last Error: {str(last_error)}")

# --- MAIN FUNCTIONS ---

def analyze_image(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    image_payload = {'mime_type': mime_type, 'data': image_bytes}
    inputs = [SYSTEM_PROMPT, image_payload]
    
    # Get code AND model name
    raw_code, model_used = generate_with_fallback(inputs)
    
    return {
        "code": clean_code(raw_code),
        "model": model_used  # 👈 Sending this back to frontend
    }

def refine_code(current_code: str, instruction: str) -> dict:
    prompt = f"""
    {SYSTEM_PROMPT}
    
    CURRENT CODE:
    {current_code}
    
    USER INSTRUCTION:
    {instruction}
    
    Return the UPDATED full HTML code.
    """
    
    # Get code AND model name
    raw_code, model_used = generate_with_fallback(prompt)
    
    return {
        "code": clean_code(raw_code),
        "model": model_used  # 👈 Sending this back to frontend
    }