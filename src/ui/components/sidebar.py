from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from src.ui.styles.styles import SIDEBAR_STYLE

class SidebarWidget(QWidget):
    navigation_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.nav_buttons = {}
        self.init_ui()
        self.setStyleSheet(SIDEBAR_STYLE)

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 24, 16, 24)
        self.main_layout.setSpacing(6)

        self.logo_container = QWidget()
        logo_layout = QVBoxLayout(self.logo_container)
        logo_layout.setContentsMargins(8, 0, 8, 20)
        logo_layout.setSpacing(4)


        self.logo_title = QLabel("PDF Manager")
        self.logo_title.setObjectName("logoTitle")
        self.logo_subtitle = QLabel("Merge, Split, Organize")
        self.logo_subtitle.setObjectName("logoSubtitle")
        logo_layout.addWidget(self.logo_title)
        logo_layout.addWidget(self.logo_subtitle)
        self.main_layout.addWidget(self.logo_container)

        self.add_section_header("Navigation")
        self.btn_files = self.create_nav_button("Files", "files")
        self.main_layout.addWidget(self.btn_files)
        self.nav_buttons["files"] = self.btn_files

        self.add_section_header("Actions")
        self.btn_merge = self.create_nav_button("Merge PDFs", "merge")
        self.main_layout.addWidget(self.btn_merge)
        self.nav_buttons["merge"] = self.btn_merge

        self.setup_convert_menu()

        self.btn_compress = self.create_nav_button("Compress PDFs", "compress")
        self.main_layout.addWidget(self.btn_compress)
        self.nav_buttons["compress"] = self.btn_compress

        self.add_section_header("Settings")
        self.btn_settings = self.create_nav_button("Settings", "settings")
        self.main_layout.addWidget(self.btn_settings)
        self.nav_buttons["settings"] = self.btn_settings

        self.set_active_button("files")

    def add_section_header(self, text):
        header = QLabel(text)
        header.setObjectName("SectionHeader")
        header.setContentsMargins(8, 8, 0, 4)
        self.main_layout.addWidget(header)

    def create_nav_button(self, text, view_name, is_submenu=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        
        if is_submenu:
            btn.setProperty("class", "SubMenuButton")
        
        btn.clicked.connect(lambda: self.on_nav_clicked(view_name))
        return btn
    
    def setup_convert_menu(self):
        self.btn_convert = QPushButton("Convert PDFs")
        self.btn_convert.setCheckable(True)
        self.btn_convert.setCursor(Qt.PointingHandCursor)
        self.main_layout.addWidget(self.btn_convert)
        self.nav_buttons["convert"] = self.btn_convert

        self.convert_submenu_widget = QWidget()
        self.convert_submenu_widget.setObjectName("SubMenuContainer")
        submenu_layout = QVBoxLayout(self.convert_submenu_widget)
        submenu_layout.setContentsMargins(0, 0, 0, 0)
        submenu_layout.setSpacing(4)

        self.btn_convert_to_word = self.create_nav_button("To Word", "convert_word", is_submenu=True)
        self.btn_convert_to_excel = self.create_nav_button("To Excel", "convert_excel", is_submenu=True)
        submenu_layout.addWidget(self.btn_convert_to_word)
        submenu_layout.addWidget(self.btn_convert_to_excel)

        self.main_layout.addWidget(self.convert_submenu_widget)

        self.nav_buttons["convert_word"] = self.btn_convert_to_word
        self.nav_buttons["convert_excel"] = self.btn_convert_to_excel

        self.convert_submenu_widget.hide()
        self.btn_convert.clicked.connect(self.toggle_convert_submenu)

    def toggle_convert_submenu(self):
        if self.convert_submenu_widget.isVisible():
            self.convert_submenu_widget.hide()
        else:
            self.convert_submenu_widget.show()
            self.on_nav_clicked("convert")

    def on_nav_clicked(self, view_name):
        self.set_active_button(view_name)
        self.navigation_requested.emit(view_name)

    def set_active_button(self, active_view_name):
        for view_name, button in self.nav_buttons.items():
            if view_name == "convertir":
                is_active = active_view_name in ["convertir", "convertir_word", "convertir_excel"]
            else:
                is_active = (view_name == active_view_name)

            button.setChecked(is_active)
            button.setProperty("active", is_active)
            button.style().unpolish(button)
            button.style().polish(button)