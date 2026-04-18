from PyQt6.QtGui import QDoubleValidator, QIntValidator
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit, ComboBox)
from ....modules.product import Product


class PurchaseDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("تسجيل عملية شراء", self)

        self.productCombo = ComboBox(self)
        self.qtyEdit = LineEdit(self)
        self.costEdit = LineEdit(self)
        self.supplierEdit = LineEdit(self)

        # Load products
        self.products = Product.get_all_products()
        for p in self.products:
            self.productCombo.addItem(f"{p['name']} ({p['code']})", p['code'])

        self.qtyEdit.setValidator(QIntValidator(1, 1000000))
        self.costEdit.setValidator(QDoubleValidator(0.0, 999999.0, 2))

        self.qtyEdit.setPlaceholderText("الكمية المشتراة")
        self.costEdit.setPlaceholderText("سعر التكلفة الإجمالي")
        self.supplierEdit.setPlaceholderText("المورد")

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.productCombo)
        self.viewLayout.addWidget(self.qtyEdit)
        self.viewLayout.addWidget(self.costEdit)
        self.viewLayout.addWidget(self.supplierEdit)

        self.yesButton.setText("حفظ")
        self.cancelButton.setText("إلغاء")

    def validate(self):
        return (self.productCombo.currentIndex() >= 0 and
                self.qtyEdit.text().isdigit() and
                self.costEdit.text().replace('.', '', 1).isdigit())

    def accept(self):
        if self.validate():
            super().accept()

    def showEvent(self, event):
        super().showEvent(event)
        frame = self.frameGeometry()
        screen = self.screen()
        if screen:
            center = screen.availableGeometry().center()
            frame.moveCenter(center)
            self.move(frame.topLeft())

    def get_data(self):
        code = self.productCombo.currentData()
        # Find product name
        name = ""
        for p in self.products:
            if p["code"] == code:
                name = p["name"]
                break

        return {
            "items": [{
                "code": code,
                "name": name,
                "quantity": int(self.qtyEdit.text()),
                "cost": float(self.costEdit.text())
            }],
            "total_cost": float(self.costEdit.text()),
            "supplier": self.supplierEdit.text()
        }
