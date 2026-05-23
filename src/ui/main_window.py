from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import QSize

from src.ui.components.sidebar import SidebarWidget
from src.ui.components.file_list import FileListWidget
from src.ui.components.preview_panel import PreviewPanelWidget
from src.ui.components.navbar import NavbarWidget

from src.ui.styles.styles import BODY_CONTAINER_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Manager")
        self.resize(1200, 750)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.sidebar = SidebarWidget(self)
        self.main_layout.addWidget(self.sidebar)

        self.body_container = QWidget(self)
        self.body_layout = QVBoxLayout(self.body_container)
        self.body_layout.setContentsMargins(20, 15, 20, 15)
        self.body_layout.setSpacing(15)

        self.navbar = NavbarWidget(self)
        self.body_layout.addWidget(self.navbar)

        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(20)

        self.file_list_panel = FileListWidget(self)
        self.preview_panel = PreviewPanelWidget(self)

        self.content_layout.addWidget(self.file_list_panel, stretch=3)
        self.content_layout.addWidget(self.preview_panel, stretch=2)

        self.body_layout.addLayout(self.content_layout)
        self.main_layout.addWidget(self.body_container)

        self.apply_base_styles()

    def apply_base_styles(self):
        self.body_container.setStyleSheet(BODY_CONTAINER_STYLE)
        