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
