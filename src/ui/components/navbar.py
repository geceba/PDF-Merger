from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class NavbarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50) 
        layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #E9ECEF; border-radius: 8px;")
        layout.addWidget(QLabel("Dummy Navbar", self))