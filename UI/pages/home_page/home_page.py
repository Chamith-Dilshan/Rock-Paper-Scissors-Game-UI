from PySide6.QtGui import QPixmap,QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout
)

class HomePage(QWidget):
    """Landing page with a single combined image and navigation buttons."""

    def __init__(self, navigate_callback:object):
        super().__init__()
        self.navigate_callback = navigate_callback
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #3b1d9e; color: white;")

        # Title
        title = QLabel("Rock, Paper\nScissors")
        title.setFont(QFont("Arial", 35, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Description
        description = QLabel(
            "Challenge the computer in a classic game of Rock, Paper, Scissors! "
            "Make your move, and see if you can outsmart the AI. It's you versus the machine—"
            "best of luck!"
        )
        # description.setFont(QFont("Arial", 12, QFont.Weight.Normal))
        description.setWordWrap(True)

        # Buttons
        start_btn = QPushButton("Start Game")
        start_btn.setStyleSheet(self.button_style())
        start_btn.setMinimumWidth(120)
        start_btn.setMaximumWidth(200)
        start_btn.clicked.connect(self.navigate_callback)

        button_layout = QHBoxLayout()
        button_layout.addWidget(start_btn)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Text Layout
        text_layout = QVBoxLayout()
        text_layout.addWidget(title)
        # text_layout.addSpacing(120)
        text_layout.addWidget(description)
        text_layout.addSpacing(30)
        text_layout.addLayout(button_layout)
        text_layout.setContentsMargins(20, 0, 0, 0)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Image on the right
        image_label = QLabel()
        pixmap = QPixmap("assets/images/home_image.png").scaled(1100, 700, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.addLayout(text_layout, stretch=1)
        main_layout.addSpacing(200)
        main_layout.addWidget(image_label, stretch=2)

    def button_style(self):
        return (
            "QPushButton {"
            "background-color: orange;"
            "color: white;"
            "padding: 10px 20px;"
            "border-radius: 10px;"
            "font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "background-color: #ffa500;"
            "}"
        )
                                  
