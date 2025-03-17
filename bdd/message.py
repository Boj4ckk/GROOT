
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mysql.connector 
from flask import Flask, g, request, jsonify # g = variable de contexte pr stocker données dans un contexte 
import logging
from flask_cors import CORS
from flask_cors import cross_origin
from flask_bcrypt import Bcrypt
from mysql.connector import pooling # pour récupérer les anciennes connexions et pas se reco a chaque requete

from flask import send_from_directory
from Edit.Video_processor import VideoProcessor
from api.Twitch.twitch_api import TwitchApi





# partie requetes db 
DATABASE = 'twitok_base'

db_config = {
    "user": "yazhug", 
    "password": "azureadmin@25", 
    "host": 'twitok-serveur.mysql.database.azure.com', 
    "database": "twitok-database",
    "ssl_ca": "GROOT\\CA\\BaltimoreCyberTrustRoot.crt.pem", # certificat pour azure 
}

connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

app = Flask(__name__) #création application flask 
CORS(app) # pour autoriser les requetes post d'autres origines que le servuer 
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})



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

@app.route("/newUser", methods=['POST'])
def insert_user () : 
    data_received = request.json
    # tiktok_password = None # pour gérer si l'user veut pas mettre ses credentials tiktok dès l'inscription 

    username = data_received.get('username')
    password = data_received.get('password')
    tiktok_username = data_received.get('tiktok_username')
    tiktok_password = data_received.get('tiktok_password')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # decode('utf-8') convertit les octets en str 
    print ("\n TIKTOK PASSWORD : >", tiktok_password, "<\n")
    if (tiktok_password) :
        hashed_tiktok_password = bcrypt.generate_password_hash(tiktok_password).decode('utf-8')
    else : 
        hashed_tiktok_password = None

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
    

@app.route("/login", methods=['POST'])
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



# partie requetes api twitch
CORS(app, resources={r"/recup_infos_clips": {"origins": "http://localhost:5173"}, 
                     r"/send_clips": {"origins": "http://localhost:5173"}})
CLIENT_ID = "k49vl0y998fywdwlvzu48b1u4kth5f"    
CLIENT_SECRET = "cnhhv1qwdxfjc8smmtjnbieg5c9p57"

@app.route('/recup_infos_clips', methods=["POST", "OPTIONS"])
def recup_infos_clips() : 
    if request.method == "OPTIONS":
        # Répondre aux requêtes OPTIONS (CORS preflight)
        return jsonify({"message": "CORS preflight request received"}), 200  # Réponse OK pour OPTIONS
    elif request.method == "POST":
        try :
            data_received = request.json 
            streamer_name = data_received.get('streamer_name')
            game = data_received.get('game')
            min_views = data_received.get('min_views')
            min_duration = 0
            max_duration = int(data_received.get('max_duration'))
            min_date_release = data_received.get('min_date_release') + "T00:00:00Z"
            max_date_release = data_received.get('max_date_release') + "T00:00:00Z"
            number_of_clips = data_received.get('number_of_clips') + 1

            twitch_instance  =  TwitchApi(CLIENT_ID,CLIENT_SECRET)  
            TwitchApi.getHeaders(twitch_instance)

            id_twitch_streamer = TwitchApi.getUserId(twitch_instance, streamer_name)
            data = TwitchApi.getClips(
                twitch_instance,
                id_twitch_streamer,
                filters={"started_at": min_date_release, "ended_at": max_date_release, "first": number_of_clips},
                min_duration=min_duration,
                max_duration=max_duration,
                min_views=min_views,
            )
            TwitchApi.downloadClipWithAudio(twitch_instance,data)
            return jsonify({"message": "Clips récupérés avec succès", "data": twitch_instance.retrived_clips_list}), 200
        except Exception as e :
            logging.error(f"Erreur lors de la récupération des clips: {e}")
            return jsonify({"error": "Erreur interne du serveur", "details": str(e)}), 500        
        
# @app.route("/send_clips", methods=["GET"])
# def send_clips () : 
#     if request.method == 'OPTIONS' : #requete options au back end avant POST quand on fait une requete post 
#         return '', 200
#     try :
#         clipsUrl_to_send = []
#         for file in os.listdir('clips'): 
#             file_path = os.path.join("clips", file)
#             absolute_file_path = os.path.abspath(file_path)
#             clipsUrl_to_send.append(absolute_file_path)
#             print("\n\n liste des url a envoyer : ", clipsUrl_to_send)
#         return jsonify({"clips": clipsUrl_to_send})
#     except Exception as e : 
#         logging.error(f"Erreur lors de l'envoie des clips: {e}")
#         return jsonify({"error": "Erreur interne du serveur", "details": str(e)}), 500

# peut pas charger les fichiers en local via le navigateur donc faut faire avec le serveur 



# OBJECTIF : envoyer les videos sur une route du serveur flask et le récupérer directement via l'url de flask. 
@app.route("/send_clipsUrls", methods=["GET"])
def send_clipsUrls () : 
    if request.method == 'OPTIONS' : #requete options au back end avant POST quand on fait une requete post 
        return '', 200
    try :
        liste_urls = [] 
        for file in os.listdir('clips') :   
            liste_urls.append(file)
        return jsonify ({"clipsUrls": liste_urls})
    except Exception as e : 
        logging.error(f"Erreur lors de l'envoie de l'url des clips : {e}")
        return ({"error": "Erreur lors de l'envoi de l'url des clips"}), 500



@app.route("/clips/<file>")
def send_clip (file):
    dossier = "../../clips/"
    # dossier = "clips"
    # file = urllib.parse.unquote(file)
    return send_from_directory(dossier, file)

@app.route("/process_clip", methods=["POST"])
@cross_origin()  # Explicitly allow CORS for this route
def process_data():

    data = request.json
    web_cam_state = data.get("webcam_detection")
    clip_format = data.get("clip_format")
    clip_path = data.get("clip_path")

    video_processor_instance = VideoProcessor(clip_path, web_cam_state, clip_format)
    video_processor_instance.process_video()

    return jsonify({"processed_clip_url" : video_processor_instance.edited_clip_path })


if __name__ == '__main__' : 
    app.run(debug=True)