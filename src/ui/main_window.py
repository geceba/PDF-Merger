from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from ui.components.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Manager")
        self.resize(1400, 900)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()
        central.setLayout(layout)

        self.sidebar = Sidebar()

        layout.addWidget(self.sidebar, 1)