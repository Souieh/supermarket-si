from datetime import datetime
from .database import Database
from .product import Product


class Sale:
    def __init__(self, items, total_amount):
        """
        items: list of dicts with {"code": str, "name": str, "price": float, "quantity": int}
        """
        self.items = items
        self.total_amount = total_amount
        self.timestamp = datetime.now()
        self.receipt_id = self._generate_receipt_id()

    def _generate_receipt_id(self):
        db = Database()
        collection = db.better_get_collection("sales")
        count = collection.count_documents({})
        return f"{count + 1:04d}"

    def to_dict(self):
        return {
            "receipt_id": self.receipt_id,
            "items": self.items,
            "total_amount": self.total_amount,
            "timestamp": self.timestamp
        }

    def process_sale(self):
        db = Database()

        def callback(session):
            # Save sale
            sales_col = db.better_get_collection("sales")
            sales_col.insert_one(self.to_dict(), session=session)

            # Update stock
            for item in self.items:
                Product.update_stock(item["code"], -item["quantity"], session=session)

            return self.receipt_id

        return db.run_transaction(callback)

    @staticmethod
    def get_sales_history():
        db = Database()
        collection = db.better_get_collection("sales")
        return list(collection.find().sort("timestamp", -1))

    @staticmethod
    def get_dashboard_stats():
        db = Database()
        products_col = db.better_get_collection("products")
        sales_col = db.better_get_collection("sales")
        categories_col = db.better_get_collection("categories")
        purchases_col = db.better_get_collection("purchases")

        total_products = products_col.count_documents({})
        out_of_stock = products_col.count_documents({"quantity": {"$lte": 0}})
        total_categories = categories_col.count_documents({})

        # Daily revenue
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        daily_sales = list(sales_col.find({"timestamp": {"$gte": today}}))
        daily_revenue = sum(sale["total_amount"] for sale in daily_sales)

        # Total Purchases
        purchases = list(purchases_col.find())
        total_purchases = sum(p.get("total_cost", 0) for p in purchases)

        return {
            "total_products": total_products,
            "out_of_stock": out_of_stock,
            "total_categories": total_categories,
            "daily_revenue": daily_revenue,
            "total_sales": sales_col.count_documents({}),
            "total_purchases": total_purchases
        }
