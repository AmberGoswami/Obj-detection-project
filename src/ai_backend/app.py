from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from src.ai_backend.schema import UploadResponse
from fastapi.staticfiles import StaticFiles
from src.ai_backend.yolo_handler import process_image
import uvicorn
import shutil
from pathlib import Path
import os

# Initialize FastAPI instance
app = FastAPI()

app.mount("/ui", StaticFiles(directory="src/static", html=True), name="static")
app.mount("/outputs/images", StaticFiles(directory="outputs/images"), name="static")
app.mount("/outputs/json", StaticFiles(directory="outputs/json"), name="static")

# Output directories
output_images_dir = Path("outputs/images/")
output_json_dir = Path("outputs/json/")
output_images_dir.mkdir(parents=True, exist_ok=True)
output_json_dir.mkdir(parents=True, exist_ok=True)

@app.post("/upload", response_model=UploadResponse, summary="Upload an image for AI detection", description="Uploads an image to the server, performs object detection using YOLO, and returns paths to the processed image and JSON result.")
async def upload_image(request: Request, file: UploadFile = File(...)):
    """
    Upload an image to be processed by YOLO for object detection.

    - **file**: The image file to be uploaded and processed.
    """
    try:
        # Save uploaded file locally
        input_image_path = output_images_dir / file.filename
        with open(input_image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Check file type
        if not input_image_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            raise HTTPException(status_code=415, detail="Unsupported media type. Please upload an image file with type: jpg, .jpeg, .png, .bmp, .gif")

        # Process image with AI (YOLO detection)
        result_image_path, result_json_path = process_image(input_image_path, file.filename)

        # Return the result paths in the response
        base_url = str(request.base_url)
        return {
            "message": "Upload and detection completed successfully",
            "result_image_path": f'{base_url}{result_image_path}',
            "result_json_path": f'{base_url}{result_json_path}'
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

