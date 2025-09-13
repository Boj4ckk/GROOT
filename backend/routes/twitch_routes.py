from flask import Blueprint
from Controller.twitch_controller import TwitchController


class TwitchRoutes:

    twitch_bp = Blueprint("twitch",__name__)
    twitch_bp.route("/recup_infos_clips",methods=["POST"])(TwitchController.fetch_clip)


