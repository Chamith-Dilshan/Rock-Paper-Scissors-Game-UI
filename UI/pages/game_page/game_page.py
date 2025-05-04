from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint, QByteArray
from PySide6.QtGui import QFont, QPixmap
import random

class GamePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
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

        main_layout = QVBoxLayout(self)

        # Top Title
        title = QLabel("Let's Play Rock - Paper - Scissors ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Score Labels
        self.computer_score_label = QLabel("Robot: 0")
        self.player_score_label = QLabel("You: 0")
        for lbl in (self.computer_score_label, self.player_score_label):
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))

         # VS label
        self.vs_label = QLabel("VS")
        self.vs_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vs_label.setStyleSheet("""
            QLabel {
                background-color: orange;
                color: white;
                border-radius: 30px;
                padding: 15px;
                min-width: 60px;
                min-height: 60px;
                font-size: 20px;
                }
            """)

        player_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.computer_score_label)
        left_layout.addWidget(self.computer_img, alignment=Qt.AlignmentFlag.AlignCenter)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.player_score_label)
        right_layout.addWidget(self.player_img, alignment=Qt.AlignmentFlag.AlignCenter)

        player_layout.addLayout(left_layout)
        player_layout.addWidget(self.vs_label)
        player_layout.addLayout(right_layout)
        main_layout.addLayout(player_layout)

        # Result Label with opacity animation
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.result_label.setStyleSheet("color: lightgreen;")
        opacity_effect = QGraphicsOpacityEffect(self.result_label)
        opacity_effect.setOpacity(0)
        self.result_label.setGraphicsEffect(opacity_effect)
        main_layout.addWidget(self.result_label)

        # Timer and Button
        self.timer_label = QLabel("Time: 3")
        self.timer_label.setFont(QFont("Arial", 14))
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("background-color: orange; color: white; padding: 10px 20px; font-weight: bold;")
        self.start_button.clicked.connect(self.start_game)

        bottom_layout = QVBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_layout.addWidget(self.timer_label)
        bottom_layout.addWidget(self.start_button)

        main_layout.addSpacing(20)
        main_layout.addLayout(bottom_layout)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 3

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

        if "Robot" in result:
            self.computer_score += 1
        elif "You" in result:
            self.player_score += 1

        self.computer_score_label.setText(f"Robot: {self.computer_score}")
        self.player_score_label.setText(f"You: {self.player_score}")
        self.fade_in_result(result)
    
    def fade_in_result(self, text: str):
        self.result_label.setText(text)

        # Ensure the result_label has a QGraphicsOpacityEffect applied
        effect = self.result_label.graphicsEffect()
        if not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(self.result_label)
            self.result_label.setGraphicsEffect(effect)

        # Create and configure the opacity animation
        animation = QPropertyAnimation(effect, QByteArray(b"opacity"), self)
        animation.setDuration(800)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Start the animation and keep a reference to prevent garbage collection
        animation.start()
        self.result_fade_anim = animation # Prevent GC



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
        self.anim = anim  # keep reference alive

    def determine_winner(self, comp: str, player: str) -> str:
        print (f"Computer: {comp}, Player: {player}")
        beats = {
            "rock": "scissors",
            "scissors": "paper",
            "paper": "rock"
        }

        if comp == player:
            return "It's a Tie!"
        elif beats[comp] == player:
            return "Robot Wins!"
        else:
            return "You Win!"
