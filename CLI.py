import sys
import datetime
from expense_tracker import create_table, add_expense, view_expenses, connect_db

def view_weekly_summary():
    """
    Prompts the user for a week number and displays a summary of expenses for that week.
    The week number is based on the ISO week number (1-52).
    """
    try:
        week_number = int(input("Enter the week number (1-52): "))
        if not 1 <= week_number <= 52:
            print("Invalid week number. Please enter a number between 1 and 52.")
            return

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Get the current year
                year = datetime.date.today().year

                # Find the start and end dates of the specified week
                start_date = datetime.date.fromisocalendar(year, week_number, 1).isoformat()
                end_date = datetime.date.fromisocalendar(year, week_number, 7).isoformat()

                cursor.execute("SELECT date, amount FROM expenses WHERE date BETWEEN ? AND ?", (start_date, end_date))
                weekly_data = cursor.fetchall()
                
                total_spending = sum(amount for date, amount in weekly_data)

                print(f"\n--- Spending Summary for Week {week_number}, {year} ---")
                if not weekly_data:
                    print("No expenses found for this week.")
                else:
                    print(f"Total spending: ${total_spending:.2f}")
                    generate_text_chart(weekly_data)
                print("-------------------------------------------\n")

            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                conn.close()
    except ValueError:
        print("Invalid input. Please enter a number.")

def generate_text_chart(data):
    """
    Generates a simple text-based bar chart of expenses per day.
    """
    daily_totals = {}
    for date, amount in data:
        day_of_week = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%a')
        if day_of_week not in daily_totals:
            daily_totals[day_of_week] = 0
        daily_totals[day_of_week] += amount

    max_amount = max(daily_totals.values()) if daily_totals else 0
    scale = 20.0 / max_amount if max_amount > 0 else 1.0

    print("\nDaily Breakdown (Text Chart):")
    for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
        amount = daily_totals.get(day, 0)
        bar_length = int(amount * scale)
        print(f"{day}: ${amount:6.2f} | {'#' * bar_length}")

def main_menu():
    """
    Displays the main menu and handles user input.
    """
    create_table()

    while True:
        print("\n--- Expense Tracker CLI ---")
        print("1. Add a new expense")
        print("2. View all expenses")
        print("3. View weekly spending summary")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            try:
                amount = float(input("Enter expense amount: $"))
                if amount <= 0:
                    print("Amount must be a positive number. Please try again.")
                    continue
                description = input("Enter expense description: ")
                if not description.strip():
                    print("Description cannot be empty. Please try again.")
                    continue
                add_expense(amount, description)
            except ValueError:
                print("Invalid input for amount. Please enter a number.")
        
        elif choice == '2':
            view_expenses()
        
        elif choice == '3':
            view_weekly_summary()
        
        elif choice == '4':
            print("Exiting Expense Tracker. Goodbye!")
            sys.exit()
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main_menu()
