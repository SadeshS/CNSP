from pydantic import BaseModel

class PredictData(BaseModel):
    url: str

    class Config:
        schema_extra = {
            "example": {
                "url": "www.xyz.ll",
            }
        }