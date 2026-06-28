from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QSize
from src.ui.components.common.svg_icon import SvgIcon
from src.ui.styles.styles import FILE_CARD_BASE_STYLE

class FileCardWidget(QWidget):
    def __init__(self, index, file_name, pages, size_mb, omitted_count=0, parent=None):
        super().__init__(parent)
        self.setObjectName("FileCard")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.index = index
        self.file_name = file_name
        self.pages = pages
        self.size_mb = size_mb
        self.omitted_count = omitted_count
        
        self.init_ui()
        self.setStyleSheet(FILE_CARD_BASE_STYLE)
    
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignVCenter)

        self.drag_handle