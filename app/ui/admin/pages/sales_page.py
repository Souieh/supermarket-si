from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidgetItem, QHeaderView)
from qfluentwidgets import (SubtitleLabel, TableWidget, LineEdit, PushButton,
                            FluentIcon as FIF, InfoBar, StrongBodyLabel)
from ....modules.product import Product
from ....modules.sale import Sale
from ....modules.receipt import Receipt


class SalesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SalesPage")
        self.mainLayout = QVBoxLayout(self)

        self.titleLabel = SubtitleLabel("معالجة المبيعات", self)

        # Product Selection
        self.selectionLayout = QHBoxLayout()
        self.codeEdit = LineEdit(self)
        self.codeEdit.setPlaceholderText("رمز المنتج")
        self.qtyEdit = LineEdit(self)
        self.qtyEdit.setPlaceholderText("الكمية")
        self.qtyEdit.setText("1")
        self.addItemButton = PushButton(FIF.ADD, "إضافة", self)
        self.addItemButton.clicked.connect(self.add_to_cart)

        self.selectionLayout.addWidget(self.codeEdit)
        self.selectionLayout.addWidget(self.qtyEdit)
        self.selectionLayout.addWidget(self.addItemButton)

        # Cart Table
        self.table = TableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["المنتج", "السعر", "الكمية", "المجموع"])
        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Bottom Bar
        self.bottomBar = QHBoxLayout()
        self.totalLabel = StrongBodyLabel("المجموع الكلي: 0.00", self)
        self.checkoutButton = PushButton(FIF.ACCEPT, "إتمام البيع", self)
        self.checkoutButton.clicked.connect(self.checkout)

        self.bottomBar.addWidget(self.totalLabel)
        self.bottomBar.addStretch(1)
        self.bottomBar.addWidget(self.checkoutButton)

        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addLayout(self.selectionLayout)
        self.mainLayout.addWidget(self.table)
        self.mainLayout.addLayout(self.bottomBar)

        self.cart_items = []

    def add_to_cart(self):
        code = self.codeEdit.text()
        try:
            qty = int(self.qtyEdit.text())
        except ValueError:
            return

        product = Product.get_product(code)
        if not product:
            InfoBar.error("خطأ", "المنتج غير موجود", parent=self)
            return

        if product["quantity"] < qty:
            InfoBar.warning("تنبيه", "الكمية المتوفرة غير كافية", parent=self)
            return

        item = {
            "code": product["code"],
            "name": product["name"],
            "price": product["price"],
            "quantity": qty
        }
        self.cart_items.append(item)
        self.update_table()
        self.codeEdit.clear()

    def update_table(self):
        self.table.setRowCount(0)
        total = 0
        for item in self.cart_items:
            row = self.table.rowCount()
            self.table.insertRow(row)
            subtotal = item["price"] * item["quantity"]
            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(f"{item['price']:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(str(item["quantity"])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{subtotal:.2f}"))
            total += subtotal

        self.totalLabel.setText(f"المجموع الكلي: {total:.2f}")

    def checkout(self):
        if not self.cart_items:
            return

        total = sum(item["price"] * item["quantity"] for item in self.cart_items)
        sale = Sale(self.cart_items, total)

        try:
            receipt_id = sale.process_sale()
            if receipt_id:
                # Generate receipt
                Receipt.generate(sale.to_dict())
                InfoBar.success("تم بنجاح", f"تم إتمام العملية. رقم الفاتورة: {receipt_id}", parent=self)
                self.cart_items = []
                self.update_table()
            else:
                InfoBar.error("خطأ", "فشلت العملية", parent=self)
        except Exception as e:
            InfoBar.error("خطأ", str(e), parent=self)
