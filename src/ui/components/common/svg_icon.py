from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer

class SvgIcon(QLabel):
    def __init__(self, svg_path, size=(16, 16), parent=None):
        super().__init__(parent)
        self.svg_path = svg_path
        self.icon_size = QSize(size[0], size[1]) if isinstance(size, tuple) else size
        
        self.init_icon()

    def init_icon(self):
        self.setFixedSize(self.icon_size)
        
        pixmap = QPixmap(self.icon_size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        renderer = QSvgRenderer(self.svg_path)
        renderer.render(painter)
        painter.end()
        
        self.setPixmap(pixmap)