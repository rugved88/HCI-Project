import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QColor, QPalette, QPixmap
from PyQt5.QtCore import Qt, QTimer

class BlueFilter(QMainWindow):
    def __init__(self):
        super().__init__()

        # Fullscreen overlay
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_geometry)

        # Make the window stay on top
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create a label to capture mouse events
        label = QLabel(self)
        pixmap = QPixmap(self.size())
        pixmap.fill(QColor(100, 100, 255, 100))  # RGBA values
        label.setPixmap(pixmap)

        # To keep updating the overlay in case of screen changes
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_overlay)
        self.timer.start(1000)  # update every second

    def update_overlay(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_geometry)
        label = self.findChild(QLabel)
        pixmap = QPixmap(self.size())
        pixmap.fill(QColor(100, 100, 255, 100))
        label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    filter = BlueFilter()
    filter.show()
    sys.exit(app.exec_())
