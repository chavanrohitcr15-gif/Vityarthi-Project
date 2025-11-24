import sqlite3
import os

DB = "simple_billing.db"  # yeah, keeping it simple

def setup():
    # just in case the db doesn't exist
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL,
                  price REAL,
                  qty INTEGER,
                  total REAL)''')
    conn.commit()
    conn.close()
    print("DB setup done, or whatever.")

def save_item(name, price, qty, item_id=None):
    # calculate total, duh
    total = price * qty
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        if item_id is not None:  # cuz None is falsy but let's be explicit
            c.execute("UPDATE items SET name=?, price=?, qty=?, total=? WHERE id=?",
                      (name, price, qty, total, item_id))
            print(f"Updated item {item_id}")
        else:
            c.execute("INSERT INTO items (name, price, qty, total) VALUES (?, ?, ?, ?)",
                      (name, price, qty, total))
            print("New item added, sweet.")
    except sqlite3.Error as e:
        print(f"Oops, db error: {e}")  # basic error handling, didn't feel like more
    finally:
        conn.commit()
        conn.close()

def delete_item(item_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    # no print here, lazy

def get_items():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, name, price, qty, total FROM items ORDER BY id DESC")  # newest first, why not
    items = c.fetchall()
    conn.close()
    return items or []  # avoid empty issues

def main():
    setup()  # call it once
    while True:
        # clear screen, windows vs unix, classic
        os.system('cls' if os.name == 'nt' else 'clear')
        print("BILLING ITEMS MANAGER")  # all caps for fun
        print("=" * 50)
        print("1. Add New Item")
        print("2. View All Items")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Exit")
        print("-" * 50)
       
        choice = input("Choose option (1-5): ").strip()  # strip just in case
        if choice == "1":
            print("\n--- Add New Item ---")
            name = input("Item Name: ").strip()
            try:
                price = float(input("Price: "))
                qty = int(input("Quantity: "))
                save_item(name, price, qty)
                print("Item added successfully!")
            except ValueError:
                print("Numbers only, dude.")
            input("\nPress Enter to continue...")
        elif choice == "2":
            print("\n--- All Items ---")
            items = get_items()
            if not items:
                print("No items found. Add some?")
            else:
                print(f"{'ID':<4} {'Name':<20} {'Price':<10} {'Qty':<6} {'Total':<10}")
                print("-" * 55)
                for item in items:
                    print(f"{item[0]:<4} {item[1]:<20} ${item[2]:<9.2f} {item[3]:<6} ${item[4]:.2f}")
            input("\nPress Enter to continue...")
        elif choice == "3":
            items = get_items()
            if not items:
                print("No items to update.")
                input("\nPress Enter to continue...")
                continue
            print("\n--- Update Item ---")
            for item in items:
                print(f"{item[0]}. {item[1]} - ${item[4]:.2f}")
            try:
                id_to_edit = int(input("Enter Item ID to update: "))
                # check if exists? nah, let it fail
                name = input("New Name: ").strip()
                price = float(input("New Price: "))
                qty = int(input("New Quantity: "))
                save_item(name, price, qty, id_to_edit)
                print("Item updated!")
            except ValueError:
                print("Invalid input, try again.")
            input("\nPress Enter to continue...")
        elif choice == "4":
            items = get_items()
            if not items:
                print("No items to delete.")
                input("\nPress Enter to continue...")
                continue
            print("\n--- Delete Item ---")
            for item in items:
                print(f"{item[0]}. {item[1]}")
            try:
                id_to_delete = int(input("Enter Item ID to delete: "))
                delete_item(id_to_delete)
                print("Item deleted! Gone forever.")
            except ValueError:
                print("Bad ID.")
            input("\nPress Enter to continue...")
        elif choice == "5":
            print("Thank you! Goodbye")
            break
        else:
            print("Invalid choice! Try again.")
            input("\nPress Enter to continue...")

# entry point, fixed that typo from before
if __name__ == "__main__":
    print("Welcome to Simple Billing System")
    main()