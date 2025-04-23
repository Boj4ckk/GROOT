from flask import Blueprint, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin

from backend.api.Twitch.Twitch_api import TwitchApi
from backend.api.Tiktok.tiktok_api import TiktokApi

from backend.Edit.Video_processor import VideoProcessor
from backend.config.config import Config

import logging
import os


api_bp = Blueprint("api", __name__)

@api_bp.route('/recup_infos_clips', methods=["OPTIONS","POST"])
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
            number_of_clips = data_received.get('number_of_clips')
            print ('\n Nombre de vidéos demandées : ', number_of_clips)
            if (number_of_clips == 0) :
                number_of_clips = 1

            twitch_instance  =  TwitchApi(Config.CLIENT_ID,Config.CLIENT_SECRET)  
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
            return jsonify({"message": "Clips récupérés avec succès", "data": data}), 200
        except Exception as e :
            logging.error(f"Erreur lors de la récupération des clips: {e}")
            return jsonify({"error": "Erreur interne du serveur", "details": str(e)}), 500        

# OBJECTIF : envoyer les videos sur une route du serveur flask et le récupérer directement via l'url de flask. 
@api_bp.route("/send_clipsUrls", methods=["OPTIONS","GET"])
def send_clipsUrls () : 
    
    if request.method == 'OPTIONS' : #requete options au back end avant POST quand on fait une requete post 
        return '', 200
    try :
        liste_urls = [] 
        for file in os.listdir('data\\fetch_clips') :   
            liste_urls.append(file)
        return jsonify ({"clipsUrls": liste_urls})
    except Exception as e : 
        logging.error(f"Erreur lors de l'envoie de l'url des clips : {e}")
        return ({"error": "Erreur lors de l'envoi de l'url des clips"}), 500




@api_bp.route("/clips/<file>")
def send_clip (file):
    dossier = os.path.abspath("C:\\Users\\yazki\\OneDrive\\Bureau\\GROOT\\data\\fetch_clips")
    return send_from_directory(dossier, file)




@api_bp.route('/process_clip', methods=["OPTIONS","POST"])
def process_data():

    if request.method == "OPTIONS":
        return jsonify({}), 200  # Just to be safe

    data = request.json
    web_cam_state = data.get("webcam_detection")
    clip_format = data.get("clip_format")
    clip_path = data.get("clip_path")

    video_processor_instance = VideoProcessor(clip_path, web_cam_state, clip_format)
    video_processor_instance.process_video()

    return jsonify({"processed_clip_url" : video_processor_instance.edited_clip_path_to_vue })






@api_bp.route("/publication", methods=["POST"])
def publication () : 
    data = request.json
    vue_video_path = data.get('vue_chemin_video')
    description = data.get("description")

    full_relative_video_path = "GROOT/twitok_website/public"+vue_video_path
    print ("\n\n full relative path : ", full_relative_video_path, "\n\n")

    full_absolute_video_path = os.path.abspath(full_relative_video_path)
    print ("\n\n full absolute path : ", full_absolute_video_path, "\n\n")


    tiktok_instance = TiktokApi()
    tiktok_instance.startDriver()
    tiktok_account_for_example = Config.TIKTOK_USERNAME
    tiktok_password_for_example = Config.TIKTOK_PASSWORD
    tiktok_instance.login(tiktok_account_for_example, tiktok_password_for_example)
    tiktok_instance.uploadVideo(full_absolute_video_path, description)
    tiktok_instance.closeDriver() 

    return jsonify({"message":"clips publié avec succès ! Vous pouvez aller voir le clip sur https://www.tiktok.com/@twitok_bot_2/"})