# src/main.py
import os
import logging
from api.Twitch.Twitch_api import TwitchApi
from api.Tiktok.tiktok_api import TiktokApi
from Edit.Video_processor import VideoProcessor
import json

CLIENT_ID = "k49vl0y998fywdwlvzu48b1u4kth5f"
CLIENT_SECRET = "cnhhv1qwdxfjc8smmtjnbieg5c9p57"
'samueletienne'

'It Takes Two  : 518213'
'Valorant : 516575'
'Fortnite : 33214'



t1  =  TwitchApi(CLIENT_ID,CLIENT_SECRET)                 
TwitchApi.getHeaders(t1)

idt = TwitchApi.getUserId(t1, "talmo")
data = TwitchApi.getClips(
    t1,
    idt,
    
    filters={"started_at": "2024-01-30T00:00:00Z", "ended_at": "2025-02-09T00:00:00Z", "first": 3},
    min_duration=20,
    max_duration=60
)

# Affichage propre des données sous forme JSON
TwitchApi.downloadClipWithAudio(t1,data)

for files in os.listdir("C:\\Users\\User\\Desktop\\Cours\\Framework Web\\GROOT\\Clips"):
    v1 = VideoProcessor(f"Clips/{files}")
    v1.process_video(1080,1920)












