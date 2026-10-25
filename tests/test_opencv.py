import sys
import os
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

class OpenCVTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Test OpenCV i PySide6")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # etykieta w której wyświetlimy obraz
        self.image_label = QLabel("Loading an image", self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        # ladowanei obrazu
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "test_image.jpg")
        self.load_and_display_image(image_path)

    def load_and_display_image(self, file_path):
        cv_img = cv2.imread(file_path)

        if cv_img is None:
            self.image_label.setText(f"File not found: {file_path}")
            return

        # konwersja z domyślnego BGR (OpenCV) na RGB
        cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        height, width, channels = cv_img_rgb.shape
        bytes_per_line = channels * width

        # konwersja macierzy NumPy na obiekt QImage
        q_image = QImage(
            cv_img_rgb.data, 
            width, 
            height, 
            bytes_per_line, 
            QImage.Format.Format_RGB888
        )

        pixmap = QPixmap.fromImage(q_image)

        scaled_pixmap = pixmap.scaled(
            self.width() - 40, self.height() - 40, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )

        self.image_label.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenCVTestWindow()
    window.show()
    sys.exit(app.exec())