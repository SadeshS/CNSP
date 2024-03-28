from pydantic import BaseModel

class PredictionResults(BaseModel):
    user_id: str
    product_id: str
    quantity: int
    date: str