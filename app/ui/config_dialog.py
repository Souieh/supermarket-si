from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout
from qfluentwidgets import LineEdit, PrimaryPushButton, PushButton, SubtitleLabel

from ..modules.database import Database


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إعدادات قاعدة البيانات")
        self.mainLayout = QVBoxLayout(self)

        self.titleLabel = SubtitleLabel("إعدادات قاعدة البيانات", self)
        self.hostLineEdit = LineEdit(self)
        self.portLineEdit = LineEdit(self)
        self.dbLineEdit = LineEdit(self)
        self.userLineEdit = LineEdit(self)
        self.passLineEdit = LineEdit(self)
        self.passLineEdit.setEchoMode(LineEdit.EchoMode.Password)

        self.hostLineEdit.setPlaceholderText("المضيف (مثال: localhost)")
        self.portLineEdit.setPlaceholderText("المنفذ (مثال: 27017)")
        self.dbLineEdit.setPlaceholderText("اسم قاعدة البيانات")
        self.userLineEdit.setPlaceholderText("اسم المستخدم (اختياري)")
        self.passLineEdit.setPlaceholderText("كلمة المرور (اختياري)")

        # Load existing config if any
        db = Database()
        if db.config:
            self.hostLineEdit.setText(db.config.get("host", "localhost"))
            self.portLineEdit.setText(str(db.config.get("port", 27017)))
            self.dbLineEdit.setText(db.config.get("db_name", "supermarket"))
            self.userLineEdit.setText(db.config.get("username", ""))
            self.passLineEdit.setText(db.config.get("password", ""))
        else:
            self.hostLineEdit.setText("localhost")
            self.portLineEdit.setText("27017")
            self.dbLineEdit.setText("supermarket")

        self.buttonLayout = QHBoxLayout()
        self.yesButton = PrimaryPushButton("حفظ واتصال", self)
        self.cancelButton = PushButton("إلغاء", self)

        self.yesButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.yesButton)
        self.buttonLayout.addWidget(self.cancelButton)

        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.hostLineEdit)
        self.mainLayout.addWidget(self.portLineEdit)
        self.mainLayout.addWidget(self.dbLineEdit)
        self.mainLayout.addWidget(self.userLineEdit)
        self.mainLayout.addWidget(self.passLineEdit)
        self.mainLayout.addLayout(self.buttonLayout)

        self.setMinimumWidth(400)
        self.setStyleSheet("background-color: #f3f3f3;")

    def validate(self):
        return (
            self.hostLineEdit.text()
            and self.portLineEdit.text().isdigit()
            and self.dbLineEdit.text()
        )

    def get_config(self):
        return (
            self.hostLineEdit.text(),
            self.portLineEdit.text(),
            self.dbLineEdit.text(),
            self.userLineEdit.text(),
            self.passLineEdit.text(),
        )

    def accept(self):
        if self.validate():
            super().accept()
        else:
            self.titleLabel.setText("خطأ في البيانات")
            self.titleLabel.setStyleSheet("color: red;")

    def showEvent(self, event):
        super().showEvent(event)
        frame = self.frameGeometry()
        screen = self.screen()
        if screen:
            center_point = screen.availableGeometry().center()
            frame.moveCenter(center_point)
            self.move(frame.topLeft())

    def exec(self):
        return super().exec() == QDialog.DialogCode.Accepted
