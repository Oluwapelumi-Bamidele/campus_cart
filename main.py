"""Main Script for Campus Cart System (OOP Phase 2 Refactored)"""

from models.item import Item
from models.cart import ShoppingCart
from inventory import (
    add_new_item,
    calc_price,
    delete_item,
    display_low_stock_report,
    display_sorted_catalog,
    update_stock,
    verify_and_add_stock,
    )
from utils.logger import log_transaction, search_transaction_by_id


def initialize_inventory():
    """Populates initial catalog with Item objects."""
    raw_data = [
        ("101", "Notebook", 2.50, 15),
        ("102", "Campus Hoodie", 25.00, 4),
        ("103", "Scientific Calculator", 15.00, 8),
        ("104", "Ballpoint Pens (10-pack)", 4.75, 40),
        ("105", "Highlighter Set", 6.25, 22),
        ("106", "Backpack", 32.99, 6),
        ("107", "USB Flash Drive 64GB", 11.50, 18),
        ("108", "Water Bottle", 9.99, 12),
        ("109", "Desk Lamp", 19.95, 3),
        ("110", "Sticky Notes", 1.99, 55),
    ]
    return {item_id: Item(item_id, name, price, stock) for item_id, name, price, stock in raw_data}

@log_transaction
def checkout_order(client_name, cart_obj):
    """Calculates final totals and passes to logger decorator."""
    subtotal = cart_obj.calculate_subtotal()
    final_total = calc_price(subtotal, order_total=subtotal)
    purchased_goods = [f"{entry['item'].name} (x{entry['quantity']})" for entry in cart_obj.items]
    return subtotal, final_total, purchased_goods

def display_user_cart(cart_obj):
    print("\n--- Your Shopping Cart ---")
    if not cart_obj.items:
        print("Your cart is currently empty.")
        return
    
    print(f"{'ID':<6} | {'Item Name':<25} | {'Qty':<5} | {'Unit Price':<10} | {'Total':<10}")
    print("-" * 65)
    for entry in cart_obj.items:
        item = entry["item"]
        qty = entry["quantity"]
        total = item.price * qty
        print(f"{item.item_id:<6} | {item.name:<25} | {qty:<5} | ${item.price:<9.2f} | ${total:<9.2f}")
    print("-" * 65)


# USER MENU WORKFLOW

def user_menu(inventory, cart_obj, client_name):
    # Keep showing user menu until user decides to go back
    while True:
        print(f"\n==========================================")
        print(f"        USER MAIN MENU (Welcome, {client_name})")
        print("==========================================")
        print("1. View Product Catalog")
        print("2. Search / Check Low Stock Items")
        print("3. Add Item to Cart")
        print("4. Remove Item from Cart")
        print("5. View Cart & Stream Receipt")
        print("6. Clear Cart")
        print("7. Checkout & Complete Order")
        print("8. Switch Role / Return to Main Landing")

        choice = input("\nEnter choice (1-8): ").strip()

        if choice == "1":
            print("\nSort option: 1. Low-to-High Price | 2. High-to-Low Price")
            sort_c = input("Select option (1-2): ").strip()
            display_sorted_catalog(inventory, ascending=(sort_c != "2"))

        elif choice == "2":
            try:
                limit = int(input("Enter stock threshold limit: "))
                display_low_stock_report(inventory, limit)
            except ValueError:
                print("\n[Error] Invalid number input.")

        elif choice == "3":
            display_sorted_catalog(inventory, ascending=True)
            item_id = input("\nEnter Item ID to add: ").strip()

            if item_id in inventory:
                item_obj = inventory[item_id]
                if item_obj.stock > 0:
                    try:
                        qty = int(input(f"Enter quantity for '{item_obj.name}' (Available: {item_obj.stock}): "))
                        success, msg = cart_obj.add_item(item_obj, quantity=qty)
                        print(f"\n[{'Success' if success else 'Error'}] {msg}")
                    except ValueError:
                        print("\n[Error] Invalid number format.")
                else:
                    print(f"\n[Sorry] '{item_obj.name}' is out of stock.")
            else:
                print("\n[Error] Invalid Item ID.")

        elif choice == "4":
            if not cart_obj.items:
                print("\n[Notice] Cart is empty.")
            else:
                display_user_cart(cart_obj)
                item_id = input("\nEnter Item ID to remove: ").strip()
                entry = next((e for e in cart_obj.items if e["item"].item_id == item_id), None)
                
                if entry:
                    try:
                        rem_qty = int(input(f"Quantity to remove (Cart Qty: {entry['quantity']}): "))
                        success, msg, _ = cart_obj.remove_item(item_id, rem_qty)
                        print(f"\n[{'Success' if success else 'Error'}] {msg}")
                    except ValueError:
                        print("\n[Error] Invalid number.")
                else:
                    print("\n[Error] Item not in cart.")

        elif choice == "5":
            display_user_cart(cart_obj)
            if cart_obj.items:
                print("\n--- Receipt Stream Preview ---")
                for line in cart_obj.stream_receipt_lines():
                    print(f"  > {line}")

        elif choice == "6":
            if not cart_obj.items:
                print("\n[Notice] Your cart is already empty.")
            else:
                cart_obj.clear()
                print("\n[Success] Cart cleared! All reserved stock returned to inventory.")

        elif choice == "7":
            if not cart_obj.items:
                print("\n[Notice] Cart is empty.")
            else:
                print("\n--- Pre-Checkout Receipt Preview ---")
                for line in cart_obj.stream_receipt_lines():
                    print(f"  > {line}")
                
                confirm = input("\nProceed with payment? (y/n): ").strip().lower()
                if confirm == "y":
                    checkout_order(client_name, cart_obj)
                    cart_obj.items.clear()  # Clear items post payment
                    print("\nThank you for your purchase! Returning to User Menu...")
                else:
                    print("\n[Payment Cancelled] Returning to User Menu.")

        elif choice == "8":
            print("\nReturning to Role Selection...")
            break

# ADMIN MENU WORKFLOW

def admin_menu(inventory):
    while True:
        print("\n==========================================")
        print("          ADMINISTRATOR PANEL             ")
        print("==========================================")
        print("1. View Full Catalog")
        print("2. Check Stock Below Threshold Limit")
        print("3. Restock Item")
        print("4. Directly Modify Item Stock")
        print("5. Add Brand New Product to Catalog")
        print("6. Delete Item from Catalog")
        print("7. Search Transaction Record by ID")
        print("8. Return to Role Selection")
        print("9. Exit Application Entirely")

        choice = input("\nEnter choice (1-9): ").strip()

        if choice == "1":
            display_sorted_catalog(inventory, ascending=True)
        elif choice == "2":
            try:
                limit = int(input("Enter stock threshold limit: "))
                display_low_stock_report(inventory, limit)
            except ValueError:
                print("\n[Error] Invalid threshold input.")
        elif choice == "3":
            display_sorted_catalog(inventory, ascending=True)
            item_id = input("\nEnter Item ID to restock: ").strip()
            try:
                add_qty = int(input("Enter quantity to add to stock: "))
                success, msg = verify_and_add_stock(inventory, item_id, add_qty)
                print(f"\n[{'Success' if success else 'Error'}] {msg}")
            except ValueError:
                print("\n[Error] Invalid quantity input.")
        elif choice == "4":
            display_sorted_catalog(inventory, ascending=True)
            item_id = input("\nEnter Item ID to modify: ").strip()
            if item_id in inventory:
                item = inventory[item_id]
                print(f"Selected: {item.name} | Current Stock: {item.stock}")
                try:
                    change = int(input("Enter quantity change (+5 or -3): "))
                    success, result = update_stock(inventory, item_id, change)
                    if success:
                        print(f"\n[Success] Updated stock for '{item.name}'. New Stock: {result}")
                    else:
                        print(f"\n[{result}]")
                except ValueError:
                    print("\n[Error] Invalid number input.")
            else:
                print("\n[Error] Item ID not found.")
        elif choice == "5":
            item_id = input("Enter new Item ID: ").strip()
            name = input("Enter Item Name: ").strip()
            try:
                price = float(input("Enter Price ($): "))
                stock = int(input("Enter Initial Stock Quantity: "))
                success, msg = add_new_item(inventory, item_id, name, price, stock)
                print(f"\n[{'Success' if success else 'Error'}] {msg}")
            except ValueError:
                print("\n[Error] Invalid numerical inputs.")
        elif choice == "6":
            display_sorted_catalog(inventory, ascending=True)
            item_id = input("\nEnter Item ID to delete from stock: ").strip()
            confirm = input(f"Are you sure you want to permanently delete Item {item_id}? (y/n): ").strip().lower()
            if confirm == "y":
                success, msg = delete_item(inventory, item_id)
                print(f"\n[{'Success' if success else 'Error'}] {msg}")
        elif choice == "7":
            tx_id = input("Enter Transaction ID (e.g., A9F321BC): ").strip()
            success, result_msg = search_transaction_by_id(tx_id)
            if success:
                print("\n[Found Transaction Record]")
                print("-" * 40)
                print(result_msg)
                print("-" * 40)
            else:
                print(f"\n[{result_msg}]")
        elif choice == "8":
            break
        elif choice == "9":
            print("\nExiting Campus Cart System. Goodbye!")
            exit()

def main():
    inventory = initialize_inventory()
    cart_obj = ShoppingCart()

    while True:
        print("\n==================================================")
        print("    WELCOME TO CAMPUS CART STUDENT STORE SYSTEM   ")
        print("==================================================")
        print("1. User / Student Interface")
        print("2. Administrator Interface")
        print("3. Exit System")

        role_choice = input("\nSelect Option (1-3): ").strip()

        if role_choice == "1":
            client_name = input("\nEnter your Name (Student/Client): ").strip()
            if not client_name:
                client_name = "Guest Student"
            user_menu(inventory, cart_obj, client_name)
        elif role_choice == "2":
            admin_menu(inventory)
        elif role_choice == "3":
            print("\nThank you for using Campus Cart!")
            break

if __name__ == "__main__":
    main()