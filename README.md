# Object Detection Microservices

## Overview

This repository contains service built with FastAPI to perform object detection on uploaded images using the YOLOv8(Large) model. The system is designed for easy integration, where users can upload images via a **UI COmponent**, which communicates with the **AI Backend** to process the images and return results.

---

## Features

- **AI Backend**:
  - Receives images from the UI Backend.
  - Performs object detection using the YOLOv8L model.
  - Outputs a processed image with bounding boxes and a JSON file containing detection details.
- **UI Component**:
  - Allows users to upload images.
  - Communicates with the AI Backend to process the images.
---

## Architecture

```plaintext
+-------------------+        +-----------------+
|   UI Component    |  --->  |   AI Backend    |
|                   |        |                 |
+-------------------+        +-----------------+
       |                          |
       |                          |
   Input Image          Detection Results
       |                          |
       +--------------------------+
```

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- **Docker**:
  - Install Docker
- **Docker Compose**:
  - Install Docker Compose
- **Git**:
  - Install Git from Git's official site.

## Setup Instructions

### Clone the Repository:
```git clone <repository_url>
   cd <repository_name>
```

### Build and Run the Services in detach mode:
```
docker-compose up --build -d
```

##  Access the Services:
- **AI Backend**:
  - Runs on port 8000.
- **UI Component**:
  - Runs on endpoint */ui*


##  File Structure
```
├── outputs/
│   ├── images/        
│   ├── json/          
├── src/
│   ├── ai_backend/    
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── schema.py
│   │   ├── yolo_handler.py
│   ├── static/    
│   │   ├── index.html
│   │   ├── style.css
├── docker-compose.yml 
├── Dockerfile         
├── README.md          
├── requirements.txt   
└── .gitignore         
```

# Endpoints Documentation

## **AI Backend Endpoints**

### **1. Upload Image for Detection**
**Endpoint:** `/upload`  
**Method:** `POST`  

**Description:**  
Uploads an image to the **AI Backend**, for object detection. Returns the processed image URL and detection results in JSON format.

**Request Parameters:**  
- **file**: (Required) The image file to be uploaded.  

**Response:**  
- **Success (200)**:  
    ```json
    {
        "message": "Upload and detection completed successfully",
        "result_image_path": "http://<ui-backend-url>/outputs/images/<processed_image>",
        "result_json_path": "http://<ui-backend-url>/outputs/json/<detection_results_json>"
    }
    ```
- **Error (400)**:  
    ```json
    {
        "detail": "Uploaded file is not an image"
    }
    ```
- **Error (500)**:  
    ```json
    {
        "detail": "An unexpected error occurred: <error_message>"
    }
    ```

---

## **UI Component**

### **1. Webpage**
**Endpoint:** `/ui`  
**Method:** `GET`  

**Description:**  
Serves the frontent webpage with a form to upload an image for detection. After inference the image is displayed with bounding boxes and detection results.

