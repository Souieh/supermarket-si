from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit,
                            ComboBox)


class UserDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("إضافة مستخدم جديد", self)

        self.userEdit = LineEdit(self)
        self.userEdit.setPlaceholderText("اسم المستخدم")

        self.passEdit = LineEdit(self)
        self.passEdit.setPlaceholderText("كلمة المرور")
        self.passEdit.setEchoMode(LineEdit.EchoMode.Password)

        self.roleCombo = ComboBox(self)
        self.roleCombo.addItem("أدمن / Admin", "admin")
        self.roleCombo.addItem("كاشير / Cashier", "cashier")

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.userEdit)
        self.viewLayout.addWidget(self.passEdit)
        self.viewLayout.addWidget(self.roleCombo)

        self.yesButton.setText("حفظ")
        self.cancelButton.setText("إلغاء")

    def validate(self):
        return self.userEdit.text() and self.passEdit.text()

    def accept(self):
        if self.validate():
            super().accept()

    def showEvent(self, event):
        super().showEvent(event)
        frame = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frame.moveCenter(screen)
        self.move(frame.topLeft())

    def get_data(self):
        return {
            "username": self.userEdit.text(),
            "password": self.passEdit.text(),
            "role": self.roleCombo.currentData()
        }
