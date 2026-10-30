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