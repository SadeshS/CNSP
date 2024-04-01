from fastapi import APIRouter, HTTPException, Depends
from services.user_service import UserService
from routes.deps import get_current_user

router = APIRouter()
    
@router.get('')
async def getUser(current_user=Depends(get_current_user),):
    try:
        us = UserService()
        user = us.get_user(current_user["uid"])
        return user
    except Exception as e:
        raise HTTPException(500, str(e))