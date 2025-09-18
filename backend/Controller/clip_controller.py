import logging
import os
from flask import request
from Service.clip_services import ClipServices
from Service.blob_service import BlobStorageService
from flask import request, jsonify
from config.azure_config import SessionLocal
from middlewares.auth_middleware import jwt_required


class ClipController():

    @staticmethod
    @jwt_required
    def send_clips_urls():
        if request.method == 'OPTIONS' : #requete options au back end avant POST quand on fait une requete post 
            return '', 200
        try :
            blob_service = BlobStorageService()
            user_fetched_clip_data = blob_service.get_user_fetched_clips(request.user_id)
        
        except Exception as e : 
            logging.error(f"Erreur lors de l'envoie de l'url des clips : {e}")
            return ({"error": "Erreur lors de l'envoi de l'url des clips"}), 500
        return user_fetched_clip_data
        