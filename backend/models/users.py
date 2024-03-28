from pydantic import BaseModel
from models.predictions import Prediction

class User(BaseModel):
    first_name: str
    last_name: str
    uid: str
    email: str
    predictions: list[Prediction] | None
