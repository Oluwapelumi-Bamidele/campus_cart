"""
Cart Module

Manages cart operations, item quantities, receipt streaming, and cart sub-totals.
"""
def add_item(cart, name, price, quantity=1, item_id=None):
    """Adds Item to cart"""
    # Check if the item is already in the cart
    for item in cart:
        if item.get("item_id") == item_id or item["name"] == name:
            # Increase the quantity if found
            item["quantity"] += quantity
            return cart

    # Add a new item dictionary to the cart list if not found
    cart.append({
        "item_id": item_id,
        "name": name,
        "price": price,
        "quantity": quantity
    })
    return cart


def remove_item(cart, item_id, quantity_to_remove):
    """Removes items from cart"""
    # Find the target item in the cart using its ID
    for item in cart:
        if item.get("item_id") == item_id:
            current_qty = item["quantity"]

            # Case 1: Cannot remove more items than are currently in the cart
            if quantity_to_remove > current_qty:
                return False, f"You only have {current_qty} in your cart.", 0

            # Case 2: If removing the full quantity, delete the item from the cart entirely
            if quantity_to_remove == current_qty:
                cart.remove(item)
                return True, f"Removed all '{item['name']}' from cart.", quantity_to_remove
            # Case 3: Reduce the item quantity by the requested amount
            else:
                item["quantity"] -= quantity_to_remove
                return True, f"Removed {quantity_to_remove} of '{item['name']}'.", quantity_to_remove

    # Return error if the ID was not found in the cart
    return False, "Item not found in your cart.", 0



def calculate_subtotal(cart):
    """Calculates subtotal"""
    # Multiply price by quantity for every item and sum them up
    return sum(item["price"] * item["quantity"] for item in cart)
