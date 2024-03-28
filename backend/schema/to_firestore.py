from models.users import User

def user_to_firestore(user: User) -> dict:
    user_dict = user.model_dump()
    user_dict["predictions"] = [prediction.model_dump() for prediction in user.predictions] if user.predictions else None
    return user_dict