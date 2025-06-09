from Service.user_services import UserService
from flask import request, jsonify
from config.azure_config import SessionLocal


class UserController():

    @staticmethod
    def create_user(data=None):
        if data is None:
            data = request.get_json()

        with SessionLocal() as db:
            user_service = UserService(db)
            user = user_service.create_user(data)

            return jsonify({
                "message" :"User Created ",

            }), 201
    
   
    


