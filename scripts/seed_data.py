import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from app.modules.category import Category
from app.modules.database import Database
from app.modules.product import Product
from app.modules.user import User


def seed():
    db = Database()
    success, msg = db.connect()
    if not success:
        print(f"Error: {msg}. Please ensure your database config is correct.")
        return

    # 1. Create Default Users
    print("Seeding users...")
    User.create_user("admin", "admin", role="admin")
    User.create_user("cashier", "cashier", role="cashier")

    # 2. Create Categories
    print("Seeding categories...")
    categories = ["Vegetables", "Fruits", "Groceries", "Dairy", "Beverages"]
    for cat in categories:
        Category.add_category(cat)

    # 3. Create Products
    print("Seeding products...")
    products = [
        {
            "code": "P001",
            "name": "Tomato",
            "category": "Vegetables",
            "price": 2.50,
            "quantity": 100,
        },
        {
            "code": "P002",
            "name": "Apple",
            "category": "Fruits",
            "price": 1.20,
            "quantity": 150,
        },
        {
            "code": "P003",
            "name": "Milk 1L",
            "category": "Dairy",
            "price": 4.00,
            "quantity": 50,
        },
        {
            "code": "P004",
            "name": "Bread",
            "category": "Groceries",
            "price": 1.50,
            "quantity": 80,
        },
        {
            "code": "P005",
            "name": "Water 500ml",
            "category": "Beverages",
            "price": 0.50,
            "quantity": 200,
        },
        {
            "code": "P006",
            "name": "Cucumber",
            "category": "Vegetables",
            "price": 1.80,
            "quantity": 120,
        },
        {
            "code": "P007",
            "name": "Banana",
            "category": "Fruits",
            "price": 0.90,
            "quantity": 300,
        },
    ]
    for p_data in products:
        if not Product.get_product(p_data["code"]):
            Product.add_product(p_data)

    print("Data seeding completed successfully!")


if __name__ == "__main__":
    seed()
