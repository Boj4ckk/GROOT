from flask import request
from Model.clip_model import Clip
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from Service.blob_service import BlobStorageService
from azure.storage.blob import ContainerClient
import os

class ClipServices:
    def __init__(self,db_session):
        self.db = db_session
        self.blob_service =  BlobStorageService()

    
    def download_and_store_clip(self,clip_data):


        clip_filename = f"clip_{clip_data['url'].split('/')[-1]}.mp4"
        fetched_clip_prefix = os.getenv("FETCHED_CLIP_BLOB_PREFIX")
        clip_blob_path = self.blob_service.upload_in_blob(
            file_content=clip_data,
            blob_path=f"user_{request.user_id}/{fetched_clip_prefix}/{clip_filename}"
        )
        new_clip = Clip(
            clip_url = clip_data["url"],
            broadcaster_id = clip_data["broadcaster_id"],
            broadcaster_name = clip_data["broadcaster_name"],
            creator_id  = clip_data["creator_id"],
            creator_name = clip_data["creator_name"],
            video_id = clip_data["video_id"],
            game_id = clip_data["game_id"],
            clip_language = clip_data["language"],
            date_creation = clip_data["created_at"],
            thumbnail_url = clip_data["thumbnail_url"],
            duration = clip_data["duration"],
        )
        self.db.add(new_clip)
        try:
            self.db.commit()
            self.db.refresh(new_clip)
            return new_clip
        except Exception as e :
            self.db.rollback()
            print(f"Erreur SQL détaillée: {e}")
            print(f"Type d'erreur: {type(e)}")
            raise e  
        