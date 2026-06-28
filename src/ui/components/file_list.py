from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class FileListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #FFFFFF; border: 1px solid #DEE2E6; border-radius: 12px;")
        layout.addWidget(QLabel("Dummy File List", self))