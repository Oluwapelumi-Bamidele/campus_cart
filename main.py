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