
# services/user_service.py
from Model.user_model import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    def __init__(self,db_session):
        self.db  = db_session

    def create_user(self,user_data):
        new_user = User(
            user_email = user_data["user_email"],
            user_password = generate_password_hash(user_data["user_password"]),
            )
        self.db.add(new_user)
        try:
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Email déjà utilisé ou autre erreur d’intégrité")
        
    def get_user_by_email(self,user_email):
        return self.db.query(User).filter(User.user_email == user_email).first()

    def authentificate(self, user_email, user_password):
        user = self.get_user_by_email(user_email)
        if user and (check_password_hash(user.user_password, user_password)):
            return user
        return None


    