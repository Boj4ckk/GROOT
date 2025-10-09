from flask import jsonify, request
from middlewares.auth_middleware import jwt_required
from Service.blob_service import BlobStorageService
import os

class BlobController():
    @staticmethod
    @jwt_required
    def delete_file_from_blob(data=None):
        if data is None:
            blob_url = request.json.get("url")
            blob_service = BlobStorageService()
            url_parts = blob_url.split('?')[0]  # Enlever le token SAS
        
            blob_path = url_parts.split(f'/{blob_service.container_name}/')[-1]
            response = blob_service.delete_file_in_blob(blob_path)
        return jsonify({
            "message" :"file deleted from blob"
        })
            