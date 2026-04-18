from PyQt6.QtCore import Qt, QSize, pyqtSignal, QUrl
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (PushButton, FluentIcon as FIF, TitleLabel,
                            CardWidget, BodyLabel, HyperlinkLabel, MessageBox)
from ..modules.database import Database


class LauncherCard(CardWidget):
    clicked = pyqtSignal()

    def __init__(self, title, icon, parent=None):
        super().__init__(parent)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn = PushButton(icon, "", self)
        self.btn.setFixedSize(100, 100)
        self.btn.setIconSize(QSize(64, 64))

        self.titleLabel = BodyLabel(title, self)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")

        self.mainLayout.addWidget(self.btn)
        self.mainLayout.addWidget(self.titleLabel)
        self.setFixedSize(200, 200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn.clicked.connect(self.clicked.emit)


class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام السوبر ماركت")
        self.resize(800, 500)
        self.setStyleSheet("background-color: #f3f3f3;")
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = TitleLabel("نظام إدارة السوبر ماركت", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.title)
        self.mainLayout.addSpacing(40)

        self.cardsLayout = QHBoxLayout()
        self.adminCard = LauncherCard("الإدارة", FIF.APPLICATION, self)
        self.cashierCard = LauncherCard("الكاشير (قريباً)", FIF.SHOPPING_CART, self)
        self.settingsCard = LauncherCard("الإعدادات", FIF.SETTING, self)

        self.cardsLayout.addWidget(self.adminCard)
        self.cardsLayout.addWidget(self.cashierCard)
        self.cardsLayout.addWidget(self.settingsCard)
        self.mainLayout.addLayout(self.cardsLayout)

        self.statusLabel = BodyLabel("", self)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.statusLabel)

        self.mainLayout.addStretch(1)
        self.githubLabel = HyperlinkLabel(QUrl("https://github.com/Souieh/supermarket-si"), "GitHub: Souieh", self)
        self.mainLayout.addWidget(self.githubLabel, 0, Qt.AlignmentFlag.AlignCenter)

        self.check_connection()

    def check_connection(self):
        db = Database()
        success, message = db.connect()
        if success:
            self.statusLabel.setText("متصل بقاعدة البيانات")
            self.statusLabel.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.statusLabel.setText(f"خطأ في الاتصال: {message}")
            self.statusLabel.setStyleSheet("color: red; font-weight: bold;")

    def closeEvent(self, event):
        w = MessageBox("تأكيد الخروج", "هل أنت متأكد من رغبتك في إغلاق البرنامج؟", self)
        w.yesButton.setText("نعم")
        w.cancelButton.setText("إلغاء")
        if w.exec():
            event.accept()
        else:
            event.ignore()
