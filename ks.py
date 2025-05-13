import sys
import cv2
import random
from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QGridLayout, QMainWindow
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer


class SingleLight(QLabel):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.setFixedSize(30, 30)
        self.setStyleSheet(f"background-color: gray; border-radius: 15px; border: 1px solid black;")

    def turn_on(self):
        self.setStyleSheet(f"background-color: {self.color}; border-radius: 15px; border: 1px solid black;")

    def turn_off(self):
        self.setStyleSheet(f"background-color: gray; border-radius: 15px; border: 1px solid black;")


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
    def __init__(self, video_path):
        super().__init__()
        self.cap = cv2.VideoCapture(video_path)

        self.video_label = QLabel()
        self.signal = TrafficSignal()

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.signal)
        self.setLayout(layout)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        # Convert frame
        frame = cv2.resize(frame, (320, 240))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        qt_img = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

        # Simulated vehicle count
        count = self.mock_vehicle_count()
        self.update_signal(count)

    def mock_vehicle_count(self):
        return random.randint(0, 20)

    def update_signal(self, count):
        if count < 7:
            self.signal.set_light("red")
        elif count < 14:
            self.signal.set_light("orange")
        else:
            self.signal.set_light("green")


class MainWindow(QMainWindow):
    def __init__(self, video_paths):
        super().__init__()
        self.setWindowTitle("Traffic Signal Monitor")
        self.setGeometry(100, 100, 800, 600)

        central = QWidget()
        self.setCentralWidget(central)

        grid = QGridLayout()
        self.video_widgets = []

        for i, path in enumerate(video_paths):
            vw = VideoWidget(path)
            self.video_widgets.append(vw)
            row, col = divmod(i, 2)
            grid.addWidget(vw, row, col)

        central.setLayout(grid)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(30)

    def update_all(self):
        for vw in self.video_widgets:
            vw.update_frame()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Replace with your actual 4 video paths
    video_files = [
        "a.mp4",
        "b.mp4",
        "c.mp4",
        "d.mp4"
    ]

    window = MainWindow(video_files)
    window.show()
    sys.exit(app.exec_())
