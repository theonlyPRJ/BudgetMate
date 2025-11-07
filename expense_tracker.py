import sqlite3
import datetime

# Define the name of the database file
DATABASE_NAME = "expenses.db"

def connect_db():
    """Connects to the SQLite database and returns the connection object."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table():
    """
    Creates the 'expenses' table if it doesn't already exist.
    The table stores the date, amount, and a description for each expense.
    """
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT NOT NULL
                )
            """)
            conn.commit()
            print("Database table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

def add_expense(amount, description):
    """
    Adds a new expense to the database.
    
    Args:
        amount (float): The monetary amount of the expense.
        description (str): A brief description of the expense.
    """
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Get the current date in YYYY-MM-DD format
            expense_date = datetime.date.today().isoformat()
            cursor.execute("INSERT INTO expenses (date, amount, description) VALUES (?, ?, ?)", 
                           (expense_date, amount, description))
            conn.commit()
            print(f"Expense of ${amount:.2f} for '{description}' added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding expense: {e}")
        finally:
            conn.close()

def view_expenses():
    """
    Retrieves and prints all expenses from the database.
    """
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT date, amount, description FROM expenses ORDER BY date DESC")
            rows = cursor.fetchall()
            if not rows:
                print("No expenses found.")
                return

            print("\n--- All Expenses ---")
            for row in rows:
                date, amount, description = row
                print(f"Date: {date} | Amount: ${amount:.2f} | Description: {description}")
            print("--------------------\n")
        except sqlite3.Error as e:
            print(f"Error viewing expenses: {e}")
        finally:
            conn.close()

# Example usage to demonstrate the functions
if __name__ == "__main__":
    create_table()
    
    # Add a couple of sample expenses
    add_expense(25.50, "Groceries")
    add_expense(12.75, "Coffee")
    
    # View all expenses
    view_expenses()
