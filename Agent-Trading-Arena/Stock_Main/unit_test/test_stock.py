"""Unit tests for Stock class"""
import unittest
import sys
import os
import tempfile
import shutil
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Stock import Stock, Market_index
from database_utils import Database_operate


class TestStock(unittest.TestCase):
    """Test cases for Stock class"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_db")
        self.db = Database_operate(self.db_path)
        
        # Create test stock data file
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
        import json
        with open(self.stock_data_path, 'w') as f:
            json.dump(test_stock_data, f)

    def tearDown(self):
        """Clean up test fixtures"""
        self.db.close()
        shutil.rmtree(self.test_dir)

    def test_stock_initialization(self):
        """Test stock initialization from JSON"""
        stock = Stock(0, self.db, self.stock_data_path)
        
        self.assertEqual(stock.stock_id, 0)
        self.assertEqual(stock.stock_name, "A")
        self.assertEqual(stock.quantity, 1000)
        self.assertEqual(stock.DPS, 5.0)
        self.assertEqual(stock.current_price, 104.0)

    def test_query_price(self):
        """Test querying stock price for a specific date"""
        stock = Stock(0, self.db, self.stock_data_path)
        
        # Query initial price (virtual_date = 0)
        result = stock.query_price(0)
        self.assertIsNotNone(result)
        self.assertEqual(result['stock_id'], 0)
        self.assertEqual(result['last_price'], 104.0)

    def test_update_trade_data(self):
        """Test updating stock trade data"""
        stock = Stock(0, self.db, self.stock_data_path)
        
        # Update with new trade
        stock.update_trade_data(0, 105.0, 10)
        
        result = stock.query_price(0)
        self.assertEqual(result['last_price'], 105.0)
        self.assertEqual(result['quantity'], 10)

    def test_query_daily_return(self):
        """Test querying historical daily returns"""
        stock = Stock(0, self.db, self.stock_data_path)
        
        prices = stock.query_daily_return(0, no_days=5)
        self.assertEqual(len(prices), 5)
        self.assertIsInstance(prices, list)

    def test_query_intraday_percentage(self):
        """Test calculating intraday percentage change"""
        stock = Stock(0, self.db, self.stock_data_path)
        
        # Initialize intraday data
        stock.update_trade_data(1, 104.0, 0)
        stock.update_trade_data(1, 110.0, 10)
        
        percentage = stock.query_intraday_percentage(1)
        self.assertAlmostEqual(percentage, (110.0 - 104.0) / 104.0, places=4)


class TestMarketIndex(unittest.TestCase):
    """Test cases for Market_index class"""

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

    def tearDown(self):
        """Clean up test fixtures"""
        self.db.close()
        shutil.rmtree(self.test_dir)

    def test_market_index_initialization(self):
        """Test market index initialization"""
        market_index = Market_index(self.stocks, self.db)
        
        self.assertIsNotNone(market_index.db)
        self.assertEqual(len(market_index.stocks), 1)

    def test_update_market_index(self):
        """Test updating market index"""
        market_index = Market_index(self.stocks, self.db)
        
        # Initial update
        market_index.update_market_index(0)
        result = market_index.query_market_index(0)
        self.assertIsNotNone(result)

    def test_query_market_index(self):
        """Test querying market index for a specific date"""
        market_index = Market_index(self.stocks, self.db)
        market_index.update_market_index(0)
        
        result = market_index.query_market_index(0)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
