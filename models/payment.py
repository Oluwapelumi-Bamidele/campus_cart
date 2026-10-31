"""
Polymorphic Payment Engine Module
Defines abstract payment interface and specialized settlement subclasses.
"""

from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Abstract Base Class establishing a uniform payment contract."""
    
    @abstractmethod
    def process_payment(self, amount: float) -> tuple[bool, str]:
        """Process payment of a given amount. Returns (success_bool, message_str)."""
        pass


class CashPayment(PaymentProcessor):
    """Handles physical cash transactions at checkout counter."""
    
    def process_payment(self, amount: float) -> tuple[bool, str]:
        if amount <= 0:
            return False, "Invalid cash amount tendered."
        return True, f"Successfully processed cash payment of ${amount:.2f}."


class CardPayment(PaymentProcessor):
    """Handles secure credit/debit card gateway transactions."""
    
    def __init__(self, card_number: str):
        self._card_masked = f"****-****-****-{card_number[-4:]}" if len(card_number) >= 4 else "****"

    def process_payment(self, amount: float) -> tuple[bool, str]:
        if amount <= 0:
            return False, "Invalid card charge amount."
        return True, f"Successfully charged ${amount:.2f} to card {self._card_masked} via secure gateway."


class MobileMoneyPayment(PaymentProcessor):
    """Handles mobile wallet/USSD transfers (e.g., MoMo, OPay, PalmPay)."""
    
    def __init__(self, phone_number: str, provider: str = "MobileMoney"):
        self._phone_number = phone_number
        self._provider = provider

    def process_payment(self, amount: float) -> tuple[bool, str]:
        if amount <= 0:
            return False, "Invalid mobile wallet amount."
        return True, f"Successfully debited ${amount:.2f} from {self._provider} account ({self._phone_number})."

# Run test code only when this file is executed directly
if __name__ == "__main__":
    print("--- Running Polymorphic Payment Engine Tests ---")

    # Sample payment processing amount
    order_amount = 45.50

    # Instantiate distinct payment strategy instances
    payment_methods: list[PaymentProcessor] = [
        CashPayment(),
        CardPayment("1234567890123456"),
        MobileMoneyPayment("08012345678", provider="OPay")
    ]

    # Polymorphically invoke process_payment() across all processors
    print(f"\nProcessing total checkout amount: ${order_amount:.2f}\n")
    for processor in payment_methods:
        success, message = processor.process_payment(order_amount)
        status = "SUCCESS" if success else "FAILED"
        print(f"[{status}] {processor.__class__.__name__}: {message}")

    print("\nPayment engine tests completed successfully!")