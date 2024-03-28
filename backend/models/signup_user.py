from pydantic import BaseModel

class SignupUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@xyz.co",
                "password": "Test@1234"
            }
        }