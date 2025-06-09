
from Controller.user_controller import UserController
from flask import request, jsonify
from Service.user_services import UserService
from config.azure_config import SessionLocal

class AuthController:

    @staticmethod
    def register():
        data = request.get_json()
        return UserController.create_user(data)


    @staticmethod
    def login():
        data = request.get_json()
        if 'user_email' not in data or 'user_password' not in data:
            return jsonify({"error": "Email or password field missing."}), 400
        
        with SessionLocal() as db:
            user_service = UserService(db)
            user = user_service.authentificate(data["user_email"], data["user_password"])
        if not user:
            return jsonify({"Error" :" User not found !"}), 401
        
        return jsonify({
            "message": "User connected"
        }),200
        