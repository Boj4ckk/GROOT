import cv2
import logging
import numpy as np

class WebCamProcessor:

    """
    A class that processes a webcam or video clip to capture frames,
    detect faces, and manually or automatically define a region of interest (ROI).
    """

    def __init__(self, clip):
        """
        Initializes the WebCamProcessor object with the given video clip.

        Parameters:
        clip (str): Path to the video file to be processed.

        Raises:
        ValueError: If the first frame of the video cannot be read.
        """
        # Initialize the video capture object with the given clip
        self.clip = cv2.VideoCapture(clip)

        # Read the first frame from the video
        ret, self.first_frame = self.clip.read()
        if not ret:
            raise ValueError("Error: Unable to read the first frame of the video.")
        
        # Initialize the list to store coordinates for the region of interest (ROI)
        self.web_cam_coordinate = []

        # Define a function to get the frame using coordinates (for later use)
        self.web_cam_frame = self.get_web_cam_frame_by_coordinate
        
        # Get the width and height of the video clip
        self.clip_width = int(self.clip.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.clip_height = int(self.clip.get(cv2.CAP_PROP_FRAME_HEIGHT))


    """ 
    Get the webcam coordinates manually by clicking on the video frame.

    This method listens for mouse clicks on the video frame and stores the coordinates of the clicked points. 
    The user should click on four points to define a rectangular region (ROI).
    """
    def get_clicked_coordinate(self, event, x, y, flags, param):
        """
        Callback function to capture mouse click coordinates.

        Parameters:
        event (int): The type of mouse event (e.g., left click).
        x (int): The x-coordinate of the mouse click.
        y (int): The y-coordinate of the mouse click.
        flags (int): Additional flags for the event (unused).
        param (any): Additional parameters for the callback (unused).
        """
        # Store the coordinates when the left mouse button is clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            self.web_cam_coordinate.append((x, y))
    
    def get_point_manually(self):
        """
        Captures four points manually by displaying the video frame and allowing the user to click on the points.

        Returns:
        list: A list of four coordinates defining the region of interest (ROI) in the format [y_min, y_max, x_min, x_max].

        If the user clicks on four points, the method calculates the bounding box using the clicked coordinates.
        """
        ret, self.frame = self.clip.read()
        if not ret:
            print("Error: Unable to capture a frame.")
            return []

        # Display the current frame and set the mouse callback to capture coordinates
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.imshow("Frame", self.frame)
        cv2.setMouseCallback("Frame", self.get_clicked_coordinate)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or len(self.web_cam_coordinate) == 4:  # Exit with ESC key or 4 points selected
                break

        # Close the window after capturing the points
        cv2.destroyAllWindows()

        if len(self.web_cam_coordinate) == 4:
            # Calculate the bounding box (min and max coordinates)
            x_coords = [coord[0] for coord in self.web_cam_coordinate]
            y_coords = [coord[1] for coord in self.web_cam_coordinate]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            
            # Store the calculated coordinates in the format [y_min, y_max, x_min, x_max]
            self.web_cam_coordinate = [y_min, y_max, x_min, x_max]
        
        return self.web_cam_coordinate
    

    """ 
    Detect faces in the video using a deep neural network (DNN) model. 
    If face detection fails, the method falls back to manual ROI extraction.
    """
    def detect_faces(self):
        """
        Detects faces in the video using a DNN-based face detector.

        The method loads a pre-trained Caffe model for face detection and attempts to detect faces in 
        each frame. If no faces are detected, it calls the manual ROI extraction method.

        Raises:
        logging.info: If face detection fails, logs a message and calls the manual method.
        """
        # Correct paths to the face detection model
        prototxt_path = "GROOT\\Edit\\sample\\deploy.prototxt"
        model_path = "GROOT\\Edit\\sample\\res10_300x300_ssd_iter_140000.caffemodel"

        # Load the DNN model
        net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        
        for i in range(30):  # Loop through the first 30 frames
            ret, frame = self.clip.read()
            if not ret:
                break
            
            # Get the dimensions of the current frame
            h, w = frame.shape[:2]

            # Prepare the frame for input into the DNN
            blob = cv2.dnn.blobFromImage(frame, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))

            # Send the frame to the neural network for processing
            net.setInput(blob)
            detections = net.forward()

            # Loop through the detected faces in the frame
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    # Extract the bounding box coordinates for the detected face
                    box = detections[0, 0, i, 3:7] * [w, h, w, h]
                    x, y, x2, y2 = box.astype("int")
                    
                    # Draw a rectangle around the detected face
                    cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)
                    
                    # Add the coordinates of the face to the list of webcam coordinates with additional padding
                    self.web_cam_coordinate.extend([max(0, y - 70), y2 + 70, max(0, x - 130), x2 + 130])
                    return  # Stop after the first face is detected
        
        # If no face is detected, log the failure and call manual coordinate extraction
        logging.info("Auto face recognition failed. Manually web cam extraction performed.")
        self.get_point_manually()


    """ 
    Extract the region of interest (ROI) from the video frame using the defined coordinates. 
    The coordinates must be provided in the format [y_min, y_max, x_min, x_max].
    """
    def get_web_cam_frame_by_coordinate(self):
        """
        Extracts the region of interest (ROI) from the first frame of the video.

        Returns:
        frame (numpy.ndarray): The cropped frame from the video based on the defined coordinates.

        Raises:
        ValueError: If the coordinates have not been defined or are invalid.
        """
        # Ensure the coordinates have been properly defined (4 points)
        if len(self.web_cam_coordinate) != 4:
            raise ValueError("Error: Coordinates are not provided or missing.")

        # Crop the frame based on the coordinates and return the cropped frame
        frame = self.first_frame[self.web_cam_coordinate[0]:self.web_cam_coordinate[1], 
                                 self.web_cam_coordinate[2]:self.web_cam_coordinate[3]]
        return frame
