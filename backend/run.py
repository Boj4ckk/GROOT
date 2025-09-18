from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from Routes.auth_routes import AuthRoutes
from Routes.clip_routes import ClipRoutes
from Routes.twitch_routes import TwitchRoutes

load_dotenv(dotenv_path="backend/.env")

def create_app():
    app = Flask(__name__)
    
    # Configuration CORS améliorée
    CORS(app, 
         origins=[
         'http://localhost:5173',
         'http://127.0.0.1:5173',
         ],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'Accept'],
         supports_credentials=True,  # Permet l'envoi de cookies
         expose_headers=['Set-Cookie']  # Expose les cookies au frontend
    )
    
    app.register_blueprint(AuthRoutes.auth_bp)
    app.register_blueprint(TwitchRoutes.twitch_bp)
    app.register_blueprint(ClipRoutes.clip_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)