"""Unit tests for Market class"""
import unittest
import sys
import os
import tempfile
import shutil
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Market import Market
from Person import Person, Broker
from Stock import Stock
from database_utils import Database_operate, submit_order


class MockArgs:
    """Mock args object for testing"""
    def __init__(self):
        self.Daily_Price_Limit = 0.7
        self.Fluctuation_Constant = 20.0


class TestMarket(unittest.TestCase):
    """Test cases for Market class"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_db")
        self.db = Database_operate(self.db_path)
        
        # Create test stock
        self.stock_data_path = os.path.join(self.test_dir, "test_stocks.json")
        test_stock_data = [
            {
                "stock_id": 0,
                "stock_name": "A",
                "quantity": 1000,
                "past_stock_last_prices": [100.0, 101.0, 102.0, 103.0, 104.0],
                "DPS": 5.0
            }
        ]
        with open(self.stock_data_path, 'w') as f:
            json.dump(test_stock_data, f)
        
        self.stocks = [Stock(0, self.db, self.stock_data_path)]
        self.broker = Broker(self.stocks, self.db)
        
        # Create test persona
        self.persona_path = os.path.join(self.test_dir, "test_persona.json")
        test_persona_data = [
            {
                "person_id": 0,
                "name": "Test Trader",
                "cash": 10000.0,
                "daily_income_from_job": 100.0,
                "minimum_living_expense": 50.0,
                "principle": "Maximize profit",
                "reflect_frequency": 3
            }
        ]
        with open(self.persona_path, 'w') as f:
            json.dump(test_persona_data, f)
        
        self.persons = [Person(0, self.broker, self.stocks, self.db, self.persona_path)]
        self.args = MockArgs()

    def tearDown(self):
        """Clean up test fixtures"""
        self.db.close()
        shutil.rmtree(self.test_dir)

    def test_market_initialization(self):
        """Test market initialization"""
        market = Market(self.broker, self.persons, self.stocks, self.db)
        
        self.assertEqual(market._bid_step, 1)
        self.assertEqual(len(market.stocks), 1)
        self.assertIsNotNone(market.broker)

    def test_fetch_orders(self):
        """Test fetching orders"""
        market = Market(self.broker, self.persons, self.stocks, self.db)
        
        # Submit a test order
        submit_order(self.db, "buy", 0, 0, 0, 0, 105.0, 10)
        
        # Fetch buy orders
        orders = market._fetch_orders("buy", 0)
        self.assertIsNotNone(orders)
        self.assertIsInstance(orders, list)

    def test_match_order_simple(self):
        """Test simple order matching"""
        market = Market(self.broker, self.persons, self.stocks, self.db)
        
        # Broker needs to IPO first to have inventory
        self.broker.ipo(0)
        
        # Submit matching buy order from person
        submit_order(self.db, "buy", 0, 0, 0, 0, 105.0, 10)
        
        initial_price = self.stocks[0].current_price
        
        # Match orders
        market.match_order(0, self.args)
        
        # Price should have changed
        self.assertNotEqual(self.stocks[0].current_price, initial_price)

    def test_end_of_day(self):
        """Test end of day processing"""
        market = Market(self.broker, self.persons, self.stocks, self.db)
        
        # Submit an order
        submit_order(self.db, "buy", 0, 0, 0, 0, 105.0, 10)
        
        # End of day should close all active orders
        market.end_of_day(0)
        
        # Check that orders are closed
        orders = market._fetch_orders("all", -1)
        for order in orders:
            self.assertEqual(order['status'], 'closed')

    def test_end_of_market(self):
        """Test end of market processing"""
        market = Market(self.broker, self.persons, self.stocks, self.db)
        
        # Broker IPO
        self.broker.ipo(0)
        
        # Submit buy order
        submit_order(self.db, "buy", 0, 0, 0, 0, 105.0, 10)
        
        initial_inventory = self.broker.inventories[0]
        
        # End of market should match remaining orders with broker
        market.end_of_market(0, self.args)
        
        # Broker inventory should have decreased
        self.assertLess(self.broker.inventories[0], initial_inventory)


if __name__ == '__main__':
    unittest.main()
