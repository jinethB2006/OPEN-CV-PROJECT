<div align="center">
  
# Vision Guard
**Classical Computer Vision for Industrial Safety Compliance**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0-green.svg)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey.svg)](https://flask.palletsprojects.com/)

*Built for the HackZen 2026 Open Challenge*

</div>

---

## Introduction

In the contemporary industrial landscape, occupational safety is governed by stringent international and national standards, including those mandated by OSHA and ISO. Monitoring compliance across vast manufacturing plants remains a critical operational challenge. While modern automated compliance systems rely heavily on Deep Learning (DL) and Artificial Intelligence (AI), these models possess critical limitations:
1. They require immense computational overhead (GPUs).
2. They function as opaque "black boxes," making formal functional safety certification exceedingly difficult.
3. They suffer from high data dependency and domain shift vulnerability.

**Vision Guard** is a completely deterministic, mathematically verifiable industrial safety monitor built entirely using Classical Computer Vision methodologies. By leveraging explicit geometry, matrix calculus, and pixel-level statistical analysis through OpenCV, the system operates in real-time on standard Central Processing Units (CPUs) with zero reliance on AI training datasets.

---

## System Features and Mathematical Underpinnings

For the HackZen 2026 demonstration, the system implements three core safety modules designed to monitor a live manufacturing diorama.

### 1. Deterministic ArUco-Based Tracking
- **Purpose**: To track the identity and location of authorized personnel in the environment deterministically.
- **Mechanism**: The system utilizes OpenCV's ArUco module to detect specific binary square markers attached to the workers.
- **Mathematics**: It performs dictionary matching and corner detection to extract the sub-pixel spatial coordinates of the worker's centroid, allowing for absolute tracking without the computational bloat or identity-switching flaws of deep learning trackers.

### 2. Dynamic Machine Guard Proximity Tripwires
- **Purpose**: To detect when a worker intrudes into a restricted or hazardous zone.
- **Mechanism**: A digital geofence is defined as a static polygon on the video feed. The system continuously evaluates the Cartesian coordinates of the tracked worker's centroid against this polygon.
- **Mathematics**: The system utilizes the Point-in-Polygon (Ray Casting) algorithm (`cv2.pointPolygonTest`) to instantly evaluate whether the centroid has mathematically intersected the restricted zone, triggering an intrusion alert with zero latency.

### 3. Conveyor Belt Jam Detection via Vector Field Divergence
- **Purpose**: To detect physical stalling or mechanical jams on a moving conveyor belt.
- **Mechanism**: Rather than training an AI to recognize specific materials or blockages, the system analyzes the fundamental velocity vector field of the belt surface itself.
- **Mathematics**: The pipeline utilizes the Farneback Dense Optical Flow algorithm (`cv2.calcOpticalFlowFarneback`) to calculate motion across the entire belt surface. It calculates the average magnitude of the 2D velocity vectors. A sudden drop in average magnitude below a calibrated threshold definitively indicates a mechanical stall, triggering a machine jam hazard alert.

---

## Web Application Architecture

To provide a modern monitoring interface, Vision Guard is deployed as a full-stack web application:

- **Backend (Python / Flask)**: A lightweight Flask server acts as the data and video pipeline. It captures the raw video feed, processes it sequentially through the highly optimized C++ OpenCV algorithms, and encodes the annotated output into an MJPEG stream. It also exposes a JSON API endpoint (`/api/status`) providing real-time system metrics.
- **Frontend (HTML / CSS / JS)**: A responsive, glassmorphic web dashboard that displays the live surveillance feed. A JavaScript polling loop retrieves data from the backend every 500 milliseconds to dynamically update the processing speed (FPS), pipeline latency, simulated CPU load, and a chronological log of critical safety alerts without flickering or reloading the page.

---

## Installation and Setup Instructions

Vision Guard is designed to be easily deployable on standard hardware.

### Prerequisites
- Python 3.10 or higher
- A connected USB Webcam (for live demonstration)

### Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/jinethB2006/OPEN-CV-PROJECT.git
   cd OPEN-CV-PROJECT
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *The dependencies include `opencv-python`, `opencv-contrib-python`, `numpy`, and `Flask`.*

### Execution
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your preferred web browser and navigate to:
   ```
   http://localhost:5000
   ```
3. The dashboard will initialize, requesting access to your webcam, and begin running the classical computer vision pipeline immediately.

---

## Performance and Results

By avoiding heavy neural network graphs, Vision Guard achieves exceptional performance:
- **Scalability**: Runs smoothly on standard embedded CPUs without the need for dedicated tensor processors or GPUs.
- **Latency**: Processes frames with single-digit millisecond latency, providing real-time responsiveness critical for emergency safety systems.
- **Interpretability**: Every safety decision made by the system is mathematically provable, completely bypassing the "black box" safety certification issues inherent in deep learning.

## Future Scope

While the primary implementation is strictly OpenCV-based per the HackZen constraints, a commercial deployment could integrate deep learning frameworks (like YOLOv11 or Segment Anything) for robust semantic feature extraction in environments with extreme lighting variance, utilizing classical logic strictly as a redundant, deterministic safety fallback.

---
*Developed by Jineth B (jinethB2006)*
