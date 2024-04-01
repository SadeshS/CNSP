from fastapi import HTTPException, status, Request
from config.firebase import auth

def get_current_user(request: Request):
    authorization: str = request.headers.get('Authorization')
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header is missing.")

    token = authorization.split(" ").pop()
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")