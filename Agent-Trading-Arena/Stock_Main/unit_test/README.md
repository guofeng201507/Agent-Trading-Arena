# Unit Tests for Agent Trading Arena

This directory contains comprehensive unit tests for the Agent Trading Arena project to support safe refactoring.

## Test Coverage

### test_stock.py
- `TestStock`: Tests for Stock class
  - Stock initialization from JSON
  - Price querying
  - Trade data updates
  - Daily return calculations
  - Intraday percentage changes
- `TestMarketIndex`: Tests for Market_index class
  - Market index initialization
  - Index updates
  - Index queries

### test_person.py
- `TestBroker`: Tests for Broker class
  - Broker initialization
  - Expense counting
  - Settlement operations (buy/sell)
  - IPO processing
- `TestPerson`: Tests for Person class
  - Person initialization
  - Memory management
  - Gossip handling
  - Stock holdings queries

### test_market.py
- `TestMarket`: Tests for Market class
  - Market initialization
  - Order fetching
  - Order matching
  - End of day processing
  - End of market processing

### test_behavior.py
- `TestBehaviorExtraction`: Tests for behavior extraction functions
  - Buy order extraction
  - Sell order extraction
  - Reflection analysis extraction
  - Strategy extraction

### test_database_utils.py
- `TestDatabaseUtils`: Tests for utility functions
  - Number rounding
  - List rounding
  - Stock name to ID conversion
- `TestDatabaseOperate`: Tests for Database operations
  - Database initialization
  - SQL execution
  - Order submission

### test_load_json.py
- `TestLoadJson`: Tests for JSON loading
  - Stock data loading
  - Persona data loading

## Running Tests

### Run all tests:
```bash
cd /Users/fengguo/my_projs/Agent-Trading-Arena/Agent-Trading-Arena/Stock_Main
python -m pytest unit_test/

# Or using unittest:
python unit_test/run_all_tests.py
```

### Run specific test file:
```bash
python -m pytest unit_test/test_stock.py -v
```

### Run specific test class:
```bash
python -m pytest unit_test/test_stock.py::TestStock -v
```

### Run specific test method:
```bash
python -m pytest unit_test/test_stock.py::TestStock::test_stock_initialization -v
```

## Dependencies

Tests use Python's built-in `unittest` framework and create temporary databases/files for isolation.

Optional: Install pytest for better test output:
```bash
pip install pytest pytest-cov
```

## Test Coverage Report

To generate coverage report:
```bash
pytest --cov=. --cov-report=html unit_test/
```

## Notes for Refactoring

- All tests use temporary directories and databases
- Tests are isolated and don't affect production data
- Mock objects (`MockArgs`) are used where needed
- Each test has proper setup and teardown methods
- Tests cover both success and failure scenarios

## Adding New Tests

When adding new functionality:
1. Create or update the relevant test_*.py file
2. Follow the existing test structure
3. Use descriptive test names (test_<what>_<condition>)
4. Include docstrings explaining what is tested
5. Ensure proper cleanup in tearDown methods
