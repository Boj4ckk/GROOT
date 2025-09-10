
from datetime import datetime, timedelta
import os
from azure.storage.blob import BlobServiceClient, generate_container_sas, ContainerSasPermissions
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

        blob_client.upload_blob(file_content,overwrite=True)
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
            "prefix" : f"user_{user_id}"
        }