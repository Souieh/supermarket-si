from datetime import datetime
from .database import Database
from .product import Product


class Purchase:
    def __init__(self, items, total_cost, supplier=""):
        """
        items: list of dicts with {"code": str, "name": str, "cost": float, "quantity": int}
        """
        self.items = items
        self.total_cost = total_cost
        self.supplier = supplier
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            "items": self.items,
            "total_cost": self.total_cost,
            "supplier": self.supplier,
            "timestamp": self.timestamp
        }

    def process_purchase(self):
        db = Database()

        def callback(session):
            # Save purchase record
            purchases_col = db.better_get_collection("purchases")
            purchases_col.insert_one(self.to_dict(), session=session)

            # Update stock (Increment)
            for item in self.items:
                Product.update_stock(item["code"], item["quantity"], session=session)

            return True

        return db.run_transaction(callback)

    @staticmethod
    def get_purchase_history():
        db = Database()
        collection = db.better_get_collection("purchases")
        return list(collection.find().sort("timestamp", -1))
