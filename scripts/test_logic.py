import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.getcwd())

# Mock the Database class BEFORE importing Sale
from app.modules import database
with patch.object(database, "Database") as MockDB:
    from app.modules.product import Product
    from app.modules.receipt import Receipt
    from app.modules.sale import Sale


class TestSupermarketLogic(unittest.TestCase):
    def test_product_to_dict(self):
        p = Product("001", "Test Product", "Category", 10.5, 100, "Description")
        d = p.to_dict()
        self.assertEqual(d["code"], "001")
        self.assertEqual(d["name"], "Test Product")
        self.assertEqual(d["price"], 10.5)

    @patch("app.modules.sale.Database")
    def test_sale_total(self, MockDB):
        # Setup mock database instance
        mock_db_instance = MockDB.return_value
        mock_collection = MagicMock()
        mock_db_instance.better_get_collection.return_value = mock_collection
        mock_collection.count_documents.return_value = 0

        items = [
            {"code": "001", "name": "P1", "price": 10.0, "quantity": 2},
            {"code": "002", "name": "P2", "price": 5.0, "quantity": 1},
        ]
        sale = Sale(items, 25.0)
        self.assertEqual(sale.total_amount, 25.0)
        self.assertEqual(len(sale.items), 2)
        self.assertEqual(sale.receipt_id, "0001")

    def test_receipt_generation(self):
        sale_data = {
            "receipt_id": "9999",
            "timestamp": datetime.now(),
            "items": [{"name": "Test Item", "price": 10.0, "quantity": 2}],
            "total_amount": 20.0,
        }
        if not os.path.exists("receipts"):
            os.makedirs("receipts")

        filename = Receipt.generate(sale_data)
        self.assertTrue(os.path.exists(filename))
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("9999", content)
            self.assertIn("Test Item", content)
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == "__main__":
    unittest.main()
