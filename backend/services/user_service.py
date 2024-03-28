from models.users import User
from config.firebase import db
from schema.to_firestore import user_to_firestore

class UserService:
    collection_name = "users"

    def create_user(self, user: User):
        data = user_to_firestore(user)
        db.collection(self.collection_name).document(user.uid).set(data)

    def update_user(self, user: User):
        data = user_to_firestore(user)
        user_ref = db.collection(self.collection_name).document(user.uid)
        user_ref.update(data)

    def get_user(self, uid: str):
        doc_ref = db.collection(self.collection_name).document(uid)
        doc = doc_ref.get()

        if doc.exists:
            return User(**doc.to_dict())
        else:
            raise Exception(f"No document found with {uid} uid")