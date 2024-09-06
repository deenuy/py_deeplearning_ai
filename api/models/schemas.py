from pydantic import BaseModel
from typing import List

class PredictRequest(BaseModel):
    image: List[float]

class PredictResponse(BaseModel):
    prediction: int

class ErrorResponse(BaseModel):
    detail: str