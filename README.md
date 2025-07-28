# 🚦 Density-Based Traffic Signal Control Using Image Processing

A real-time system that dynamically controls traffic signals using vehicle detection from video feeds, built with Python, OpenCV (CUDA), and YOLOv8.

---

### 📽️ Demo

🚦 Watch the full demo on LinkedIn:  
[🔗 Smart Traffic Control System Demo – LinkedIn Video](https://www.linkedin.com/posts/alwin-hemanth-ks_smarttraffic-admindashboard-djangoproject-activity-7317804517218017281-t0oA?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD2FL74BK3Uq2EF9GMHcO-Y5ABw5jjmFuqY)


---

## 🧠 Project Description

This project controls traffic signals dynamically using **image processing** instead of traditional timers or electronic sensors. Vehicles are detected in real time from rotating camera footage, and traffic lights are automatically adjusted based on lane density.

---

## ⚙️ Technologies Used

- 🐍 Python
- 🎯 YOLOv8 (Ultralytics)
- 🎥 OpenCV with CUDA acceleration
- 🧮 NumPy, Pandas
- 💻 Jupyter Notebooks / PyQt5 (optional GUI)

---

## 🚀 Features

- ✅ Real-time vehicle detection from live video
- ✅ CUDA-accelerated image processing
- ✅ Green signal time adjusted per lane based on density
- ✅ Fallback system for safety on detection failure

---

## 🏗️ System Architecture

This project uses an offline video file (`.mp4`) as the input source for simulating smart traffic signal control. The video is processed frame by frame to detect vehicle density per lane using YOLOv8. Based on the density, the system dynamically assigns green signal times and visualizes changes in a GUI using PyQt5.

### 🔄 Architecture Flow:
┌────────────────────┐      
│  Video File (.mp4) │  ←── Input video file (uploaded by user)
│  (Input Dataset)   │      
└────────────────────┘      
          │
          ▼
┌────────────────────────┐  
│  Frame Extraction      │  ←── Read video frame by frame using OpenCV
│  (cv2.VideoCapture)    │  
└────────────────────────┘  
          │
          ▼
┌────────────────────────┐  
│    Pre‑Processing      │  ←── Resize, blur, gray scale conversion etc.
└────────────────────────┘  
          │
          ▼
┌──────────────────────┐   
│  Object Detection     │  ←── Use YOLOv8 to detect vehicles in the frame
│     (YOLOv8)          │   
└──────────────────────┘   
          │
          ▼
┌──────────────────────────────┐  
│ Vehicle Count per Lane        │  ←── Count number of vehicles per direction
│ (based on ROI or Grid zones)  │  
└──────────────────────────────┘  
          │
          ▼
┌──────────────────────────────┐  
│ Signal Timing Scheduler       │  ←── Decide green time dynamically based on density
│ (Density-based logic)         │  
└──────────────────────────────┘  
          │
          ▼
┌──────────────────────────────┐  
│ GUI / Signal Visualizer       │  ←── Show traffic signal status in real-time (PyQt5)
└──────────────────────────────┘  
          │
          ▼
┌──────────────────────────────┐  
│ Logging & History Recording   │  ←── Store vehicle counts & signal timing to CSV/DB
└──────────────────────────────┘  





