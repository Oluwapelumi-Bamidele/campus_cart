"""
Item Model Module 
Encapsulates product data and protects attributes using property decorators.
"""

class Item:
    def __init__(self, item_id, name, price, stock):
        self._item_id = str(item_id)
        self._name = name
        self._price = price
        self._stock = stock

    @property
    def item_id(self):
        """Get unique item ID."""
        return self._item_id

    @property
    def name(self):
        """Get product name."""
        return self._name

    @property
    def price(self):
        """Get unit price."""
        return self._price

    @price.setter
    def price(self, new_price):
        """Set unit price with validation."""
        if new_price >= 0:
            self._price = new_price
        else:
            raise ValueError("Price cannot be negative.")

    @property
    def stock(self):
        """Get available stock."""
        return self._stock

    @stock.setter
    def stock(self, new_stock):
        """Set available stock with validation."""
        if new_stock >= 0:
            self._stock = new_stock
        else:
            raise ValueError("Stock cannot be negative.")

    def __str__(self):
        return f"{self._name} (ID: {self._item_id}) - ${self._price:.2f} [Stock: {self._stock}]"
    
if __name__ == "__main__":
    print("--- Running Item Model Tests ---")

    # 1. Test Item Initialization and Property Getters
    notebook = Item("101", "Notebook", 2.50, 15)
    print(f"Created Item: {notebook}")
    print(f"  - ID: {notebook.item_id}")
    print(f"  - Name: {notebook.name}")
    print(f"  - Price: ${notebook.price:.2f}")
    print(f"  - Stock: {notebook.stock}")

    # 2. Test Property Setters (Valid updates)
    notebook.price = 3.00
    notebook.stock = 20
    print(f"\nAfter valid updates: {notebook}")

    # 3. Test Property Setters Validation (Negative values)
    print("\nTesting validation against negative values:")
    try:
        notebook.price = -1.00
    except ValueError as e:
        print(f"  [Caught Expected Error] Price setter: {e}")

    try:
        notebook.stock = -5
    except ValueError as e:
        print(f"  [Caught Expected Error] Stock setter: {e}")

    print("\nItem model tests completed successfully!")