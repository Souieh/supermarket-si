from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    IconWidget,
    PushButton,
    StrongBodyLabel,
    SubtitleLabel,
)
from qfluentwidgets import FluentIcon as FIF

from ....modules.sale import Sale


class StatCard(CardWidget):
    def __init__(self, title, value, icon, parent=None):
        super().__init__(parent)
        self.cardLayout = QHBoxLayout(self)
        self.iconWidget = IconWidget(icon, self)
        self.iconWidget.setFixedSize(32, 32)

        self.textLayout = QVBoxLayout()
        self.titleLabel = BodyLabel(title, self)
        self.valueLabel = StrongBodyLabel(value, self)
        self.valueLabel.setStyleSheet("font-size: 24px; color: #0078d4;")

        self.textLayout.addWidget(self.titleLabel)
        self.textLayout.addWidget(self.valueLabel)

        self.cardLayout.addWidget(self.iconWidget)
        self.cardLayout.addLayout(self.textLayout)


class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DashboardPage")
        self.mainLayout = QVBoxLayout(self)

        self.titleLabel = SubtitleLabel("لوحة التحكم", self)
        self.mainLayout.addWidget(self.titleLabel)

        self.grid = QGridLayout()
        self.mainLayout.addLayout(self.grid)

        self.mainLayout.addSpacing(40)
        self.shortcutsLabel = SubtitleLabel("إجراءات سريعة", self)
        self.mainLayout.addWidget(self.shortcutsLabel)

        self.shortcutsLayout = QHBoxLayout()
        self.shortcutsLayout.setSpacing(15)
        self.shortcutsLayout.setContentsMargins(10, 10, 10, 10)

        # FIX 1: Use self.mainLayout instead of self.layout (which is a method)
        self.mainLayout.addLayout(self.shortcutsLayout)

        self.btnAddProduct = PushButton(FIF.ADD, "إضافة منتج")
        self.btnRecordPurchase = PushButton(FIF.BASKETBALL, "تسجيل شراء")
        self.btnViewSales = PushButton(FIF.SHOPPING_CART, "عرض المبيعات")
        self.btnManageCategories = PushButton(FIF.MENU, "إدارة الفئات")

        self.shortcutsLayout.addWidget(self.btnAddProduct)
        self.shortcutsLayout.addWidget(self.btnRecordPurchase)
        self.shortcutsLayout.addWidget(self.btnViewSales)
        self.shortcutsLayout.addWidget(self.btnManageCategories)
        self.shortcutsLayout.addStretch(1)

        self.setup_shortcuts()
        self.refresh_stats()

    def setup_shortcuts(self):
        self.btnAddProduct.clicked.connect(lambda: self.switch_to_page("ProductPage"))
        self.btnRecordPurchase.clicked.connect(
            lambda: self.switch_to_page("PurchasePage")
        )
        self.btnViewSales.clicked.connect(lambda: self.switch_to_page("SalesPage"))
        self.btnManageCategories.clicked.connect(
            lambda: self.switch_to_page("CategoryPage")
        )

    def switch_to_page(self, object_name):
        window = self.window()
        # Runtime safety checks – Pylance may still warn but these are safe
        if (
            window
            and hasattr(window, "stackedWidget")
            and hasattr(window, "navigationInterface")
        ):
            stacked = window.stackedWidget  # type: ignore
            nav = window.navigationInterface  # type: ignore
            for i in range(stacked.count()):
                widget = stacked.widget(i)
                if widget.objectName() == object_name:
                    stacked.setCurrentWidget(widget)
                    nav.setCurrentItem(widget.objectName())
                    break

    def refresh_stats(self):
        try:
            stats = Sale.get_dashboard_stats()
        except Exception:
            stats = {
                "total_products": 0,
                "out_of_stock": 0,
                "total_categories": 0,
                "daily_revenue": 0,
                "total_sales": 0,
                "total_purchases": 0,
            }

        # Clear grid safely
        for i in reversed(range(self.grid.count())):
            item = self.grid.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        self.grid.setSpacing(20)
        self.grid.addWidget(
            StatCard("المنتجات", str(stats["total_products"]), FIF.APPLICATION), 0, 0
        )
        self.grid.addWidget(
            StatCard("الفئات", str(stats["total_categories"]), FIF.MENU), 0, 1
        )
        self.grid.addWidget(
            StatCard("نفاذ المخزون", str(stats["out_of_stock"]), FIF.CLOSE), 0, 2
        )

        self.grid.addWidget(
            StatCard("إيرادات اليوم", f"{stats['daily_revenue']:.2f}", FIF.TAG), 1, 0
        )
        self.grid.addWidget(
            StatCard("إجمالي المبيعات", str(stats["total_sales"]), FIF.SHOPPING_CART),
            1,
            1,
        )
        self.grid.addWidget(
            StatCard(
                "إجمالي المشتريات", f"{stats['total_purchases']:.2f}", FIF.BASKETBALL
            ),
            1,
            2,
        )

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_stats()
