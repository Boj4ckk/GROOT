import jwt
import os
from datetime import datetime, timedelta


SECRET_KEY  = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

class JwtAdapter:
    @staticmethod
    def encode(payload):
        payload["exp"] = datetime.utcnow() + timedelta(hours=1)
        return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    
    @staticmethod
    def decode(token):
        return jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)