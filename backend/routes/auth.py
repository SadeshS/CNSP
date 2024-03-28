from fastapi import APIRouter, HTTPException
from models.signup_user import SignupUser
from config.firebase import firebase_auth
from models.users import User
from services.user_service import UserService

router = APIRouter()

@router.post('/signup')
async def signup(user_data: SignupUser):
    try:
        user: firebase_auth.UserRecord = firebase_auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=f"{user_data.first_name} {user_data.last_name}"
        )
        tempUser = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            uid=user.uid,
            email=user_data.email,
            predictions=[]
        )
        us = UserService()
        us.create_user(tempUser)
    except firebase_auth.EmailAlreadyExistsError:
        raise HTTPException(400, f"A user has been already registered using the email {user_data.email}")
    except Exception as e:
        raise HTTPException(500, str(e))