from PySide6.QtWidgets import QApplication, QWidget, QMainWindow,
from PySide6.QtCore import QSize, Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Weather App")
wgui = QApplication(sys.argv)
window = MainWindow()
window.show()
