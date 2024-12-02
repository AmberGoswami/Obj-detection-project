from pydantic import BaseModel

class UploadResponse(BaseModel):
    message: str
    result_image_path: str
    result_json_path: str
