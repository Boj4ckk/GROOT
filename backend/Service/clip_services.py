from flask import request
from Model.clip_model import Clip
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from Service.blob_service import BlobStorageService
from azure.storage.blob import ContainerClient
import os
import uuid

class ClipServices:
    def __init__(self,db_session):
        self.db = db_session
        self.blob_service =  BlobStorageService()

    def upload_fetched_clip_in_blob(self,clip_data):

        # Gén un nom de fichier unique pour le blob
        unique_filename = f"{uuid.uuid4()}.mp4"
        fetched_clip_prefix = os.getenv("FETCHED_CLIP_BLOB_PREFIX")

        # Création d'un chemin vers le clip dans le blob
        blob_path = f"{fetched_clip_prefix}/{unique_filename}"
        #Upload le fichier dans le blob.
        clip_blob_path = self.blob_service.upload_in_blob(
            file_content=clip_data,
            blob_path=blob_path
        )
        return clip_blob_path

    def add_fetched_clip_to_db(self,clip_data,user_id):

        clip_blob_path = self.upload_fetched_clip_in_blob(clip_data)
        new_clip = Clip(
            blob_name = clip_blob_path["blob_path"],
            broadcaster_id = clip_data["broadcaster_id"],
            broadcaster_name = clip_data["broadcaster_name"],
            creator_id  = clip_data["creator_id"],
            creator_name = clip_data["creator_name"],
            video_id = clip_data["video_id"],
            game_id = clip_data["game_id"],
            title = clip_data["title"],
            clip_language = clip_data["language"],
            date_creation = clip_data["created_at"],
            thumbnail_url = clip_data["thumbnail_url"],
            duration = clip_data["duration"],
            view_count = clip_data["view_count"],
            user_id = user_id,
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
    


    def get_clips_with_urls(self, user_id):

        user_clips_form_db = self.db.query(Clip).filter_by(user_id=user_id).all()

        enriched_clips = []
        for clip in user_clips_form_db:
            secure_url = self.blob_service.generate_blob_sas_url(clip.blob_name)

            if secure_url:
                enriched_clips.append({
                    "id_clip": clip.id_clip,
                    "url": secure_url,
                    "broadcaster_id": clip.broadcaster_id,
                    "broadcaster_name" : clip.broadcaster_name,
                    "creator_id" : clip.creator_id,
                    "game_id" : clip.game_id,
                    "title" : clip.title,
                    "clip_language" : clip.clip_language,
                    "date_creation": clip.date_creation,
                    "duration" : clip.duration,
                    "view_count" : clip.view_count,
                })
        return enriched_clips
                
 