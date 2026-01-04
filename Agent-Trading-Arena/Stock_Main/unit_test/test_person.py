"""Unit tests for Person and Broker classes"""
import unittest
import sys
import os
import tempfile
import shutil
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Person import Person, Broker
from Stock import Stock
from database_utils import Database_operate


class TestBroker(unittest.TestCase):
    """Test cases for Broker class"""

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

    def test_broker_initialization(self):
        """Test broker initialization"""
        broker = Broker(self.stocks, self.db)
        
        self.assertEqual(broker.person_id, -1)
        self.assertEqual(broker.cash, 0)
        self.assertGreater(broker.asset, 0)
        self.assertEqual(len(broker.inventories), 1)
        self.assertEqual(broker.inventories[0], 1000)

    def test_broker_count_expense(self):
        """Test broker expense counting"""
        broker = Broker(self.stocks, self.db)
        initial_cash = broker.cash
        
        broker.count_expense(100.0)
        
        self.assertEqual(broker.cash, initial_cash + 100.0)
        self.assertEqual(broker.total_expense, 100.0)

    def test_broker_settlement_sell(self):
        """Test broker settlement for sell order"""
        broker = Broker(self.stocks, self.db)
        initial_cash = broker.cash
        initial_inventory = broker.inventories[0]
        
        order = {
            "type": "sell",
            "stock_id": 0,
            "virtual_date": 0
        }
        
        broker.settlement(order, 105.0, 10)
        
        self.assertEqual(broker.cash, initial_cash + 105.0 * 10)
        self.assertEqual(broker.inventories[0], initial_inventory - 10)

    def test_broker_settlement_buy(self):
        """Test broker settlement for buy order"""
        broker = Broker(self.stocks, self.db)
        broker.cash = 10000.0  # Give broker some cash
        initial_cash = broker.cash
        initial_inventory = broker.inventories[0]
        
        order = {
            "type": "buy",
            "stock_id": 0,
            "virtual_date": 0
        }
        
        broker.settlement(order, 100.0, 10)
        
        self.assertEqual(broker.cash, initial_cash - 100.0 * 10)
        self.assertEqual(broker.inventories[0], initial_inventory + 10)


class TestPerson(unittest.TestCase):
    """Test cases for Person class"""

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

    def tearDown(self):
        """Clean up test fixtures"""
        self.db.close()
        shutil.rmtree(self.test_dir)

    def test_person_initialization(self):
        """Test person initialization"""
        person = Person(0, self.broker, self.stocks, self.db, self.persona_path)
        
        self.assertEqual(person.person_id, 0)
        self.assertEqual(person.cash, 10000.0)
        self.assertEqual(person.income, 100.0)
        self.assertEqual(person.principle, "Maximize profit")
        self.assertEqual(person.reflect_frequency, 3)

    def test_add_memory(self):
        """Test adding memory to person"""
        person = Person(0, self.broker, self.stocks, self.db, self.persona_path)
        
        # Need a market index for add_memory
        from Stock import Market_index
        market_index = Market_index(self.stocks, self.db)
        market_index.update_market_index(0)
        
        person.add_memory(
            virtual_date=0,
            iteration=0,
            stock_op="buy 10 shares of A",
            type="buy",
            gossip="Market is bullish",
            analysis_stocks="Stock A looks promising",
            analysis_strategy="None",
            market_index=market_index,
            stocks_list=self.stocks
        )
        
        memory = person.query_memory(0)
        self.assertIsNotNone(memory)
        self.assertGreater(len(memory), 0)

    def test_add_gossip(self):
        """Test adding gossip"""
        person = Person(0, self.broker, self.stocks, self.db, self.persona_path)
        
        person.add_gossip(0, "Market is bullish")
        
        gossip = person.query_gossip(0)
        self.assertIsNotNone(gossip)

    def test_query_hold_stocks(self):
        """Test querying held stocks"""
        person = Person(0, self.broker, self.stocks, self.db, self.persona_path)
        
        # Initially should have no holdings
        holdings = person.query_hold_stocks(0)
        self.assertTrue(holdings is None or len(holdings) == 0)


if __name__ == '__main__':
    unittest.main()
