from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import services.gemini_service # <--- You imported the MODULE here

app = FastAPI()

# Allow connections from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_code(file: UploadFile = File(...)):
    try:
        content = await file.read()
        content_type = file.content_type
        
        if not content_type.startswith("image/"):
             raise HTTPException(status_code=400, detail="Invalid file type.")
             
        # --- FIX IS HERE ---
        # We must use 'services.gemini_service.' before the function name
        generated_html = services.gemini_service.analyze_image(content, content_type)
        
        return {"html": generated_html}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refine")
async def refine_code_endpoint(
    code: str = Form(...), 
    instruction: str = Form(...)
):
    try:
        # This one was already correct!
        updated_html = services.gemini_service.refine_code(code, instruction)
        return {"html": updated_html}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))