from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class GamePage(QWidget):
    """Page displayed after clicking 'Start Game'."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121212; color: white;")
        layout = QVBoxLayout()
        label = QLabel("Welcome to the Game!")
        label.setFont(QFont("Arial", 24))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)
