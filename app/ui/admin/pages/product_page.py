from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    InfoBar,
    LineEdit,
    MessageBox,
    PushButton,
    SubtitleLabel,
    TableWidget,
)

from ....modules.product import Product
from ..components.product_dialog import ProductDialog


class ProductPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ProductPage")
        self.layout = QVBoxLayout(self)

        self.titleLabel = SubtitleLabel("إدارة المنتجات", self)

        # Search and Action Bar
        self.actionBar = QHBoxLayout()
        self.searchEdit = LineEdit(self)
        self.searchEdit.setPlaceholderText("بحث بالرمز، الاسم، أو الفئة")
        self.searchEdit.textChanged.connect(self.load_products)

        self.addButton = PushButton(FIF.ADD, "إضافة", self)
        self.addButton.clicked.connect(self.show_add_dialog)

        self.editButton = PushButton(FIF.EDIT, "تعديل", self)
        self.editButton.clicked.connect(self.show_edit_dialog)

        self.deleteButton = PushButton(FIF.DELETE, "حذف", self)
        self.deleteButton.clicked.connect(self.delete_product)

        self.actionBar.addWidget(self.searchEdit)
        self.actionBar.addWidget(self.addButton)
        self.actionBar.addWidget(self.editButton)
        self.actionBar.addWidget(self.deleteButton)

        # Table
        self.table = TableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["الرمز", "الاسم", "الفئة", "السعر", "الكمية", "الوصف"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.layout.addWidget(self.titleLabel)
        self.layout.addLayout(self.actionBar)
        self.layout.addWidget(self.table)

        self.load_products()

    def load_products(self):
        search_query = self.searchEdit.text()
        products = Product.get_all_products(search_query)
        self.table.setRowCount(0)
        for p in products:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(p["code"]))
            self.table.setItem(row, 1, QTableWidgetItem(p["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(p["category"]))
            self.table.setItem(row, 3, QTableWidgetItem(f"{p['price']:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(str(p["quantity"])))
            self.table.setItem(row, 5, QTableWidgetItem(p.get("description", "")))

    def show_add_dialog(self):
        w = ProductDialog(self.window())
        if w.exec():
            data = w.get_data()
            if Product.get_product(data["code"]):
                InfoBar.error("خطأ", "هذا الرمز موجود مسبقاً", parent=self)
                return
            Product.add_product(data)
            self.load_products()
            InfoBar.success("تم", "تمت الإضافة بنجاح", parent=self)

    def show_edit_dialog(self):
        row = self.table.currentRow()
        if row < 0:
            return
        code = self.table.item(row, 0).text()
        product = Product.get_product(code)

        w = ProductDialog(self.window(), product)
        if w.exec():
            data = w.get_data()
            Product.update_product(code, data)
            self.load_products()
            InfoBar.success("تم", "تم التحديث بنجاح", parent=self)

    def delete_product(self):
        row = self.table.currentRow()
        if row < 0:
            return
        code = self.table.item(row, 0).text()

        w = MessageBox(
            "تأكيد الحذف", f"هل أنت متأكد من حذف المنتج {code}؟", self.window()
        )
        w.yesButton.setText("نعم")
        w.cancelButton.setText("إلغاء")

        if w.exec():
            Product.delete_product(code)
            self.load_products()
            InfoBar.success("تم", "تم الحذف بنجاح", parent=self)
