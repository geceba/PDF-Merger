from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(QPushButton("Archivos"))
        layout.addWidget(QPushButton("Combinar"))
        layout.addWidget(QPushButton("Convertir"))
        layout.addWidget(QPushButton("Comprimir"))