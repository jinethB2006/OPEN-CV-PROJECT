import cv2
import numpy as np

class DangerZoneMonitor:
    def __init__(self, danger_zone_pts):
        """
        danger_zone_pts: list of (x,y) coordinates defining the danger zone polygon.
        """
        self.polygon = np.array(danger_zone_pts, np.int32)
        self.polygon = self.polygon.reshape((-1, 1, 2))

    def check_intrusion(self, frame, worker_centers):
        """
        Checks if any worker centroid is inside the danger zone polygon.
        Returns: 
            frame_annotated: Frame with danger zone drawn
            alert: Boolean indicating if an intrusion was detected
        """
        alert = False
        overlay = frame.copy()
        
        # Default color: Green (Safe), Alert color: Red (Danger)
        color = (0, 255, 0)
        
        for center in worker_centers:
            # pointPolygonTest returns positive if inside, negative if outside, 0 on edge
            dist = cv2.pointPolygonTest(self.polygon, center, False)
            if dist >= 0:
                alert = True
                color = (0, 0, 255)
                # Draw intrusion warning near the centroid
                cv2.putText(frame, "INTRUSION!", (center[0] - 40, center[1] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                break
                
        # Draw the danger zone polygon
        cv2.fillPoly(overlay, [self.polygon], color)
        # Blend overlay for transparency
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        cv2.polylines(frame, [self.polygon], isClosed=True, color=color, thickness=2)
        
        return frame, alert
