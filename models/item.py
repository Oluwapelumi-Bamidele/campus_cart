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

class PerishableItem(Item):
    """Specialized item that tracks expiration and shelf-life details."""
    def __init__(self, item_id, name, price, stock, expiration_date):
        super().__init__(item_id, name, price, stock)
        self._expiration_date = expiration_date

    @property
    def expiration_date(self):
        return self._expiration_date

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} [Exp: {self._expiration_date}]"


class DigitalVoucher(Item):
    """Specialized digital item with infinite stock redemption capabilities."""
    def __init__(self, item_id, name, price):
        # Stock is fixed to infinity or a very large sentinel for digital assets
        super().__init__(item_id, name, price, stock=999999)

    @property
    def stock(self):
        """Override stock getter to always report infinite availability."""
        return float('inf')

    @stock.setter
    def stock(self, new_stock):
        """Digital vouchers ignore physical stock reductions."""
        pass

    def __str__(self):
        return f"[Digital Voucher] {self.name} (ID: {self.item_id}) - ${self.price:.2f} [Unlimited Stock]"

if __name__ == "__main__":
    print("--- Running Item & Subclass Model Tests ---")

    # 1. Base Item
    notebook = Item("101", "Notebook", 2.50, 15)
    print(f"Base Item: {notebook}")

    # 2. Perishable Item
    milk = PerishableItem("201", "Fresh Milk", 3.50, 10, "2026-11-15")
    print(f"Perishable Item: {milk}")
    print(f"  - Expiration Date: {milk.expiration_date}")

    # 3. Digital Voucher (Infinite stock test)
    voucher = DigitalVoucher("301", "Campus Bookstore $10 Gift Card", 10.00)
    print(f"Digital Voucher: {voucher}")
    print(f"  - Initial Stock: {voucher.stock}")
    
    # Verify stock reduction is ignored
    voucher.stock -= 5
    print(f"  - Stock after attempting reduction: {voucher.stock}")

    print("\nAll Item model tests completed successfully!")