from PyQt6.QtCore import pyqtSignal
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import FluentWindow, MessageBox, NavigationItemPosition

from .pages.category_page import CategoryPage
from .pages.dashboard_page import DashboardPage
from .pages.product_page import ProductPage
from .pages.purchase_page import PurchasePage
from .pages.sales_page import SalesPage
from .pages.user_page import UserPage


class AdminWindow(FluentWindow):
    switchToCashier = pyqtSignal()
    returnToLauncher = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("لوحة الإدارة")
        self.resize(1100, 750)

        # Create pages
        self.dashboardPage = DashboardPage(self)
        self.categoryPage = CategoryPage(self)
        self.productPage = ProductPage(self)
        self.purchasePage = PurchasePage(self)
        self.salesPage = SalesPage(self)
        self.userPage = UserPage(self)

        self.init_navigation()

    def show_about(self):
        content = "نظام إدارة السوبر ماركت\nتم التطوير بواسطة Souieh\nGitHub: https://github.com/Souieh/supermarket-si"
        w = MessageBox("عن النظام", content, self)
        w.yesButton.setText("إغلاق")
        w.cancelButton.hide()
        if w.exec():
            pass

    def init_navigation(self):
        self.addSubInterface(self.dashboardPage, FIF.HOME, "لوحة التحكم")
        self.addSubInterface(self.categoryPage, FIF.MENU, "الفئات")
        self.addSubInterface(self.productPage, FIF.APPLICATION, "المنتجات")
        self.addSubInterface(self.purchasePage, FIF.BASKETBALL, "المشتريات")
        self.addSubInterface(self.salesPage, FIF.SHOPPING_CART, "المبيعات")
        self.addSubInterface(self.userPage, FIF.PEOPLE, "المستخدمين")

        # Switch to Cashier
        self.navigationInterface.addItem(
            routeKey="cashier",
            icon=FIF.SHOPPING_CART,
            text="واجهة الكاشير (قريباً)",
            onClick=self.switchToCashier.emit,
            position=NavigationItemPosition.BOTTOM,
        )

        # Return to Launcher
        self.navigationInterface.addItem(
            routeKey="launcher",
            icon=FIF.HOME,
            text="القائمة الرئيسية",
            onClick=self.returnToLauncher.emit,
            position=NavigationItemPosition.BOTTOM,
        )

        # GitHub / About
        self.navigationInterface.addItem(
            routeKey="about",
            icon=FIF.INFO,
            text="عن النظام",
            onClick=self.show_about,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setExpandWidth(280)
        self.navigationInterface.setMinimumExpandWidth(0)

    def closeEvent(self, event):
        w = MessageBox("تأكيد الخروج", "هل أنت متأكد من رغبتك في إغلاق البرنامج؟", self)
        w.yesButton.setText("نعم")
        w.cancelButton.setText("إلغاء")
        if w.exec():
            event.accept()
        else:
            event.ignore()
