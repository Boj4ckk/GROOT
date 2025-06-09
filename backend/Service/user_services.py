
# services/user_service.py
from Model.user_model import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

class UserService:
    def __init__(self,db_session):
        self.db  = db_session

    def create_user(self, user_email: str, user_password: str) -> User:
        new_user = User(user_email=user_email, user_password=user_password)
        self.db.add(new_user)
        try:
            self.db.commit()
            self.db.refresh(new_user)  # récupère l'ID auto-généré
            return new_user
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Email déjà utilisé ou autre erreur d’intégrité")

    