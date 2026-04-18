from .database import Database


class Category:
    @staticmethod
    def add_category(name):
        db = Database()
        collection = db.better_get_collection("categories")
        if collection.find_one({"name": name}):
            return None
        return collection.insert_one({"name": name}).inserted_id

    @staticmethod
    def delete_category(name):
        db = Database()
        collection = db.better_get_collection("categories")
        return collection.delete_one({"name": name})

    @staticmethod
    def get_all_categories():
        db = Database()
        collection = db.better_get_collection("categories")
        return list(collection.find())
