# Object Detection Microservices

## Overview

This repository contains two microservices built with FastAPI to perform object detection on uploaded images using the YOLOv8 model. The system is designed for easy integration, where users can upload images via the **UI Backend**, which communicates with the **AI Backend** to process the images and return results.

---

## Features

- **AI Backend**:
  - Performs object detection using the YOLOv8n model.
  - Outputs a processed image with bounding boxes and a JSON file containing detection details.
- **UI Backend**:
  - Accepts image uploads.
  - Sends images to the AI Backend and returns the processed results (image and JSON).

---

## Architecture

```plaintext
+-------------------+        +-----------------+
|   UI Backend      |  --->  |   AI Backend    |
|  (Port 8001)      |        |  (Port 8000)    |
+-------------------+        +-----------------+
       |                          |
       |                          |
   Processed Image          Detection Results
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
- **UI Backend**:
  - Runs on port 8001.


##  File Structure
```
├── outputs/
│   ├── images/        
│   ├── json/          
├── src/
│   ├── ai_backend/    
│   │   ├── __init__.py
│   │   ├── app.py
│   ├── ui_backend/    
│   │   ├── __init__.py
│   │   ├── app.py
├── docker-compose.yml 
├── Dockerfile         
├── README.md          
├── requirements.txt   
└── .gitignore         
```

# Endpoints Documentation

## **UI Backend Endpoints**

### **1. Upload Image for Detection**
**Endpoint:** `/upload`  
**Method:** `POST`  

**Description:**  
Uploads an image to the **UI Backend**, which sends it to the **AI Backend** for object detection. Returns the processed image URL and detection results in JSON format.

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

## **AI Backend Endpoints**

### **1. Detect Objects in Image**
**Endpoint:** `/detect`  
**Method:** `POST`  

**Description:**  
Uploads an image to the **AI Backend** for object detection using YOLOv8. Returns the processed image and detection results as JSON.

**Request Parameters:**  
- **file**: (Required) The image file to be uploaded.  

**Response:**  
- **Success (200)**:  
    ```json
    {
        "message": "Detection completed",
        "image_path": "outputs/images/result_<uploaded_filename>",
        "json_path": "outputs/json/result_<uploaded_filename>.json"
    }
    ```
- **Error (415)**:  
    ```json
    {
        "detail": "Unsupported media type. Please upload an image file with type: jpg, jpeg, png, bmp, gif."
    }
    ```
- **Error (500)**:  
    ```json
    {
        "detail": "Error performing object detection: <error_message>"
    }
    ```

- **No Objects Detected (200)**:  
    ```json
    {
        "message": "No objects detected in the image."
    }
    ```
