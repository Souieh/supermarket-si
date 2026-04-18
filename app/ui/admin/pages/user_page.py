from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, MessageBox, PushButton, SubtitleLabel, TableWidget

from ....modules.user import User
from ..components.user_dialog import UserDialog


class UserPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("UserPage")
        self.mainLayout = QVBoxLayout(self)

        self.titleLabel = SubtitleLabel("إدارة المستخدمين", self)

        self.actionBar = QHBoxLayout()
        self.addButton = PushButton(FIF.ADD, "إضافة مستخدم", self)
        self.addButton.clicked.connect(self.show_add_dialog)

        self.editButton = PushButton(FIF.EDIT, "تعديل المستخدم", self)
        self.editButton.clicked.connect(self.show_edit_dialog)

        self.deleteButton = PushButton(FIF.DELETE, "حذف المستخدم", self)
        self.deleteButton.clicked.connect(self.delete_user)

        self.actionBar.addWidget(self.addButton)
        self.actionBar.addWidget(self.editButton)
        self.actionBar.addWidget(self.deleteButton)
        self.actionBar.addStretch(1)

        self.table = TableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["اسم المستخدم", "الصلاحية"])
        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addLayout(self.actionBar)
        self.mainLayout.addWidget(self.table)

        self.load_users()

    def load_users(self):
        users = User.get_all_users()
        self.table.setRowCount(0)
        for u in users:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(u["username"]))
            self.table.setItem(row, 1, QTableWidgetItem(u["role"]))

    def show_add_dialog(self):
        w = UserDialog(self.window())
        if w.exec():
            data = w.get_data()
            success, msg = User.create_user(
                data["username"], data["password"], data["role"]
            )
            if success:
                self.load_users()
                InfoBar.success("تم", msg, parent=self)
            else:
                InfoBar.error("خطأ", msg, parent=self)

    def show_edit_dialog(self):
        row = self.table.currentRow()
        if row < 0:
            return
        item_user = self.table.item(row, 0)
        item_role = self.table.item(row, 1)
        if item_user is None or item_role is None:
            return
        username = item_user.text()
        role = item_role.text()

        w = UserDialog(self.window(), {"username": username, "role": role})
        if w.exec():
            data = w.get_data()
            User.update_user(username, data)
            self.load_users()
            InfoBar.success("تم", "تم تحديث بيانات المستخدم", parent=self)

    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            return
        item = self.table.item(row, 0)
        if item is None:
            return
        username = item.text()

        if username == "admin":
            InfoBar.warning("تنبيه", "لا يمكن حذف مستخدم الأدمن الرئيسي", parent=self)
            return

        w = MessageBox(
            "تأكيد الحذف", f"هل أنت متأكد من حذف المستخدم {username}؟", self.window()
        )
        w.yesButton.setText("نعم")
        w.cancelButton.setText("إلغاء")

        if w.exec():
            User.delete_user(username)
            self.load_users()
            InfoBar.success("تم", "تم حذف المستخدم بنجاح", parent=self)
