from PySide6.QtWidgets import QApplication
from pages.home_page.home_page import HomePage
import sys

app = QApplication(sys.argv)
widget = HomePage()
widget.show()

app.exec() 