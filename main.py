"""
CampusCart CLI Application
Author: Bamidele Oluwapelumi Adeleke
Description: An interactive procedural CLI tools for managing a CampusCart using variables,
    conditional loops, dictionaries, and list structures.
"""

# Display Welcome Banner and input
print("=" * 40)
print("     WELCOME TO CAMPUSCART CLI SYSTEM     ")
print("=" * 40)

user_name = input("Enter your name to start: ").strip().title()
print(f"\nHello, {user_name}! System initialized successfully.\n")

#phase 2: data structures design
#catalogue dictionary structure and active shooping cart list
inventory = {
    "101": {"name": "40 leaves notebook", "price": 2.50, "stock": 15},
    "102": {"name": "80 leaves notebook", "price": 4.50, "stock": 15},
    "103": {"name": "Pen Packs", "price": 5, "stock": 10},
    "104": {"name": "school bags", "price": 7.5, "stock": 5},
    "105": {"name": "Food Flasks", "price": 10, "stock": 3},
    "106": {"name": "school uniform", "price": 10, "stock": 23},
    "107": {"name": "lamp", "price": 2.7, "stock": 25},
    "108": {"name": "shoe", "price": 8, "stock": 15},
    "109": {"name": "water bottle", "price": 4.9, "stock": 15},
    "110": {"name": "laptop", "price": 50, "stock": 30}
    }

cart = []

print("\n--- Goods ready ---")
print(f"Catalogue loaded with {len(inventory)} products.")
print(f"initial cart state: {cart}")



