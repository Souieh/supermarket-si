from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QHeaderView, QGridLayout, QScrollArea, QLabel, QFrame
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
        self.setWindowTitle("واجهة الكاشير / POS Interface")
        self.showMaximized()
        self.monoFont = QFont("Monospace")
        self.monoFont.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(self.monoFont)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(20)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)

        # 1. Top Section – Order Summary
        self.setup_order_summary()

        # Bottom section split into Left and Right
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setSpacing(20)
        self.mainLayout.addLayout(self.bottomLayout, 3)

        # 2. Left Panel – Products & Categories
        self.setup_left_panel()

        # 3. Right Panel – Customer Actions & Payments
        self.setup_right_panel()

        self.bottomLayout.addLayout(self.leftPanel, 2)
        self.bottomLayout.addLayout(self.rightPanel, 1)

        self.cart_items = []
        self.load_categories()

    def setup_order_summary(self):
        self.summaryContainer = QFrame()
        self.summaryContainer.setFrameShape(QFrame.Shape.Box)
        self.summaryLayout = QVBoxLayout(self.summaryContainer)

        # Item List Table
        self.cartTable = TableWidget()
        self.cartTable.setColumnCount(5)
        self.cartTable.setHorizontalHeaderLabels(["Item Name", "Price", "QTY", "Discount", "Total"])
        self.cartTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.cartTable.setStyleSheet("font-family: Monospace; font-size: 16px;")
        self.cartTable.verticalHeader().setDefaultSectionSize(60)
        self.cartTable.horizontalHeader().setFixedHeight(50)
        self.summaryLayout.addWidget(self.cartTable)

        # Summary Totals Area
        self.totalsLayout = QGridLayout()
        self.totalsLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.subtotalLabel = QLabel("Subtotal    0.00")
        self.discountLabel = QLabel("Discount    - 0.00")
        self.taxLabel      = QLabel("Tax    0.00")
        self.inhouseLabel  = QLabel("Inhouse Charge    0.00")
        self.totalLabel    = QLabel("Total Payment    0.00")
        self.balanceLabel  = QLabel("Balance    $0.00")

        labels = [self.subtotalLabel, self.discountLabel, self.taxLabel,
                  self.inhouseLabel, self.totalLabel, self.balanceLabel]
        for i, lbl in enumerate(labels):
            lbl.setFont(self.monoFont)
            lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.totalsLayout.addWidget(lbl, i, 0)

        self.summaryLayout.addLayout(self.totalsLayout)
        self.mainLayout.addWidget(self.summaryContainer, 2)

    def setup_left_panel(self):
        self.leftPanel = QVBoxLayout()

        # Search
        self.searchEdit = LineEdit()
        self.searchEdit.setPlaceholderText("SEARCH...")
        self.searchEdit.setFont(self.monoFont)
        self.searchEdit.setFixedHeight(60)
        self.searchEdit.setStyleSheet("font-size: 24px;")
        self.searchEdit.textChanged.connect(lambda: self.load_products())
        self.leftPanel.addWidget(self.searchEdit)

        # Scroll Area for Categories and Products
        self.selectionArea = QScrollArea()
        self.selectionArea.setWidgetResizable(True)
        self.selectionWidget = QWidget()
        self.selectionLayout = QVBoxLayout(self.selectionWidget)
        self.selectionLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.selectionArea.setWidget(self.selectionWidget)
        self.leftPanel.addWidget(self.selectionArea)

        # Foods Forgot Section at bottom of left panel
        self.forgotContainer = QFrame()
        self.forgotContainer.setFrameShape(QFrame.Shape.Box)
        self.forgotLayout = QVBoxLayout(self.forgotContainer)
        self.forgotTitle = QLabel("FOODS FORGOT")
        self.forgotTitle.setStyleSheet("font-weight: bold; border-bottom: 1px solid black;")
        self.forgotLayout.addWidget(self.forgotTitle)

        self.forgotItemsLayout = QVBoxLayout()
        self.forgotLayout.addLayout(self.forgotItemsLayout)
        self.leftPanel.addWidget(self.forgotContainer)

    def setup_right_panel(self):
        self.rightPanel = QVBoxLayout()

        # CUSTOMER Section
        self.customerGroup = QFrame()
        self.customerGroup.setFrameShape(QFrame.Shape.Box)
        self.customerLayout = QVBoxLayout(self.customerGroup)
        self.customerTitle = QLabel("CUSTOMER")
        self.customerTitle.setFont(self.monoFont)
        self.customerLayout.addWidget(self.customerTitle)

        self.actionsGrid = QGridLayout()
        self.actionsGrid.setSpacing(10)
        actions = ["DELETE ITEM", "SETTING", "PROMO", "DISCOUNT", "INHOUSE", "HOLD"]
        for i, act in enumerate(actions):
            btn = TouchButton(act)
            btn.setFont(self.monoFont)
            if act == "DELETE ITEM":
                btn.clicked.connect(self.clear_cart)
            elif act == "SETTING":
                btn.clicked.connect(self.switchToAdmin.emit)
            elif act == "HOLD":
                btn.clicked.connect(self.returnToLauncher.emit)
            self.actionsGrid.addWidget(btn, i // 2, i % 2)

        self.customerLayout.addLayout(self.actionsGrid)
        self.rightPanel.addWidget(self.customerGroup)

        self.rightPanel.addStretch(1)

        # Payment Methods
        self.paymentGroup = QFrame()
        self.paymentGroup.setFrameShape(QFrame.Shape.Box)
        self.paymentLayout = QVBoxLayout(self.paymentGroup)
        self.paymentLayout.setSpacing(10)

        paymentMethods = ["CASH", "CARD", "GIFT CARD", "LOYALTY"]
        for pay in paymentMethods:
            btn = TouchButton(pay)
            btn.setFont(self.monoFont)
            btn.setFixedHeight(70)
            if pay == "CASH":
                btn.clicked.connect(self.checkout)
            self.paymentLayout.addWidget(btn)

        self.rightPanel.addWidget(self.paymentGroup)

    def load_categories(self):
        # Clear selection layout
        while self.selectionLayout.count():
            item = self.selectionLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Need to clear sub-layouts too if any
                pass

        search_query = self.searchEdit.text()

        # In this specific UI, we list categories and products under them
        categories = ["VEGETABLE", "GROCERY", "FRUITS"]
        for cat_name in categories:
            header = QLabel(cat_name)
            header.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
            header.setFont(self.monoFont)
            self.selectionLayout.addWidget(header)

            # Products for this category
            products = Product.get_all_products(search_query=search_query) # Intentional: same products for all
            for p in products:
                btn = TouchButton(f"{p['name']} {p['price']:.2f} - 12g")
                btn.setFont(self.monoFont)
                btn.setStyleSheet("text-align: left; padding-left: 15px; font-size: 18px;")
                btn.clicked.connect(lambda ch, prod=p: self.add_item(prod))
                self.selectionLayout.addWidget(btn)

        self.load_forgot_foods()

    def load_forgot_foods(self):
        while self.forgotItemsLayout.count():
            item = self.forgotItemsLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        forgot_foods = [
            {"name": "Lobster Forgot", "price": 50.00},
            {"name": "Cucumber", "price": 50.00},
            {"name": "Pumpkin", "price": 50.00}
        ]
        for f in forgot_foods:
            btn = TouchButton(f"{f['name']} {f['price']:.2f} - 12g")
            btn.setFont(self.monoFont)
            btn.setStyleSheet("text-align: left; padding-left: 15px; font-size: 18px;")
            btn.clicked.connect(lambda ch, prod=f: self.add_item({
                "code": "FORGOT", "name": f["name"], "price": f["price"]
            }))
            self.forgotItemsLayout.addWidget(btn)

    def load_products(self, category=None):
        # Overriding old load_products to use the new category-based listing
        self.load_categories()

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
        subtotal_sum = 0
        discount_sum = 0
        for item in self.cart_items:
            row = self.cartTable.rowCount()
            self.cartTable.insertRow(row)
            qty = item["quantity"]
            price = item["price"]
            discount = item.get("discount", 0)
            total = (price * qty) - discount

            self.cartTable.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.cartTable.setItem(row, 1, QTableWidgetItem(f"{price:.2f}"))
            self.cartTable.setItem(row, 2, QTableWidgetItem(str(qty)))
            self.cartTable.setItem(row, 3, QTableWidgetItem(f"{discount:.2f}"))
            self.cartTable.setItem(row, 4, QTableWidgetItem(f"{total:.2f}"))

            subtotal_sum += (price * qty)
            discount_sum += discount

        tax = subtotal_sum * 0.15 # Example 15% tax
        inhouse = 0 # Example
        total_payment = subtotal_sum - discount_sum + tax + inhouse
        balance = 500.00 # Example placeholder

        self.subtotalLabel.setText(f"Subtotal    {subtotal_sum:10.2f}")
        self.discountLabel.setText(f"Discount    - {discount_sum:8.2f}")
        self.taxLabel.setText(f"Tax    {tax:13.2f}")
        self.inhouseLabel.setText(f"Inhouse Charge    {inhouse:10.2f}")
        self.totalLabel.setText(f"Total Payment    {total_payment:10.2f}")
        self.balanceLabel.setText(f"Balance    ${balance:10.2f}")

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
