import os, sys
import mysql.connector 
from flask import Flask, g, request, jsonify  # g = variable de contexte pour stocker des données dans un contexte
import logging
from flask_cors import CORS
from flask_cors import cross_origin
from backend.routes.api import api_bp
from backend.Edit.Video_processor import VideoProcessor
import backend.extensions as ext  # Importation de extensions.py pour récupérer db_pool et bcrypt


# Utilisation de bcrypt et db_pool de backend.extensions
bcrypt = ext.bcrypt


def get_db(): 
    db = getattr(g, '_database', None)
    if db is None:
        print("bdd non connectée, connexion...")
        try:
            db = g._database = ext.db_pool.get_connection()  # Utilisation de db_pool de backend.extensions
            print("bdd connectée")
        except mysql.connector.Error as err:
            print(f"Erreur de connexion MySQL : {err}")
    return db

@api_bp.route('/showUsers')
def show_user():
    db = get_db()
    cursor = db.cursor() 

    query = ("SELECT * FROM user")
    cursor.execute(query, ())
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)  # Retourner les résultats sous forme de JSON

def user_already_exists(username):
    db = get_db() 
    cursor = db.cursor() 

    query = ("SELECT username FROM user")
    cursor.execute(query, ())
    usernames_already_registered = cursor.fetchall() 
    print(f"username recherché : {username}")
    print(f"usernames already registered : {usernames_already_registered}")
    if username in usernames_already_registered: 
        return True
    return False

@api_bp.route("/newUser", methods=['POST'])
def insert_user(): 
    data_received = request.json

    username = data_received.get('username')
    password = data_received.get('password')
    tiktok_username = data_received.get('tiktok_username')
    tiktok_password = data_received.get('tiktok_password')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Decode pour convertir en str
    print(f"\n TIKTOK PASSWORD : >{tiktok_password}<\n")
    if tiktok_password:
        hashed_tiktok_password = bcrypt.generate_password_hash(tiktok_password).decode('utf-8')
    else:
        hashed_tiktok_password = None

    db = get_db() 
    cursor = db.cursor() 

    query = ('INSERT INTO user (username, password, tiktok_username, tiktok_password) VALUES (%s, %s, %s, %s)')

    try:
        if user_already_exists(username): 
            logging.error(f'user {username} already exists')
            return jsonify({"error": f'user {username} already exists'}), 400
        if not username or not password: 
            logging.error(f'username and password mustn\'t be empty')
            return jsonify({"error" : f'username and password mustn\'t be empty'})
        cursor.execute(query, (username, hashed_password, tiktok_username, hashed_tiktok_password))
        db.commit()
        logging.info(f'user {username} successfully registered')
        return jsonify({"info" : f'user: {username} successfully registered'})
    except mysql.connector.Error as e: 
        logging.error(f'Erreur de requête : {e}')
        db.rollback()  # Pour éviter de push la requête en cas d'erreur
        return jsonify({"error" : "query error"}), 500  # Retourne erreur 500
