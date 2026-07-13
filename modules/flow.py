import cv2
import numpy as np

class ConveyorMonitor:
    def __init__(self, roi, flow_threshold=1.5):
        """
        roi: tuple (x, y, w, h) defining the conveyor belt region.
        flow_threshold: minimum average magnitude of flow to consider the belt "moving".
        """
        self.roi = roi
        self.flow_threshold = flow_threshold
        self.prev_gray = None

    def check_jam(self, frame):
        """
        Uses Farneback Optical Flow to detect if the conveyor belt has stopped/jammed.
        Returns:
            frame_annotated: Frame with ROI and flow visualized
            alert: Boolean indicating if a jam is detected
        """
        alert = False
        x, y, w, h = self.roi
        
        # Ensure ROI is within frame bounds
        if x < 0 or y < 0 or x+w > frame.shape[1] or y+h > frame.shape[0]:
            return frame, False
            
        roi_frame = frame[y:y+h, x:x+w]
        gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
        
        if self.prev_gray is None:
            self.prev_gray = gray
            return frame, False
            
        # Calculate Dense Optical Flow
        flow = cv2.calcOpticalFlowFarneback(self.prev_gray, gray, None, 
                                            pyr_scale=0.5, levels=3, winsize=15, 
                                            iterations=3, poly_n=5, poly_sigma=1.2, flags=0)
                                            
        # Compute magnitude and angle of the 2D vectors
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        
        # Calculate average motion magnitude in the ROI
        avg_mag = np.mean(magnitude)
        
        # If motion drops below threshold, trigger jam alert
        if avg_mag < self.flow_threshold:
            alert = True
            
        self.prev_gray = gray
        
        # Draw ROI
        color = (0, 0, 255) if alert else (255, 0, 0)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        # Status Text
        status_text = "JAM HAZARD!" if alert else "FLOW OK"
        cv2.putText(frame, f"Belt: {status_text} (mag: {avg_mag:.2f})", 
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
        return frame, alert
