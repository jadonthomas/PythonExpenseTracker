import datetime
import re # Module 8: For validating the date format

# Base class for all expenses (Module 4)
class Expense:
    """Represents a single expense transaction."""
    # Attribute names: amount, category, date
    def __init__(self, amount, category, date_str):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number.")
        
        # Module 8: Use regex to validate date format (YYYY-MM-DD)
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, date_str):
            raise ValueError("Date format must be YYYY-MM-DD.")
            
        self.amount = float(amount)
        self.category = category.strip().capitalize()
        # Convert valid date string to datetime object for easier sorting/comparison
        self.date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    def __repr__(self):
        """String representation for saving/loading."""
        return f"{self.date.strftime('%Y-%m-%d')},{self.category},{self.amount:.2f}"

    def display(self):
        """User-friendly display."""
        return f"Date: {self.date}, Category: {self.category}, Amount: ${self.amount:.2f}"

# Subclass using inheritance for recurring expenses (Module 7)
class RecurringExpense(Expense):
    """Represents an expense that occurs repeatedly."""
    def __init__(self, amount, category, date_str, frequency="Monthly"):
        super().__init__(amount, category, date_str)
        self.frequency = frequency

    def __repr__(self):
        """Includes frequency in the representation."""
        base_repr = super().__repr__()
        return f"{base_repr},{self.frequency}"

    def display(self):
        """Includes frequency in the display."""
        base_display = super().display()
        return f"{base_display} ({self.frequency} Recurring)"