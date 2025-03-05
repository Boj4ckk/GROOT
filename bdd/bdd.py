import mysql.connector 
from flask import Flask, g, request, jsonify # g = variable de contexte pr stocker données dans un contexte 
import logging
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from mysql.connector import pooling # pour récupérer les anciennes connexions et pas se reco a chaque requete

DATABASE = 'twitok_base'

db_config = {
    "user": "root", 
    "password": "", 
    "host": 'localhost', 
    "database": "twitok_base"
}

connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

app = Flask(__name__) #création application flask 
CORS(app) # pour autoriser les requetes post d'autres origines que le servuer 
bcrypt = Bcrypt(app) # pour cryptage des mdp 

@app.route('/')
def home(): 
    return "Bienvenu brother"

def get_db(): 
    db = getattr(g, '_database', None)
    if db is None:
        print("bdd non connectée, connexion...")
        try:
            # db = g._database = mysql.connector.connect(
            #     host="localhost", user="root", password="", database=DATABASE
            # )
            db = g._database = connection_pool.get_connection() # pour recup les anciennes co 
            print("bdd connectée")
        except mysql.connector.Error as err:
            print(f"Erreur de connexion MySQL : {err}")
    return db

@app.route('/showUsers')
def show_user() : 
    db = get_db()
    cursor = db.cursor() 

    query = ("Select * from user")
    cursor.execute(query, ())
    users = cursor.fetchall()
    cursor.close()
    return users

def user_already_exists (username) : 
    db = get_db() 
    cursor = db.cursor() 

    query = ("Select username from user")
    cursor.execute (query, ())
    usernames_already_registered = cursor.fetchall() 
    print ("username recherché : " + username)
    print ("usernames already registered :", usernames_already_registered)
    if (username in usernames_already_registered) : 
        return True
    return False

@app.route("/login", methods=['POST'])
def register() : 
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

@app.route("/newUser", methods=['POST'])
def insert_user () : 
    data_received = request.json
    username = data_received.get('username')
    password = data_received.get('password')
    tiktok_username = data_received.get('tiktok_username')
    tiktok_password = data_received.get('tiktok_password')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # decode('utf-8') convertit les octets en str 
    hashed_tiktok_password = bcrypt.generate_password_hash(tiktok_password).decode('utf-8')

    db = get_db() 
    cursor = db.cursor() 

    query = ('Insert into user (username, password, tiktok_username, tiktok_password) VALUES (%s, %s, %s, %s)')

    try :
        if (user_already_exists(username)) : 
            logging.error(f'user {username} already exists')
            return jsonify({"error": f'user {username} already exists'}), 400
        if (username == "" or password == "") : 
            logging.error(f'username and password mustn\'t be empty')
            return jsonify({"error" : f'username and password mustn\'t be empty'})
        cursor.execute(query, (username, hashed_password, tiktok_username, hashed_tiktok_password))
        db.commit()
        logging.info(f'user {username} succsfully registered')
        return jsonify({"info" : f'user : username succesfuly registered'})
    except mysql.connector.Error as e : 
        logging.error(f'Erreur de requete : {e}')
        db.rollback() # pour éviter de push la requete vu qu'elle va flop 
        return jsonify({"error" : "query error"}), 500 # retourne erreur 500  
    
if __name__ == '__main__' : 
    app.run(debug=True)