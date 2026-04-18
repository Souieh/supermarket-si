import os


class Receipt:
    @staticmethod
    def generate(sale_data):
        receipt_id = sale_data["receipt_id"]
        timestamp = sale_data["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        items = sale_data["items"]
        total = sale_data["total_amount"]

        if not os.path.exists("receipts"):
            os.makedirs("receipts")

        filename = f"receipts/receipt_{receipt_id}.txt"

        content = f"""
==========================================
        SUPERMARKET RECEIPT
==========================================
Date: {timestamp}
Receipt No: {receipt_id}
------------------------------------------
Product            Qty    Price     Total
------------------------------------------
"""
        for item in items:
            name = item["name"][:18].ljust(18)
            qty = str(item["quantity"]).ljust(6)
            price = f"{item['price']:.2f}".ljust(9)
            subtotal = f"{item['price'] * item['quantity']:.2f}"
            content += f"{name} {qty} {price} {subtotal}\n"

        content += f"""------------------------------------------
TOTAL:                          {total:.2f}
------------------------------------------
      Thank you for your purchase!
      شكراً لزيارتكم! نتمنى رؤيتكم قريباً
==========================================
"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        return filename
