
import requests
import logging
class TwitchApi:
    """
    Handles Twitch API interactions for authentication, video fetching, and downloading.
    """

    BASE_URL = "https://api.twitch.tv/helix"
    logging.basicConfig(filename="logs\editing.log",  level=logging.DEBUG,format="%(asctime)s - %(levelname)s - %(message)s",  datefmt="%Y-%m-%d %H:%M:%S")

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
    


    def getClips(self, userId, filters=None): 
        """
        Fetch clips for a given Twitch user based on filters.

        :param userId: Twitch user ID.
        :param filters: Dictionary of filters (e.g., started_at, game_id).
        :return: List of clips metadata dictionaries.
        """
        """
        logging.info("\n\nCleaning in_process_clips...\n\n")
        path = os.path.join("backend","data","fetch_clips")
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            logging.info(f"\n\nRemoving file : {file_path}\n")
            os.remove(file_path)
       """
        url = f"{self.BASE_URL}/clips"
        params = {"broadcaster_id": userId,}

        if filters:
            params.update(filters)

        response = requests.get(url,headers=self.getHeaders(), params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        logging.error(f"Failed to fetch clips for user {userId}: {response.text}")
        return []