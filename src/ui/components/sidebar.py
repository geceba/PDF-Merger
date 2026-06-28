from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QButtonGroup
from PySide6.QtCore import QSize, Qt, Signal

from src.ui.components.common.svg_icon import SvgIcon
from src.ui.styles.styles import SIDEBAR_STYLE

class SidebarWidget(QWidget):
    navigation_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.nav_buttons = {}

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.init_ui()
        self.setStyleSheet(SIDEBAR_STYLE)

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 24, 16, 24)
        self.main_layout.setSpacing(8)

        self.logo_container = QWidget(self)
        logo_layout = QVBoxLayout(self.logo_container)
        logo_layout.setContentsMargins(8, 0, 8, 20)
        logo_layout.setSpacing(4)

        self.logo_title = QLabel("PDF Manager", self.logo_container)
        self.logo_title.setObjectName("LogoTitle")
        self.logo_subtitle = QLabel("Unifica. Organiza. Simplifica.")
        self.logo_subtitle.setObjectName("LogoSubtitle")

        logo_layout.addWidget(self.logo_title)
        logo_layout.addWidget(self.logo_subtitle)
        self.main_layout.addWidget(self.logo_container)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        self.btn_files = QPushButton("Archivos", self)
        self.btn_files.setProperty("class", "SidebarBtn")
        self.btn_files.setCursor(Qt.PointingHandCursor)

        files_icon = SvgIcon("src/ui/assets/files.svg", size=(18, 18))
        self.btn_files.setIcon(files_icon.pixmap())
        self.btn_files.setIconSize(QSize(18, 18)) 

        self.btn_files.clicked.connect(lambda: self.on_nav_clicked("files"))
        self.main_layout.addWidget(self.btn_files)
        self.nav_buttons["files"] = self.btn_files

        self.btn_config = QPushButton("Configuracion", self)
        self.btn_config.setProperty("class", "SidebarBtn")
        self.btn_config.setCursor(Qt.PointingHandCursor)

        config_icon = SvgIcon("src/ui/assets/settings.svg", size=(18, 18))
        self.btn_config.setIcon(config_icon.pixmap())
        self.btn_config.setIconSize(QSize(18, 18))
        self.btn_config.clicked.connect(lambda: self.on_nav_clicked("settings"))
        self.main_layout.addWidget(self.btn_config)
        self.nav_buttons["settings"] = self.btn_config
        self.button_group.addButton(self.btn_config)

        self.main_layout.addStretch()
        self.set_active_button("files")

    def on_nav_clicked(self, view_name):
        self.set_active_button(view_name)
        self.navigation_changed.emit(view_name)
    
    def set_active_button(self, active_view_name):
        for view_name, button in self.nav_buttons.items():
            is_active = (view_name == active_view_name)
            
            button.setProperty("active", is_active)

            button.style().unpolish(button)
            button.style().polish(button)