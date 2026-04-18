from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit,
                            ComboBox)


class UserDialog(MessageBoxBase):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        title = "تعديل مستخدم" if user else "إضافة مستخدم جديد"
        self.titleLabel = SubtitleLabel(title, self)

        self.userEdit = LineEdit(self)
        self.userEdit.setPlaceholderText("اسم المستخدم")

        self.passEdit = LineEdit(self)
        self.passEdit.setPlaceholderText("كلمة المرور")
        self.passEdit.setEchoMode(LineEdit.EchoMode.Password)
        if user:
            self.passEdit.setPlaceholderText("اتركه فارغاً للإبقاء على كلمة المرور الحالية")

        self.roleCombo = ComboBox(self)
        self.roleCombo.addItem("أدمن / Admin", "admin")
        self.roleCombo.addItem("كاشير / Cashier", "cashier")

        if user:
            self.userEdit.setText(user["username"])
            self.userEdit.setEnabled(False)
            self.roleCombo.setCurrentIndex(0 if user["role"] == "admin" else 1)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.userEdit)
        self.viewLayout.addWidget(self.passEdit)
        self.viewLayout.addWidget(self.roleCombo)

        self.yesButton.setText("حفظ")
        self.cancelButton.setText("إلغاء")

    def validate(self):
        if self.user:
            return True
        return self.userEdit.text() and self.passEdit.text()

    def accept(self):
        if self.validate():
            super().accept()

    def showEvent(self, event):
        super().showEvent(event)
        frame = self.frameGeometry()
        screen = self.screen()
        if screen:
            center = screen.availableGeometry().center()
            frame.moveCenter(center)
            self.move(frame.topLeft())

    def get_data(self):
        return {
            "username": self.userEdit.text(),
            "password": self.passEdit.text(),
            "role": self.roleCombo.currentData()
        }
