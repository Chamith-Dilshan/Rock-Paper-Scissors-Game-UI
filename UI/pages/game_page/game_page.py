from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QGraphicsOpacityEffect, 
    QGridLayout, QSizePolicy, QSpacerItem, QMenuBar, QMenu, QDialog,
    QMessageBox
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint, QByteArray
from PySide6.QtGui import QFont, QPixmap, QImage
import random
import cv2
from pages.widgets.vs_widget import VSWidget

class CameraWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Camera Feed")
        self.setFixedSize(640, 480)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        
    def start_camera(self):
        """Attempt to start the camera and return success status"""
        try:
            self.capture = cv2.VideoCapture(0)
            if not self.capture.isOpened():
                raise RuntimeError("Could not open camera")
            self.timer.start(30)
            return True
        except Exception as e:
            print(f"Camera error: {str(e)}")
            return False

    def update_frame(self):
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()

    def stop_camera(self):
        if self.capture and self.capture.isOpened():
            self.capture.release()
        self.timer.stop()

    def show_camera(self):
        """Show the camera window and display status message"""
        if self.capture and self.capture.isOpened():
            self.show()
            QMessageBox.information(self, "Camera Status", 
                                   "Camera is now active and showing live feed!")
        else:
            QMessageBox.critical(self, "Camera Error", 
                               "Camera is not available. Please check your camera connection.")

class GamePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.camera_window = None
        self.camera_active = False
        self.init_ui()
        self.initialize_camera()

    def initialize_camera(self):
        """Initialize camera and show appropriate message"""
        self.camera_window = CameraWindow(self)
        if self.camera_window.start_camera():
            # Don't show message here - we'll show it when user explicitly opens camera
            pass
        else:
            QMessageBox.critical(self, "Camera Error", 
                               "Could not initialize camera. Please check if camera is connected and try again.")

    def init_ui(self):
        self.setStyleSheet("background-color: #3b1d9e; color: white;")
        self.choices = ["rock", "paper", "scissors"]
        self.image_paths = {
            "rock": "assets/images/rock.png",
            "paper": "assets/images/paper.png",
            "scissors": "assets/images/scissors.png"
        }

        # Initialize QLabel for computer and player images
        self.computer_img = QLabel()
        self.computer_img.setPixmap(QPixmap(self.image_paths["rock"]).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        self.computer_img.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.player_img = QLabel()
        self.player_img.setPixmap(QPixmap(self.image_paths["rock"]).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        self.player_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.player_score = 0
        self.computer_score = 0

        # Menu Bar
        menu_bar = QMenuBar(self)
        menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #3b1d9e;
                color: white;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 15px;
            }
            QMenuBar::item:selected {
                background-color: #5a3dbf;
            }
            QMenu {
                background-color: #2c1584;
                color: white;
                border: 1px solid #888;
            }
            QMenu::item {
                background-color: transparent;
                padding: 6px 20px;
            }
            QMenu::item:selected {
                background-color: #ff9900;
                color: black;
            }
        """)

        # Create the "Actions" menu
        actions_menu = QMenu("Actions", self)
        camera_action = actions_menu.addAction("Show Camera")
        camera_action.triggered.connect(self.show_camera_window)
        ai_action = actions_menu.addAction("Show AI")
        ai_action.triggered.connect(self.show_ai_info)

        menu_bar.addMenu(actions_menu)

        # Main Layout
        main_layout = QVBoxLayout(self)

        # Grid Layout
        grid_layout = QGridLayout()

        # Top Title
        title = QLabel("Let's Play Rock - Paper - Scissors ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        grid_layout.addWidget(title, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        # Score Labels
        self.computer_score_label = QLabel("Computer: 0")
        self.player_score_label = QLabel("Player: 0")
        for lbl in (self.computer_score_label, self.player_score_label):
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))

        # VS Layout
        self.vs_widget = VSWidget()

        # Add components to the grid layout
        grid_layout.addWidget(self.computer_score_label, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.player_score_label, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.computer_img, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.vs_widget, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.player_img, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        # Result Label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.result_label.setStyleSheet("color: lightgreen;")
        opacity_effect = QGraphicsOpacityEffect(self.result_label)
        opacity_effect.setOpacity(0)
        self.result_label.setGraphicsEffect(opacity_effect)
        grid_layout.addWidget(self.result_label, 3, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        # Timer and Button
        self.timer_label = QLabel("Time: 3")
        self.timer_label.setFont(QFont("Arial", 14))
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: black;
                font-size: 30px;
                font-weight: bold;
                border: none;
                border-radius: 50px;
                width: 100px;
                height: 100px;
            }
            QPushButton:hover {
                background-color: darkorange;
            }
        """)
        self.start_button.clicked.connect(self.start_game)

        bottom_layout = QVBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_layout.addWidget(self.timer_label)
        bottom_layout.addWidget(self.start_button)

        # Add bottom layout to the grid
        grid_layout.addLayout(bottom_layout, 4, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add a spacer to the grid layout
        grid_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed), 5, 0, 1, 3)

        # Add the grid layout to the main layout
        main_layout.addLayout(grid_layout)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 3

    def show_camera_window(self):
        """Show camera window with status message"""
        if self.camera_window:
            self.camera_window.show_camera()

    def show_ai_info(self):
        """Show information about the AI"""
        QMessageBox.information(self, "AI Information", 
                              "This game uses a simple random choice algorithm for the computer player.")

    def start_game(self):
        self.result_label.setText("")
        opacity_effect = self.result_label.graphicsEffect()
        if isinstance(opacity_effect, QGraphicsOpacityEffect):
            opacity_effect.setOpacity(0)
        self.time_left = 3
        self.timer_label.setText(f"Time: {self.time_left}")
        self.timer.start()

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time: {self.time_left}")
        if self.time_left <= 0:
            self.timer.stop()
            self.play_round()

    def play_round(self):
        comp_choice = random.choice(self.choices)
        player_choice = random.choice(self.choices)

        comp_pixmap = QPixmap(self.image_paths[comp_choice]).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio)
        player_pixmap = QPixmap(self.image_paths[player_choice]).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio)

        self.animate_choice(comp_pixmap)
        self.player_img.setPixmap(player_pixmap)

        result = self.determine_winner(comp_choice, player_choice)

        if "Computer" in result:
            self.computer_score += 1
        elif "You" in result:
            self.player_score += 1

        self.computer_score_label.setText(f"Computer: {self.computer_score}")
        self.player_score_label.setText(f"You: {self.player_score}")
        self.fade_in_result(result)
    
    def fade_in_result(self, text: str):
        self.result_label.setText(text)
        effect = self.result_label.graphicsEffect()
        if not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(self.result_label)
            self.result_label.setGraphicsEffect(effect)

        animation = QPropertyAnimation(effect, QByteArray(b"opacity"), self)
        animation.setDuration(800)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        self.result_fade_anim = animation

    def animate_choice(self, new_pixmap: QPixmap):
        start_pos = self.computer_img.pos() - QPoint(100, 0)
        end_pos = self.computer_img.pos()

        self.computer_img.setPixmap(new_pixmap)
        self.computer_img.move(start_pos)

        anim = QPropertyAnimation(self.computer_img, QByteArray(b"pos"))
        anim.setDuration(500)
        anim.setStartValue(start_pos)
        anim.setEndValue(end_pos)
        anim.setEasingCurve(QEasingCurve.Type.OutBack)
        anim.start()
        self.anim = anim

    def determine_winner(self, comp: str, player: str) -> str:
        beats = {
            "rock": "scissors",
            "scissors": "paper",
            "paper": "rock"
        }

        if comp == player:
            return "It's a Tie!"
        elif beats[comp] == player:
            return "Computer Wins!"
        else:
            return "You Win!"

    def closeEvent(self, event):
        if self.camera_window:
            self.camera_window.close()
        event.accept()
