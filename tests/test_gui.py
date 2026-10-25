import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Test GUI")
        self.setGeometry(100, 100, 400, 200) # (x, y, szerokość, wysokość)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.label = QLabel("Waiting", self)
        self.label.setStyleSheet("font-size: 14px; color: #3a3;") 
        layout.addWidget(self.label)

        self.button = QPushButton("Click", self)
        self.button.setStyleSheet("padding: 10px; font-size: 14px;")
        
        # podpięcie akcji pod kliknięcie
        self.button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.button)

    def on_button_clicked(self):
        self.label.setText("Loop works, button was clicked")
        print("Button was clicked")

if __name__ == "__main__":
    # inicjalizacja aplikacji i pętli zdarzeń
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    # główna pętla
    sys.exit(app.exec())