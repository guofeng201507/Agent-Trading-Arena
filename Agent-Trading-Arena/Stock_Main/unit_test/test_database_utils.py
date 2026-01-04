"""Unit tests for database_utils module"""
import unittest
import sys
import os
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database_utils import (
    Database_operate,
    round_two_decimal,
    round_lists_two_decimals,
    stock_name_to_id,
    submit_order
)


class TestDatabaseUtils(unittest.TestCase):
    """Test cases for database utility functions"""

    def test_round_two_decimal(self):
        """Test rounding to two decimal places"""
        self.assertEqual(round_two_decimal(3.14159), 3.14)
        self.assertEqual(round_two_decimal(10), 10.0)
        self.assertEqual(round_two_decimal(0.999), 1.0)

    def test_round_lists_two_decimals(self):
        """Test rounding list values to two decimals"""
        input_list = [3.14159, 2.71828, 1.41421]
        result = round_lists_two_decimals(input_list, in_percentage=False)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], 3.14)
        self.assertEqual(result[1], 2.72)
        self.assertEqual(result[2], 1.41)

    def test_round_lists_two_decimals_percentage(self):
        """Test rounding with percentage conversion"""
        input_list = [0.0314, 0.0272, 0.0141]
        result = round_lists_two_decimals(input_list, in_percentage=True)
        
        self.assertEqual(result[0], 3.14)
        self.assertEqual(result[1], 2.72)
        self.assertEqual(result[2], 1.41)

    def test_stock_name_to_id(self):
        """Test converting stock name to ID"""
        # Create a test database for this test
        test_dir = tempfile.mkdtemp()
        db_path = os.path.join(test_dir, "test_db")
        db = Database_operate(db_path)
        
        try:
            # Create mock stocks
            from Stock import Stock
            stock_a = Stock(0, db, self.create_test_stock_file(test_dir, 0, "A"))
            stock_b = Stock(1, db, self.create_test_stock_file(test_dir, 1, "B"))
            stocks = [stock_a, stock_b]
            
            self.assertEqual(stock_name_to_id(stocks, "A"), 0)
            self.assertEqual(stock_name_to_id(stocks, "B"), 1)
        finally:
            db.close()
            shutil.rmtree(test_dir)
    
    def create_test_stock_file(self, test_dir, stock_id, stock_name):
        """Helper to create test stock file"""
        import json
        stock_path = os.path.join(test_dir, f"test_stock_{stock_id}.json")
        test_data = [{
            "stock_id": stock_id,
            "stock_name": stock_name,
            "quantity": 1000,
            "past_stock_last_prices": [100.0, 101.0, 102.0, 103.0, 104.0],
            "DPS": 5.0
        }]
        with open(stock_path, 'w') as f:
            json.dump(test_data, f)
        return stock_path


class TestDatabaseOperate(unittest.TestCase):
    """Test cases for Database_operate class"""

    def setUp(self):
        """Set up test database"""
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_db")
        self.db = Database_operate(self.db_path)

    def tearDown(self):
        """Clean up test database"""
        self.db.close()
        shutil.rmtree(self.test_dir)

    def test_database_initialization(self):
        """Test database initialization"""
        self.assertIsNotNone(self.db._conn)
        self.assertIsNotNone(self.db._cur)

    def test_execute_sql(self):
        """Test SQL execution"""
        # Create a simple test table
        self.db.execute_sql(
            "CREATE TABLE IF NOT EXISTS test_table (id INTEGER, value TEXT)"
        )
        
        # Insert data
        self.db.execute_sql("INSERT INTO test_table VALUES (1, 'test')")
        
        # Query data
        self.db.execute_sql("SELECT * FROM test_table WHERE id = 1")
        results = self.db.fetchall()
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 1)
        self.assertEqual(results[0][1], 'test')

    def test_submit_order(self):
        """Test order submission"""
        submit_order(self.db, "buy", 0, 0, 0, 0, 105.0, 10)
        
        # Verify order was inserted
        self.db.execute_sql("SELECT * FROM active_orders WHERE person_id = 0")
        results = self.db.fetchall()
        
        self.assertGreater(len(results), 0)


if __name__ == '__main__':
    unittest.main()
