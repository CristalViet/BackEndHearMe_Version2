from pydantic import BaseModel
from typing import List

class VideoProcessRequest(BaseModel):
    frames: List[str]
    lessonPath: str

class VideoResponse(BaseModel):
    similarity: float
    status: str 