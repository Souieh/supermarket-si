from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QHeaderView, QGridLayout, QScrollArea
from qfluentwidgets import (SubtitleLabel, TableWidget, LineEdit, PushButton,
                             FluentIcon as FIF, InfoBar, StrongBodyLabel, TitleLabel)
from ..modules.product import Product
from ..modules.category import Category
from ..modules.sale import Sale
from ..modules.receipt import Receipt

class TouchButton(PushButton):
    def _postInit(self):
        self.setFixedHeight(80)
        self.setIconSize(QSize(32, 32))
        self.setStyleSheet("font-size: 18px; font-weight: bold;")

class CashierWindow(QWidget):
    switchToAdmin = pyqtSignal()
    returnToLauncher = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("واجهة الكاشير / Cashier Interface")
        self.showMaximized()
        self.layout = QHBoxLayout(self)

        # Left side: Product Selection and Cart
        self.leftLayout = QVBoxLayout()
        self.titleLabel = TitleLabel("الكاشير / Cashier", self)

        self.cartTable = TableWidget(self)
        self.cartTable.setColumnCount(4)
        self.cartTable.setHorizontalHeaderLabels(["المنتج", "السعر", "الكمية", "المجموع"])
        self.cartTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.cartTable.setStyleSheet("font-size: 16px;")

        self.leftLayout.addWidget(self.titleLabel)

        # Selection Panel (Categories and Products)
        self.selectionPanel = QWidget(self)
        self.selectionPanel.setFixedHeight(400)
        self.selectionLayout = QHBoxLayout(self.selectionPanel)
        self.selectionLayout.setContentsMargins(0, 0, 0, 0)

        # Category Selection
        self.categoryArea = QScrollArea(self)
        self.categoryArea.setFixedWidth(180)
        self.categoryArea.setWidgetResizable(True)
        self.categoryWidget = QWidget()
        self.categoryLayout = QVBoxLayout(self.categoryWidget)
        self.categoryLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.categoryArea.setWidget(self.categoryWidget)

        # Product Selection
        self.productArea = QScrollArea(self)
        self.productArea.setWidgetResizable(True)
        self.productWidget = QWidget()
        self.productLayout = QGridLayout(self.productWidget)
        self.productLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.productArea.setWidget(self.productWidget)

        self.selectionLayout.addWidget(self.categoryArea)
        self.selectionLayout.addWidget(self.productArea)

        self.leftLayout.addWidget(self.selectionPanel)
        self.leftLayout.addWidget(self.cartTable)

        # Right side: Controls
        self.rightPanel = QWidget(self)
        self.rightPanel.setFixedWidth(400)
        self.rightLayout = QVBoxLayout(self.rightPanel)

        self.codeEdit = LineEdit(self)
        self.codeEdit.setPlaceholderText("ادخل رمز المنتج / Enter Code")
        self.codeEdit.setFixedHeight(60)
        self.codeEdit.setStyleSheet("font-size: 24px;")
        self.codeEdit.returnPressed.connect(self.add_by_code)

        self.numpad = QGridLayout()
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '.', 'C'
        ]
        for i, b in enumerate(buttons):
            btn = PushButton(b)
            btn.setFixedSize(80, 80)
            btn.setStyleSheet("font-size: 20px;")
            btn.clicked.connect(lambda ch, x=b: self.numpad_click(x))
            self.numpad.addWidget(btn, i // 3, i % 3)

        self.totalLabel = StrongBodyLabel("المجموع: 0.00", self)
        self.totalLabel.setStyleSheet("font-size: 32px; color: #0078d4;")

        self.payButton = TouchButton(FIF.ACCEPT, "دفع / PAY (F5)", self)
        self.payButton.setStyleSheet("background-color: #28a745; color: white; font-size: 24px;")
        self.payButton.clicked.connect(self.checkout)

        self.clearButton = TouchButton(FIF.DELETE, "مسح الكل / Clear All", self)
        self.clearButton.clicked.connect(self.clear_cart)

        self.rightLayout.addWidget(self.codeEdit)
        self.rightLayout.addLayout(self.numpad)
        self.rightLayout.addStretch(1)
        self.rightLayout.addWidget(self.totalLabel)
        self.rightLayout.addWidget(self.payButton)
        self.rightLayout.addWidget(self.clearButton)

        # Switching buttons
        self.switchLayout = QHBoxLayout()
        self.adminBtn = PushButton(FIF.APPLICATION, "الإدارة / Admin")
        self.adminBtn.clicked.connect(self.switchToAdmin.emit)
        self.homeBtn = PushButton(FIF.HOME, "الرئيسية / Home")
        self.homeBtn.clicked.connect(self.returnToLauncher.emit)
        self.switchLayout.addWidget(self.adminBtn)
        self.switchLayout.addWidget(self.homeBtn)
        self.rightLayout.addLayout(self.switchLayout)

        self.layout.addLayout(self.leftLayout, 1)
        self.layout.addWidget(self.rightPanel)

        self.cart_items = []
        self.load_categories()

    def load_categories(self):
        # Clear category layout
        while self.categoryLayout.count():
            item = self.categoryLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # All button
        btn = PushButton("الكل / All")
        btn.clicked.connect(lambda: self.load_products())
        self.categoryLayout.addWidget(btn)

        categories = Category.get_all_categories()
        for cat in categories:
            name = cat["name"]
            btn = PushButton(name)
            btn.clicked.connect(lambda ch, n=name: self.load_products(n))
            self.categoryLayout.addWidget(btn)

        self.load_products()

    def load_products(self, category=None):
        # Clear product layout
        while self.productLayout.count():
            item = self.productLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        products = Product.get_all_products(category=category)
        for i, p in enumerate(products):
            btn = TouchButton(f"{p['name']}\n{p['price']:.2f}")
            btn.clicked.connect(lambda ch, prod=p: self.add_item(prod))
            self.productLayout.addWidget(btn, i // 4, i % 4)

    def numpad_click(self, val):
        if val == 'C':
            self.codeEdit.clear()
        else:
            self.codeEdit.setText(self.codeEdit.text() + val)

    def add_by_code(self):
        code = self.codeEdit.text()
        if not code: return
        product = Product.get_product(code)
        if product:
            self.add_item(product)
            self.codeEdit.clear()
        else:
            InfoBar.error("خطأ", "المنتج غير موجود", parent=self)

    def add_item(self, product):
        for item in self.cart_items:
            if item["code"] == product["code"]:
                item["quantity"] += 1
                self.update_table()
                return

        self.cart_items.append({
            "code": product["code"],
            "name": product["name"],
            "price": product["price"],
            "quantity": 1
        })
        self.update_table()

    def update_table(self):
        self.cartTable.setRowCount(0)
        total = 0
        for item in self.cart_items:
            row = self.cartTable.rowCount()
            self.cartTable.insertRow(row)
            subtotal = item["price"] * item["quantity"]
            self.cartTable.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.cartTable.setItem(row, 1, QTableWidgetItem(f"{item['price']:.2f}"))
            self.cartTable.setItem(row, 2, QTableWidgetItem(str(item["quantity"])))
            self.cartTable.setItem(row, 3, QTableWidgetItem(f"{subtotal:.2f}"))
            total += subtotal
        self.totalLabel.setText(f"المجموع: {total:.2f}")

    def clear_cart(self):
        self.cart_items = []
        self.update_table()

    def checkout(self):
        if not self.cart_items: return
        total = sum(item["price"] * item["quantity"] for item in self.cart_items)
        sale = Sale(self.cart_items, total)
        try:
            receipt_id = sale.process_sale()
            Receipt.generate(sale.to_dict())
            InfoBar.success("تم", f"تم البيع بنجاح. فاتورة: {receipt_id}", parent=self)
            self.clear_cart()
        except Exception as e:
            InfoBar.error("خطأ", str(e), parent=self)
