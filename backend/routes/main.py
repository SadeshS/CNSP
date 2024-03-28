from fastapi import APIRouter
from routes import auth, predictions, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(users.router, prefix="/user", tags=["user"])
