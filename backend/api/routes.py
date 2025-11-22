from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
import shutil
import os
import json
from app.translation_agents import TranslationPipeline
from app.file_handlers import FileHandler

router = APIRouter()

# Directory for temporary files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

from fastapi.responses import StreamingResponse

@router.post("/translate")
async def translate_file(
    file: UploadFile = File(...),
    glossary_file: UploadFile = File(None),
    source_lang: str = Form(...),
    target_lang: str = Form(...),
    translation_type: str = Form(...),
    brief: str = Form(""),
    api_key: str = Form(...),
    provider: str = Form(...),
    model: str = Form(...),
    temperature: float = Form(0.7),
    output_format: str = Form("docx"),
    # Advanced mode temperatures (optional)
    temp_literary: Optional[float] = Form(None),
    temp_legal: Optional[float] = Form(None),
    temp_technical: Optional[float] = Form(None),
    temp_medical: Optional[float] = Form(None),
    temp_news: Optional[float] = Form(None),
    temp_academic: Optional[float] = Form(None),
    temp_marketing: Optional[float] = Form(None),
    temp_business: Optional[float] = Form(None),
    temp_master: Optional[float] = Form(None),
):
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process glossary if provided
        glossary = None
        if glossary_file:
            glossary_path = os.path.join(UPLOAD_DIR, glossary_file.filename)
            with open(glossary_path, "wb") as buffer:
                shutil.copyfileobj(glossary_file.file, buffer)
            
            file_handler = FileHandler()
            try:
                glossary = file_handler.parse_glossary(glossary_path)
            except Exception as e:
                print(f"Error parsing glossary: {e}")
                # Continue without glossary if parsing fails, but maybe log it
                pass

        # Prepare temperature dict
        temperatures = {}
        if temp_literary is not None:
            temperatures['literary'] = temp_literary
        if temp_legal is not None:
            temperatures['legal'] = temp_legal
        if temp_technical is not None:
            temperatures['technical'] = temp_technical
        if temp_medical is not None:
            temperatures['medical'] = temp_medical
        if temp_news is not None:
            temperatures['news'] = temp_news
        if temp_academic is not None:
            temperatures['academic'] = temp_academic
        if temp_marketing is not None:
            temperatures['marketing'] = temp_marketing
        if temp_business is not None:
            temperatures['business'] = temp_business
        if temp_master is not None:
            temperatures['master'] = temp_master

        # Initialize pipeline with user credentials and temperatures
        pipeline = TranslationPipeline(
            api_key=api_key,
            provider=provider,
            model=model,
            temperatures=temperatures if temperatures else None
        )
        if temperature is not None:
            pipeline.temperature = temperature

        # Process file
        file_handler = FileHandler()
        text_chunks = file_handler.process_file(file_path)

        async def event_generator():
            try:
                # Run translation generator with model info
                iterator = pipeline.translate(
                    text_chunks,
                    source_lang,
                    target_lang,
                    translation_type,
                    brief,
                    glossary,
                    model_name=model,
                    provider_name=provider
                )
                
                for event in iterator:
                    # If completed, save files
                    if event.get("status") == "completed":
                        result = event["result"]
                        translated_text = result["translated_text"]
                        details = result["details"]
                        
                        # Add model and provider info to details
                        details["model"] = model
                        details["provider"] = provider
                        
                        # Save results
                        output_file = file_handler.save_translated_file(
                            translated_text,
                            file_path,
                            details,
                            output_format
                        )
                        details_file = file_handler.save_translation_details(details, file_path)
                        
                        # Add file info to result
                        event["result"]["output_file"] = os.path.basename(output_file)
                        event["result"]["message"] = "Translation completed successfully"
                    
                    yield json.dumps(event) + "\n"
            except Exception as e:
                import traceback
                traceback.print_exc()
                yield json.dumps({"status": "error", "message": str(e)}) + "\n"

        return StreamingResponse(event_generator(), media_type="application/x-ndjson")

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")
