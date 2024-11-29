from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from ultralytics import YOLO
import shutil
import json
from pathlib import Path
import cv2
import os

# Initialize YOLOv8 model
try:
    model = YOLO("yolov8n.pt")  
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading YOLO model: {str(e)}")

# Create FastAPI instance
app = FastAPI()

# Output directories for images and JSON
output_images_dir = Path("outputs/images/")
output_json_dir = Path("outputs/json/")
output_images_dir.mkdir(parents=True, exist_ok=True)
output_json_dir.mkdir(parents=True, exist_ok=True)

# Define a color palette (for example, using RGB values)
colors = [
    (0, 255, 0),  
    (255, 0, 0),  
    (0, 0, 255),  
    (0, 255, 255),  
    (255, 0, 255),  
    (255, 255, 0),  
]

# Define response model for Swagger documentation
class DetectionResult(BaseModel):
    message: str
    image_path: str
    json_path: str

class NoObjectsDetected(BaseModel):
    message: str
@app.post("/detect", 
          responses={200: {"model": DetectionResult}, 415: {"model": NoObjectsDetected}}, 
          summary="Detect objects in the uploaded image", 
          description="Uploads an image and performs object detection using YOLOv8, returning the detected objects in a JSON file and a marked-up image.")
async def detect_objects(file: UploadFile = File(...)):
    """
    Upload an image to be processed by YOLO for object detection.

    - **file**: The image file to be uploaded and processed.
    """
    try:
        input_image_path = output_images_dir / file.filename
        with open(input_image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving uploaded file: {str(e)}")
    
    # Check file type
    if not input_image_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        raise HTTPException(status_code=415, detail="Unsupported media type. Please upload an image file with type: jpg, .jpeg, .png, .bmp, .gif")
    
    # Perform object detection
    try:
        results = model.predict(source=str(input_image_path), save=False, conf=0.25)  # Adjust confidence as needed
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing object detection: {str(e)}")

    # Process the results
    if len(results) > 0:
        result = results[0]  

        try:
            image = cv2.imread(str(input_image_path))
            if image is None:
                raise ValueError("Failed to load the image.")

            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  
                conf = box.conf[0]  
                cls = int(box.cls[0]) 
                label = f"{model.names[cls]} {conf:.2f}" 

                color = colors[cls % len(colors)]  

                thickness = 4  
                font_scale = 1.0  
                font_thickness = 2  
                cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)  
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)

            # Save the result image
            result_image_path = output_images_dir / f"result_{file.filename}"
            cv2.imwrite(str(result_image_path), image)

            # Save detection results to a JSON file (no image extension)
            result_json_path = output_json_dir / f"result_{Path(file.filename).stem}.json"
            results_json = [
                {
                    "class": model.names[int(box.cls[0])],
                    "confidence": float(box.conf[0]),
                    "x1": int(box.xyxy[0][0]),
                    "y1": int(box.xyxy[0][1]),
                    "x2": int(box.xyxy[0][2]),
                    "y2": int(box.xyxy[0][3]),
                }
                for box in result.boxes
            ]
            with open(result_json_path, "w") as json_file:
                json.dump(results_json, json_file, indent=4)

            return {
                "message": "Detection completed",
                "image_path": str(result_image_path),
                "json_path": str(result_json_path),
            }

        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=f"Error processing detection results: {str(e)}")

    # If no objects detected, return a message
    return {"message": "No objects detected in the image."}
