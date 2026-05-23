from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
class PrivacyBannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignCenter)

        self.icon_label = QLabel(self)
        self.icon_label.setObjectName("PrivacyIcon")

        svg_path = "src/ui/assets/shield_check.svg"
        icon_size = QSize(20, 20)

        pixmap = QPixmap(icon_size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        renderer = QSvgRenderer(svg_path)
        renderer.render(painter)
        painter.end()

        self.icon_label.setPixmap(pixmap)
        self.icon_label.setFixedSize(icon_size)

        self.text_label = QLabel(
            "Tus archivos no salen de aquí. Todo el procesamiento se realiza de forma 100% local y segura."
        )
        self.text_label.setObjectName("PrivacyText")
        self.text_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
