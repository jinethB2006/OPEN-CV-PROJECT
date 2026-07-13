<div align="center">
  
# 🛡️ Vision Guard
**Classical Computer Vision for Industrial Safety Compliance**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0-green.svg)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey.svg)](https://flask.palletsprojects.com/)

*Built for the HackZen 2026 Open Challenge* 🚀

</div>

---

## 👋 Hey there!

Welcome to **Vision Guard**! Have you ever noticed how modern industrial safety systems heavily rely on massive, power-hungry AI models? They need expensive GPUs, they're hard to certify for safety because they act like "black boxes," and a simple lighting change can break them completely.

We decided to take a step back and solve this problem using pure, foundational mathematics. **Vision Guard** is a lightning-fast, highly deterministic safety compliance monitor built entirely on Classical Computer Vision (OpenCV) algorithms. 

No deep learning. No training data bias. Just pure geometry and calculus running on a standard CPU. 🧠⚙️

---

## ✨ What Does It Do?

For our HackZen 2026 demo, we've built three core safety features designed to monitor a live industrial diorama:

1. **📍 ArUco Worker Tracking**: Instead of guessing if someone is a person, we track authorized personnel using deterministic ArUco fiducial markers. It's foolproof and requires zero inference time.
2. **⚠️ Danger Zone Intrusion**: We set up a digital tripwire using Point-in-Polygon mathematics. If a worker steps into the restricted zone, the system flags it instantly.
3. **🛑 Conveyor Jam Detection**: Using Farneback Dense Optical Flow, we analyze the micro-movements of a conveyor belt. If the velocity vectors drop to zero, we know the belt has jammed and trigger an immediate hazard alert.

All of this is presented in a beautiful, real-time **Glassmorphic Web Dashboard** that streams the camera feed and logs critical alerts!

---

## 🛠️ How to Run It

It's super easy to get this up and running on your local machine.

### 1. Clone the project
```bash
git clone https://github.com/jinethB2006/OPEN-CV-PROJECT.git
cd OPEN-CV-PROJECT
```

### 2. Install dependencies
We just need OpenCV, NumPy, and Flask.
```bash
pip install -r requirements.txt
```

### 3. Start the Server!
Make sure your webcam is plugged in, and run:
```bash
python app.py
```
Then, open up your favorite web browser and go to `http://localhost:5000` to see the beautiful dashboard in action! 🎨

---

## 🏗️ Under the Hood (For the Geeks)

Curious about how it works without AI?
- **Backend**: A lightweight Flask server (`app.py`) captures the video, processes it through our classical CV modules, and streams it via an MJPEG HTTP feed.
- **Frontend**: A custom HTML/CSS/JS dashboard featuring smooth gradients, dynamic API polling, and a modern dark-mode aesthetic.
- **CV Pipeline**: The video frames go through `cv2.aruco.detectMarkers`, `cv2.pointPolygonTest`, and `cv2.calcOpticalFlowFarneback`. Because we use classical algorithms, we can achieve over 60 FPS on standard CPUs with single-digit millisecond latency. 

---

## 🚀 Future Scope
While this was built specifically for the HackZen constraints, in the real world, we'd love to combine this deterministic logic with semantic deep learning (like YOLOv11) to get the best of both worlds: extreme robustness against lighting changes combined with absolute mathematical certainty.

---
*Created by Jineth B (jinethB2006) for HackZen 2026. Build. Innovate. Qualify.*
