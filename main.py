"""
CampusCart CLI Application
Author: Bamidele Oluwapelumi Adeleke
Description: An interactive procedural CLI tools for managing a CampusCart using variables,
    conditional loops, dictionaries, and list structures.
"""


#phase 2: data structures design
#catalogue dictionary structure and active shooping cart list
inventory = {
    "101": {"name": "40 leaves notebook", "price": 2.50, "stock": 150},
    "102": {"name": "80 leaves notebook", "price": 4.50, "stock": 150},
    "103": {"name": "Pen Packs", "price": 5, "stock": 100},
    "104": {"name": "school bags", "price": 7.5, "stock": 50},
    "105": {"name": "Food Flasks", "price": 10, "stock": 30},
    "106": {"name": "school uniform", "price": 10, "stock": 230},
    "107": {"name": "lamp", "price": 2.7, "stock": 250},
    "108": {"name": "shoe", "price": 8, "stock": 150},
    "109": {"name": "water bottle", "price": 4.9, "stock": 150},
    "110": {"name": "laptop", "price": 50, "stock": 300}
    }

while True:
    # Display Welcome Banner and input
    print("=" * 40)
    print("     WELCOME TO CAMPUSCART CLI SYSTEM     ")
    print("=" * 40)
    
    user_action = input("Enter 'ok' to proceed or anykey to stop: ").upper()
    if user_action != 'ok'.upper():
        break

    user_name = input("Enter your name to start: ").strip().title()
    print(f"\nHello, {user_name}! System initialized successfully.\n")

    cart = []

    print("\n--- Goods ready ---")
    print(f"Catalogue loaded with {len(inventory)} products.")
    print(f"initial cart state: {cart}\n")

    #main execution loop and menu branching
    while True:
        print("\n" + "=" * 35)
        print("        CAMPUS CART MAIN MENU        ")
        print("=" * 35)
        print("1. view Catalog")
        print("2. Add Item to Cart")
        print("3. View Cart")
        print("4. Checkout & Exit")
        print("=" * 35)

        choice = input("\nselect an option (1-4): ").strip()
        
        if choice == "1":
            #catalog view
            print("\n" + "-" * 50)
            print("        PRODUCT CATALOG VIEW       ")
            print("-" * 50 + "\n")
            print(f"{'ID':<6} | {'Item Name':<20} | {'Price':<8} | {'Stock':<6}")
            print("-" * 50)
            for item_id, item_data in inventory.items():
                print(f"{item_id:<6} | {item_data['name']:<20} | ${item_data['price']:<7.2f} | {item_data['stock']:<6}")
                
        elif choice == "2":
            # cart seletion
            print("\n" + "-" * 50)
            print("        ADD TO CART        ")
            print("-" * 50 + "\n")
            item_id = input("Enter product ID: ").strip()
            
            #verifying product exist in catalog
            if item_id in inventory:
                product = inventory[item_id]
                
                qty_in_cart = sum(item["qty"] for item in cart if item["id"] == item_id)
                available_stock = product['stock']
                
                print(f"Selected: {product['name']} (Available Stock: {available_stock})")
                
                qty_input = input("Enter quantity to add: ").strip()
                
                #verify quantity is positive integer and stock validation
                if qty_input.isdigit() and int(qty_input) > 0:
                    req_qty = int(qty_input)
                    if req_qty <= available_stock:
                        subtotal = req_qty * product['price']
                        
                        product['stock'] -= req_qty
                        
                        #update existing cart item
                        existing_item = next((item for item in cart if item["id"] == item_id), None)
                        if existing_item:
                            existing_item["qty"] += req_qty
                            existing_item["subtotal"] += subtotal
                        else:
                        #Add item requested into cart list
                            cart.append({
                                "id": item_id,
                                "name": product["name"],
                                "qty": req_qty,
                                "price": product["price"],
                                "subtotal": subtotal
                                })
                            print(f"SUCCESS: Added {req_qty} * '{product['name']}' to your cart!")
                    else:
                        print(f"ERROR: Insufficient stock! Only {available_stock} available")
                else:
                    print(f"ERROR: Invalid quantity! please enter a positive integer.")
            else:
                print(f"ERROR: Product ID not found in inventory!")
                

        elif choice == "3":
            #current cart display
            print("\n" + "-" * 50)
            print("        YOUR SHOPPING CART        ")
            print("-" * 50 + "\n")
            if not cart:
                print(f"Your cart is currently empty")
            else:
                print(f"{'Item Name':<20} | {'qty':<6} | {'Price':<8} | {'subtotal':<8}")
                print("-" * 42)
                total = 0.0
                for line_item in cart:
                    print(f"{line_item['name']:<20} | {line_item['qty']:<6} | ${line_item['price']:<7.2f} | ${line_item['subtotal']:7.2f}")
                    total += line_item['subtotal']
                print("-" * 42)
                print(f"Current Total: ${total:.2f}")
                
        elif choice == "4":
            #checkout and exit route
            print("\n" + "-" * 50)
            print("        PROCESSING CHECKOUT        ")
            print("-" * 50 + "\n")
            if not cart:
                print("Cart is empty. Exiting application. Have a great day!\n")
                break
            else: 
                #Calculate Grand Subtotal
                raw_total = sum(item["subtotal"] for item in cart)
            
                #discount (10% off orders over $20)
                discount = 0.0
                if raw_total > 20.0:
                    discount = raw_total * 0.10
                
                final_total = raw_total - discount
            
                #Deduct stock counts from inventory
               # for item in cart:
                #    inventory[item["id"]]["stock"] -= item["qty"]
                
                #Print Receipt
                print("\n" + "*" * 40)
                print("        OFFICIAL RECEIPT        ")
                print("*" * 40)
                for item in cart:
                    print(f"{item['name']:<20} * {item['qty']:<3}  ${item['subtotal']:>8.2f}")
                print("-" * 40)
                print(f"{'subtotal:':<25} ${raw_total:>8.2f}")
                if discount > 0:
                    print(f"{'Discount (10% over $20):':<24} -${discount:>7.2f}")
                print("_" * 40)
                print(f"{'Grand Total:':<25} ${final_total:>8.2f}")
                print("*" * 40)
                print("        Thank you for using CampusCart!        \n")
            
                #clearing cart
                cart.clear()
                print("cart cleared. Returning to menu\n")
                break
            
        else:
            #user error handling
            print("\nInvalid selection! Please enter a number between 1 and 4.")
