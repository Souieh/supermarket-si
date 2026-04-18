import bcrypt
from .database import Database

class User:
    @staticmethod
    def create_user(username, password, role="admin"):
        db = Database()
        collection = db.get_collection("users")

        if collection.find_one({"username": username}):
            return False, "User already exists"

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            "username": username,
            "password": hashed_pw,
            "role": role
        }
        collection.insert_one(user_data)
        return True, "User created successfully"

    @staticmethod
    def authenticate(username, password):
        db = Database()
        collection = db.get_collection("users")
        if collection is None:
            return False, "Database not connected"

        user = collection.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            return True, user["role"]

        return False, "Invalid username or password"
