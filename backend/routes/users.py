from fastapi import APIRouter, HTTPException
from services.user_service import UserService

router = APIRouter()
    
@router.get('/{uid}')
async def getUser(uid: str):
    try:
        us = UserService()
        user = us.get_user(uid)
        return user
    except Exception as e:
        raise HTTPException(500, str(e))