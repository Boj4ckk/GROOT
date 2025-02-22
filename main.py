# src/main.py
import os
import logging
from Api.Twitch.Twitch_api import TwitchApi
import json

CLIENT_ID = "k49vl0y998fywdwlvzu48b1u4kth5f"
CLIENT_SECRET = "cnhhv1qwdxfjc8smmtjnbieg5c9p57"
'samueletienne'

'It Takes Two  : 518213'
'Valorant : 516575'
'Fortnite : 33214'

t1  =  TwitchApi(CLIENT_ID,CLIENT_SECRET)                 
TwitchApi.getHeaders(t1)

idt = TwitchApi.getUserId(t1, "samueletienne")
data = TwitchApi.getClips(
    t1,
    idt,
    games=['516575', '518213'],
    filters={"started_at": "2025-01-30T00:00:00Z", "ended_at": "2025-02-09T00:00:00Z", "first": 10},
    min_duration=20,
    max_duration=60
)



# Affichage propre des données sous forme JSON
print(json.dumps(data,indent=2))












