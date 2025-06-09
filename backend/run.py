
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from Routes.auth_routes import AuthRoutes
import os
import sys


load_dotenv(dotenv_path="backend/.env")
def create_app():
    app = Flask(__name__) #création application flask 


    CORS(app)

    app.register_blueprint(AuthRoutes.auth_bp)


    return app

app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)