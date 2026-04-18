from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import (LineEdit, PasswordLineEdit, PrimaryPushButton,
                            PushButton, FluentIcon as FIF, MessageBox,
                            TitleLabel, BodyLabel, InfoBar, InfoBarPosition)
from ..modules.user import User
from ..modules.database import Database


class LoginWindow(QWidget):
    loginSuccess = pyqtSignal(str)  # Emits role
    returnToLauncher = pyqtSignal()

    def __init__(self, target_role="admin", title="تسجيل دخول الإدارة"):
        super().__init__()
        self.target_role = target_role
        self.setWindowTitle(title)
        self.resize(400, 500)
        self.setStyleSheet("background-color: #f3f3f3;")

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setSpacing(20)

        self.titleLabel = TitleLabel(title, self)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.subtitleLabel = BodyLabel("يرجى تسجيل الدخول للمتابعة", self)
        self.subtitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.userEdit = LineEdit(self)
        self.userEdit.setPlaceholderText("اسم المستخدم")
        self.userEdit.setFixedWidth(300)
        self.userEdit.setFixedHeight(40)

        self.passEdit = PasswordLineEdit(self)
        self.passEdit.setPlaceholderText("كلمة المرور")
        self.passEdit.setFixedWidth(300)
        self.passEdit.setFixedHeight(40)

        self.loginBtn = PrimaryPushButton("تسجيل الدخول", self)
        self.loginBtn.setFixedWidth(300)
        self.loginBtn.setFixedHeight(45)
        self.loginBtn.clicked.connect(self.do_login)

        self.homeBtn = PushButton(FIF.HOME, "العودة للرئيسية", self)
        self.homeBtn.setFixedWidth(300)
        self.homeBtn.setFixedHeight(40)
        self.homeBtn.clicked.connect(self.returnToLauncher.emit)

        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.subtitleLabel)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.userEdit)
        self.mainLayout.addWidget(self.passEdit)
        self.mainLayout.addWidget(self.loginBtn)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addWidget(self.homeBtn)

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
            if role_or_msg == self.target_role:
                self.loginSuccess.emit(role_or_msg)
            else:
                self.show_error("فشل الدخول", f"هذا الحساب ليس {self.target_role}")
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
