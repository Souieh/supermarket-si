from PyQt6.QtGui import QDoubleValidator
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit,
                            TextEdit)


class ProductDialog(MessageBoxBase):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("إضافة/تعديل منتج", self)

        self.codeEdit = LineEdit(self)
        self.nameEdit = LineEdit(self)
        self.categoryEdit = LineEdit(self)
        self.priceEdit = LineEdit(self)
        self.qtyEdit = LineEdit(self)
        self.descEdit = TextEdit(self)

        self.priceEdit.setValidator(QDoubleValidator(0.0, 999999.0, 2))
        self.codeEdit.setPlaceholderText("الرمز")
        self.nameEdit.setPlaceholderText("الاسم")
        self.categoryEdit.setPlaceholderText("الفئة")
        self.priceEdit.setPlaceholderText("السعر")
        self.qtyEdit.setPlaceholderText("الكمية")
        self.descEdit.setPlaceholderText("الوصف")
        self.descEdit.setFixedHeight(100)

        if product:
            self.codeEdit.setText(product.get("code", ""))
            self.nameEdit.setText(product.get("name", ""))
            self.categoryEdit.setText(product.get("category", ""))
            self.priceEdit.setText(str(product.get("price", "")))
            self.qtyEdit.setText(str(product.get("quantity", "")))
            self.descEdit.setText(product.get("description", ""))
            self.codeEdit.setEnabled(False)  # Don't allow changing code

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.codeEdit)
        self.viewLayout.addWidget(self.nameEdit)
        self.viewLayout.addWidget(self.categoryEdit)
        self.viewLayout.addWidget(self.priceEdit)
        self.viewLayout.addWidget(self.qtyEdit)
        self.viewLayout.addWidget(self.descEdit)

        self.yesButton.setText("حفظ")
        self.cancelButton.setText("إلغاء")

    def validate(self):
        return (self.codeEdit.text() and
                self.nameEdit.text() and
                self.priceEdit.text().replace('.', '', 1).isdigit() and
                self.qtyEdit.text().isdigit())

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
        return {
            "code": self.codeEdit.text(),
            "name": self.nameEdit.text(),
            "category": self.categoryEdit.text(),
            "price": float(self.priceEdit.text()),
            "quantity": int(self.qtyEdit.text()),
            "description": self.descEdit.toPlainText()
        }
