from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
from pathlib import Path
import shutil
import os

# Create FastAPI instance
app = FastAPI()
app.mount("/outputs/images", StaticFiles(directory="outputs/images"), name="static")
app.mount("/outputs/json", StaticFiles(directory="outputs/json"), name="static")

# AI backend URL
AI_BACKEND_URL = "http://0.0.0.0:8000/detect"

# Output directories
output_images_dir = Path("../outputs/images/")
output_json_dir = Path("../outputs/json/")
output_images_dir.mkdir(parents=True, exist_ok=True)
output_json_dir.mkdir(parents=True, exist_ok=True)

# Define response model for Swagger documentation
class UploadResponse(BaseModel):
    message: str
    result_image_path: str
    result_json_path: str

@app.post("/upload", response_model=UploadResponse, summary="Upload an image for AI detection", description="Uploads an image to the server, sends it to the AI backend for detection, and returns paths to the processed image and JSON result.")
async def upload_image(request: Request, file: UploadFile = File(...)):
    """
    Upload an image to be processed by the AI backend for detection tasks.
    
    - **file**: The image file to be uploaded and processed.
    """
    try:
        # Check if the file is a valid image (optional)
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Uploaded file is not an image")

        # Save uploaded file locally
        input_image_path = output_images_dir / file.filename
        with open(input_image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Send the image to AI backend
        try:
            with open(input_image_path, "rb") as image_file:
                response = requests.post(AI_BACKEND_URL, files={"file": image_file})
            response.raise_for_status()  
        except requests.exceptions.RequestException as e:
            # Handle errors with AI backend request
            raise HTTPException(status_code=500, detail=f"Error communicating with AI backend: {e}")

        # Get response data from the AI backend
        try:
            response_data = response.json()
        except ValueError:
            raise HTTPException(status_code=500, detail="Failed to parse response from AI backend")

        # Ensure paths exist in the AI backend response
        if "image_path" not in response_data or "json_path" not in response_data:
            raise HTTPException(status_code=500, detail="Missing image or json path in AI backend response")

        base_url = str(request.base_url)

        return {
            "message": "Upload and detection completed successfully",
            "result_image_path": f'{base_url}{response_data["image_path"]}',
            "result_json_path": f'{base_url}{response_data["json_path"]}'
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
