import cv2
import time
import argparse
from modules.tracker import WorkerTracker
from modules.intrusion import DangerZoneMonitor
from modules.flow import ConveyorMonitor

def main(video_source=0):
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    # Define geometry for the demonstration diorama (adjust these points to fit actual camera view)
    # Example Danger Zone: A polygon on the left side of the frame
    danger_zone_pts = [(50, 50), (250, 50), (250, 300), (50, 300)]
    
    # Example Conveyor Belt ROI: x, y, w, h
    conveyor_roi = (300, 150, 200, 100)

    # Initialize Modules
    tracker = WorkerTracker()
    intrusion_monitor = DangerZoneMonitor(danger_zone_pts)
    conveyor_monitor = ConveyorMonitor(conveyor_roi, flow_threshold=0.5)

    print("Vision Guard: System Started.")
    print("Press 'q' to quit.")

    prev_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of stream or cannot read frame.")
            break
            
        start_time = time.time()
        
        # 1. Track Workers (ArUco)
        frame, worker_centers = tracker.process_frame(frame)
        
        # 2. Monitor Danger Zone Intrusion
        frame, intrusion_alert = intrusion_monitor.check_intrusion(frame, worker_centers)
        
        # 3. Monitor Conveyor Belt for Jams (Optical Flow)
        frame, jam_alert = conveyor_monitor.check_jam(frame)
        
        # Calculate Performance Metrics
        calc_time = time.time() - start_time
        fps = 1.0 / (time.time() - prev_time)
        prev_time = time.time()
        latency = calc_time * 1000  # in ms
        cpu_load_mock = min(100, int(calc_time * 1000)) # Mock CPU load based on latency for demo purposes
        
        # Overlay Dashboard
        dashboard_text = [
            "Vision Guard Dashboard",
            f"Processing: {fps:.1f} FPS",
            f"Latency: {latency:.1f} ms",
            f"CPU Load: {cpu_load_mock}%"
        ]
        
        y_offset = 30
        for text in dashboard_text:
            cv2.putText(frame, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
            y_offset += 25
            
        if intrusion_alert:
            print(f"[{time.strftime('%H:%M:%S.%f')[:-3]}] CRITICAL: Zone Intrusion Detected.")
        if jam_alert:
            print(f"[{time.strftime('%H:%M:%S.%f')[:-3]}] WARNING: Conveyor Flow Interrupted.")
            
        # Display
        cv2.imshow("Vision Guard - HackZen 2026", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vision Guard System")
    parser.add_argument('--source', type=str, default='0', help='Video source (0 for webcam, or path to video file)')
    args = parser.parse_args()
    
    # Parse source correctly (int if digit)
    source = int(args.source) if args.source.isdigit() else args.source
    main(source)
