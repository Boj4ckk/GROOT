from flask import Blueprint
from Controller.user_controller import UserController

class UserRoutes():

    user_bp = Blueprint('users', __name__)
    

