from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, LineEdit, PushButton, SubtitleLabel, TableWidget

from ....modules.category import Category


class CategoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CategoryPage")

        # Fix 1: Rename 'layout' to avoid conflict with QWidget's layout() method
        self.mainLayout = QVBoxLayout(self)

        self.titleLabel = SubtitleLabel("إدارة الفئات", self)

        self.actionBar = QHBoxLayout()
        self.nameEdit = LineEdit(self)
        self.nameEdit.setPlaceholderText("اسم الفئة")
        self.addButton = PushButton(FIF.ADD, "إضافة", self)
        self.addButton.clicked.connect(self.add_category)

        self.actionBar.addWidget(self.nameEdit)
        self.actionBar.addWidget(self.addButton)

        self.table = TableWidget(self)
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["الفئة"])

        # Fix 2: Safe access for horizontalHeader()
        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.deleteButton = PushButton(FIF.DELETE, "حذف الفئة المختارة", self)
        self.deleteButton.clicked.connect(self.delete_category)

        # Now use self.mainLayout instead of self.layout
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addLayout(self.actionBar)
        self.mainLayout.addWidget(self.table)
        self.mainLayout.addWidget(self.deleteButton)

        self.load_categories()

    def load_categories(self):
        categories = Category.get_all_categories()
        self.table.setRowCount(0)
        for cat in categories:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(cat["name"]))

    def add_category(self):
        name = self.nameEdit.text()
        if not name:
            return
        if Category.add_category(name):
            self.load_categories()
            self.nameEdit.clear()
            InfoBar.success("تم", "تمت إضافة الفئة", parent=self)
        else:
            InfoBar.error("خطأ", "الفئة موجودة مسبقاً", parent=self)

    def delete_category(self):
        row = self.table.currentRow()
        if row < 0:
            return
        # Fix 3: Check that item is not None before accessing .text()
        item = self.table.item(row, 0)
        if item is None:
            return
        name = item.text()
        if Category.delete_category(name):
            self.load_categories()
            InfoBar.success("تم", "تم حذف الفئة", parent=self)
