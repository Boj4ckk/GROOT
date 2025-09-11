import logging
import os
from Service.clip_services import ClipServices
from flask import request, jsonify
from api.Twitch.Twitch_api import TwitchApi
from config.azure_config import SessionLocal


class ClipController():


    @staticmethod
    def fetch_clip(data=None):
        if data is None:
            data_received = request.json
            streamer_name = data_received.get('streamer_name')
            game = data_received.get('game')
            min_views = data_received.get('min_views')
            min_duration = 0
            max_duration = int(data_received.get('max_duration'))
            min_date_release = data_received.get('min_date_release') + "T00:00:00Z"
            max_date_release = data_received.get('max_date_release') + "T00:00:00Z"
            number_of_clips = data_received.get('number_of_clips')

            twitch_instance  =  TwitchApi(os.getenv("TWITCH_CLIENT_ID"),os.getenv("TWITCH_CLIENT_SECRET"))  
            TwitchApi.getHeaders(twitch_instance)
            

            id_twitch_streamer = TwitchApi.getUserId(twitch_instance, streamer_name)
           
            fetched_clips = TwitchApi.getClips(
                twitch_instance,
                id_twitch_streamer,
                filters={"started_at": min_date_release, "ended_at": max_date_release, "first": number_of_clips},
                min_duration=min_duration,
                max_duration=max_duration,
                min_views=min_views,
            )
            TwitchApi.downloadClipWithAudio(twitch_instance,fetched_clips)
            
        with SessionLocal() as db:
            for clip in fetched_clips:
                
                clip_service = ClipServices(db)
                clip = clip_service.download_and_store_clip(clip)
                

            return jsonify({
                "message" :"clip added !",

            }), 201
    

    @staticmethod
    def send_clips_urls():
        if request.method == 'OPTIONS' : #requete options au back end avant POST quand on fait une requete post 
            return '', 200
        try :
            liste_urls = [] 
            path = os.path.join("backend","data","fetch_clips")
            for file in os.listdir(path) :   
                liste_urls.append(file)
            return jsonify ({"clipsUrls": liste_urls})
        except Exception as e : 
            logging.error(f"Erreur lors de l'envoie de l'url des clips : {e}")
            return ({"error": "Erreur lors de l'envoi de l'url des clips"}), 500

        