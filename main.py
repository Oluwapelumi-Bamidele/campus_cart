"""
PROGRAM SCOPE: An interactive procedural CLI tool for CampusCart.

Author: Oluatomisin Tomoloju
Description: A CLI tool for CampusCart using conditional, loops, dictionaries and list.

"""

import os


ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

# Inventory
inventory = {
    "101": { "name": "Notebook", "price": 2.50, "stock": 15 },
    "102": { "name": "Ballpoint Pen", "price": 1.20, "stock": 50 },
    "103": { "name": "Mechanical Pencil", "price": 3.00, "stock": 30 },
    "104": { "name": "Highlighter Set", "price": 4.50, "stock": 20 },
    "105": { "name": "Sticky Note", "price": 1.80, "stock": 45 },
    "106": { "name": "Paperclips Pack", "price": 0.99, "stock": 100 },
    "107": { "name": "Three-Ring Binder", "price": 5.25, "stock": 12 },
    "108": { "name": "Scissors", "price": 3.50, "stock": 25 },
    "109": { "name": "Glue Stick", "price": 1.10, "stock": 60 },
    "110": { "name": "Stapler", "price": 8.75, "stock": 8 }
}


cart_list = []

def message_box(message):
    '''Message Wrapper'''
    print()
    print("="*20)
    print()
    print(message)
    print()
    print("="*20)
    print()

def admin_auth():
    '''Authenticates Admnin Login'''
    if  not ADMIN_PASSWORD:
        message_box("ADMIN PASSWORD NOT SET")
        print("Set the ADMIN_PASSWORD environment variable and restart the app.")
        print("See the README for instructions.")
        return False
    entered = input("Admin password: ")
    if entered != ADMIN_PASSWORD:
        message_box("ACCESS DENIED! Wrong Password")
        return
    message_box("Welcome back, Admin")
    return True



# ASCII Function
def box(text, padding=2):
    '''Box function'''
    length = len(text) + (padding * 2)
    print("+" + "-" * length + "+")
    print("|" + " " * length + "|")
    print(f"|{' ' * padding}{text}{' ' * padding}|")
    print("|" + " " * length + "|")
    print("+" + "-" * length + "+")

# ADMIN SECTION

# Inventory Management Function
def manage_inventory():
    '''Manages the inventory'''
    while True:
        message_box("INVENTORY MANAGEMENT CENTER")
        print("1 = Update product price")
        print("2 = Update product stock")
        print("3 = Add new product")
        print("0 = Return to main menu")
        print()

        option = input("Enter an option: ").strip()

        # Update price
        if option == "1":
            product_id = input("Enter the product ID: ").strip()

            if product_id in inventory:
                print(f"Current product: {inventory[product_id]['name']}")
                print(f"Current price: ${inventory[product_id]['price']:.2f}")

                price_input = input("Enter the new price: $").strip()

                if price_input.replace(".", "", 1).isdigit():
                    new_price = float(price_input)

                    if new_price <= 0:
                        print("The price must be greater than zero.")
                    else:
                        inventory[product_id]["price"] = new_price
                        message_box("Price updated successfully.")
                else:
                    message_box("Invalid price. Please enter a number.")
            else:
                message_box("Product ID not found.")


        # Update Stock
        elif option == "2":
            product_id = input("Enter the product ID: ").strip()

            if product_id in inventory:
                print(f"Current product: {inventory[product_id]['name']}")
                print(f"Current stock: {inventory[product_id]['stock']}")

                stock_input = input("Enter the new stock: ").strip()

                if stock_input.isdigit():
                    new_stock = int(stock_input)

                    if new_stock <= 0:
                        print("Stock cannot be less that 0")
                    else:
                        inventory[product_id]["stock"] = new_stock
                        message_box("Stock updated successfully.")
                else:
                    message_box("Invalid stock. Please enter a whole number.")
            else:
               message_box("Product ID not found.")

        # Add a new product
        elif option == "3":
            product_id = input("Enter the new product ID: ").strip()

            if product_id in inventory:
                message_box("That product ID already exists.")

            elif not product_id.isdigit():
                message_box("The product ID must contain only numbers.")
            else:
                product_name = input("Enter the product name: ").strip()
                price_input = input("Enter the product price: $").strip()
                stock_input = input("Enter the stock quantity: ").strip()


                if not product_name:
                    message_box("The product name cannot be empty.")

                elif not price_input.replace(".", "", 1).isdigit():
                    message_box("Enter a valid number for the product price.")


                elif not stock_input.isdigit():
                    message_box("Enter a valid whole number for the stock.")


                else:
                    product_price = float(price_input)
                    product_stock = int(stock_input)

                    if product_price <= 0:
                        message_box("The product price must be greater than zero.")

                    else:
                        inventory[product_id] = {
                            "name": product_name,
                            "price": product_price,
                            "stock": product_stock
                        }

                        message_box(f"{product_name} added successfully.")
                        print(inventory[product_id])

        elif option == "0":
            break
        else:
            message_box("Enter a valid option.")






# Customer Section

def view_cart():
    '''Opens the catalogue'''
    if not cart_list:
        print()
        print("=" * 55)
        print("Your cart is empty. Please add items from the catalogue.")
        print("=" * 55)
        return

    total = 0

    border = (
        "+"
        + "-" * 8
        + "+"
        + "-" * 26
        + "+"
        + "-" * 10
        + "+"
        + "-" * 14
        + "+"
    )

    print()
    print("YOUR SHOPPING CART")
    print(border)
    print(
        f"| {'ID':<6} "
        f"| {'PRODUCT':<24} "
        f"| {'QUANTITY':>8} "
        f"| {'SUBTOTAL':>12} |"
    )
    print(border)

    for cart_item in cart_list:
        product_id = cart_item["product_id"]
        name = cart_item["name"]
        quantity = cart_item["qty"]
        subtotal = f"${cart_item['subtotal']:.2f}"

        print(
            f"| {product_id:<6} "
            f"| {name:<24} "
            f"| {quantity:>8} "
            f"| {subtotal:>12} |"
        )

        total += cart_item["subtotal"]

    total_text = f"${total:.2f}"

    print(border)
    print(
        f"| {'':<6} "
        f"| {'':<24} "
        f"| {'TOTAL':>8} "
        f"| {total_text:>12} |"
    )
    print(border)



# Checkout function
def checkout():
    '''Checkout orders'''
    if not cart_list:
        message_box("Your cart is empty. Please add items before checking out.")
        return

    total_list = []

    print()
    print("="*20)
    print("YOUR RECEIPT")
    print("-"*20)
    print()

    for item_dict in cart_list:
        product_id = item_dict["product_id"]
        name = item_dict["name"]
        qty = item_dict["qty"]
        subtotal = item_dict["subtotal"]


        for item_id, product_details in inventory.items():
            if item_id == product_id:
                if qty > product_details["stock"]:
                    print("The quantity of this item you added to your cart is more than the available stock. Please reduce it.")
                else:
                    product_details["stock"] -= qty


        total_list.append(subtotal)

        print(f"{name:<22} | Quantity: {qty:>3} | Subtotal: ${subtotal:>8.2f}")
    print("-" * 65)

    total = sum(total_list)

    if total > 20:
        discounted_total = total - (total * 0.1)

        print(f"{'Total before discount:':<45}${total:>10.2f}")
        print(f"{'Discount (10%):':<45}-${total * 0.1:>9.2f}")
        print("-" * 65)
        print(f"{'Total after discount:':<45}${discounted_total:>10.2f}")

    else:
        print(f"{'Total:':<45}${total:>10.2f}")

    print()
    print("="*20)
    print()
    box("Thank you for your patronage. See you again")
    cart_list.clear()





# Add to cart Function
def add_to_cart():
    '''Adds items to cart'''
    while True:
        item = input("Enter the name of the item: (or enter exit to quit ) ").strip().lower()
        if item == "exit":
            break
        else:
            for item_id, product_details in inventory.items():
                if item == product_details["name"].lower():
                    product_id = item_id
                    product_price = product_details["price"]
                    product_stock = product_details["stock"]

                    # Getting quantity to purchase

                    item_qty = int(input("How many? "))
                    if item_qty <= 0:
                        print("Quantity must be greater than zero.")
                        break

                    if item_qty > product_stock:
                        print(
                            f"Not enough stock. Only {product_stock} "
                            f"{product_details["name"]}(s) are available."
                        )
                        break

                    for cart_item in cart_list:
                        if cart_item["product_id"] == item_id:
                            new_quantity = cart_item["qty"] + item_qty

                            if new_quantity > product_stock:
                                print(
                                    f"You already have {cart_item['qty']} in your cart. "
                                    f"Only {product_stock} {product_details["name"]}(s) are available."
                                )
                            else:
                                cart_item["qty"] = new_quantity
                                cart_item["subtotal"] = product_price * new_quantity
                                message_box(f"{item} cart quantity updated successfully")

                            break
                    else:
                        to_purchase = {
                            "product_id": item_id,
                            "name": product_details["name"],
                            "qty": item_qty,
                            "subtotal": product_price * item_qty
                        }

                        cart_list.append(to_purchase)
                        message_box(f"{item} added to cart successfully")

                    break

            else:
                item != product_details["name"].lower()
                message_box(f"{item} not available, check back later.")




# Function to display the cart
def display_cat():
    '''Displays catalogue'''
    print()
    print("=" * 58)
    print(f"{'ID':<8}{'PRODUCT':<25}{'PRICE':>12}{'STOCK':>10}")
    print("-" * 58)

    for product_id, product_details in inventory.items():
        name = product_details["name"]
        price = f"${product_details['price']:.2f}"
        stock = product_details["stock"]

        print(f"{product_id:<8}{name:<25}{price:>12}{stock:>10}")

    print("=" * 58)




# Menu
menu_options = (0, 1, 2,)

# Menu Logic
while True:
    print()
    box("WELCOME TO CAMPUS CART")
    print("="*20)
    print ("Select an option that applies to you")
    print("="*20)
    print()

    print("1 = I am a customer")
    print("2 = I am the admin")
    print("# = Exit")
    print()
    first_input = input("Enter an option: ")

    if first_input == "1":
        while True:
            print ()
            box("How can I help you today?")
            print()
            print("="*20)
            print ("Select an option below")
            print("="*20)
            print()
            print ("1 = Display catalogue")
            print ("2 = Add to  cart")
            print ("3 = View cart")
            print ("4 = Checkout")
            print ("0 = Exit Menu")

            print()
            user_input = input("Enter an option: ")
            print()

            if user_input == "1":
                print()
                print("Here are the available products:")
                print()
                display_cat()

            elif user_input == "2":
                add_to_cart()
            elif user_input == "3":
                view_cart()
            elif user_input == "4":
                checkout()
            elif user_input == "0":
                break
            else:
                print ("Enter a valid option")

    elif first_input == "2":
        if admin_auth():
            while True:
                print()
                print()
                print ("1 = Display Inventory")
                print ("2 = Manage Inventory")
                print ("0 = Exit Menu")
                print()

                admin_input = input("Enter an option: ")

                if admin_input == "1":
                    print()
                    print("Here is your inventory:")
                    print()
                    display_cat()

                elif admin_input == "2":
                    manage_inventory()
                elif admin_input == "0":
                    break
                else:
                    print ("Enter a valid option")
    elif first_input == "#":
        break
    else:
        print("="*20)
        print ("Enter a valid option")
        print("="*20)
