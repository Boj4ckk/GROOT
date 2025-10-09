from flask import Blueprint
from Controller.Blob_controller import BlobController



class BlobRoutes:

    blob_bp = Blueprint("blob",__name__)
    blob_bp.route("/delete_file_from_blob",methods=["POST", "GET"])(BlobController.delete_file_from_blob)