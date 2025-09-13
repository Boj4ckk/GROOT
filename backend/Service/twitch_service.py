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
                 if clip["game_id"] in games
            ]

        return clips_data
        
        
    
        

