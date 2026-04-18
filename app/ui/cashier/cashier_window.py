import os
import sys

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QScrollArea,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import InfoBar, LineEdit, PushButton, TableWidget

from ...modules.category import Category
from ...modules.product import Product
from ...modules.receipt import Receipt
from ...modules.sale import Sale


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
        self.setWindowTitle("واجهة الكاشير")
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
        self.cartTable.setHorizontalHeaderLabels(
            ["الاسم", "السعر", "الكمية", "الخصم", "المجموع"]
        )

        # Safe header access
        header = self.cartTable.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.cartTable.setStyleSheet("font-family: Monospace; font-size: 16px;")

        vheader = self.cartTable.verticalHeader()
        if vheader is not None:
            vheader.setDefaultSectionSize(60)

        hheader = self.cartTable.horizontalHeader()
        if hheader is not None:
            hheader.setFixedHeight(50)

        self.summaryLayout.addWidget(self.cartTable)

        # Summary Totals Area
        self.totalsLayout = QGridLayout()
        self.totalsLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.subtotalLabel = QLabel("المجموع الفرعي    0.00")
        self.discountLabel = QLabel("الخصم    - 0.00")
        self.taxLabel = QLabel("الضريبة    0.00")
        self.inhouseLabel = QLabel("رسوم الخدمة    0.00")
        self.totalLabel = QLabel("المجموع الكلي    0.00")
        self.balanceLabel = QLabel("الرصيد    $0.00")

        labels = [
            self.subtotalLabel,
            self.discountLabel,
            self.taxLabel,
            self.inhouseLabel,
            self.totalLabel,
            self.balanceLabel,
        ]
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

        # Code entry for manual product code (added to fix missing attribute)
        self.codeEdit = LineEdit()
        self.codeEdit.setPlaceholderText("أدخل رمز المنتج")
        self.codeEdit.setFixedHeight(60)
        self.codeEdit.setFont(self.monoFont)
        self.codeEdit.setStyleSheet("font-size: 24px;")
        self.codeEdit.returnPressed.connect(self.add_by_code)
        self.leftPanel.addWidget(self.codeEdit)

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
        self.forgotTitle.setStyleSheet(
            "font-weight: bold; border-bottom: 1px solid black;"
        )
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
        self.customerTitle = QLabel("العميل")
        self.customerTitle.setFont(self.monoFont)
        self.customerLayout.addWidget(self.customerTitle)

        self.actionsGrid = QGridLayout()
        self.actionsGrid.setSpacing(10)
        actions = [
            ("حذف عنصر", "DELETE ITEM"),
            ("الإعدادات", "SETTING"),
            ("عرض", "PROMO"),
            ("خصم", "DISCOUNT"),
            ("داخلي", "INHOUSE"),
            ("تعليق", "HOLD"),
        ]
        for i, (text, act) in enumerate(actions):
            btn = TouchButton(text)
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

        paymentMethods = [
            ("نقداً", "CASH"),
            ("بطاقة", "CARD"),
            ("قسيمة", "GIFT CARD"),
            ("ولاء", "LOYALTY"),
        ]
        for text, pay in paymentMethods:
            btn = TouchButton(text)
            btn.setFont(self.monoFont)
            btn.setFixedHeight(70)
            if pay == "CASH":
                btn.clicked.connect(self.checkout)
            self.paymentLayout.addWidget(btn)

        self.rightPanel.addWidget(self.paymentGroup)

    def load_categories(self):
        # Clear selection layout safely
        while self.selectionLayout.count():
            item = self.selectionLayout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            layout = item.layout()
            if layout is not None:
                # Recursively clear any sub-layout
                while layout.count():
                    subitem = layout.takeAt(0)
                    subwidget = subitem.widget() if subitem else None
                    if subwidget:
                        subwidget.deleteLater()

        search_query = self.searchEdit.text()

        # Fetch actual categories from database
        categories = Category.get_all_categories()
        for cat in categories:
            cat_name = cat["name"]
            header = QLabel(cat_name)
            header.setStyleSheet(
                "font-weight: bold; font-size: 16px; margin-top: 10px;"
            )
            header.setFont(self.monoFont)
            self.selectionLayout.addWidget(header)

            # Products for this category
            products = Product.get_all_products(search_query=search_query, category=cat_name)
            for p in products:
                btn = TouchButton(f"{p['name']} {p['price']:.2f}")
                btn.setFont(self.monoFont)
                btn.setStyleSheet(
                    "text-align: left; padding-left: 15px; font-size: 18px;"
                )
                btn.clicked.connect(lambda ch, prod=p: self.add_item(prod))
                self.selectionLayout.addWidget(btn)

        self.load_forgot_foods()

    def load_forgot_foods(self):
        # Clear safely
        while self.forgotItemsLayout.count():
            item = self.forgotItemsLayout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        forgot_foods = [
            {"name": "Lobster Forgot", "price": 50.00},
            {"name": "Cucumber", "price": 50.00},
            {"name": "Pumpkin", "price": 50.00},
        ]
        for f in forgot_foods:
            btn = TouchButton(f"{f['name']} {f['price']:.2f} - 12g")
            btn.setFont(self.monoFont)
            btn.setStyleSheet("text-align: left; padding-left: 15px; font-size: 18px;")
            btn.clicked.connect(
                lambda ch, prod=f: self.add_item(
                    {"code": "FORGOT", "name": prod["name"], "price": prod["price"]}
                )
            )
            self.forgotItemsLayout.addWidget(btn)

    def load_products(self, category=None):
        # Reload categories (including products) when search text changes
        self.load_categories()

    def numpad_click(self, val):
        """Called by a numeric keypad (if implemented)"""
        if val == "C":
            self.codeEdit.clear()
        else:
            self.codeEdit.setText(self.codeEdit.text() + val)

    def add_by_code(self):
        """Called when user submits a product code"""
        code = self.codeEdit.text()
        if not code:
            return
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

        self.cart_items.append(
            {
                "code": product["code"],
                "name": product["name"],
                "price": product["price"],
                "quantity": 1,
            }
        )
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

            subtotal_sum += price * qty
            discount_sum += discount

        tax = subtotal_sum * 0.15  # Example 15% tax
        inhouse = 0  # Example
        total_payment = subtotal_sum - discount_sum + tax + inhouse
        balance = 500.00  # Example placeholder

        self.subtotalLabel.setText(f"المجموع الفرعي    {subtotal_sum:10.2f}")
        self.discountLabel.setText(f"الخصم    - {discount_sum:8.2f}")
        self.taxLabel.setText(f"الضريبة    {tax:13.2f}")
        self.inhouseLabel.setText(f"رسوم الخدمة    {inhouse:10.2f}")
        self.totalLabel.setText(f"المجموع الكلي    {total_payment:10.2f}")
        self.balanceLabel.setText(f"الرصيد    ${balance:10.2f}")

    def clear_cart(self):
        self.cart_items = []
        self.update_table()

    def checkout(self):
        if not self.cart_items:
            return
        total = sum(item["price"] * item["quantity"] for item in self.cart_items)
        sale = Sale(self.cart_items, total)
        try:
            receipt_id = sale.process_sale()
            filename = Receipt.generate(sale.to_dict())
            InfoBar.success("تم", f"تم البيع بنجاح. فاتورة: {receipt_id}", parent=self)
            self.clear_cart()

            # Attempt to open the receipt file
            try:
                if sys.platform == "win32":
                    os.startfile(filename)
                elif sys.platform == "darwin":
                    import subprocess
                    subprocess.run(["open", filename])
                else:
                    import subprocess
                    subprocess.run(["xdg-open", filename])
            except Exception:
                pass
        except Exception as e:
            InfoBar.error("خطأ", str(e), parent=self)
