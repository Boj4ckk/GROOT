
# src/edit/video_processor.py

from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
from Edit.Web_cam_processor import WebCamProcessor
from PIL import Image, ImageFilter
import logging
import uuid
import numpy as np
import cv2
import os 
import re



# Setting up logging for tracking the processing steps
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename='GROOT\\logs\\editing.log')


"""
    VideoProcessor class for processing video clips.
"""
class VideoProcessor:

    """
      Initialize the VideoProcessor with the given clip URL.

      Parameters:
        - clip_url (str) : Local path of the clip.
        - clip_id  (str) : Unique clip id.
        - clip_Video (MoviePy Video) : Video object from the clip _url.
        - clip_width(int), clip_height(int) : Video clip size.
        - web_cam_video (MoviePy Video) : Will hold the web cam video from the orignal video clip.
        - content_video (MovePy Video) : Will hold the content video from the original video clip .
    """
    def __init__(self,clipUrl):
        
        self.clip_url =  clipUrl
        self.clipId = str(uuid.uuid4())
        self.clipVideo = VideoFileClip(self.clip_url)
        self.clip_width , self.clip_height = self.clipVideo.size
        self.web_cam_video = None 
        self.content_video = None
  
    """
        Extract all frames (images) from the video clip and return them as a list of frames.
    """
    def extract_frames(self):
        frames_list = []  # List to store all the extracted frames
        clip = self.clipVideo  # Video clip object

        if not clip.isOpened():
            logging.error("Error: failed to open the clip.")  # Error logging if clip can't be opened
            return

        while True:
            ret, frame = clip.read()  # Read each frame from the video
            if not ret:
                break  # Exit if no more frames are available (end of video)

            frames_list.append(frame)  # Append the frame to the frames list

        clip.release()  # Release the clip once done
        return frames_list  # Return the list of frames

    """
    Get the first frame of the video clip (returns a single frame).
    """
    def get_first_frame(self):
        """
        Retrieves the first frame of the video.
        
        Returns:
        first_frame (numpy.array): The first frame of the video.
        """
        if not self.clipVideo.isOpened():
            logging.error("Error: Unable to open video.")  # Error logging if the video can't be opened
            return None
        ret, first_frame = self.clipVideo.read()  # Read the first frame
        if not ret:
            logging.error("Error: Unable to read the first frame.")  # Error if the frame can't be read
            return None  # Return None if the frame can't be read

        return first_frame  # Return the first frame

    """
    Get the video clip object (returns MoviePy Video).
    """
    def get_clip(self):
        """
        Returns the video clip object.
        
        Returns:
        clipVideo (VideoFileClip): The video clip object.
        """
        return self.clipVideo

    """
    Extract the webcam video from the video clip, assigns it to self.web_cam_video.
    """
    def extract_web_cam(self):
        """
        Processes the video to extract the webcam section and save it as a separate video.
        """
        web_cam_processor = WebCamProcessor(self.clip_url)  # Initialize WebCamProcessor to handle webcam extraction
        web_cam_processor.detect_faces()  # Detect faces in the video

        web_cam_coordinate = web_cam_processor.web_cam_coordinate  # Get the coordinates for the webcam section
        # Crop the webcam section from the video using the detected coordinates
        web_cam_clip = self.clipVideo.crop(x1=web_cam_coordinate[2], y1=web_cam_coordinate[0], 
                                           x2=web_cam_coordinate[3], y2=web_cam_coordinate[1])

        web_cam_clip_path = f'GROOT/Edit/in_process_clips/{self.clipId}_cam.mp4'  # Path for saving the webcam clip
        web_cam_audio_clip_path = f'GROOT/Edit/in_process_clips/{self.clipId}audio_cam.mp3'  # Path for saving the webcam audio

        # Write the cropped webcam video and audio to file
        web_cam_clip.write_videofile(web_cam_clip_path, codec="libx264", fps=30)
        web_cam_clip.audio.write_audiofile(web_cam_audio_clip_path)

        # Load the webcam video clip into self.web_cam_video for later use
        self.web_cam_video = VideoFileClip(web_cam_clip_path)

    """
    Crop the video to fit a short format (TikTok-style: 9:16).
    
    Parameters:
    target_width (int): The target width of the final video.
    target_height (int): The target height of the final video.
    """
    def crop_to_short_format(self, target_width, target_height):
        """
        Crops and resizes the video to a short format (typically for TikTok).
        """
  
        original_ratio = self.clipVideo.w / self.clipVideo.h  # Aspect ratio of the original video
        target_ratio = 9 / 16  # Target aspect ratio for TikTok (short format)

        if original_ratio > target_ratio:
            # Video is too wide, crop from the sides
            new_width = int(self.clipVideo.h * target_ratio * 1.4)
            x1 = (self.clipVideo.w - new_width) // 2  # Calculate cropping coordinates
            x2 = x1 + new_width
            y1, y2 = 0, self.clipVideo.h
        else:
            # Video is too tall, crop from the top and bottom
            new_height = int(self.clipVideo.w / target_ratio)
            y1 = (self.clipVideo.h - new_height) // 2  # Calculate cropping coordinates
            y2 = y1 + new_height
            x1, x2 = 0, self.clipVideo.w

        # Perform the crop operation
        cropped_video = self.clipVideo.crop(x1=x1, y1=y1, x2=x2, y2=y2)

        # Path for saving the cropped content video
        content_clip_path = f"GROOT/Edit/in_process_clips/{self.clipId}_content.mp4"
        content_audio_clip_path = f"GROOT/Edit/in_process_clips/{self.clipId}audio_content.mp3"
        # Resize the cropped video to the exact target dimensions
        content_clip = cropped_video.resize((target_width, int((2 * target_height) / 3)))

        # Write the resized content video and audio to file
        content_clip.write_videofile(content_clip_path, codec="libx264", fps=30)
        content_clip.audio.write_audiofile(content_audio_clip_path)

        # Store the processed content video
        self.content_video = VideoFileClip(content_clip_path)

    """
    Process the video by extracting the webcam, cropping the content to a short format, and combining them.
    
    Parameters:
    target_width (int): The target width of the final video.
    target_height (int): The target height of the final video.
    """
    def process_video(self, target_width, target_height):
        """
        Main method to process the video: extract webcam, crop to short format, and combine clips.
        """
        # Removing unnecessary audio files from temporary files
        for file in os.listdir("."):
            audio_file_regex = re.compile(r"TEMP_MPY_wvf_snd\.mp3")
            if re.search(audio_file_regex, file) is not None:
                file_path = os.path.join(".\\", file)
                logging.info(f"Removing file : {file_path}\n")
                os.remove(file_path)

        # Path for saving the processed video
        processed_video_path = f'GROOT/Edit/processed_clips/{self.clipId}_processed.mp4'

        logging.info("Extracting webcam from clip..\n")
        self.extract_web_cam()  # Extract webcam section
        logging.info("Crop clip to short format..")
        self.crop_to_short_format(target_width, target_height)  # Crop content to the short format

        # Create an empty clip for background
        empty_clip = ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=self.content_video.duration)

        # Resize the webcam video
        web_cam = self.web_cam_video.resize(width=1080)
        if web_cam.h > 640:
            web_cam = web_cam.crop(y1=0, y2=640)  # Crop the webcam video if it's too tall
        web_cam = web_cam.set_position(("center", 0))  # Position the webcam video in the center

        # Set the position for the content video
        content = self.content_video.set_position(("center", 1920 - 1280))
        final_clip = CompositeVideoClip([empty_clip, content, web_cam])  # Combine all clips into a final clip
        logging.info("Writing new clip composite from webcam and content..")
        # Write the final composite video to file
        final_clip.write_videofile(processed_video_path, codec="libx264", fps=30)

        # Cleaning up temporary files
        logging.info("Cleaning in_process_clips...\n")
        for file in os.listdir("GROOT\\Edit\\in_process_clips"):
            file_path = os.path.join("GROOT\\Edit\\in_process_clips", file)
            logging.info(f"Removing file : {file_path}\n")
            os.remove(file_path)