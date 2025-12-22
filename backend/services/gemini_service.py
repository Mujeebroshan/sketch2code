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

# Using Gemini 2.0 Flash to avoid daily limits of the 'Preview' models
model = genai.GenerativeModel('gemini-3-flash-preview')

SYSTEM_PROMPT = """You are an expert Tailwind CSS developer. You are strictly forbidden from generating markdown code blocks. You must return a raw HTML string. The HTML must be a single file containing a standard HTML5 boilerplate, a script tag importing Tailwind CSS via CDN, and the body content derived from the image. Use FontAwesome via CDN for icons. Use 'https://placehold.co/600x400' for placeholder images."""

def analyze_image(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    try:
        image_payload = {'mime_type': mime_type, 'data': image_bytes}
        response = model.generate_content([SYSTEM_PROMPT, image_payload])
        generated_code = response.text
        
        # Clean Markdown formatting
        if generated_code.strip().startswith('```html'):
            generated_code = re.sub(r'^```html\s*', '', generated_code.strip())
            generated_code = re.sub(r'\s*```$', '', generated_code)
        elif generated_code.strip().startswith('```'):
            generated_code = re.sub(r'^```\s*', '', generated_code.strip())
            generated_code = re.sub(r'\s*```$', '', generated_code)
        
        return generated_code.strip()
    except Exception as e:
        print(f"Error in analyze_image: {str(e)}")
        raise Exception(f"Failed to generate code: {str(e)}")
    # ... (Keep your existing imports and analyze_image function) ...

REFINE_PROMPT = """
You are an expert Tailwind web developer. 
You will receive existing HTML code and a user instruction.
Your goal is to MODIFY the code exactly as requested.
Rules:
1. Return the FULL updated HTML file (not just the snippet).
2. Do not explain your changes.
3. Do not wrap in markdown code blocks (return raw string).
4. Keep the original structure/libs unless asked to change.
"""

def refine_code(current_code: str, instruction: str) -> str:
    try:
        prompt = f"""
        {REFINE_PROMPT}
        
        CURRENT CODE:
        {current_code}
        
        USER INSTRUCTION:
        {instruction}
        """
        
        response = model.generate_content(prompt)
        generated_code = response.text
        
        # Clean Markdown (Same as before)
        if generated_code.strip().startswith('```html'):
            generated_code = re.sub(r'^```html\s*', '', generated_code.strip())
            generated_code = re.sub(r'\s*```$', '', generated_code)
        elif generated_code.strip().startswith('```'):
            generated_code = re.sub(r'^```\s*', '', generated_code.strip())
            generated_code = re.sub(r'\s*```$', '', generated_code)
            
        return generated_code.strip()
        
    except Exception as e:
        print(f"Error in refine_code: {str(e)}")
        raise Exception(f"Failed to refine code: {str(e)}")