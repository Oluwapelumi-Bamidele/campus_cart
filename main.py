'''Main Script for Campus Cart System'''

# Import helper functions from external custom modules
from inventory import (
    add_new_item,
    calc_price,
    check_stock,
    delete_item,
    display_low_stock_report,
    display_sorted_catalog,
    update_stock,
    verify_and_add_stock,
)
from cart import add_item, remove_item, calculate_subtotal, stream_receipt_lines
from logger import log_transaction, search_transaction_by_id


def initialize_inventory():
    # Define and return default items, prices, and available stock quantities
    return {
        "101": {"name": "Notebook", "price": 2.50, "stock": 15},
        "102": {"name": "Campus Hoodie", "price": 25.00, "stock": 4},
        "103": {"name": "Scientific Calculator", "price": 15.00, "stock": 8},
        "104": {"name": "Ballpoint Pens (10-pack)", "price": 4.75, "stock": 40},
        "105": {"name": "Highlighter Set", "price": 6.25, "stock": 22},
        "106": {"name": "Backpack", "price": 32.99, "stock": 6},
        "107": {"name": "USB Flash Drive 64GB", "price": 11.50, "stock": 18},
        "108": {"name": "Water Bottle", "price": 9.99, "stock": 12},
        "109": {"name": "Desk Lamp", "price": 19.95, "stock": 3},
        "110": {"name": "Sticky Notes", "price": 1.99, "stock": 55},
    }

@log_transaction
def checkout_order(client_name, cart):
    """
    Calculates the subtotal and final total (with discount/tax), returning them 
    to the @log_transaction decorator for official receipt generation and text logging.
    """
    subtotal = calculate_subtotal(cart)
    final_total = calc_price(subtotal, order_total=subtotal)
    purchased_goods = [f"{item['name']} (x{item['quantity']})" for item in cart]
    
    return subtotal, final_total, purchased_goods


def display_user_cart(cart):
    print("\n--- Your Shopping Cart ---")
    
    # Check if cart has items; exit function early if empty
    if not cart:
        print("Your cart is currently empty.")
        return
    
    # Print formatted table header
    print(f"{'ID':<6} | {'Item Name':<25} | {'Qty':<5} | {'Unit Price':<10} | {'Total':<10}")
    print("-" * 65)
    
    # Print each item line with calculated line totals
    for item in cart:
        item_id = item.get('item_id', 'N/A')
        total = item['price'] * item['quantity']
        print(f"{item_id:<6} | {item['name']:<25} | {item['quantity']:<5} | ${item['price']:<9.2f} | ${total:<9.2f}")
    print("-" * 65)


def clear_cart_and_restore_stock(cart, inventory):
    # Add back saved quantities to inventory stock before emptying cart
    for item in cart:
        if "item_id" in item and item["item_id"] in inventory:
            update_stock(inventory, item["item_id"], item["quantity"])
    cart.clear()

# USER MENU WORKFLOW

def user_menu(inventory, cart, client_name):
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

        # Option 1: Show product catalog sorted by price
        if choice == "1":
            print("\nSort option: 1. Low-to-High Price | 2. High-to-Low Price")
            sort_c = input("Select option (1-2): ").strip()
            display_sorted_catalog(inventory, ascending=(sort_c != "2"))

        # Option 2: Filter products by minimum stock threshold
        elif choice == "2":
            try:
                limit = int(input("Enter stock threshold limit: "))
                display_low_stock_report(inventory, limit)
            except ValueError:
                print("\n[Error] Invalid number input.")

        # Option 3: Add selected item to user cart
        elif choice == "3":
            display_sorted_catalog(inventory, ascending=True)
            item_id = input("\nEnter Item ID to add: ").strip()

            if item_id in inventory:
                item_data = inventory[item_id]
                available = item_data["stock"]
                if available > 0:
                    try:
                        qty = int(input(f"Enter quantity for '{item_data['name']}' (Available: {available}): "))
                        if 0 < qty <= available:
                            # Add item to cart and reduce available inventory stock
                            add_item(cart, item_data["name"], item_data["price"], quantity=qty, item_id=item_id)
                            update_stock(inventory, item_id, -qty)
                            print(f"\n[Success] Added {qty} x '{item_data['name']}' to cart!")
                        else:
                            print(f"\n[Error] Quantity must be between 1 and {available}.")
                    except ValueError:
                        print("\n[Error] Invalid number format.")
                else:
                    print(f"\n[Sorry] '{item_data['name']}' is out of stock.")
            else:
                print("\n[Error] Invalid Item ID.")

        # Option 4: Remove items or lower quantity from cart
        elif choice == "4":
            if not cart:
                print("\n[Notice] Cart is empty.")
            else:
                display_user_cart(cart)
                item_id = input("\nEnter Item ID to remove: ").strip()
                cart_item = next((i for i in cart if i.get("item_id") == item_id), None)
                
                if cart_item:
                    try:
                        rem_qty = int(input(f"Quantity to remove (Cart Qty: {cart_item['quantity']}): "))
                        if rem_qty > 0:
                            success, msg, qty_removed = remove_item(cart, item_id, rem_qty)
                            if success:
                                update_stock(inventory, item_id, qty_removed)
                                print(f"\n[Success] {msg}")
                            else:
                                print(f"\n[Error] {msg}")
                        else:
                            print("\n[Error] Please enter a valid positive number") 
                    except ValueError:
                        print("\n[Error] Invalid number.")
                else:
                    print("\n[Error] Item not in cart.")

        # Option 5: Display cart items and receipt preview
        elif choice == "5":
            display_user_cart(cart)
            if cart:
                print("\n--- Receipt Stream Preview ---")
                for line in stream_receipt_lines(cart):
                    print(f"  > {line}")

        # Option 6: Cancel cart order and restore store stock
        elif choice == "6":
            if not cart:
                print("\n[Notice] Your cart is already empty.")
            else:
                clear_cart_and_restore_stock(cart, inventory)
                print("\n[Success] Cart cleared! All reserved stock returned to inventory.")

        # Option 7: Process order payment and clear cart
        elif choice == "7":
            if not cart:
                print("\n[Notice] Cart is empty.")
            else:
                print("\n--- Pre-Checkout Receipt Preview ---")
                for line in stream_receipt_lines(cart):
                    print(f"  > {line}")
                
                confirm = input("\nProceed with payment? (y/n): ").strip().lower()
                if confirm == "y":
                    # Triggers @log_transaction decorator (displays official receipt, logs data to text file)
                    checkout_order(client_name, cart)
                    cart.clear()
                    print("\nThank you for your purchase! Returning to User Menu...")
                else:
                    print("\n[Payment Cancelled] Returning to User Menu. Items remain in your cart.")

        # Option 8: Exit user menu loop back to role selection
        elif choice == "8":
            print("\nReturning to Role Selection...")
            break

# ADMIN MENU WORKFLOW

def admin_menu(inventory):
    while True:
        print("\n==========================================")
        print("          ADMINISTRATOR PANEL             ")
        print("==========================================")
        print("1. View Full Catalog (Includes Stock & Unit Codes)")
        print("2. Check Stock Below Threshold Limit")
        print("3. Restock Item")
        print("4. Directly Modify Item Stock (Add/Remove)")
        print("5. Add Brand New Product to Catalog")
        print("6. Delete Item from Catalog")
        print("7. Search Transaction Record by ID")
        print("8. Return to Role Selection / Main Interface")
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
                if add_qty > 0:
                    success, msg = verify_and_add_stock(inventory, item_id, add_qty)
                    print(f"\n[{'Success' if success else 'Error'}] {msg}")
                else:
                    print("\n[Error] Quantity must be greater than 0.")
            except ValueError:
                print("\n[Error] Invalid quantity input.")
        elif choice == "4":
            display_sorted_catalog(inventory, ascending=True)
            item_id = input("\nEnter Item ID to modify: ").strip()
            if item_id in inventory:
                item = inventory[item_id]
                print(f"Selected: {item['name']} | Current Stock: {item['stock']}")
                try:
                    change = int(input("Enter quantity change (Positive to add, Negative to remove e.g., +5 or -3): "))
                    success, result = update_stock(inventory, item_id, change)
                    if success:
                        print(f"\n[Success] Updated stock for '{item['name']}'. New Stock: {result}")
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
                print("\n[Error] Invalid numerical inputs for price or stock.")
        elif choice == "6":
            display_sorted_catalog(inventory, ascending=True)
            item_id = input("\nEnter Item ID to delete from stock: ").strip()
            confirm = input(f"Are you sure you want to permanently delete Item {item_id}? (y/n): ").strip().lower()
            if confirm == "y":
                success, msg = delete_item(inventory, item_id)
                print(f"\n[{'Success' if success else 'Error'}] {msg}")
        elif choice == "7":
            print("\n==========================================")
            print("       SEARCH TRANSACTION RECORD          ")
            print("==========================================")
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
            print("\nReturning to Role Selection Interface...")
            break
        elif choice == "9":
            print("\nExiting Campus Cart System. Goodbye!")
            exit()
        else:
            print("\n[Error] Invalid selection. Choose between 1 and 9.")