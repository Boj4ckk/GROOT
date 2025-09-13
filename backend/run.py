
from flask import Flask, make_response, request
from flask_cors import CORS
from dotenv import load_dotenv
from Routes.auth_routes import AuthRoutes
from Routes.clip_routes import ClipRoutes
from Routes.twitch_routes import TwitchRoutes
import os
import sys


load_dotenv(dotenv_path="backend/.env")
def create_app():
    app = Flask(__name__)
    
    # Configuration CORS spécifique pour votre frontend
    CORS(app, 
         origins=['http://localhost:5173'],  # Votre frontend Vite
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'Accept'],
         supports_credentials=True
    )
    
    # Gestion explicite des requêtes OPTIONS (preflight)
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
            response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,Accept")
            response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response

    app.register_blueprint(AuthRoutes.auth_bp)
    app.register_blueprint(TwitchRoutes.twitch_bp)
    app.register_blueprint(ClipRoutes.clip_bp)

    
    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)