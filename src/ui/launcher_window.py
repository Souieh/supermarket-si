from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton as QPush
from qfluentwidgets import (SubtitleLabel, PrimaryPushButton, PushButton,
                             FluentIcon as FIF, TitleLabel, CardWidget, BodyLabel)
from .config_dialog import ConfigDialog
from ..modules.database import Database

class LauncherCard(CardWidget):
    clicked = pyqtSignal()

    def __init__(self, title, icon, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn = PushButton(icon, "", self)
        self.btn.setFixedSize(100, 100)
        self.btn.setIconSize(QSize(64, 64))

        self.titleLabel = BodyLabel(title, self)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.titleLabel)
        self.setFixedSize(200, 200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn.clicked.connect(self.clicked.emit)


class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supermarket Launcher - نظام السوبر ماركت")
        self.resize(800, 500)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = TitleLabel("نظام إدارة السوبر ماركت / Supermarket System", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addSpacing(40)

        self.cardsLayout = QHBoxLayout()
        self.adminCard = LauncherCard("الإدارة / Admin", FIF.APPLICATION, self)
        self.cashierCard = LauncherCard("الكاشير (قريباً) / Cashier (Soon)", FIF.SHOPPING_CART, self)
        self.settingsCard = LauncherCard("الإعدادات / Settings", FIF.SETTING, self)

        self.cardsLayout.addWidget(self.adminCard)
        self.cardsLayout.addWidget(self.cashierCard)
        self.cardsLayout.addWidget(self.settingsCard)
        self.layout.addLayout(self.cardsLayout)

        self.statusLabel = BodyLabel("", self)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.statusLabel)

        self.check_connection()

    def check_connection(self):
        db = Database()
        success, message = db.connect()
        if success:
            self.statusLabel.setText("متصل بقاعدة البيانات / Database Connected")
            self.statusLabel.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.statusLabel.setText(f"خطأ في الاتصال: {message} / Connection Error")
            self.statusLabel.setStyleSheet("color: red; font-weight: bold;")
