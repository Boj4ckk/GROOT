
# src/edit/video_processor.py

from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
from PIL import Image, ImageFilter
import logging
import numpy as np
import cv2


# Setting up logging for tracking the processing steps
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class VideoProcessor:

    def __init__(self,format_type,clip):
        self.format_type = format_type
        self.clip = cv2.VideoCapture(clip)
        self.clip_width = int(self.clip.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.clip_height = int(self.clip.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.web_cam_coordinate = []
        self.web_cam_frame = self.get_web_cam_frame_by_coordinate
  
    def extract_frames(self):
        frames_list = []
        clip = self.clip

        if not clip.isOpened():
            print("Erreur : Impossible d'ouvrir la vidéo.")
            return

        while True:
            ret, frame = clip.read()
            if not ret:
                break  # Fin de la vidéo

            frames_list.append(frame)  # Ajouter la frame à la liste

        clip.release()
        return frames_list

    def get_first_frame(self):
        if not self.clip.isOpened():
            logging.error("Erreur: Impossible d'ouvrir la vidéo.")
            return None
        ret, first_frame = self.clip.read()
        if not ret:
            logging.error("Erreur: Impossible de lire la première frame")
            return None  # Retourne None si l'image n'a pas pu être lue

        return first_frame
    def get_clip(self):
        return self.clip

    def get_clip_coordinate(self):
        return (self.clip_width, self.clip_height)
    
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
    
    
    """
    def sub_frame(self):
        sub_frame_list = []
        frame = self.get_first_frame()  # Récupère la frame complète

        height, width = self.clip_height, self.clip_width  # Dimensions de la frame

        third_width = width // 3  # Divise la largeur en 3 parties égales
        third_height = height // 3  # Divise la hauteur en 3 parties égales

        # Prendre uniquement la partie gauche et droite
        left_part = frame[:, 0:third_width]  # Partie gauche
        right_part = frame[:, 2 * third_width:width]  # Partie droite

        # Découper chaque partie en 3 sous-parties en hauteur
        for i in range(3):
            sub_frame_left = left_part[i * third_height:(i + 1) * third_height, :]
            sub_frame_right = right_part[i * third_height:(i + 1) * third_height, :]

            sub_frame_list.append(sub_frame_left)  # Ajouter la sous-image gauche
            sub_frame_list.append(sub_frame_right)  # Ajouter la sous-image droite

        return sub_frame_list  # Retourne la liste des 6 sous-images

    """

    def detect_faces(frame):
        """ Détecte les visages avec un modèle DNN plus précis. """
        
        # Chemins corrects des fichiers du modèle
        prototxt_path = "Edit\\sample\\deploy.prototxt"
        model_path = "Edit\\sample\\res10_300x300_ssd_iter_140000.caffemodel"

        # Charger le modèle
        net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

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

        return frame


    def get_web_cam_frame_by_coordinate(self):
        if len(self.web_cam_coordinate) != 4:
            raise ValueError("Erreur : Les coordonnées sont pas renseigner ou manquant.")

        points = np.array(self.web_cam_coordinate, dtype=np.int32)
    
        x_min = np.min(points[:, 0])
       
        y_min = np.min(points[:, 1])
        x_max = np.max(points[:, 0])
        y_max = np.max(points[:, 1])

        # Découper la sous-frame
        sub_frame = self.get_first_frame()[y_min:y_max, x_min:x_max]

        return sub_frame
    






    
    


        

            
            