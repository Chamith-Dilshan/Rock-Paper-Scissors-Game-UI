from PySide6.QtWidgets import QWidget

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rock Paper Scissors")
        self.setGeometry(100, 100, 300, 100)