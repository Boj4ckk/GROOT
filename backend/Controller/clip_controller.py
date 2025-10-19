import logging
import os
from flask import request,jsonify

from Service.blob_service import BlobStorageService
from Service.clip_services import ClipServices

from middlewares.auth_middleware import jwt_required
from config.azure_config import SessionLocal


class ClipController():

    @staticmethod
    @jwt_required
    def send_clips_urls():
        if request.method == 'OPTIONS' : #requete options au back end avant POST quand on fait une requete post 
            return '', 200
        db_session = SessionLocal()
        try :
           
            clip_service = ClipServices(db_session)
            user_fetched_clip_data = clip_service.get_clips_with_urls(request.user_id)
            return jsonify(user_fetched_clip_data), 200
       
        except Exception as e : 
            logging.error(f"Erreur lors de l'envoie de l'url des clips : {e}")
            return ({"error": "Erreur lors de l'envoi de l'url des clips"}), 500
        finally:
            db_session.close()
       
        