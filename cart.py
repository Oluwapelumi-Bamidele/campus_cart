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


def stream_receipt_lines(cart):
    """Steams receipt"""
    # Yield formatted line items one by one
    for item in cart:
        total_price = item["price"] * item["quantity"]
        yield f"{item['name']} (x{item['quantity']}) - ${total_price:.2f}"
    # Yield the final subtotal line
    yield f"Subtotal: ${calculate_subtotal(cart):.2f}"



# Run test code only when this file is executed directly
if __name__ == "__main__":
    print("--- Running Cart Engine Tests ---")

    # Initialize empty cart
    test_cart = []

    # 1. Test adding items
    add_item(test_cart, name="Notebook", price=2.50, quantity=2, item_id="101")
    add_item(test_cart, name="Campus Hoodie", price=25.00, quantity=1, item_id="102")
    # Adding more of an existing item
    add_item(test_cart, name="Notebook", price=2.50, quantity=1, item_id="101")

    print("\nCart items after additions:")
    for item in test_cart:
        print(f"  - {item['name']}: Qty {item['quantity']} @ ${item['price']} each")

    # 2. Test subtotal calculation
    subtotal = calculate_subtotal(test_cart)
    print(f"\nCalculated Subtotal: ${subtotal:.2f}")

    # 3. Test streaming receipt lines
    print("\nReceipt Lines Preview:")
    for line in stream_receipt_lines(test_cart):
        print(f"  > {line}")

    # 4. Test partial item removal
    print("\nRemoving 1 Notebook:")
    success, message, removed_qty = remove_item(test_cart, item_id="101", quantity_to_remove=1)
    print(f"  Result: {message}")

    # 5. Test removing full item quantity
    print("\nRemoving Campus Hoodie entirely:")
    success, message, removed_qty = remove_item(test_cart, item_id="102", quantity_to_remove=1)
    print(f"  Result: {message}")

    print("\nFinal Cart State:")
    print(test_cart)