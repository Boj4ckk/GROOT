import logging
import os
from Service.clip_services import ClipServices
from flask import request, jsonify
from config.azure_config import SessionLocal


class ClipController():

    @staticmethod
    def send_clips_urls():
        if request.method == 'OPTIONS' : #requete options au back end avant POST quand on fait une requete post 
            return '', 200
        try :
            liste_urls = [] 
            path = os.path.join("backend","data","fetch_clips")
            for file in os.listdir(path) :   
                liste_urls.append(file)
            return jsonify ({"clipsUrls": liste_urls})
        except Exception as e : 
            logging.error(f"Erreur lors de l'envoie de l'url des clips : {e}")
            return ({"error": "Erreur lors de l'envoi de l'url des clips"}), 500

        