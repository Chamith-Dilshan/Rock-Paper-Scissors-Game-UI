from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, 
                              QPushButton, QSpacerItem, QSizePolicy, QFrame)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QFont, QPixmap, QImage, QPainter
from PySide6.QtMultimedia import QMediaDevices, QCamera
from PySide6.QtMultimediaWidgets import QVideoWidget
import random
import cv2
import numpy as np

class GamePage(QWidget):
    """Rock Paper Scissors game page with camera integration."""

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_game()
        self.setup_camera()
        
    def setup_ui(self):
        """Initialize the UI components."""
        self.setStyleSheet("""
            background-color: #121212; 
            color: white;
            QPushButton {
                background-color: #333333;
                border: 2px solid #555555;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #222222;
            }
            QFrame {
                border: 2px solid #555555;
                border-radius: 10px;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Rock Paper Scissors")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Score display
        self.score_layout = QHBoxLayout()
        self.human_score_label = QLabel("Human: 0")
        self.human_score_label.setFont(QFont("Arial", 16))
        self.robot_score_label = QLabel("Robot: 0")
        self.robot_score_label.setFont(QFont("Arial", 16))
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.score_layout.addWidget(self.human_score_label)
        self.score_layout.addItem(spacer)
        self.score_layout.addWidget(self.robot_score_label)
        
        # Camera and choices display
        self.camera_choices_layout = QHBoxLayout()
        
        # Camera frame
        self.camera_frame = QFrame()
        self.camera_frame.setFixedSize(320, 240)
        self.camera_layout = QVBoxLayout(self.camera_frame)
        
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_layout.addWidget(self.camera_label)
        
        # Choices display
        self.choices_display = QHBoxLayout()
        
        vs_label = QLabel("VS")
        vs_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.robot_choice = QLabel()
        self.robot_choice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.robot_choice.setFixedSize(120, 120)
        
        self.choices_display.addWidget(self.camera_frame)
        self.choices_display.addWidget(vs_label)
        self.choices_display.addWidget(self.robot_choice)
        
        # Result display
        self.result_label = QLabel("Make your choice!")
        self.result_label.setFont(QFont("Arial", 18))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.rock_btn = QPushButton("Rock")
        self.paper_btn = QPushButton("Paper")
        self.scissors_btn = QPushButton("Scissors")
        self.capture_btn = QPushButton("Capture Choice")
        
        for btn in [self.rock_btn, self.paper_btn, self.scissors_btn, self.capture_btn]:
            btn.setFixedHeight(50)
        
        button_layout.addWidget(self.rock_btn)
        button_layout.addWidget(self.paper_btn)
        button_layout.addWidget(self.scissors_btn)
        button_layout.addWidget(self.capture_btn)
        
        # Add widgets to main layout
        main_layout.addWidget(title)
        main_layout.addLayout(self.score_layout)
        main_layout.addLayout(self.choices_display)
        main_layout.addWidget(self.result_label)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def setup_game(self):
        """Initialize game variables and connections."""
        self.human_score = 0
        self.robot_score = 0
        self.choices = ["rock", "paper", "scissors"]
        self.choice_images = {
            "rock": self.create_icon("R", QSize(120, 120)),
            "paper": self.create_icon("P", QSize(120, 120)),
            "scissors": self.create_icon("S", QSize(120, 120)),
            "unknown": self.create_icon("?", QSize(120, 120))
        }
        
        # Set default images
        self.robot_choice.setPixmap(self.choice_images["unknown"])
        
        # Connect buttons
        self.rock_btn.clicked.connect(lambda: self.play_round("rock"))
        self.paper_btn.clicked.connect(lambda: self.play_round("paper"))
        self.scissors_btn.clicked.connect(lambda: self.play_round("scissors"))
        self.capture_btn.clicked.connect(self.capture_gesture)
        
        # Camera variables
        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.update_camera)
        self.current_frame = None
        self.human_choice = None
        
    def create_icon(self, text, size):
        """Create a pixmap icon with text."""
        pixmap = QPixmap(size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.GlobalColor.darkGray)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawEllipse(10, 10, size.width()-20, size.height()-20)
        
        font = QFont("Arial", 48)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text)
        painter.end()
        
        return pixmap
        
    def setup_camera(self):
        """Initialize the camera."""
        cameras = QMediaDevices.videoInputs()
        if not cameras:
            self.result_label.setText("No camera found!")
            return
            
        self.camera = QCamera(cameras[0])
        self.camera.start()
        self.camera_timer.start(30)  # Update ~30fps
        
    def update_camera(self):
        """Update the camera preview."""
        # This is a placeholder - in a real implementation you would:
        # 1. Capture frame from camera
        # 2. Process it to detect gesture
        # 3. Display it in the camera_label
        
        # For demo purposes, we'll just show a colored frame
        width, height = 320, 240
        image = QImage(width, height, QImage.Format.Format_RGB32)
        color = Qt.GlobalColor.darkGreen if self.human_choice else Qt.GlobalColor.darkRed
        image.fill(color)
        
        # Draw hand gesture if detected
        if self.human_choice:
            painter = QPainter(image)
            font = QFont("Arial", 72)
            painter.setFont(font)
            painter.setPen(Qt.GlobalColor.white)
            
            text = {
                "rock": "✊",
                "paper": "✋",
                "scissors": "✌"
            }.get(self.human_choice, "?")
            
            painter.drawText(image.rect(), Qt.AlignmentFlag.AlignCenter, text)
            painter.end()
        
        self.camera_label.setPixmap(QPixmap.fromImage(image))
        
    def capture_gesture(self):
        """Capture the current gesture from camera."""
        # In a real implementation, this would:
        # 1. Analyze the current frame for hand gesture
        # 2. Determine if it's rock, paper, or scissors
        # 3. Set self.human_choice
        
        # For demo, we'll just cycle through choices
        if not hasattr(self, 'demo_counter'):
            self.demo_counter = 0
        else:
            self.demo_counter = (self.demo_counter + 1) % 3
            
        self.human_choice = self.choices[self.demo_counter]
        self.result_label.setText(f"Detected: {self.human_choice.capitalize()}")
        
    def play_round(self, human_choice=None):
        """Play one round of the game."""
        if human_choice is None and self.human_choice is None:
            self.result_label.setText("Please capture a gesture first!")
            return
            
        # Use camera gesture if available, otherwise use button choice
        human_choice = self.human_choice if self.human_choice else human_choice
        
        # Disable buttons during animation
        for btn in [self.rock_btn, self.paper_btn, self.scissors_btn, self.capture_btn]:
            btn.setEnabled(False)
        
        # Start robot "thinking" animation
        self.animation_counter = 0
        self.robot_choice_timer = QTimer()
        self.robot_choice_timer.timeout.connect(lambda: self.animate_robot_choice(human_choice))
        self.robot_choice_timer.start(100)  # Update every 100ms
        
    def animate_robot_choice(self, human_choice):
        """Animate robot choice before revealing final selection."""
        self.animation_counter += 1
        
        if self.animation_counter < 10:  # Animate for 1 second (10*100ms)
            # Cycle through choices for animation effect
            current = self.choices[self.animation_counter % 3]
            self.robot_choice.setPixmap(self.choice_images[current])
        else:
            # Stop animation and reveal final choice
            self.robot_choice_timer.stop()
            robot_choice = random.choice(self.choices)
            self.robot_choice.setPixmap(self.choice_images[robot_choice])
            self.determine_winner(human_choice, robot_choice)
            
            # Re-enable buttons
            for btn in [self.rock_btn, self.paper_btn, self.scissors_btn, self.capture_btn]:
                btn.setEnabled(True)
                
            # Reset human choice for next round
            self.human_choice = None
    
    def determine_winner(self, human_choice, robot_choice):
        """Determine the winner of the round and update scores."""
        if human_choice == robot_choice:
            self.result_label.setText("It's a tie!")
            return
            
        win_conditions = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }
        
        if win_conditions[human_choice] == robot_choice:
            self.result_label.setText("You win this round!")
            self.human_score += 1
            self.human_score_label.setText(f"Human: {self.human_score}")
        else:
            self.result_label.setText("Robot wins this round!")
            self.robot_score += 1
            self.robot_score_label.setText(f"Robot: {self.robot_score}")
            
    def closeEvent(self, event):
        """Clean up camera when closing."""
        if hasattr(self, 'camera'):
            self.camera.stop()
        if hasattr(self, 'camera_timer'):
            self.camera_timer.stop()
        super().closeEvent(event)
