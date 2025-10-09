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

    @staticmethod
    def search_games():
        query = request.args.get('q', '')
        twitch_service = TwitchService()
        games = twitch_service.twitch_api.getGames(query)
        return jsonify({"games": games})
    
    
    @staticmethod
    def search_streamers():
        query = request.args.get('q', '')
        twitch_service = TwitchService()
        un_sorted_streamers_list = twitch_service.twitch_api.getStreamers(query)
   
        return jsonify({"streamers": un_sorted_streamers_list})
    
    @staticmethod
    def verify_streamer():
        query = request.args.get('username', '')
        if not query:
            return jsonify({"exists": False, "error": "Username required"}), 400
        
        twitch_service = TwitchService()
        streamers_list = twitch_service.twitch_api.getStreamers(query)
        
        # Vérifier si le nom exact existe dans la liste (insensible à la casse)
        exists = any(streamer.lower() == query.lower() for streamer in streamers_list)
        
        return jsonify({"exists": exists})