from pydantic import BaseModel

class LoginUser(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@xyz.co",
                "password": "Test@1234"
            }
        }