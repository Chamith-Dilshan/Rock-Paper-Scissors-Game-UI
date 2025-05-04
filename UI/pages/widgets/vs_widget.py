from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFrame, QSizePolicy
)

class VSWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Top Line (Vertical)
        self.top_line = QFrame()
        self.top_line.setFrameShape(QFrame.Shape.VLine)
        self.top_line.setFrameShadow(QFrame.Shadow.Plain)
        self.top_line.setStyleSheet("background-color: black; color: black;")
        self.top_line.setFixedWidth(5)
        self.top_line.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.top_line.setFixedHeight(200)
        layout.addWidget(self.top_line, alignment=Qt.AlignmentFlag.AlignCenter)

        # VS Label
        self.vs_label = QLabel("VS")
        self.vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vs_label.setFont(QFont("Arial", 35, QFont.Weight.Bold))
        self.vs_label.setStyleSheet("color: black;")
        layout.addWidget(self.vs_label)

        # Bottom Line (Vertical)
        self.bottom_line = QFrame()
        self.bottom_line.setFrameShape(QFrame.Shape.VLine)
        self.bottom_line.setFrameShadow(QFrame.Shadow.Plain)
        self.bottom_line.setStyleSheet("background-color: black; color: black;")
        self.bottom_line.setFixedWidth(5)
        self.bottom_line.setFixedHeight(200)
        self.bottom_line.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.bottom_line, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.setSpacing(10)  # Space between the lines and the label
        layout.setContentsMargins(0, 0, 0, 0)