# src/main.py

import os
import logging
from Api.Twitch.Twitch_api import TwitchApi
from Edit.Video_processor import VideoProcessor
import time
import json
import threading
import cv2
CLIENT_ID = "k49vl0y998fywdwlvzu48b1u4kth5f"
CLIENT_SECRET = "cnhhv1qwdxfjc8smmtjnbieg5c9p57"
'samueletienne'

'It Takes Two  : 518213'
'Valorant : 516575'
'Fortnite : 33214'


    


v1 = VideoProcessor(1,"Clips\\20250211_DarkNeighborlyKangarooGrammarKing-Oyve7HxhxAm4ikJL_source.mp4")








while True:
        ret, frame = VideoProcessor.get_clip(v1).read()  # Lire une nouvelle frame à chaque boucle
        if not ret:  # Arrêter si la lecture échoue (fin de vidéo)
            break
        cv2.namedWindow("Frame",cv2.WINDOW_NORMAL)
        cv2.imshow("Frame", VideoProcessor.detect_faces(frame))

        # Quitter avec la touche 'ESC'
        if cv2.waitKey(25) & 0xFF == 27:
            break

VideoProcessor.get_clip(v1)  # Libérer la idéo
cv2.destroyAllWindows()  # Fermer la fenêtre








