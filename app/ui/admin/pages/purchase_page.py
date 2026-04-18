from PyQt6.QtWidgets import QHeaderView, QTableWidgetItem, QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, PushButton, SubtitleLabel, TableWidget

from ....modules.purchase import Purchase
from ..components.purchase_dialog import PurchaseDialog


class PurchasePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PurchasePage")
        self.layout = QVBoxLayout(self)

        self.titleLabel = SubtitleLabel("سجل المشتريات", self)

        self.addButton = PushButton(FIF.ADD, "إضافة عملية شراء", self)
        self.addButton.clicked.connect(self.show_add_dialog)

        self.table = TableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["التاريخ", "المورد", "المنتجات", "الكمية", "التكلفة"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.layout.addWidget(self.titleLabel)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.table)

        self.load_purchases()

    def load_purchases(self):
        purchases = Purchase.get_purchase_history()
        self.table.setRowCount(0)
        for pur in purchases:
            row = self.table.rowCount()
            self.table.insertRow(row)
            date_str = pur["timestamp"].strftime("%Y-%m-%d %H:%M")
            items_str = ", ".join([i["name"] for i in pur["items"]])
            qty_str = ", ".join([str(i["quantity"]) for i in pur["items"]])

            self.table.setItem(row, 0, QTableWidgetItem(date_str))
            self.table.setItem(row, 1, QTableWidgetItem(pur.get("supplier", "")))
            self.table.setItem(row, 2, QTableWidgetItem(items_str))
            self.table.setItem(row, 3, QTableWidgetItem(qty_str))
            self.table.setItem(row, 4, QTableWidgetItem(f"{pur['total_cost']:.2f}"))

    def show_add_dialog(self):
        w = PurchaseDialog(self.window())
        if w.exec():
            data = w.get_data()
            pur = Purchase(data["items"], data["total_cost"], data["supplier"])
            if pur.process_purchase():
                self.load_purchases()
                InfoBar.success(
                    "تم", "تم تسجيل المشتريات وتحديث المخزون بنجاح", parent=self
                )
            else:
                InfoBar.error("خطأ", "فشل في تسجيل العملية", parent=self)
