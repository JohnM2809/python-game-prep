import json
from datetime import datetime

FILE = "finance.json"

# ---------- FILE HANDLING ----------
def load_data():
    try:
        with open(FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------- ADD TRANSACTION ----------
def add_transaction(data, kind):
    try:
        amount = float(input("Amount: Rs. "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Invalid amount!")
        return

    category = input("Category: ").strip().title() or "Other"
    note = input("Note: ").strip() or "-"

    data.append({
        "type": kind,
        "amount": amount,
        "category": category,
        "note": note,
        "date": datetime.now().strftime("%d-%m-%Y")
    })

    save_data(data)
    print("Transaction added!")

# ---------- VIEW ----------
def view(data):
    if not data:
        print("No transactions found.")
        return

    print("\n--- TRANSACTIONS ---")
    for i, x in enumerate(data, 1):
        sign = "+" if x["type"] == "income" else "-"
        print(f"{i}. {x['date']} | {x['category']:<12} | "
              f"{sign}Rs.{x['amount']:.2f} | {x['note']}")

# ---------- SUMMARY ----------
def summary(data):
    income = sum(x["amount"] for x in data if x["type"] == "income")
    expense = sum(x["amount"] for x in data if x["type"] == "expense")

    print("\n--- FINANCIAL SUMMARY ---")
    print(f"Income : Rs.{income:.2f}")
    print(f"Expense: Rs.{expense:.2f}")
    print(f"Balance: Rs.{income - expense:.2f}")

    status = ("Positive balance" if income > expense
              else "Expenses exceed income" if expense > income
              else "Balanced")
    print("Status:", status)

# ---------- CATEGORY REPORT ----------
def category_report(data):
    report = {}

    for x in data:
        if x["type"] == "expense":
            c = x["category"]
            report[c] = report.get(c, 0) + x["amount"]

    print("\n--- EXPENSE BY CATEGORY ---")

    if not report:
        print("No expenses found.")
        return

    for c, amount in sorted(report.items(),
                             key=lambda x: x[1], reverse=True):
        print(f"{c:<15} Rs.{amount:.2f}")

# ---------- SEARCH ----------
def search(data):
    c = input("Category to search: ").strip().lower()
    found = [x for x in data if x["category"].lower() == c]

    if not found:
        print("No matching transactions.")
        return

    print("\n--- SEARCH RESULTS ---")
    for x in found:
        sign = "+" if x["type"] == "income" else "-"
        print(f"{x['date']} | {sign}Rs.{x['amount']:.2f} | {x['note']}")

# ---------- DELETE ----------
def delete(data):
    view(data)

    if not data:
        return

    try:
        n = int(input("Transaction number to delete: "))
        if not 1 <= n <= len(data):
            raise ValueError
    except ValueError:
        print("Invalid number!")
        return

    removed = data.pop(n - 1)
    save_data(data)
    print(f"Deleted {removed['category']} transaction.")

# ---------- MAIN MENU ----------
def main():
    data = load_data()

    while True:
        print("""
================================
       PERSONAL FINANCE
================================
1. Add Income
2. Add Expense
3. View Transactions
4. Financial Summary
5. Expense by Category
6. Search Category
7. Delete Transaction
8. Exit
================================""")

        choice = input("Enter choice: ")

        if choice == "1":
            add_transaction(data, "income")
        elif choice == "2":
            add_transaction(data, "expense")
        elif choice == "3":
            view(data)
        elif choice == "4":
            summary(data)
        elif choice == "5":
            category_report(data)
        elif choice == "6":
            search(data)
        elif choice == "7":
            delete(data)
        elif choice == "8":
            save_data(data)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
