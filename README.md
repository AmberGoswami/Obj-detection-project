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

## Endpoints
- **UI Backend (Port 8001)**: POST /upload: Upload an image for detection.
- **AI Backend (Port 8000)**: POST /detect: Perform object detection on an uploaded image.
