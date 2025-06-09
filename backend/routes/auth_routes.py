from flask import Blueprint
from Controller.auth_controller import AuthController



class AuthRoutes:

    auth_bp = Blueprint("auth",__name__)
    auth_bp.route("/register",methods=['POST'])(AuthController.register)
    auth_bp.route("/login",methods=['POST'])(AuthController.login)