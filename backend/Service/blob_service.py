
from datetime import datetime, timedelta
import os
import subprocess
from azure.storage.blob import BlobServiceClient, generate_container_sas, ContainerSasPermissions, ContainerClient,BlobSasPermissions, generate_blob_sas
class BlobStorageService:

    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        )
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        self.account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        self.key = os.getenv("AZURE_STORAGE_KEY")

    def upload_clip(self,user_id,file_content,filename):

        blob_path = f"user_{user_id}/fetched_clips/{filename}"
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_path
        )
        # Obligatoire pour telecharger le clip issue de la page (twitch donne le lien vers la page twitch du clip pas l'objet clip en lui meme)
        process = subprocess.Popen(
            ["streamlink","--stdout",file_content["url"],"best"],
            stdout=subprocess.PIPE
        )

        #enregistre dans le blob la sortie du process de streamlink (le clip video)
        blob_client.upload_blob(process.stdout,overwrite=True)
        return blob_path
    
    def get_user_sas(self,user_id):

        sas_token = generate_container_sas(
            account_name=self.account_name,
            container_name=self.container_name,
            account_key=self.key,
            permission=ContainerSasPermissions(read=True, list=True),
            expiry = datetime.utcnow() + timedelta(hours=1)
        )

        sas_url = f"https://{self.account_name}.blob.core.windows.net/{self.container_name}?{sas_token}"
        return {
            "sas_url" : sas_url,
            "prefix" : f"user_{user_id}/"
        }
    def get_user_fetched_clips(self,user_id):
        sas_url = self.get_user_sas(user_id)["sas_url"]
        url_prefix = self.get_user_sas(user_id)["prefix"]

        container_client = ContainerClient.from_container_url(sas_url)
        blobs = container_client.list_blobs(name_starts_with=f"user_{user_id}/fetched_clips/")
        fetched_clips = []
        for blob in blobs:
            sas_token = generate_blob_sas(
                account_name="clipsstorage091283",  # Votre nom de compte
                container_name="clips",
                blob_name=blob.name,
                account_key=self.key,  # Votre clé de compte
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(minutes=15)  # Token valable 15 min
            )
            secure_url = f"https://clipsstorage091283.blob.core.windows.net/clips/{blob.name}?{sas_token}"
            fetched_clips.append({
                "name" : blob.name.replace(url_prefix,''),
                "url": secure_url,
                "size": blob.size,
                "created_date": blob.creation_time

            })
          
        return fetched_clips
    

   