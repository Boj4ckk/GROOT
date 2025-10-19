
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

    def upload_in_blob(self,file_content,blob_path):

        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_path
        )

        try:
            # Obligatoire pour telecharger le clip issue de la page (twitch donne le lien vers la page twitch du clip pas l'objet clip en lui meme)
            process = subprocess.Popen(
                ["streamlink","--stdout",file_content["url"],"best"],
                stdout=subprocess.PIPE
            )

            #enregistre dans le blob la sortie du process de streamlink (le clip video)
            blob_client.upload_blob(process.stdout,overwrite=True)
            return {"success": True, "blob_path" : blob_path}
        except Exception as e:
            return {"succes": False, "error": str(e)}
     
    
    def delete_file_in_blob(self,blob_path):
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_path
        )
        try:
            blob_client.delete_blob(delete_snapshots="include")
            return {"success":True, "message": f"Blob {blob_path} Deleted !"}
        except Exception as e:
            return {"success": False, "message": f"Error {str(e)}"}

    
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

    def generate_blob_sas_url(self, blob_name):
        if not all([self.account_name, self.key, self.container_name, blob_name]):
            print("Erreur: Informations manquantes")
            return None
        
        try:
            sas_token = generate_blob_sas(
                account_name=self.account_name,
                container_name=self.container_name,
                blob_name=blob_name,
                account_key=self.key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=1)
            )
            secure_url = f"https://{self.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}?{sas_token}"
            return secure_url
        except Exception as e:
            print(f"Erreur lors de la génération de l'url sas pour {blob_name}: {e}")
            return None
        

   