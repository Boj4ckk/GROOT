
# src/edit/video_processor.py

from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
from Edit.Web_cam_processor import WebCamProcessor
from PIL import Image, ImageFilter
import logging
import uuid
import numpy as np
import cv2
import os 



# Setting up logging for tracking the processing steps
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class VideoProcessor:

    def __init__(self,clipUrl):
        
        self.clip_url =  clipUrl
        self.clipId = str(uuid.uuid4())
        self.clipVideo = VideoFileClip(self.clip_url)
        self.clip_width , self.clip_height = self.clipVideo.size
        self.web_cam_video = None 
        self.content_video = None

  
    def extract_frames(self):
        frames_list = []
        clip = self.clipVideo

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
        if not self.clipVideo.isOpened():
            logging.error("Erreur: Impossible d'ouvrir la vidéo.")
            return None
        ret, first_frame = self.clipVideo.read()
        if not ret:
            logging.error("Erreur: Impossible de lire la première frame")
            return None  # Retourne None si l'image n'a pas pu être lue

        return first_frame
    def get_clip(self):
        return self.clipVideo

    def get_clip_coordinate(self):
        return (self.clip_width, self.clip_height)
    

    def extract_web_cam(self):
        web_cam_processor = WebCamProcessor(self.clip_url)
        web_cam_processor.detect_faces()

       

        web_cam_coordinate = web_cam_processor.web_cam_coordinate

        web_cam_clip = self.clipVideo.crop(x1=web_cam_coordinate[2],y1=web_cam_coordinate[0],x2=web_cam_coordinate[3],y2=web_cam_coordinate[1])

        web_cam_clip_path = f'in_process_clips/{self.clipId}_cam.mp4'
        web_cam_clip.write_videofile(web_cam_clip_path,codec="libx264",fps=30)

        self.web_cam_video = VideoFileClip(web_cam_clip_path)

    

    def crop_to_short_format(self, target_width, target_height):
        original_ratio = self.clipVideo.w / self.clipVideo.h
        target_ratio = 9 / 16  # Format TikTok

        if original_ratio > target_ratio:
            # Trop large, on coupe sur les côtés
            new_width = int(self.clipVideo.h * target_ratio * 1.4)
            x1 = (self.clipVideo.w - new_width) // 2
            x2 = x1 + new_width
            y1, y2 = 0, self.clipVideo.h
        else:
            # Trop haut, on coupe en haut et en bas
            new_height = int(self.clipVideo.w / target_ratio)
            y1 = (self.clipVideo.h - new_height) // 2
            y2 = y1 + new_height
            x1, x2 = 0, self.clipVideo.w

        # Rogner la vidéo
        cropped_video = self.clipVideo.crop(x1=x1, y1=y1, x2=x2, y2=y2)

        content_clip_path = f"in_process_clips/{self.clipId}_content.mp4"
        # Redimensionner exactement à 1080x1920
        content_clip = cropped_video.resize((target_width, int((2 * target_height) / 3)))
        content_clip.write_videofile(content_clip_path, codec="libx264", fps=30)

        self.content_video = VideoFileClip(content_clip_path)

    def process_video(self,target_width,target_height):
        """ Ajuster la webcam : même largeur que la vidéo de contenu, et 1/3 de sa hauteur """



        processed_video_path = f'Processed_clips/{self.clipId}_processed.mp4'
        empty_clip = ColorClip(size=(1080,1920), color=(0,0,0),duration=self.clipVideo.duration)

        self.extract_web_cam()
        self.crop_to_short_format(target_width,target_height)
        web_cam = self.web_cam_video.resize(width=1080)
        if web_cam.h > 640:
            web_cam = web_cam.crop(y1=0, y2=640)
        else:
            web_cam = web_cam
        web_cam = web_cam.set_position(("center", 0))


        content = self.content_video.set_position(("center",1920-1280))
        final_clip = CompositeVideoClip([empty_clip,content, web_cam])
        final_clip.write_videofile(processed_video_path, codec="libx264", fps=30)

        os.remove(f'in_process_clips/{self.clipId}_cam.mp4')
        os.remove(f'in_process_clips/{self.clipId}_content.mp4')
    

    


   






    
    


        

            
            