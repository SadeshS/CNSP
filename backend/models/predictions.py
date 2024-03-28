from pydantic import BaseModel
from models.prediction_results import PredictionResults
from enum import Enum

class PredictionStatus(str, Enum):
    in_progress = "in_progress"
    success = "success"
    failed = "failed"

class Prediction(BaseModel):
    id: int
    created_time: str
    status: PredictionStatus
    predictions: list[PredictionResults] | None

