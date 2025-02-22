import cv2
import logging
import numpy as np


class WebCamProcessor:

    def __init__(self,clip):
        self.clip = cv2.VideoCapture(clip)

        ret, self.first_frame = self.clip.read()
        if not ret:
            raise ValueError("Erreur : Impossible de lire le premier cadre de la vidéo.")
        

        
        self.web_cam_coordinate = []
        self.web_cam_frame = self.get_web_cam_frame_by_coordinate
        self.clip_width = int(self.clip.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.clip_height = int(self.clip.get(cv2.CAP_PROP_FRAME_HEIGHT))



    """ Get the web cam coordinate MANUALLY  """
    def get_clicked_coordinate(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
           self.web_cam_coordinate.append((x,y))
    
    def get_point_manually(self):
        ret, self.frame = self.clip.read()
        if not ret:
            print("Erreur : Impossible de capturer une image.")
            return []
        cv2.namedWindow("Frame",cv2.WINDOW_NORMAL)
        cv2.imshow("Frame", self.frame)
        cv2.setMouseCallback("Frame", self.get_clicked_coordinate)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or len(self.web_cam_coordinate) == 4:  # Quitter avec ESC
                break

        cv2.destroyAllWindows()
        return self.web_cam_coordinate
    

    """ Get Web Cam coordinate with face recongition"""
    def detect_faces(self):
            """ Détecte les visages avec un modèle DNN plus précis. """
            
            # Chemins corrects des fichiers du modèle
            prototxt_path = "Edit\\sample\\deploy.prototxt"
            model_path = "Edit\\sample\\res10_300x300_ssd_iter_140000.caffemodel"

            # Charger le modèle
            net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        

            for i in range(600):
                ret, frame = self.clip.read()
                if not ret:
                    break
                
                # Récupérer la taille de l'image
                h, w = frame.shape[:2]

                # Préparer l'image pour le réseau de neurones
                blob = cv2.dnn.blobFromImage(frame, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))

                # Envoyer l'image dans le réseau de neurones
                net.setInput(blob)
                detections = net.forward()

                # Traiter les résultats
                for i in range(detections.shape[2]):
                    confidence = detections[0, 0, i, 2]
                    if confidence > 0.5:
                        box = detections[0, 0, i, 3:7] * [w, h, w, h]
                        x, y, x2, y2 = box.astype("int")
                        cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)
                        # max to not have negative values
                        self.web_cam_coordinate.extend([max(0,y - 70),y2 + 70 ,max(0,x - 130),x2 + 130])
                        return
            
                    
            
                    




    """ Get Frame of the web cam using coordinate"""

    def get_web_cam_frame_by_coordinate(self):
        if len(self.web_cam_coordinate) != 4:
            raise ValueError("Erreur : Les coordonnées sont pas renseigner ou manquant.")

        frame = self.first_frame[self.web_cam_coordinate[0]:self.web_cam_coordinate[1], self.web_cam_coordinate[2]:self.web_cam_coordinate[3]]

        return frame
    


    