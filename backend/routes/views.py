from flask import Blueprint, jsonify

from backend.extensions import bcrypt
from backend.services.azure_db import get_db
from flask import request

import logging




views_bp = Blueprint('views',__name__)


@views_bp.route('/')
def home(): 
    return "Bienvenu brother"



@views_bp.route("/login", methods=['POST'])
def login() : 
    data_received = request.json
    username = data_received.get('username')
    password = data_received.get('password')

    db = get_db()
    cursor = db.cursor() 

    query = ('Select username, password from user where username=(%s)')
    cursor.execute(query, (username,))

    user = cursor.fetchone()
    logging.info(f"user trouvé : {user}")
    if (user is None) : 
        logging.error(f'user {username} doesn\'t exist')
        return jsonify({"error" : "invalid username"}), 401
    
    hashed_password = user[1] #user[1] car ce que rend user = cursror.fetchone() renvoie un tuple donc c des indices sous forme de nombre 
    logging.info(f"hashed password : {hashed_password}")
    if (not bcrypt.check_password_hash(hashed_password, password)) : 
        logging.error(f'user {password} isn\'t correct')
        return jsonify({"error": "password isn't correct"}), 401
    return jsonify({"info" : f'user : username succesfuly registered'})