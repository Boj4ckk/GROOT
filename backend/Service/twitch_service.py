from datetime import datetime, timezone
import logging
from Adapter.twitch_api import TwitchApi
import os

class TwitchService:

    def __init__(self):
        self.twitch_api = TwitchApi(os.getenv("TWITCH_CLIENT_ID"), os.getenv("TWITCH_CLIENT_SECRET"))

    def get_clips(self, streamer_name, filters=None,games=[], min_duration=0, max_duration=60, min_views=0):

        user_id = self.twitch_api.getUserId(streamer_name)
        if not user_id:
            logging.error(f"Streamer {streamer_name} not found ! ")
            return []
        
        if(filters['started_at'] != None  and 'ended_at' not in filters):
                filters['ended_at'] = datetime.now(timezone.utc).isoformat()
        

        fetched_clips = self.twitch_api.getClips(user_id,filters)

        clips_data = [
            clip for clip in fetched_clips
            if min_duration <= clip['duration'] <= max_duration
            and clip["view_count"] >= min_views
        ]
        
        games_id_list = []
        for game in games:
             if len(game) > 0:
                games_id_list.append(self.twitch_api.getGameId(game))
             
        if (len(games_id_list) > 0 ):
            clips_data = [
                 clip for clip in clips_data
                 if clip["game_id"] in games_id_list
            ]

        return clips_data
    

    def sort_streamers_list_by_followers(self,streamers_list):
        streamers_followers_count = []

        for streamer in streamers_list:
            streamer_followers = self.twitch_api.getFollowerCount(streamer["id"])
            if streamer_followers == None:
                streamer_followers = 0
            streamers_followers_count.append((streamer["display_name"],streamer_followers))

        streamers_followers_count.sort(key=lambda x: x[1], reverse=True)
        return [streamers_tuple[0] for streamers_tuple in streamers_followers_count]
    
    def get_game_box_art(self, game_id):
        box_art_url = self.twitch_api.getGameboxArtUrl(game_id)
        return box_art_url

       



        

         
         
        
        
    
        

