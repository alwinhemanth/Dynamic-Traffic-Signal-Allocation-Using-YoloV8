import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QGridLayout, QMainWindow
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QTime
from ultralytics import YOLO


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


class VideoWidget(QWidget):
    def __init__(self, video_path, model):
        super().__init__()
        self.cap = cv2.VideoCapture(video_path)
        self.model = model
        self.vehicle_count = 0
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

        edges = cv2.Canny(frame, threshold1=100, threshold2=200)




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

        self.vehicle_count = count
        self.count_label.setText(f"Vehicle Count: {count}")

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

    def set_signal_color(self, active):
        if active:
            self.signal.set_light("green")
        else:
            self.signal.set_light("red")


class MainWindow(QMainWindow):
    def __init__(self, video_paths):
        super().__init__()
        self.setWindowTitle("Smart Traffic Controller")
        self.setGeometry(100, 100, 1000, 700)

        self.model = YOLO("yolov8n.pt")

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

        self.current_index = 0
        self.signal_duration = 30000  # 30 seconds default
        self.signal_timer = QTimer()
        self.signal_timer.timeout.connect(self.switch_signal)
        self.signal_timer.start(self.signal_duration)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_all_frames)
        self.update_timer.start(100)

    def update_all_frames(self):
        for vw in self.video_widgets:
            vw.update_frame()

    def switch_signal(self):
        # Turn off current green light
        self.video_widgets[self.current_index].set_signal_color(False)

        # Go to next signal
        self.current_index = (self.current_index + 1) % len(self.video_widgets)

        # Turn on green for next one
        current_widget = self.video_widgets[self.current_index]
        current_widget.set_signal_color(True)

        # Adjust signal duration
        vehicle_count = current_widget.vehicle_count
        if vehicle_count > 12:
            self.signal_duration = 45000  # 45 seconds
        else:
            self.signal_duration = 30000  # 30 seconds

        self.signal_timer.start(self.signal_duration)  # Restart timer with new duration


if __name__ == "__main__":
    app = QApplication(sys.argv)

    video_files = ["north.mp4", "south.mp4", "east.mp4", "west.mp4"]  # your 4 video paths
    window = MainWindow(video_files)
    window.show()
    sys.exit(app.exec_())
