import pytest
from expense import Expense
from expense_tracker import load_expenses

# Module 3: Test functions using pytest and assert statements
def test_expense_creation():
    """Test successful creation and attributes of an Expense object."""
    e = Expense(100.50, "Rent", "2025-10-01")
    assert e.amount == 100.50
    assert e.category == "Rent" # Category should be capitalized (check expense.py)
    assert str(e.date) == "2025-10-01"

def test_expense_invalid_amount():
    """Test error handling for invalid expense amount."""
    # This uses pytest.raises to check if a ValueError is raised
    with pytest.raises(ValueError) as excinfo:
        Expense(-10.00, "Invalid", "2025-01-01")
    # assert "positive number" in str(excinfo.value) 
def test_expense_invalid_date_format():
    """Test error handling for invalid date format (Module 8)."""
    with pytest.raises(ValueError) as excinfo:
        Expense(50.00, "Test", "01/01/2025") # Incorrect format
    assert "YYYY-MM-DD" in str(excinfo.value)
    
# Module 5: Test unique category set logic (indirectly through load)
# Note: For this to pass, you need an expenses.txt file with duplicate categories.
def test_unique_categories_loading(tmp_path):
    """Tests the logic for counting unique categories during file load."""
    
    # Create a temporary test file with expense data
    test_data = [
        "2025-01-01,Groceries,50.00",
        "2025-01-02,Rent,1000.00",
        "2025-01-03,Groceries,25.00"
    ]
    test_file = tmp_path / "test_data.txt"
    test_file.write_text('\n'.join(test_data))

    # Load data from the temporary file
    expenses = load_expenses(test_file)
    
    # Check that only 2 unique categories were loaded
    # This verifies the logic used in load_expenses which uses a set comprehension
    unique_categories = {e.category for e in expenses} 
    assert len(unique_categories) == 2 
    assert "Groceries" in unique_categories
    assert "Rent" in unique_categories