from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import (LineEdit, PasswordLineEdit, PrimaryPushButton,
                             TitleLabel, BodyLabel, InfoBar, InfoBarPosition)
from ..modules.user import User
from ..modules.database import Database

class LoginWindow(QWidget):
    loginSuccess = pyqtSignal(str) # Emits role

    def __init__(self):
        super().__init__()
        self.setWindowTitle("تسجيل الدخول / Login")
        self.resize(400, 500)
        self.setStyleSheet("background-color: #f3f3f3;")

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(20)

        self.titleLabel = TitleLabel("نظام السوبر ماركت", self)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.subtitleLabel = BodyLabel("يرجى تسجيل الدخول للمتابعة / Please login to continue", self)
        self.subtitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.userEdit = LineEdit(self)
        self.userEdit.setPlaceholderText("اسم المستخدم / Username")
        self.userEdit.setFixedWidth(300)
        self.userEdit.setFixedHeight(40)

        self.passEdit = PasswordLineEdit(self)
        self.passEdit.setPlaceholderText("كلمة المرور / Password")
        self.passEdit.setFixedWidth(300)
        self.passEdit.setFixedHeight(40)

        self.loginBtn = PrimaryPushButton("تسجيل الدخول / Login", self)
        self.loginBtn.setFixedWidth(300)
        self.loginBtn.setFixedHeight(45)
        self.loginBtn.clicked.connect(self.do_login)

        self.layout.addWidget(self.titleLabel)
        self.layout.addWidget(self.subtitleLabel)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.userEdit)
        self.layout.addWidget(self.passEdit)
        self.layout.addWidget(self.loginBtn)

    def do_login(self):
        username = self.userEdit.text()
        password = self.passEdit.text()

        if not username or not password:
            self.show_error("تنبيه", "يرجى إدخال اسم المستخدم وكلمة المرور")
            return

        # Attempt to connect first if not connected
        db = Database()
        success, msg = db.connect()
        if not success:
            self.show_error("خطأ في الاتصال", f"لا يمكن الاتصال بقاعدة البيانات: {msg}")
            return

        authenticated, role_or_msg = User.authenticate(username, password)
        if authenticated:
            self.loginSuccess.emit(role_or_msg)
        else:
            self.show_error("فشل الدخول", role_or_msg)

    def show_error(self, title, content):
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
