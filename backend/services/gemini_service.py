import google.generativeai as genai
import os
import re
from pathlib import Path
from dotenv import load_dotenv

# --- SETUP ---
# Robustly find the .env file (Goes up one level from 'backend' to root)
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
# Ordered by Intelligence/Capability (Smartest -> Fastest)
# This ensures complex logic (JS sliders, layout) works correctly.
MODEL_LIST = [
    # --- TIER 1: THE BRAINIACS (Highest Reasoning & Coding Ability) ---
    "gemini-2.5-pro",                   # Current Stable Flagship (Best for Code)
    "gemini-3-pro-preview",             # Next-Gen Reasoning
    "gemini-exp-1206",                  # Experimental High-Reasoning Model
    "gemini-1.5-pro",                   # The Reliable Expert (Great Fallback)

    # --- TIER 2: HEAVYWEIGHT OPEN MODELS ---
    "gemma-3-27b-it",                   # Largest Gemma (Very smart)
    "gemma-3-12b-it",                   # Balanced High-Performance
    
    # --- TIER 3: SPEED & EFFICIENCY (Smart but Optimized) ---
    "gemini-2.5-flash",                 # Best "Flash" model currently
    "gemini-3-flash-preview",           # Newest Flash Preview
    "gemini-1.5-flash",                 # Standard Daily Driver
    "gemini-flash-latest",              # Points to the current best Flash
    
    # --- TIER 4: EXPERIMENTAL / SPECIALIZED ---
    "gemini-2.0-flash-exp",             # Experimental Flash
    "gemini-robotics-er-1.5-preview",   # Surprisingly good at logic
    
    # --- TIER 5: SAFETY NET (Legacy) ---
    "gemini-pro",                       # Old 1.0 Pro (If everything else fails)
    "gemma-3-4b-it"                     # Lightweight backup
]

# --- 🧠 SUPERIOR SYSTEM PROMPT (DEPLOY-READY) ---
# Demands working JS, specific CDNs, and no markdown blocks.
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
    """Removes markdown backticks if Gemini adds them."""
    if not text: return ""
    # Remove ```html ... ``` or just ``` ... ```
    text = re.sub(r'^```html\s*', '', text.strip())
    text = re.sub(r'^```\s*', '', text.strip())
    text = re.sub(r'\s*```$', '', text)
    return text.strip()

def generate_with_fallback(inputs):
    """Tries models one by one from MODEL_LIST until one succeeds."""
    last_error = None
    
    for model_name in MODEL_LIST:
        try:
            print(f"🔄 Trying model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(inputs)
            print(f"✅ Success with {model_name}!")
            return response.text
            
        except Exception as e:
            # We catch ALL errors here so the loop never breaks until the end
            # This fixes the "404 Not Found" and "Quota" errors.
            print(f"❌ {model_name} Failed.") 
            last_error = e
            continue 
            
    # If we run out of models
    raise Exception(f"All {len(MODEL_LIST)} models failed. Last Error: {str(last_error)}")

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
    
    Return the UPDATED full HTML code.
    """
    generated_code = generate_with_fallback(prompt)
    return clean_code(generated_code)