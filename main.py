# src/main.py
import os
import logging
from Api.Twitch.Twitch_api import TwitchApi
from Api.Tiktok.tiktok_api import TiktokApi
from Edit.Video_processor import VideoProcessor
import json

CLIENT_ID = "k49vl0y998fywdwlvzu48b1u4kth5f"
CLIENT_SECRET = "cnhhv1qwdxfjc8smmtjnbieg5c9p57"
'samueletienne'

'It Takes Two  : 518213'
'Valorant : 516575'
'Fortnite : 33214'



ti1 = TiktokApi()

ti1.startDriver()
ti1.login("yazkilito@gmail.com","Didoleboss12$")
ti1.uploadVideo("C:\\Users\\User\\Desktop\\Cours\\Framework Web\\GROOT\\Processed_clips\\97dc3e85-7503-4d78-ba66-e5e87d3205bc_processed.mp4","test1")












