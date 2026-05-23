from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import QSize, Qt

from src.ui.components.sidebar import SidebarWidget
from src.ui.components.file_list import FileListWidget
from src.ui.components.preview_panel import PreviewPanelWidget
from src.ui.components.navbar import NavbarWidget
from src.ui.components.privacy_banner import PrivacyBannerWidget

from src.ui.styles.styles import BODY_CONTAINER_STYLE, PRIVACY_BANNER_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Manager")
        self.resize(1200, 750)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.global_layout = QVBoxLayout(self.central_widget)
        self.global_layout.setContentsMargins(0, 0, 0, 0)
        self.global_layout.setSpacing(0)

        self.upper_container = QWidget(self)
        self.upper_layout = QHBoxLayout(self.upper_container)
        self.upper_layout.setContentsMargins(0, 0, 0, 0)
        self.upper_layout.setSpacing(0)

        self.global_layout.addWidget(self.upper_container, stretch=1)

        self.sidebar = SidebarWidget(self)
        self.sidebar.setFixedWidth(190)
        self.upper_layout.addWidget(self.sidebar)

        self.body_container = QWidget(self)
        self.right_layout = QVBoxLayout(self.body_container)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)
        
        self.upper_layout.addWidget(self.body_container)

        self.privacy_banner = PrivacyBannerWidget(self)
        self.global_layout.addWidget(self.privacy_banner)
        
        self.init_right_sections()

        self.apply_base_styles()
        
        self.sidebar.navigation_changed.connect(self.on_navigation_changed)

    def apply_base_styles(self):
        self.body_container.setStyleSheet(BODY_CONTAINER_STYLE)
        self.privacy_banner.setStyleSheet(PRIVACY_BANNER_STYLE)

    def init_right_sections(self):
        self.navbar = NavbarWidget(self)
        self.right_layout.addWidget(self.navbar)

        self.workspace_container = QWidget(self)
        self.workspace_layout = QHBoxLayout(self.workspace_container)
        self.workspace_layout.setContentsMargins(24, 24, 24, 16)
        self.workspace_layout.setSpacing(20)

        self.file_list = FileListWidget(self)
        self.preview_panel = PreviewPanelWidget(self)

        self.workspace_layout.addWidget(self.file_list, stretch=4)
        self.workspace_layout.addWidget(self.preview_panel, stretch=6)

        self.right_layout.addWidget(self.workspace_container, stretch=1)

        self.actions_placeholder = QWidget(self)
        self.actions_placeholder.setMinimumHeight(140)
        
        self.right_layout.addWidget(self.actions_placeholder)

    def on_navigation_changed(self, view_name):
        if view_name == "files":
            self.navbar.setVisible(True)
            self.workspace_container.setVisible(True)
            self.actions_placeholder.setVisible(True)
        elif view_name == "settings":
            self.navbar.setVisible(False)
            self.workspace_container.setVisible(False)
            self.actions_placeholder.setVisible(False)
    