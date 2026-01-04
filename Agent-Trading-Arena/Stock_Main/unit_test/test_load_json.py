"""Unit tests for load_json module"""
import unittest
import sys
import os
import tempfile
import shutil
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from load_json import load_stocks, load_persona


class TestLoadJson(unittest.TestCase):
    """Test cases for JSON loading functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)

    def test_load_stocks(self):
        """Test loading stocks from JSON"""
        # Create test stock file
        stock_path = os.path.join(self.test_dir, "test_stocks.json")
        test_data = [
            {
                "stock_id": 0,
                "stock_name": "A",
                "quantity": 1000,
                "past_stock_last_prices": [100.0, 101.0, 102.0, 103.0, 104.0],
                "DPS": 5.0
            },
            {
                "stock_id": 1,
                "stock_name": "B",
                "quantity": 2000,
                "past_stock_last_prices": [200.0, 201.0, 202.0, 203.0, 204.0],
                "DPS": 10.0
            }
        ]
        
        with open(stock_path, 'w') as f:
            json.dump(test_data, f)
        
        stocks = load_stocks(stock_path)
        
        self.assertEqual(len(stocks), 2)
        self.assertEqual(stocks[0]['stock_name'], 'A')
        self.assertEqual(stocks[1]['stock_name'], 'B')
        self.assertEqual(stocks[0]['DPS'], 5.0)

    def test_load_persona(self):
        """Test loading persona from JSON"""
        # Create test persona file
        persona_path = os.path.join(self.test_dir, "test_persona.json")
        test_data = [
            {
                "person_id": 0,
                "name": "Alice",
                "cash": 10000.0,
                "daily_income_from_job": 100.0,
                "minimum_living_expense": 50.0,
                "principle": "Growth investor",
                "reflect_frequency": 3
            },
            {
                "person_id": 1,
                "name": "Bob",
                "cash": 20000.0,
                "daily_income_from_job": 200.0,
                "minimum_living_expense": 100.0,
                "principle": "Value investor",
                "reflect_frequency": 5
            }
        ]
        
        with open(persona_path, 'w') as f:
            json.dump(test_data, f)
        
        personas = load_persona(persona_path)
        
        self.assertEqual(len(personas), 2)
        self.assertEqual(personas[0]['name'], 'Alice')
        self.assertEqual(personas[1]['name'], 'Bob')
        self.assertEqual(personas[0]['cash'], 10000.0)


if __name__ == '__main__':
    unittest.main()
