import mysql.connector 
from flask import Flask, g, request, jsonify # g = variable de contexte pr stocker données dans un contexte 
import logging
from flask_cors import CORS

DATABASE = 'twitok_base'

app = Flask(__name__) #création application flask 
CORS(app) # pour autoriser les requetes post d'autres origines que le servuer 

@app.route('/')
def home(): 
    return "Bienvenu brother"

# def get_db(): 
#     db = getattr(g, '_database', None) #retourne le nom d'un attribut de l'objet
#     if db is None : 
#         print ("bdd non connectée, connexion...")
#         db = g._database = mysql.connector.connect(host="localhost", user="root", password="", database=DATABASE)
#         print ("bdd connectée")
#         return db

def get_db(): 
    db = getattr(g, '_database', None)
    if db is None:
        print("bdd non connectée, connexion...")
        try:
            db = g._database = mysql.connector.connect(
                host="localhost", user="root", password="", database=DATABASE
            )
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

@app.route("/newUser", methods=['POST'])
def insert_user () : 
    data_received = request.json
    username = data_received.get('username')
    password = data_received.get('password')
    tiktok_username = data_received.get('tiktok_username')
    tiktok_password = data_received.get('tiktok_password')

    db = get_db() 
    cursor = db.cursor() 

    query = ('Insert into user (username, password, tiktok_username, tiktok_password) VALUES (%s, %s, %s, %s)')

    try :
        if (user_already_exists(username)) : 
            logging.error(f'user {username} already exists')
            return jsonify({"error", f'user {username} already exists'}), 400
        if (username == "" or password == "") : 
            logging.error(f'username and password mustn\'t be empty')
            return jsonify({"error" : f'username and password mustn\'t be empty'})
        cursor.execute(query, (username, password, tiktok_username, tiktok_password))
        db.commit()
        logging.info(f'user {username} succsfully registered')
        return jsonify({"info" : f'user : username succesfuly registered'})
    except mysql.connector.Error as e : 
        logging.error(f'Erreur de requete : {e}')
        db.rollback() # pour éviter de push la requete vu qu'elle va flop 
        return jsonify({"error" : "query error"}), 500 # retourne erreur 500  

    



# @app.route('/insert_new_user', methods=["POST"]) 
# # def insert_new_user (username, password_not_hashed, tiktok_username="", tiktok_password_not_hashed="") : 
# def insert_new_user () : # test sans les arguments en les donnant et y accedant vaec request pour voir si ca marche  

#     recup_data = request.get_json() # recup des données envoyés depuis vue 

#     username = recup_data.get('username') 
#     password_not_hashed = recup_data.get('password')
#     tiktok_username = recup_data.get('tiktok_username', '')  # deuxieme arg pour dire que c vide p/defaut 
#     tiktok_password_not_hashed = recup_data.get('tiktok_password', '')

#     print (f"username : {username}") # ici username = None 

#     db = get_db() 
#     cursor = db.cursor() 
#     try :
#         if (user_already_exists(username)) :
#             logging.warning(f"user {username} already exists.")
#             return jsonify({"error": "Username already exists"}), 400


#         query = ("Insert into user (username, password, tiktok_username, tiktok_password) VALUES (%s, %s, %s, %s)") 
#         values = (username, password_not_hashed, tiktok_username, tiktok_password_not_hashed)

#         insert = cursor.execute(query, values) 
#         db.commit() 
#         cursor.close() 

#         logging.info(f"User '{username}' inserted successfully.")
#         return jsonify({"message": "User inserted "}), 400

#     except mysql.connector.Error as e : 
#         logging.error(f" Erreur requete  {e}")
#         db.rollback()  # Annule la requete si erreur jcrois 






# with app.app_context() : # pour executer get_db() dans un contexte valide 
#     db = get_db()
#     insert_new_user("yahugozid", "yazid_password", "yazid_tiktok", "yazid_password_tiktok") 

if __name__ == '__main__' : 
    app.run(debug=True)