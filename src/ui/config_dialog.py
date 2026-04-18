from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (SubtitleLabel, LineEdit,
                             PrimaryPushButton, PushButton, FluentIcon as FIF)
from ..modules.database import Database

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إعدادات قاعدة البيانات / Database Settings")
        self.layout = QVBoxLayout(self)

        self.titleLabel = SubtitleLabel("إعدادات قاعدة البيانات / Database Settings", self)
        self.hostLineEdit = LineEdit(self)
        self.portLineEdit = LineEdit(self)
        self.dbLineEdit = LineEdit(self)
        self.userLineEdit = LineEdit(self)
        self.passLineEdit = LineEdit(self)
        self.passLineEdit.setEchoMode(LineEdit.EchoMode.Password)

        self.hostLineEdit.setPlaceholderText("المضيف / Host (e.g. localhost)")
        self.portLineEdit.setPlaceholderText("المنفذ / Port (e.g. 27017)")
        self.dbLineEdit.setPlaceholderText("اسم قاعدة البيانات / Database Name")
        self.userLineEdit.setPlaceholderText("اسم المستخدم / Username (Optional)")
        self.passLineEdit.setPlaceholderText("كلمة المرور / Password (Optional)")

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
        self.yesButton = PrimaryPushButton("حفظ واتصال / Save & Connect", self)
        self.cancelButton = PushButton("إلغاء / Cancel", self)

        self.yesButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.yesButton)
        self.buttonLayout.addWidget(self.cancelButton)

        self.layout.addWidget(self.titleLabel)
        self.layout.addWidget(self.hostLineEdit)
        self.layout.addWidget(self.portLineEdit)
        self.layout.addWidget(self.dbLineEdit)
        self.layout.addWidget(self.userLineEdit)
        self.layout.addWidget(self.passLineEdit)
        self.layout.addLayout(self.buttonLayout)

        self.setMinimumWidth(400)
        self.setStyleSheet("background-color: #f3f3f3;")

    def validate(self):
        return (self.hostLineEdit.text() and
                self.portLineEdit.text().isdigit() and
                self.dbLineEdit.text())

    def get_config(self):
        return (self.hostLineEdit.text(),
                self.portLineEdit.text(),
                self.dbLineEdit.text(),
                self.userLineEdit.text(),
                self.passLineEdit.text())

    def accept(self):
        if self.validate():
            super().accept()
        else:
            self.titleLabel.setText("خطأ في البيانات / Invalid Data")
            self.titleLabel.setStyleSheet("color: red;")

    def exec(self):
        return super().exec() == QDialog.DialogCode.Accepted
