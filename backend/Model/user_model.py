
from sqlalchemy import Column, Integer, String
from  database import Base


class User(Base):
    __tablename__ = "users"
    
    id_user= Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String, unique=True, nullable=False)
    user_password = Column(String(256), nullable=False)
