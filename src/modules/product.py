from .database import Database


class Product:
    def __init__(self, code, name, category, price, quantity, description=""):
        self.code = code
        self.name = name
        self.category = category
        self.price = float(price)
        self.quantity = int(quantity)
        self.description = description

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "description": self.description
        }

    @staticmethod
    def add_product(product_data):
        db = Database()
        collection = db.better_get_collection("products")
        return collection.insert_one(product_data).inserted_id

    @staticmethod
    def update_product(code, update_data):
        db = Database()
        collection = db.better_get_collection("products")
        return collection.update_one({"code": code}, {"$set": update_data})

    @staticmethod
    def delete_product(code):
        db = Database()
        collection = db.better_get_collection("products")
        return collection.delete_one({"code": code})

    @staticmethod
    def get_product(code):
        db = Database()
        collection = db.better_get_collection("products")
        return collection.find_one({"code": code})

    @staticmethod
    def get_all_products(search_query=None, category=None):
        db = Database()
        collection = db.better_get_collection("products")
        query = {}
        if search_query:
            query["$or"] = [
                {"code": {"$regex": search_query, "$options": "i"}},
                {"name": {"$regex": search_query, "$options": "i"}},
                {"category": {"$regex": search_query, "$options": "i"}}
            ]
        if category:
            query["category"] = category

        return list(collection.find(query))

    @staticmethod
    def update_stock(code, quantity_change, session=None):
        db = Database()
        collection = db.better_get_collection("products")
        return collection.update_one(
            {"code": code},
            {"$inc": {"quantity": quantity_change}},
            session=session
        )
