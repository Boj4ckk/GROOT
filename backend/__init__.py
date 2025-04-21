from flask import Flask
from flask_cors import CORS


from backend.config.config import Config


from backend.routes.api import api_bp
from backend.routes.views import views_bp








db_pool = None
def create_app():

    app = Flask(__name__) #création application flask 
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(views_bp)

    import backend.extensions
    backend.extensions.db_pool = Config.init_pool()

    from backend.extensions import bcrypt
    bcrypt.init_app(app)

    return app

