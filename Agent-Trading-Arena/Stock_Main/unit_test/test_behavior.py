"""Unit tests for behavior module"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from behavior import (
    extract_for_choose_buy,
    extract_for_choose_sell,
    extract_analysis_for_reflect,
    extract_strategy
)


class TestBehaviorExtraction(unittest.TestCase):
    """Test cases for behavior extraction functions"""

    def test_extract_for_choose_buy_valid(self):
        """Test extracting valid buy order"""
        response = "Operation: buy, Stock name: A, Investment Amount: $1000, Best Buying Price: $105.5"
        
        stock_name, quantity, price = extract_for_choose_buy(response)
        
        self.assertEqual(stock_name, "A")
        self.assertGreater(quantity, 0)
        self.assertEqual(price, 105.5)

    def test_extract_for_choose_buy_hold(self):
        """Test extracting hold decision"""
        response = "Hold"
        
        stock_name, quantity, price = extract_for_choose_buy(response)
        
        self.assertEqual(stock_name, "hold")
        self.assertEqual(quantity, 0)
        self.assertEqual(price, 0)

    def test_extract_for_choose_buy_invalid(self):
        """Test extracting invalid buy order"""
        response = "Invalid response format"
        
        result = extract_for_choose_buy(response)
        
        self.assertFalse(result)

    def test_extract_for_choose_sell_valid(self):
        """Test extracting valid sell order"""
        response = "Operation: sell, Stock name: B, The number of shares: 50, Best Selling Price: $110.25"
        
        stock_name, quantity, price = extract_for_choose_sell(response)
        
        self.assertEqual(stock_name, "B")
        self.assertEqual(quantity, "50")
        self.assertEqual(price, 110.25)

    def test_extract_for_choose_sell_hold(self):
        """Test extracting hold decision for sell"""
        response = "Hold"
        
        stock_name, quantity, price = extract_for_choose_sell(response)
        
        self.assertEqual(stock_name, "hold")
        self.assertEqual(quantity, 0)
        self.assertEqual(price, 0)

    def test_extract_analysis_for_reflect_valid(self):
        """Test extracting reflection analysis"""
        response = "Weakness: Over-trading leads to high costs. Strength: Good risk management"
        
        result = extract_analysis_for_reflect(response)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertIn("Over-trading", result[0])
        self.assertIn("Good risk management", result[1])

    def test_extract_analysis_for_reflect_invalid(self):
        """Test extracting invalid reflection"""
        response = "Invalid format"
        
        result = extract_analysis_for_reflect(response)
        
        self.assertFalse(result)

    def test_extract_strategy_valid(self):
        """Test extracting new strategy"""
        response = "New investment strategy: Focus on dividend stocks with stable growth"
        
        result = extract_strategy(response)
        
        self.assertIsNotNone(result)
        self.assertIn("dividend stocks", result)

    def test_extract_strategy_invalid(self):
        """Test extracting invalid strategy"""
        response = "Invalid strategy format"
        
        result = extract_strategy(response)
        
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
