
from flask import jsonify, request
from Service.twitch_service import TwitchService
from Service.clip_services import ClipServices
from middlewares.auth_middleware import jwt_required
from config.azure_config import SessionLocal


class TwitchController():

    @staticmethod
    @jwt_required
    def fetch_clip(data=None):
        twitch_service = TwitchService()
        if data is None:
            data_received = request.json


            streamer_name = data_received.get('streamer_name')
            game = data_received.get('game')
            min_views = data_received.get('min_views')
            min_duration = 0
            max_duration = int(data_received.get('max_duration'))

            filters = {
                "started_at": data_received.get('min_date_release') + "T00:00:00Z",
                "ended_at":  data_received.get('max_date_release') + "T00:00:00Z", 
                "first": data_received.get('number_of_clips')
            }
           
            fetched_clips = twitch_service.get_clips(
                streamer_name,
                filters,
                game,
                min_duration,
                max_duration,
                min_views
            )

            
        with SessionLocal() as db:
            for clip in fetched_clips:
                
                clip_service = ClipServices(db)
                clip = clip_service.download_and_store_clip(clip)
                

            return jsonify({
                "message" :"clip added !",

            }), 201
