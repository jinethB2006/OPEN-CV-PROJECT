import cv2
import numpy as np

class WorkerTracker:
    def __init__(self, dictionary=cv2.aruco.DICT_4X4_50):
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(dictionary)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
        
    def process_frame(self, frame):
        """
        Detects ArUco markers in the frame and returns their centers.
        Returns: 
            frame_annotated: Frame with drawn markers
            worker_centers: List of (x,y) tuples for detected workers
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = self.detector.detectMarkers(gray)
        
        worker_centers = []
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            for i in range(len(ids)):
                c = corners[i][0]
                center_x = int(np.mean(c[:, 0]))
                center_y = int(np.mean(c[:, 1]))
                worker_centers.append((center_x, center_y))
                # Draw centroid
                cv2.circle(frame, (center_x, center_y), 4, (0, 255, 0), -1)
                
        return frame, worker_centers
