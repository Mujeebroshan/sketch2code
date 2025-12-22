import google.generativeai as genai
import os
import re
from pathlib import Path
from dotenv import load_dotenv

# --- BULLETPROOF ENV LOADING ---
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

# --- THE ULTIMATE FALLBACK LIST ---
# Strategy:
# 1. Tier A: PROVEN WORKING MODELS (✅) - Try these first for instant success.
# 2. Tier B: HIGH POWER MODELS (❌) - Currently quota full, but great backups if they reset.
# 3. Tier C: EXPERIMENTAL / SPECIALIZED - Good last resorts.
# 4. Tier D: LEGACY SAFETY NET - Old reliable models guaranteed to exist.

MODEL_LIST = [
    # --- TIER A: WORKING NOW (✅) ---
    "gemini-3-flash-preview",          # Newest Working Flash
    "gemini-2.5-flash",                # Stable 2.5
    "gemini-flash-latest",             # Standard Alias
    "gemini-2.5-flash-preview-09-2025",# Specific Version
    
    # Gemma Models (Open Weights - Often separate quotas!)
    "gemma-3-27b-it",                  # Smartest Gemma
    "gemma-3-12b-it",                  # Balanced Gemma
    "gemma-3-4b-it",                   # Fast Gemma
    "gemma-3-1b-it",                   # Ultra-Fast Gemma
    "gemma-3n-e4b-it",                 # Nano Gemma
    
    # Specialized Working
    "gemini-robotics-er-1.5-preview",  # Unexpectedly working!
    
    # --- TIER B: QUOTA FULL BUT POWERFUL (❌) ---
    "gemini-3-pro-preview",            # Gemini 3 Pro
    "gemini-2.5-pro",                  # Gemini 2.5 Pro
    "gemini-2.0-flash-exp",            # 2.0 Experimental
    "gemini-2.0-flash",                # 2.0 Flash Standard
    "gemini-exp-1206",                 # December Experiment
    
    # --- TIER C: FLASH LITE & OTHERS (❌) ---
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite-preview-02-05",
    "gemini-flash-lite-latest",
    
    # --- TIER D: SAFETY NET (The Classics) ---
    "gemini-1.5-flash",                # Old Reliable
    "gemini-1.5-pro",                  # Old Intelligence
    "gemini-pro"                       # Legacy 1.0 (Ultimate Backup)
]

SYSTEM_PROMPT = """You are an expert Tailwind CSS developer. You are strictly forbidden from generating markdown code blocks. You must return a raw HTML string. The HTML must be a single file containing a standard HTML5 boilerplate, a script tag importing Tailwind CSS via CDN, and the body content derived from the image. Use FontAwesome via CDN for icons. Use 'https://placehold.co/600x400' for placeholder images."""

# --- HELPER FUNCTIONS ---

def clean_code(text):
    """Removes markdown backticks if Gemini adds them."""
    if not text: return ""
    if text.strip().startswith('```html'):
        text = re.sub(r'^```html\s*', '', text.strip())
        text = re.sub(r'\s*```$', '', text)
    elif text.strip().startswith('```'):
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
            
            # Generate content
            response = model.generate_content(inputs)
            
            print(f"✅ Success with {model_name}!")
            return response.text
            
        except Exception as e:
            # We catch ALL errors here so the loop never breaks until the end
            error_msg = str(e)
            print(f"❌ {model_name} Failed: {error_msg[:100]}...") 
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