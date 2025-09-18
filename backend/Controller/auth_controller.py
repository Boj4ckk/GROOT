
from Controller.user_controller import UserController
from flask import make_response, request, jsonify
from Service.user_services import UserService
from config.azure_config import SessionLocal
from Adapter.jwt_adapter import JwtAdapter

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
                return jsonify({"error": "Utilisateur non trouvé"}), 404

            payload = {"user_id": user.id_user}
            token_jwt  = JwtAdapter.encode(payload)

            response = make_response(jsonify({"message":"Logged in"}))
            response.set_cookie(
                "access_token", 
                token_jwt,
                httponly=True,
                secure=False,  # Mettre à True en production avec HTTPS
                samesite='Lax',  # Important pour CORS
                max_age=3600,
                path='/'  # Assure que le cookie est disponible sur toutes les routes
            )
            return response
    
        