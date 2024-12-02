import json
import cv2
from pathlib import Path
from ultralytics import YOLO
from fastapi import HTTPException

# Initialize YOLOv8 model
try:
    model = YOLO("yolov8n.pt")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading YOLO model: {str(e)}")

# Define a color palette for bounding boxes
colors = [
    (0, 255, 0),  
    (255, 0, 0),  
    (0, 0, 255),  
    (0, 255, 255),  
    (255, 0, 255),  
    (255, 255, 0), 
]

def process_image(input_image_path: Path, filename: str):
    """
    Process the image with YOLO model, detect objects, save results and return paths.

    - **input_image_path**: The path to the uploaded image.
    - **filename**: The name of the uploaded image file.
    """
    try:
        # Perform object detection using YOLO
        results = model.predict(source=str(input_image_path), save=False, conf=0.25)  # Adjust confidence as needed
        if len(results) == 0:
            return None, None

        # Process the results
        result = results[0]  

        image = cv2.imread(str(input_image_path))
        if image is None:
            raise ValueError("Failed to load the image.")

        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            label = f"{model.names[cls]} {conf:.2f}"

            color = colors[cls % len(colors)]  
            thickness = 2  # Adjusted thickness
            font_scale = 0.8  # Adjusted font scale
            font_thickness = 2  # Adjusted font thickness

            # Draw the rectangle around the detected object
            cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

            # Place text inside the bounding box
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
            text_width, text_height = text_size

            # Ensure text stays within the bounding box
            text_x = x1 + 5  # Offset from the left side
            text_y = y1 + text_height + 5  # Offset from the top side

            # Ensure the text doesn't overflow the bounding box
            if text_x + text_width > x2:
                text_x = x2 - text_width - 5
            if text_y > y2:
                text_y = y2 - text_height - 5

            # Draw the text inside the bounding box
            cv2.putText(image, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)

        # Save the result image
        result_image_path = Path(f"outputs/images/result_{filename}")
        cv2.imwrite(str(result_image_path), image)

        # Save detection results to a JSON file
        result_json_path = Path(f"outputs/json/result_{Path(filename).stem}.json")
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

        return result_image_path, result_json_path

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
