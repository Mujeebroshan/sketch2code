from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import services.gemini_service 

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
             
        # ✅ CALL THE SERVICE
        # Now returns a dictionary: { "code": "...", "model": "gemini-2.5-pro" }
        result = services.gemini_service.analyze_image(content, content_type)
        
        # ✅ RETURN BOTH HTML AND MODEL NAME
        # We map 'code' -> 'html' so your existing frontend keeps working!
        return {
            "html": result["code"], 
            "model": result["model"]
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refine")
async def refine_code_endpoint(
    code: str = Form(...), 
    instruction: str = Form(...)
):
    try:
        # ✅ CALL THE SERVICE
        # Now returns a dictionary: { "code": "...", "model": "..." }
        result = services.gemini_service.refine_code(code, instruction)
        
        # ✅ RETURN BOTH
        return {
            "html": result["code"], 
            "model": result["model"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))