import json
import os
import requests
import subprocess
import logging
from datetime import datetime, timezone
">"
class TwitchApi:
    """
    Handles Twitch API interactions for authentication, video fetching, and downloading.
    """

    BASE_URL = "https://api.twitch.tv/helix"

    def __init__(self, clientId, clientSecret):
        """
        Initialize TwitchApi instance and authenticate.

        :param clientId: Twitch application client ID.
        :param clientSecret: Twitch application client secret.
        """
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.accessToken = self.authenticate()
       
    def authenticate(self):
        """
        Authenticate and get an app access token.

        :return: Access token as a string.
        """
        
        url = "https://id.twitch.tv/oauth2/token"
        payload = {
            "client_id": self.clientId,
            "client_secret": self.clientSecret,
            "grant_type": "client_credentials"
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        token = response.json()["access_token"]
        logging.info("Successfully authenticated with Twitch API.")
        return token

    def getHeaders(self):
        """
        Generate headers for Twitch API requests.

        :return: Dictionary of headers.
        """
        return {
            "Client-Id": self.clientId,
            "Authorization": f"Bearer {self.accessToken}"
        }

    def getUserId(self, username):
        """
        Fetch the user ID for a given Twitch username.

        :param username: Twitch username.
        :return: User ID as a string, or None if not found.
        """
        url = f"{self.BASE_URL}/users"
        params = {"login": username}
        response = requests.get(url, headers=self.getHeaders(), params=params)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                return data[0]["id"]
        logging.error(f"Failed to fetch user ID for {username}: {response.text}")
        return None


    def getGameId(self,game_name):

        url = f"{self.BASE_URL}/games"
        params = {"name": game_name}
        response = requests.get(url, headers=self.getHeaders(), params=params)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                return data[0]["id"]
        logging.error(f"Failed to fetch user ID for {game_name}: {response.text}")
        return None

    def getVideos(self, userId, filters=None):
        """
        Fetch videos for a given Twitch user based on filters.

        :param userId: Twitch user ID.
        :param filters: Dictionary of filters (e.g., views, duration).
        :return: List of video metadata dictionaries.
        """
       
        url = f"{self.BASE_URL}/videos"
        params = {"user_id": userId}
        if filters:
            params.update(filters)
        response = requests.get(url, headers=self.getHeaders(), params=params)
     
        if response.status_code == 200:
            return response.json().get("data", [])
        logging.error(f"Failed to fetch videos for user {userId}: {response.text}")
        return []
    


    def getClips(self, userId, filters=None,games=[], min_duration=0, max_duration=60, min_views=0): 
        """
        Fetch clips for a given Twitch user based on filters.

        :param userId: Twitch user ID.
        :param filters: Dictionary of filters (e.g., started_at, game_id).
        :return: List of clips metadata dictionaries.
        """

        url = f"{self.BASE_URL}/clips"
        params = {"broadcaster_id": userId}
    
        if filters:
            # If ended date not specified, set it to current date and time.
            if(filters['started_at'] != None  and 'ended_at' not in filters):
                filters['ended_at'] = datetime.now(timezone.utc).isoformat()
                print(filters)
            params.update(filters)

        response = requests.get(url, headers=self.getHeaders(), params=params)
        if response.status_code == 200:
            clips_data =  response.json().get("data", [])
            # Filter clips based on games list provided in the argument
            if (len(games) > 0 ):
                clips_data = [clip for clip in clips_data if clip["game_id"] in games ]
            # Filter clips based on duration and views
            clips_data = [clip for clip in clips_data if min_duration <= clip['duration'] <= max_duration  and clip["view_count"] >= min_views]
                       
            return clips_data
        logging.error(f"Failed to fetch clips for user {userId}: {response.text}")
        return []


    def downloadClipWithAudio(self, clips , savePath="clips"):
        """
        Download a Twitch clip with audio using Streamlink.

        :param clip: Dictionary containing clip metadata.
        :param savePath: Directory to save the downloaded clip.
        """
       
        os.makedirs(savePath, exist_ok=True)
        for clip in clips:
            videoUrl = clip["url"]
            fileName = f"{savePath}/{clip['broadcaster_name']}_{clip['title']}.mp4"

            # Use streamlink to download the clip with audio
            command = [
                "streamlink",
                videoUrl,
                "best",
                "-o",
                fileName
            ]
          
            try:
                subprocess.run(command, check=True)
                logging.info(f"Clip successfully downloaded: {fileName}")
            except subprocess.CalledProcessError as error:
                logging.error(f"Failed to download clip {clip['id']} ({error})")