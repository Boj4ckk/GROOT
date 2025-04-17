# src/config.py
import os
from dotenv import load_dotenv
import mysql.connector.pooling as pooling

load_dotenv()


class Config:
    
    DB_CONFIG = {
        "user": "yazhug", 
        "password": "azureadmin@25", 
        "host": 'twitok-serveur.mysql.database.azure.com', 
        "database": "twitok-database",
        "ssl_ca": "CA\BaltimoreCyberTrustRoot.crt.pem", # certificat pour azure 
    }


    @staticmethod
    def init_pool():
        return pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **Config.DB_CONFIG)


    CLIENT_ID = "k49vl0y998fywdwlvzu48b1u4kth5f"    
    CLIENT_SECRET = "cnhhv1qwdxfjc8smmtjnbieg5c9p57"
    # Twitch API credentials
    TWITCH_CLIENT_ID = "hluyhcffqf78xpz43fpfkq7ww8nuw2"  # Replace with your Twitch API Client ID
    TWITCH_CLIENT_SECRET = "w2dnf2qwh9v5oisvv9dcn97oh5zz8k" # Replace with your Twitch API Client Secret
    TWITCH_ACCESS_TOKEN = ""  # Replace with a valid OAuth token

    # TikTok automation setup
    TIKTOK_DRIVER_PATH = "./drivers/chromedriver"  # Path to ChromeDriver for Selenium
    TIKTOK_COOKIES_PATH = "./src/tiktok_cookies.pkl"  # Path to saved TikTok cookies
    
    TIKTOK_USERNAME = "twitok_bot_2" # Replace with your TikTok Username
    TIKTOK_PASSWORD = "twitok_bot_2.0" # Replace with your TikTok Password

    # # File paths for clip management
    # METADATA_FILE = "./src/metadata/clips_metadata.json"  # File to store Twitch video metadata
    # USERS_FILE = "./src/metadata/user.json"
    DOWNLOAD_FOLDER_RELATIVE = "data/clip_ready_to_upload/"  # Folder to store raw Twitch clips
    DOWNLOAD_FOLDER_ABSOLUTE = os.path.abspath(DOWNLOAD_FOLDER_RELATIVE) + "/" # Folder to store raw Twitch clips


