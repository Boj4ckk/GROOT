from flask import Blueprint
from Controller.clip_controller import ClipController



class ClipRoutes:

    clip_bp = Blueprint("clip",__name__)
    clip_bp.route("/recup_infos_clips",methods=["POST"])(ClipController.fetch_clip)