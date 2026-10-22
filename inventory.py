"""
Inventory Engine Module

Provides tools for managing product inventory levels, calculating pricing,
filtering stock levels, displaying reports, and administrative management.
"""

def check_stock(inventory, item_id):
    """Check and return the current stock count for a specific item.
    
    Args:
        inventory (dict): The main inventory data structure.
        item_id (str): The unique identifier of the product.
        
    Returns:
        int: The stock count if found, otherwise 0.
    """
    if item_id in inventory:
        return inventory[item_id]["stock"]
    return 0

def update_stock(inventory, item_id, qty_change):
    """Modify an item's stock level by a given quantity change.
    
    Args:
        inventory (dict): The main inventory data structure.
        item_id (str): The unique identifier of the product.
        qty_change (int): Positive to add stock, negative to reduce stock.
        
    Returns:
        tuple: (bool, int or str) Success status and remaining stock or error message.
    """
    if item_id in inventory:
        current_stock = inventory[item_id]["stock"]
        new_stock = current_stock + qty_change
        
        # Ensure stock does not drop below zero
        if new_stock >= 0:
            inventory[item_id]["stock"] = new_stock
            return True, inventory[item_id]["stock"]
        return False, "Error: Requested quantity exceeds available stock."
    return False, "Error: Item ID not found."

def verify_and_add_stock(inventory, item_id, add_qty):
    """Verify item existence and add a specific quantity to its stock.
    
    Args:
        inventory (dict): The main inventory data structure.
        item_id (str): The unique identifier of the product.
        add_qty (int): The positive quantity to add.
        
    Returns:
        tuple: (bool, str) Success status and status message.
    """
    if item_id not in inventory:
        return False, "Error: Item ID not found in inventory."
    
    # Increase stock count by the added quantity
    inventory[item_id]["stock"] += add_qty
    return True, f"Successfully added {add_qty} units! New stock: {inventory[item_id]['stock']}"