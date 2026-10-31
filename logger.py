"""
A logger module that uses a decorator function to add logging to any transaction function
and records transaction details to a permanent text file.
"""

import datetime
import uuid
import os

def log_transaction(func):
    """
    A higher-order decorator function that intercepts checkout calls,
    counts existing logs in the file, generates transaction metadata,
    appends a record to 'transaction_log.txt', and displays execution details.
    """
    def wrapper(client_name, cart, *args, **kwargs):
        print("\nProcessing your payment...")
        
        # Count existing transaction records inside 'transaction_log.txt'
        existing_count = 0
        if os.path.exists("transaction_log.txt"):
            with open("transaction_log.txt", "r", encoding="utf-8") as file:
                content = file.read()
                existing_count = content.count("--- TRANSACTION RECORD ---")
        
        total_transactions = existing_count + 1
        
        # Execute the original checkout function -> returns (subtotal, final_total, purchased_goods)
        subtotal, final_total, purchased_goods = func(client_name, cart, *args, **kwargs)
        
        # Factor in discount (10% if subtotal > 20, else 0)
        discount_amount = subtotal * 0.10 if subtotal > 20 else 0.0
        discounted_subtotal = subtotal - discount_amount
        
        # Generate unique transaction metadata
        transaction_id = str(uuid.uuid4())[:8].upper()
        purchase_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        goods_str = ", ".join(purchased_goods)
        
        # Display the official receipt to the user
        print(f"\n==========================================")
        print(f"            OFFICIAL RECEIPT              ")
        print(f"==========================================")
        print(f" Client Name : {client_name}")
        print(f" Purchased Goods:")
        for item in cart:
            line_cost = item['price'] * item['quantity']
            print(f"   - {item['name']} (x{item['quantity']}) : ${line_cost:.2f}")
        print(f" ----------------------------------------")
        print(f" Subtotal (Original)       : ${subtotal:.2f}")
        if discount_amount > 0:
            print(f" Discount Applied (10%)    : -${discount_amount:.2f}")
            print(f" Subtotal (After Discount) : ${discounted_subtotal:.2f}")
        print(f" Final Amount Paid (Tax incl.) : ${final_total:.2f}")
        print(f"==========================================")
        
        # Construct the detailed log entry block for the text file
        log_entry = (
            f"--- TRANSACTION RECORD ---\n"
            f"Transaction ID      : {transaction_id}\n"
            f"Client Name         : {client_name}\n"
            f"Purchased Goods     : {goods_str}\n"
            f"Original Subtotal   : ${subtotal:.2f}\n"
            f"Discount Applied    : ${discount_amount:.2f}\n"
            f"Final Amount Paid   : ${final_total:.2f}\n"
            f"Time of Purchase    : {purchase_time}\n"
            f"--------------------------\n\n"
        )
        
        # Append the record to the text file
        with open("transaction_log.txt", "a", encoding="utf-8") as file:
            file.write(log_entry)
        
        # Display success summary
        print(f"Transaction ID {transaction_id} logged to 'transaction_log.txt'.")
        print(f"Transaction completed successfully! (Total logged transactions: {total_transactions})")
        
        return final_total
        
    return wrapper

def search_transaction_by_id(transaction_id):
    """
    Searches 'transaction_log.txt' for a specific transaction ID 
    and returns the complete transaction record if found.
    """
    if not os.path.exists("transaction_log.txt"):
        return False, "Error: No transaction log file found yet. No transactions have been recorded."
        
    with open("transaction_log.txt", "r", encoding="utf-8") as file:
        content = file.read()
        
    # Split records by the header delimiter
    records = content.split("--- TRANSACTION RECORD ---")
    
    target_id = transaction_id.strip().upper()
    for record in records:
        if not record.strip():
            continue
        if target_id in record.upper():
            full_record = "--- TRANSACTION RECORD ---" + record
            return True, full_record.strip()
            
    return False, f"Error: Transaction ID '{target_id}' was not found in the log."

# Run test code only when this file is executed directly
if __name__ == "__main__":
    print("========================================")
    print("        RUNNING LOGGER MODULE TESTS       ")
    print("========================================")

    # 1. Define a sample checkout function and wrap it with @log_transaction
    @log_transaction
    def sample_checkout(client_name, cart):
        # Calculate mock subtotal and final total (with 7.5% tax)
        subtotal = sum(item['price'] * item['quantity'] for item in cart)
        final_total = round(subtotal * 1.075, 2)
        purchased_goods = [f"{item['name']} (x{item['quantity']})" for item in cart]
        return subtotal, final_total, purchased_goods

    # 2. Prepare sample mock carts for testing
    cart_one = [
        {"name": "Notebook", "price": 2.50, "quantity": 2},
        {"name": "Campus Hoodie", "price": 25.00, "quantity": 1}
    ]
    
    cart_two = [
        {"name": "Sticky Notes", "price": 1.99, "quantity": 3}
    ]

    # 3. Test Test Checkout 1
    print("\n--- Test 1: Processing First Checkout ---")
    sample_checkout("Alice Smith", cart_one)

    # 4. Test Test Checkout 2 (Verifies incrementing total transaction count)
    print("\n--- Test 2: Processing Second Checkout ---")
    sample_checkout("Bob Johnson", cart_two)

    # 5. Test Transaction Search Functionality
    print("\n========================================")
    print("        TESTING TRANSACTION SEARCH        ")
    print("========================================")
    print("Open your 'transaction_log.txt' file, copy one of the Transaction IDs, and paste it below.")
    
    test_id = input("\nEnter Transaction ID to search (or press Enter to skip): ").strip()
    
    if test_id:
        found, result_message = search_transaction_by_id(test_id)
        if found:
            print("\n[Success] Transaction Found:")
            print("-" * 40)
            print(result_message)
            print("-" * 40)
        else:
            print(f"\n[{result_message}]")
    else:
        print("Skipped search test.")