from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, 
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QPixmap, QFont, QPainter
from PySide6.QtCore import Qt


class HomePage(QWidget):
    """Landing page with navigation, game description, and trending games section."""

    def __init__(self, navigate_callback: object):
        super().__init__()
        self.navigate_callback = navigate_callback
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            background-color: #3b1d9e; 
            color: white;
            font-family: Arial;
        """)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(30)

        # Navigation bar
        nav_bar = self.create_nav_bar()
        main_layout.addLayout(nav_bar)

        # Content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(50)

        # Left side - Text content
        left_content = QVBoxLayout()
        left_content.setSpacing(20)

        # Game title
        title = QLabel("Rock, Paper\nScissors")
        title.setFont(QFont("Arial", 35, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Description
        description = QLabel(
            "Lorem ipsum is simply dummy text of the printing and "
            "typesetting industry. Lorem ipsum has been the industry's "
            "standard."
        )
        description.setFont(QFont("Arial", 12))
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Profile and Start buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        profile_btn = QPushButton("Profile")
        profile_btn.setStyleSheet(self.button_style("#6a4bce"))
        profile_btn.setFixedSize(100, 40)

        start_btn = QPushButton("Start Game")
        start_btn.setStyleSheet(self.button_style("orange"))
        start_btn.setFixedSize(120, 40)
        start_btn.clicked.connect(self.navigate_callback)

        button_layout.addWidget(profile_btn)
        button_layout.addWidget(start_btn)
        button_layout.addStretch()

        # Add to left content
        left_content.addWidget(title)
        left_content.addWidget(description)
        left_content.addLayout(button_layout)
        left_content.addStretch()

        # Right side - Image placeholder (would be replaced with actual image)
        image_label = QLabel()
        image_label.setFixedSize(400, 300)
        image_label.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border-radius: 10px;")

        # Add to content layout
        content_layout.addLayout(left_content, stretch=2)
        content_layout.addWidget(image_label, stretch=1, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(content_layout)

        # Trending games section
        trending_section = self.create_trending_section()
        main_layout.addLayout(trending_section)

        # Footer
        footer = QLabel("Proved by predesigner")
        footer.setFont(QFont("Arial", 8))
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(footer)

    def create_nav_bar(self):
        nav_bar = QHBoxLayout()
        nav_bar.setSpacing(30)

        # Logo placeholder
        logo = QLabel("LOGO")
        logo.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        # Navigation items
        nav_items = ["Home", "About us", "Games", "News"]
        for item in nav_items:
            btn = QPushButton(item)
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    background: transparent;
                    border: none;
                    font-size: 14px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    color: orange;
                }
            """)
            nav_bar.addWidget(btn)

        nav_bar.addStretch()
        return nav_bar

    def create_trending_section(self):
        trending_layout = QVBoxLayout()
        trending_layout.setSpacing(15)

        # Section header
        header = QHBoxLayout()
        title = QLabel("Currently Trending Games")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        see_all = QPushButton("SEE ALL")
        see_all.setStyleSheet("""
            QPushButton {
                color: orange;
                background: transparent;
                border: none;
                font-size: 12px;
            }
        """)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(see_all)

        # Game cards
        games_layout = QHBoxLayout()
        games_layout.setSpacing(15)

        for i in range(4):
            card = QVBoxLayout()
            card.setSpacing(5)
            
            # Game image placeholder
            game_img = QLabel()
            game_img.setFixedSize(80, 80)
            game_img.setStyleSheet("""
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            """)
            
            # Followers label
            followers = QLabel("40 Followers")
            followers.setFont(QFont("Arial", 8))
            followers.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            card.addWidget(game_img)
            card.addWidget(followers)
            games_layout.addLayout(card)

        trending_layout.addLayout(header)
        trending_layout.addLayout(games_layout)

        # News section
        news = QVBoxLayout()
        news.setSpacing(10)
        
        news_title = QLabel("Lorem Ipsum")
        news_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        
        news_content = QLabel(
            "Lorem ipsum is simply dummy text of the printing and typesetting "
            "industry.Lorem ipsum has been the industry's standard dummy text "
            "ever since the 1500s."
        )
        news_content.setFont(QFont("Arial", 10))
        news_content.setWordWrap(True)
        
        read_more = QPushButton("Read more")
        read_more.setStyleSheet("""
            QPushButton {
                color: orange;
                background: transparent;
                border: none;
                font-size: 12px;
                text-align: left;
                padding: 0;
            }
        """)
        
        news.addWidget(news_title)
        news.addWidget(news_content)
        news.addWidget(read_more)
        
        trending_layout.addLayout(news)

        return trending_layout

    def button_style(self, bg_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {'#ffa500' if bg_color == 'orange' else '#7d5cd9'};
            }}
        """

    def paintEvent(self, event):
        """Optional: Add background image/pattern if needed"""
        painter = QPainter(self)
        painter.setOpacity(0.05)
        # If you have a background image:
        # pixmap = QPixmap("path/to/background.png")
        # painter.drawPixmap(self.rect(), pixmap)
        painter.end()