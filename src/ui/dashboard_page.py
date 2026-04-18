from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import SubtitleLabel, CardWidget, BodyLabel, StrongBodyLabel, FluentIcon as FIF, PushButton
from ..modules.sale import Sale

from qfluentwidgets import IconWidget

class StatCard(CardWidget):
    def __init__(self, title, value, icon, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.iconWidget = IconWidget(icon, self)
        self.iconWidget.setFixedSize(32, 32)

        self.textLayout = QVBoxLayout()
        self.titleLabel = BodyLabel(title, self)
        self.valueLabel = StrongBodyLabel(value, self)
        self.valueLabel.setStyleSheet("font-size: 24px; color: #0078d4;")

        self.textLayout.addWidget(self.titleLabel)
        self.textLayout.addWidget(self.valueLabel)

        self.layout.addWidget(self.iconWidget)
        self.layout.addLayout(self.textLayout)

class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DashboardPage")
        self.layout = QVBoxLayout(self)

        self.titleLabel = SubtitleLabel("لوحة التحكم / Dashboard", self)
        self.layout.addWidget(self.titleLabel)

        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)

        self.layout.addSpacing(40)
        self.shortcutsLabel = SubtitleLabel("إجراءات سريعة / Quick Actions", self)
        self.layout.addWidget(self.shortcutsLabel)

        self.shortcutsLayout = QHBoxLayout()
        self.shortcutsLayout.setSpacing(15)
        self.shortcutsLayout.setContentsMargins(10, 10, 10, 10)
        self.layout.addLayout(self.shortcutsLayout)

        self.btnAddProduct = PushButton(FIF.ADD, "إضافة منتج / Add Product")
        self.btnRecordPurchase = PushButton(FIF.BASKETBALL, "تسجيل شراء / Record Purchase")
        self.btnViewSales = PushButton(FIF.SHOPPING_CART, "عرض المبيعات / View Sales")
        self.btnManageCategories = PushButton(FIF.MENU, "إدارة الفئات / Categories")

        self.shortcutsLayout.addWidget(self.btnAddProduct)
        self.shortcutsLayout.addWidget(self.btnRecordPurchase)
        self.shortcutsLayout.addWidget(self.btnViewSales)
        self.shortcutsLayout.addWidget(self.btnManageCategories)
        self.shortcutsLayout.addStretch(1)

        self.setup_shortcuts()
        self.refresh_stats()

    def setup_shortcuts(self):
        self.btnAddProduct.clicked.connect(lambda: self.switch_to_page("ProductPage"))
        self.btnRecordPurchase.clicked.connect(lambda: self.switch_to_page("PurchasePage"))
        self.btnViewSales.clicked.connect(lambda: self.switch_to_page("SalesPage"))
        self.btnManageCategories.clicked.connect(lambda: self.switch_to_page("CategoryPage"))

    def switch_to_page(self, object_name):
        window = self.window()
        if hasattr(window, 'navigationInterface'):
            # Find the interface by object name
            for widget in window.stackedWidget.widgets():
                if widget.objectName() == object_name:
                    window.stackedWidget.setCurrentWidget(widget)
                    # Update navigation selection visually
                    window.navigationInterface.setCurrentItem(widget.objectName())
                    break

    def refresh_stats(self):
        try:
            stats = Sale.get_dashboard_stats()
        except:
            stats = {"total_products": 0, "out_of_stock": 0, "total_categories": 0,
                     "daily_revenue": 0, "total_sales": 0, "total_purchases": 0}

        # Clear grid
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        self.grid.setSpacing(20)
        self.grid.addWidget(StatCard("المنتجات / Products", str(stats["total_products"]), FIF.APPLICATION), 0, 0)
        self.grid.addWidget(StatCard("الفئات / Categories", str(stats["total_categories"]), FIF.MENU), 0, 1)
        self.grid.addWidget(StatCard("نفاذ المخزون / Out of Stock", str(stats["out_of_stock"]), FIF.CLOSE), 0, 2)

        self.grid.addWidget(StatCard("إيرادات اليوم / Daily Revenue", f"{stats['daily_revenue']:.2f}", FIF.TAG), 1, 0)
        self.grid.addWidget(StatCard("إجمالي المبيعات / Sales", str(stats["total_sales"]), FIF.SHOPPING_CART), 1, 1)
        self.grid.addWidget(StatCard("إجمالي المشتريات / Purchases", f"{stats['total_purchases']:.2f}", FIF.BASKETBALL), 1, 2)

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_stats()
