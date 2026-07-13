from flask import Flask, render_template, Response, jsonify
import cv2
import time
import threading
from modules.tracker import WorkerTracker
from modules.intrusion import DangerZoneMonitor
from modules.flow import ConveyorMonitor

app = Flask(__name__)

# Global state for metrics and alerts
system_state = {
    'fps': 0,
    'latency': 0,
    'cpu_load': 0,
    'alerts': []
}

def generate_frames():
    global system_state
    
    # Try multiple camera indices if 0 fails
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        # Fallback to a mock generator if no camera is available
        while True:
            frame = cv2.imread('placeholder.jpg') # fallback if needed
            if frame is None:
                frame = __import__("numpy").zeros((480, 640, 3), dtype="uint8")
                cv2.putText(frame, "No Camera Found", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.1)

    # Modules
    danger_zone_pts = [(50, 50), (250, 50), (250, 300), (50, 300)]
    conveyor_roi = (300, 150, 200, 100)
    tracker = WorkerTracker()
    intrusion_monitor = DangerZoneMonitor(danger_zone_pts)
    conveyor_monitor = ConveyorMonitor(conveyor_roi, flow_threshold=0.5)

    prev_time = time.time()

    while True:
        success, frame = cap.read()
        if not success:
            break
            
        start_time = time.time()
        
        # 1. Track Workers (ArUco)
        frame, worker_centers = tracker.process_frame(frame)
        
        # 2. Monitor Danger Zone Intrusion
        frame, intrusion_alert = intrusion_monitor.check_intrusion(frame, worker_centers)
        
        # 3. Monitor Conveyor Belt for Jams (Optical Flow)
        frame, jam_alert = conveyor_monitor.check_jam(frame)
        
        # Performance Metrics
        calc_time = time.time() - start_time
        fps = 1.0 / (time.time() - prev_time)
        prev_time = time.time()
        latency = calc_time * 1000
        cpu_load = min(100, int(calc_time * 1000))
        
        # Update Global State
        system_state['fps'] = round(fps, 1)
        system_state['latency'] = round(latency, 1)
        system_state['cpu_load'] = cpu_load
        
        current_time_str = time.strftime('%H:%M:%S')
        if intrusion_alert:
            system_state['alerts'].append(f"[{current_time_str}] CRITICAL: Zone Intrusion Detected!")
        if jam_alert:
            system_state['alerts'].append(f"[{current_time_str}] WARNING: Conveyor Flow Interrupted.")
            
        # Keep only the last 5 alerts
        if len(system_state['alerts']) > 5:
            system_state['alerts'].pop(0)

        # Encode frame to MJPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/status')
def get_status():
    global system_state
    return jsonify(system_state)

if __name__ == '__main__':
    # Run Flask in a separate thread so it doesn't block the camera loop context
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
