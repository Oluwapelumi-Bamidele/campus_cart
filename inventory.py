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

def add_new_item(inventory, item_id, name, price, stock):
    """Register a new product entry into the inventory catalog.
    
    Args:
        inventory (dict): The main inventory data structure.
        item_id (str): A unique product identifier.
        name (str): Product name.
        price (float): Unit price.
        stock (int): Initial stock quantity.
        
    Returns:
        tuple: (bool, str) Success status and descriptive message.
    """
    if item_id in inventory:
        return False, "Error: An item with this ID already exists."
    
    # Add new product entry to inventory dictionary
    inventory[item_id] = {
        "name": name,
        "price": price,
        "stock": stock,
    }
    return True, f"Successfully added '{name}' (ID: {item_id}) to inventory!"

def delete_item(inventory, item_id):
    """Remove an item from the inventory catalog entirely.
    
    Args:
        inventory (dict): The main inventory data structure.
        item_id (str): The unique identifier of the product to remove.
        
    Returns:
        tuple: (bool, str) Success status and removal confirmation message.
    """
    if item_id in inventory:
        removed_item = inventory.pop(item_id)
        return True, f"Successfully removed '{removed_item['name']}' from inventory."
    return False, "Error: Item ID not found."

def calc_price(base_price, tax_rate=0.075, order_total=0.0):
    """Calculate the final price of an item including conditional discounts and taxes.
    
    Args:
        base_price (float): Original unit price.
        tax_rate (float): Applicable tax rate (default is 7.5%).
        order_total (float): Total order amount used for discount eligibility.
        
    Returns:
        float: Final calculated price rounded to two decimal places.
    """
    # Apply 10% discount if order total exceeds $20
    discount = 0.10 if order_total > 20 else 0.0
    discounted_price = base_price * (1 - discount)
    
    # Calculate tax and round to two decimal places
    final_price = discounted_price * (1 + tax_rate)
    return round(final_price, 2)