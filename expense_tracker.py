import os
import re
from expense import Expense, RecurringExpense # Module 3: Import our custom module

# Constant for the data file (Module 2)
DATA_FILE = 'expenses.txt' 

def load_expenses(filename=DATA_FILE):
    """Loads expenses from the file and returns a list of Expense objects."""
    expenses = []
    # Module 2: File I/O for loading data
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    # Standard Expense: Date, Category, Amount
                    expenses.append(Expense(float(parts[2]), parts[1], parts[0]))
                elif len(parts) == 4:
                    # Recurring Expense: Date, Category, Amount, Frequency
                    expenses.append(RecurringExpense(float(parts[2]), parts[1], parts[0], parts[3]))
        # Module 5: Use a set for unique categories
        unique_categories = {e.category for e in expenses} 
        print(f"\n[Feedback] Loaded {len(expenses)} expenses with {len(unique_categories)} unique categories.")
    except FileNotFoundError:
        # Program Goal: Simple error feedback (file not found)
        print(f"\n[Error] Data file '{filename}' not found. Starting with an empty tracker.")
    except ValueError as e:
        print(f"\n[Error] Invalid data found in file: {e}")
    return expenses

def save_expenses(expenses, filename=DATA_FILE):
    """Saves the current list of expenses to the file."""
    # Module 2: File I/O for saving data
    with open(filename, 'w') as f:
        # The __repr__ method in the Expense class handles the formatting
        for expense in expenses:
            f.write(f"{repr(expense)}\n")
    print(f"\n[Feedback] Successfully saved {len(expenses)} expenses to '{filename}'.")

def add_expense(expenses):
    """Prompts user for expense details and adds it to the list."""
    # Program Goal: Allow the user to add new expenses
    print("\n--- Add New Expense ---")
    while True:
        try:
            amount = float(input("Enter amount (e.g., 15.50): "))
            # Simple error handling for non-positive amount
            if amount <= 0:
                print("[Error] Amount must be positive.")
                continue
            break
        except ValueError:
            print("[Error] Invalid amount. Please enter a number.")
            
    category = input("Enter category (e.g., Groceries): ").strip()
    
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ")
        # Module 8: Use regex for date validation
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, date_str):
            print("[Error] Invalid date format. Please use YYYY-MM-DD.")
            continue
        break
        
    expense_type = input("Is this a recurring expense? (yes/no): ").lower()
    
    try:
        if expense_type == 'yes':
            frequency = input("Enter frequency (e.g., Monthly): ")
            new_expense = RecurringExpense(amount, category, date_str, frequency)
        else:
            new_expense = Expense(amount, category, date_str)
        
        expenses.append(new_expense)
        print(f"\n[Feedback] Added: {new_expense.display()}")
        
    except ValueError as e:
        # Program Goal: Simple error feedback
        print(f"[Error] Could not create expense: {e}")


def view_all_expenses(expenses):
    """Prints all recorded expenses in a list."""
    # Program Goal: View all expenses in a list
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses recorded.")
        return

    # Module 6: Use sorting to display by date (oldest first)
    # The Expense class's date attribute is a datetime.date object, which is sortable.
    sorted_expenses = sorted(expenses, key=lambda e: e.date) 

    for i, expense in enumerate(sorted_expenses, 1):
        print(f"{i}. {expense.display()}")


def search_expenses(expenses):
    """Searches for expenses by category, date, or amount."""
    # Program Goal: Search for expenses
    print("\n--- Search Expenses ---")
    if not expenses:
        print("No expenses to search.")
        return

    search_term = input("Enter search term (category, date, or amount): ").lower()
    
    # Module 5: Use a list of dictionaries implicitly (Expense objects) 
    # to search by word/date/category
    def matches_search(expense):
        # Check category 
        if search_term in expense.category.lower():
            return True
        # Check date 
        if search_term == str(expense.date).lower():
            return True
        # Check amount 
        if search_term == f"{expense.amount:.2f}":
            return True
        return False
        
    # Module 6: Use a list comprehension to filter results
    found_expenses = [e for e in expenses if matches_search(e)]

    if found_expenses:
        print(f"\nFound {len(found_expenses)} matching expenses:")
        for expense in found_expenses:
            print(f"- {expense.display()}")
    else:
        print("No expenses found matching the search term.")


def view_summary_reports(expenses):
    """Calculates and displays summary reports."""
    # Program Goal: View summary reports
    print("\n--- Summary Reports ---")
    if not expenses:
        print("No expenses to summarize.")
        return
        
    # Module 5: Use a dictionary for categorizing and summing expenses
    category_totals = {}
    month_totals = {} # New dictionary for monthly totals

    for expense in expenses:
        # Category Summary
        category = expense.category
        category_totals[category] = category_totals.get(category, 0) + expense.amount
        
        # Monthly Summary: Format date as YYYY-MM 
        month_key = expense.date.strftime('%Y-%m') 
        month_totals[month_key] = month_totals.get(month_key, 0) + expense.amount
    
    # Report 1: Spending by Category
    print("\n[Report] Total Spending by Category:")
    # Module 6: Sort categories for cleaner output
    sorted_categories = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)
    for category, total in sorted_categories:
        print(f"- {category}: ${total:.2f}")

    # Report 2: Spending by Month
    print("\n[Report] Total Spending by Month:")
    # Sort by month key (Module 6)
    sorted_months = sorted(month_totals.items())
    for month, total in sorted_months:
        print(f"- {month}: ${total:.2f}")
        
    total_spending = sum(category_totals.values())
    print(f"\n[Report] TOTAL SPENDING: ${total_spending:.2f}")


def main_menu():
    """Displays the main menu and handles user input (Module 1)."""
    # Program Goal: Conditional statements, loops, and function calls for user menus and control
    expenses = load_expenses() # Load data when program starts
    
    while True:
        print("\n==============================")
        print("  PYTHON EXPENSE TRACKER MENU")
        print("==============================")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Search Expenses")
        print("4. View Summary Reports")
        print("5. Save and Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        # Module 1: Conditional statements
        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_all_expenses(expenses)
        elif choice == '3':
            search_expenses(expenses)
        elif choice == '4':
            view_summary_reports(expenses)
        elif choice == '5':
            save_expenses(expenses) # Program Goal: Save all expense data
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            # Program Goal: Simple error feedback (invalid input)
            print("[Error] Invalid choice. Please enter a number between 1 and 5.")
            
if __name__ == "__main__":
    main_menu()