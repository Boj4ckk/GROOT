import requests
from Model.clip_model import Clip
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from Service.blob_service import BlobStorageService
from azure.storage.blob import ContainerClient

class ClipServices:
    def __init__(self,db_session):
        self.db = db_session
        self.blob_service =  BlobStorageService()

    
    def download_and_store_clip(self,clip_data):


        clip_filename = f"clip_{clip_data['url'].split('/')[-1]}.mp4"

        clip_blob_path = self.blob_service.upload_clip(
            user_id=1,
            file_content=clip_data,
            filename=clip_filename
        )
        user_sas = self.blob_service.get_user_sas(1)
        container_client = ContainerClient.from_container_url(user_sas["sas_url"])
        for blob in container_client.list_blobs(name_starts_with=user_sas["prefix"]):
                print("Nom du blob :", blob.name)
    
                # Télécharger chaque blob
                blob_client = container_client.get_blob_client(blob)
                with open(blob.name.split('/')[-1], "wb") as f:  # sauvegarde local avec le nom du fichier
                    f.write(blob_client.download_blob().readall())



        
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
        