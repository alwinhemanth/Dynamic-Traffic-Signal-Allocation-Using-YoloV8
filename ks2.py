import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QGridLayout, QMainWindow
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from ultralytics import YOLO


# --- Traffic Light UI Components ---

class SingleLight(QLabel):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.setFixedSize(30, 30)
        self.setStyleSheet("background-color: gray; border-radius: 15px; border: 1px solid black;")

    def turn_on(self):
        self.setStyleSheet(f"background-color: {self.color}; border-radius: 15px; border: 1px solid black;")

    def turn_off(self):
        self.setStyleSheet("background-color: gray; border-radius: 15px; border: 1px solid black;")


class TrafficSignal(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(4)
        self.red = SingleLight("red")
        self.orange = SingleLight("orange")
        self.green = SingleLight("green")
        layout.addWidget(self.red)
        layout.addWidget(self.orange)
        layout.addWidget(self.green)
        self.setLayout(layout)

    def set_light(self, color):
        self.red.turn_off()
        self.orange.turn_off()
        self.green.turn_off()

        if color == "red":
            self.red.turn_on()
        elif color == "orange":
            self.orange.turn_on()
        elif color == "green":
            self.green.turn_on()


# --- Main Video Widget ---

class VideoWidget(QWidget):
    def __init__(self, video_path, model):
        super().__init__()
        self.cap = cv2.VideoCapture(video_path)
        self.model = model  # YOLOv8 model

        self.video_label = QLabel()
        self.signal = TrafficSignal()
        self.count_label = QLabel("Vehicle Count: 0")
        self.count_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.signal)
        layout.addWidget(self.count_label)
        self.setLayout(layout)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        frame = cv2.resize(frame, (320, 240))

        # --- Run YOLO detection ---
        results = self.model(frame, verbose=False)[0]
        vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
        count = 0
        for box in results.boxes:
            if int(box.cls) in vehicle_classes:
                count += 1

        # Display frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

        # Update traffic signal and count
        self.update_signal(count)

    def update_signal(self, count):
        self.count_label.setText(f"Vehicle Count: {count}")

        if count < 7:
            self.signal.set_light("red")
        elif count < 14:
            self.signal.set_light("orange")
        else:
            self.signal.set_light("green")


# --- Main App Window ---

class MainWindow(QMainWindow):
    def __init__(self, video_paths):
        super().__init__()
        self.setWindowTitle("YOLO Traffic Monitor")
        self.setGeometry(100, 100, 800, 600)

        self.model = YOLO("yolov8n.pt")  # Load YOLOv8 nano model (you can use yolov8s.pt for better accuracy)

        central = QWidget()
        self.setCentralWidget(central)
        grid = QGridLayout()

        self.video_widgets = []
        for i, path in enumerate(video_paths):
            vw = VideoWidget(path, self.model)
            self.video_widgets.append(vw)
            row, col = divmod(i, 2)
            grid.addWidget(vw, row, col)

        central.setLayout(grid)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(100)  # Adjust FPS here

    def update_all(self):
        for vw in self.video_widgets:
            vw.update_frame()


# --- Main Entrypoint ---

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Replace with paths to your 4 traffic videos
    video_files = [
        "a.mp4",
        "b.mp4",
        "c.mp4",
        "d.mp4"
    ]

    window = MainWindow(video_files)
    window.show()
    sys.exit(app.exec_())
