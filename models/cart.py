"""
ShoppingCart Model Module 
Manages cart items, quantity updates, stock adjustments, and receipt streaming.
"""

class ShoppingCart:
    def __init__(self):
        self._items = [] # List of dicts: [{"item": Item instance, "quantity": int}]

    @property
    def items(self):
        """Return items currently in cart"""
        return self._items
    
    def add_item(self, item_obj, quantity=1):
        """Adds Item instance to cart and reduces available stock"""
        if quantity <= 0:
            return False, "quantity must be greater than zero"

        if item_obj.stock < quantity:
            return False, f"Insufficient stock. Available: {item_obj.stock}"
    
        # Check if the item is already in the cart
        for entry in self._items:
            if entry["item"].item_id == item_obj.item_id:
                entry["quantity"] += quantity
                item_obj.stock -= quantity
                return True, f"Updated quantity for '{item_obj.name}'."

        # Add a new item entry
        self._items.append({"item": item_obj, "quantity": quantity})
        item_obj.stock -= quantity
        return True, f"Added {quantity} x '{item_obj.name}' to cart."


    def remove_item(self, item_id, quantity_to_remove):
        """Removes specified quantity from cart and restores item stock."""
        for entry in self._items:
            item_obj = entry["item"]
            if item_obj.item_id == item_id:
                current_qty = entry["quantity"]

                if quantity_to_remove > current_qty:
                    return False, f"You only have {current_qty} in your cart.", 0

                if quantity_to_remove == current_qty:
                    self._items.remove(entry)
                    item_obj.stock += quantity_to_remove
                    return True, f"Removed all '{item_obj.name}' from cart.", quantity_to_remove
                else:
                    entry["quantity"] -= quantity_to_remove
                    item_obj.stock += quantity_to_remove
                    return True, f"Removed {quantity_to_remove} of '{item_obj.name}'.", quantity_to_remove

        return False, "Item not found in your cart.", 0

    def calculate_subtotal(self):
        """Calculates total price of items in cart."""
        return sum(entry["item"].price * entry["quantity"] for entry in self._items)

    def stream_receipt_lines(self):
        """Steams receipt"""
        # Yield receipt lines one by one
        for entry in self._items:
            item = entry["item"]
            qty = entry["quantity"]
            line_total = item.price * qty
            yield f"{item.name} (x{qty}) - ${line_total:.2f}"
        yield f"Subtotal: ${self.calculate_subtotal():.2f}"

    def clear(self):
        """Clears cart and restores all quantities back to item stock."""
        for entry in self._items:
            entry["item"].stock += entry["quantity"]
        self._items.clear()



# Run test code only when this file is executed directly
# Run test code only when this file is executed directly
if __name__ == "__main__":
    print("--- Running Cart Engine Tests ---")

    # Import Item model for testing
    from item import Item

    # Initialize sample items and cart object
    item1 = Item("101", "Notebook", 2.50, stock=10)
    item2 = Item("102", "Campus Hoodie", 25.00, stock=5)
    
    test_cart = ShoppingCart()

    # 1. Test adding items
    success, msg = test_cart.add_item(item1, quantity=2)
    print(f"Add 1: {msg}")
    
    success, msg = test_cart.add_item(item2, quantity=1)
    print(f"Add 2: {msg}")
    
    # Adding more of an existing item
    success, msg = test_cart.add_item(item1, quantity=1)
    print(f"Add 3: {msg}")

    print("\nCart items after additions:")
    for entry in test_cart.items:
        print(f"  - {entry['item'].name}: Qty {entry['quantity']} @ ${entry['item'].price} each")

    # 2. Test subtotal calculation
    subtotal = test_cart.calculate_subtotal()
    print(f"\nCalculated Subtotal: ${subtotal:.2f}")

    # 3. Test streaming receipt lines
    print("\nReceipt Lines Preview:")
    for line in test_cart.stream_receipt_lines():
        print(f"  > {line}")

    # 4. Test partial item removal
    print("\nRemoving 1 Notebook:")
    success, message, removed_qty = test_cart.remove_item(item_id="101", quantity_to_remove=1)
    print(f"  Result: {message}")

    # 5. Test removing full item quantity
    print("\nRemoving Campus Hoodie entirely:")
    success, message, removed_qty = test_cart.remove_item(item_id="102", quantity_to_remove=1)
    print(f"  Result: {message}")

    print("\nFinal Cart State:")
    for entry in test_cart.items:
        print(f"  - {entry['item'].name}: Qty {entry['quantity']}")