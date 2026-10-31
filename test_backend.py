"""
Phase 4 Backend Verification Test Script
Tests full integration of OOP models, subclasses, polymorphic payments, and loggers.
"""

from models.item import Item, PerishableItem, DigitalVoucher
from models.cart import ShoppingCart
from models.payment import CashPayment, CardPayment, MobileMoneyPayment
from utils.logger import log_transaction, search_transaction_by_id
from inventory import calc_price

print("========================================")
print("    PHASE 4: BACKEND INTEGRATION TEST   ")
print("========================================")

# 1. Setup inventory with base and specialized items
milk = PerishableItem("201", "Fresh Milk", 3.50, stock=10, expiration_date="2026-11-15")
voucher = DigitalVoucher("301", "Campus Gift Card", 20.00)

cart = ShoppingCart()

# 2. Add items to cart (tests stock bounds & infinite stock override)
print("\n[1] Adding items to cart...")
cart.add_item(milk, quantity=2)
cart.add_item(voucher, quantity=5) # Should handle unlimited stock smoothly

# 3. Define checkout function wrapped with @log_transaction
@log_transaction
def process_store_checkout(client_name, cart_obj, payment_processor):
    subtotal = cart_obj.calculate_subtotal()
    final_total = calc_price(subtotal, order_total=subtotal)
    
    # Polymorphic payment execution
    success, msg = payment_processor.process_payment(final_total)
    if not success:
        raise Exception(msg)
    print(f"  > {msg}")

    purchased_goods = [f"{e['item'].name} (x{e['quantity']})" for e in cart_obj.items]
    return subtotal, final_total, purchased_goods

# 4. Test checkout using a polymorphic Mobile Money payment
print("\n[2] Executing checkout with Mobile Money Payment...")
momo_processor = MobileMoneyPayment("08098765432", provider="OPay")
process_store_checkout("Oluwapelumi Bamidele", cart, momo_processor)

print("\nPhase 4 backend verification script executed successfully!")