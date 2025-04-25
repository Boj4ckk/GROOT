


from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
from backend.Edit.Web_cam_processor import WebCamProcessor

from PIL import Image, ImageFilter
import logging
import uuid
import os 
import re




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
    def __init__(self,clipUrl,webcam_extraction,clip_format):
        
        self.clip_url =  clipUrl
        self.webcam_extraction = webcam_extraction
        self.clip_format = clip_format

        self.clipId = str(uuid.uuid4())
        self.clipVideo = VideoFileClip(self.clip_url)
        self.clip_width , self.clip_height = self.clipVideo.size
        self.web_cam_video = None 
        self.content_video = None
        self.edited_clip_path = None
  
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

        web_cam_clip_path = f'backend\\Edit\\in_process_clips\\{self.clipId}_cam.mp4'  # Path for saving the webcam clip
        web_cam_audio_clip_path = f'backend\\Edit\\in_process_clips\\{self.clipId}audio_cam.mp3'  # Path for saving the webcam audio

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
    def clip_to_target_format(self, target_width, target_height):
        """
        Transforme la vidéo selon le format demandé :
        - Si self.clip_format == "portrait" → recadrage en 9:16 pour TikTok
        - Si self.clip_format == "landscape" → garde la vidéo en format paysage
        """

        content_clip_path = f"backend\\Edit\\in_process_clips\\{self.clipId}_content.mp4"
        content_audio_clip_path = f"backend\\Edit\\in_process_clips\\{self.clipId}_content_audio.mp3"

        if self.clip_format == "portrait":
            # Recadrer en format portrait (9:16)
            original_ratio = self.clip_width / self.clip_height
            target_ratio = 9 / 16  # Format TikTok

            if original_ratio > target_ratio:
                # Trop large → on coupe sur les côtés
                new_width = int(self.clip_height * target_ratio)
                x1 = (self.clip_width - new_width) // 2
                x2 = x1 + new_width
                y1, y2 = 0, self.clip_height
            else:
                # Trop haut → on coupe en haut et en bas
                new_height = int(self.clip_width / target_ratio)
                y1 = (self.clip_height - new_height) // 2
                y2 = y1 + new_height
                x1, x2 = 0, self.clip_width

            cropped_video = self.clipVideo.crop(x1=x1, y1=y1, x2=x2, y2=y2)
            final_video = cropped_video.resize((target_width, target_height))

        if self.clip_format == 'landscape':  # "landscape" (on garde la vidéo telle quelle)
            final_video = self.clipVideo.resize((self.clip_width, self.clip_height))

        # Sauvegarde de la vidéo et de l'audio
        final_video.write_videofile(content_clip_path, codec="libx264", fps=30)
        
        if final_video.audio:
            final_video.audio.write_audiofile(content_audio_clip_path)

        # Stocke la vidéo transformée
        self.content_video = VideoFileClip(content_clip_path)





    def removing_audio_files(self):
        for file in os.listdir("."):
            audio_file_regex = re.compile(r"TEMP_MPY_wvf_snd\.mp3")
            if re.search(audio_file_regex, file) is not None:
                file_path = os.path.join(".\\", file)
                logging.info(f"Removing file : {file_path}\n")
                os.remove(file_path)

    def cleaning_in_process_folder(self):
       
        logging.info("Cleaning in_process_clips...\n")
        for file in os.listdir("backend\\Edit\\in_process_clips"):
            file_path = os.path.join("backend\\Edit\\in_process_clips", file)
            logging.info(f"Removing f   ile : {file_path}\n")
            os.remove(file_path) 


    def cleaning_processed_clips(self):
        logging.info("Cleaning Process_clips...\n")
        for file in os.listdir("twitok_website\\public\\media\\processed_clips"):
            file_path = os.path.join("twitok_website\\public\\media\\processed_clips", file)
            logging.info(f"Removing f   ile : {file_path}\n")
            os.remove(file_path) 

    

    """
    Process the video by extracting the webcam, cropping the content to a short format, and combining them.
    
    Parameters:
    target_width (int): The target width of the final video.
    target_height (int): The target height of the final video.
    """
    def process_video(self, target_width=1080, target_height=1920):
        """
        Main method to process the video: extract webcam, crop to short format, and combine clips.
        """
        # Removing unnecessary audio files from temporary files
        
        self.removing_audio_files()
        self.cleaning_in_process_folder()
        self.cleaning_processed_clips()
        # Path for saving the processed video
        
        processed_video_path = f'twitok_website\\public\\media\\processed_clips\\{self.clipId}_processed.mp4'
        processed_video_path_to_send = f'media\\processed_clips\\{self.clipId}_processed.mp4'
        

        webcam = None
        if self.webcam_extraction ==True:
            logging.info("Extracting webcam from clip..\n")
            self.extract_web_cam()  # Extract webcam section
             # Resize the webcam video
            webcam = self.web_cam_video.resize(width=1080)
            if webcam.h > 640:
                webcam = webcam.crop(y1=0, y2=640)  # Crop the webcam video if it's too tall
            webcam = webcam.set_position(("center", 0))  # Position the webcam video in the center

   
        logging.info("Crop to wanted format")
        self.clip_to_target_format(target_width, target_height)  

        # Create an empty clip for background
        empty_clip = ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=self.content_video.duration)

       

        # Set the position for the content video
        content = self.content_video.set_position(("center", 1920 - 1280))
        # Combine all clips into a final clip
        if webcam is  not None:
            final_clip = CompositeVideoClip([empty_clip, content, webcam])  # Combine all clips into a final clip
        else:
            final_clip =  CompositeVideoClip([empty_clip, content])  

        logging.info("Writing new clip composite from webcam and content..")
        # Write the final composite video to file
        final_clip.write_videofile(processed_video_path, codec="libx264", fps=30)

        self.edited_clip_path_to_vue = processed_video_path_to_send
        self.cleaning_in_process_folder

       

       