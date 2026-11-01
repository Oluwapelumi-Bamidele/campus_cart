"""
CampusCart Streamlit Frontend Application (app.py)
Complete Integration: Student Storefront & Advanced Administrator Suite
"""

import streamlit as st
import os
from models.item import Item, PerishableItem, DigitalVoucher
from models.cart import ShoppingCart
from models.payment import CashPayment, CardPayment, MobileMoneyPayment
from inventory import (
    calc_price,
    delete_item,
    update_stock,
    verify_and_add_stock,
    filter_low_stock
)
from utils.logger import log_transaction, search_transaction_by_id

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="CampusCart Store",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛒 CampusCart Student Store System")
st.caption("Enterprise-Grade OOP Store Front & Administrator Management Dashboard")
st.divider()

# 2. REACTIVE SESSION STATE INITIALIZATION
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "101": Item("101", "Notebook", 2.50, 15),
        "102": Item("102", "Campus Hoodie", 25.00, 4),
        "103": Item("103", "Scientific Calculator", 15.00, 8),
        "104": Item("104", "Ballpoint Pens (10-pack)", 4.75, 40),
        "105": PerishableItem("105", "Fresh Milk", 3.50, 10, expiration_date="2026-11-15"),
        "106": DigitalVoucher("106", "Campus Gift Card $20", 20.00),
    }

if "cart" not in st.session_state:
    st.session_state.cart = ShoppingCart()

inventory = st.session_state.inventory
cart = st.session_state.cart

# 3. DECORATED CHECKOUT BRIDGE FOR STREAMLIT
@log_transaction
def execute_streamlit_checkout(client_name, cart_obj, payment_processor):
    subtotal = cart_obj.calculate_subtotal()
    final_total = calc_price(subtotal, order_total=subtotal)
    
    success, payment_msg = payment_processor.process_payment(final_total)
    if not success:
        raise ValueError(payment_msg)
        
    purchased_goods = [f"{entry['item'].name} (x{entry['quantity']})" for entry in cart_obj.items]
    return subtotal, final_total, purchased_goods


# 4. MAIN TABS: STUDENT STOREFRONT & ADMINISTRATOR PANEL
store_tab, admin_tab = st.tabs(["🛍️ Student Storefront", "⚙️ Administrator Panel"])

with store_tab:
    st.subheader("📦 Available Products Catalog")
    
    sort_option = st.radio("Sort Catalog By:", ["Price: Low to High", "Price: High to Low"], horizontal=True)
    ascending_sort = (sort_option == "Price: Low to High")
    
    sorted_items = sorted(inventory.items(), key=lambda entry: entry[1].price, reverse=not ascending_sort)

    # 3-Column Grid for Product Cards
    cols = st.columns(3)
    for idx, (item_id, item_obj) in enumerate(sorted_items):
        col = cols[idx % 3]
        with col:
            with st.container(border=True):
                st.markdown(f"### {item_obj.name}")
                
                if isinstance(item_obj, PerishableItem):
                    st.caption(f"⏳ **Perishable** | Exp: {item_obj.expiration_date}")
                elif isinstance(item_obj, DigitalVoucher):
                    st.caption("⚡ **Digital Voucher** | Instant Delivery")
                else:
                    st.caption(f"🆔 Item ID: {item_obj.item_id}")

                m1, m2 = st.columns(2)
                m1.metric("Price", f"${item_obj.price:.2f}")
                
                stock_label = "Unlimited" if item_obj.stock == float('inf') else f"{int(item_obj.stock)} left"
                m2.metric("Stock", stock_label)

                if item_obj.stock > 0 or item_obj.stock == float('inf'):
                    max_val = 99 if item_obj.stock == float('inf') else max(1, int(item_obj.stock))
                    qty_selected = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=max_val,
                        value=1,
                        key=f"qty_{item_id}"
                    )
                    
                    if st.button("➕ Add to Cart", key=f"btn_{item_id}", use_container_width=True):
                        success, msg = cart.add_item(item_obj, quantity=qty_selected)
                        if success:
                            st.toast(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.error(msg)
                else:
                    st.error("❌ Out of Stock")

with admin_tab:
    st.subheader("⚙️ Administrator Management Panel")
    st.markdown("Manage catalog inventory, restock items, modify stock levels, and review audit logs.")
    
    admin_action = st.selectbox(
        "Select Admin Operation",
        [
            "1. View Full Catalog & Stock Status",
            "2. Check Stock Below Threshold Limit",
            "3. Restock Item",
            "4. Directly Modify Item Stock (+/-)",
            "5. Add Specialized Product (Base/Perishable/Voucher)",
            "6. Delete Item from Catalog",
            "7. Search Transaction Record by ID",
            "8. View Full Transaction Audit History"
        ]
    )
    st.divider()

    if "1." in admin_action:
        st.markdown("### 📋 Full Inventory Catalog")
        catalog_data = []
        for item in inventory.values():
            meta = "Standard Item"
            if isinstance(item, PerishableItem):
                meta = f"Perishable (Exp: {item.expiration_date})"
            elif isinstance(item, DigitalVoucher):
                meta = "Digital Voucher (Unlimited)"
                
            catalog_data.append({
                "ID": str(item.item_id),
                "Name": str(item.name),
                "Category / Metadata": str(meta),
                "Price ($)": f"${item.price:.2f}",
                "Stock": "Unlimited" if item.stock == float('inf') else str(int(item.stock))
            })
        st.table(catalog_data)

    elif "2." in admin_action:
        st.markdown("### ⚠️ Low Stock Threshold Report")
        threshold = st.number_input("Enter stock threshold limit:", min_value=1, value=10)
        low_stock = filter_low_stock(inventory, threshold)
        
        if not low_stock:
            st.success("Status: All items are currently well-stocked above the threshold!")
        else:
            low_data = [
                {"ID": item.item_id, "Name": item.name, "Price ($)": f"${item.price:.2f}", "Stock Remaining": int(item.stock)}
                for item in low_stock.values()
            ]
            st.table(low_data)

    elif "3." in admin_action:
        st.markdown("### 📦 Restock Existing Item")
        item_id_input = st.selectbox("Select Item to Restock", options=list(inventory.keys()), format_func=lambda x: f"{x} - {inventory[x].name} (Current Stock: {inventory[x].stock})")
        add_qty = st.number_input("Quantity to add:", min_value=1, value=10)
        
        if st.button("Confirm Restock"):
            success, msg = verify_and_add_stock(inventory, item_id_input, add_qty)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    elif "4." in admin_action:
        st.markdown("### 🔄 Directly Modify Item Stock")
        item_id_input = st.selectbox("Select Item to Modify", options=list(inventory.keys()), format_func=lambda x: f"{x} - {inventory[x].name} (Current Stock: {inventory[x].stock})")
        qty_change = st.number_input("Enter quantity change (positive to add, negative to reduce):", value=0, step=1)
        
        if st.button("Apply Stock Modification"):
            success, result = update_stock(inventory, item_id_input, qty_change)
            if success:
                st.success(f"Successfully updated stock! New Stock: {result}")
                st.rerun()
            else:
                st.error(result)

    elif "5." in admin_action:
        st.markdown("### ➕ Add Specialized Product to Catalog")
        
        product_type = st.selectbox("Product Subclass Type", ["Base Item", "Perishable Item", "Digital Voucher"])
        new_id = st.text_input("New Item ID (e.g., 201):")
        new_name = st.text_input("Item Name:")
        new_price = st.number_input("Unit Price ($):", min_value=0.01, value=5.00)
        
        exp_date = "N/A"
        new_stock = 20
        
        if product_type == "Perishable Item":
            exp_date = st.text_input("Expiration Date (YYYY-MM-DD)", value="2026-12-31")
            new_stock = st.number_input("Initial Stock Quantity:", min_value=0, value=15)
        elif product_type == "Base Item":
            new_stock = st.number_input("Initial Stock Quantity:", min_value=0, value=20)
        else:
            st.info("Digital Vouchers automatically feature infinite stock redemption.")

        if st.button("Register New Product"):
            if new_id and new_name:
                if new_id in inventory:
                    st.error("Error: An item with this ID already exists.")
                else:
                    if product_type == "Perishable Item":
                        inventory[new_id] = PerishableItem(new_id, new_name, new_price, new_stock, exp_date)
                    elif product_type == "Digital Voucher":
                        inventory[new_id] = DigitalVoucher(new_id, new_name, new_price)
                    else:
                        inventory[new_id] = Item(new_id, new_name, new_price, new_stock)
                        
                    st.success(f"Successfully registered '{new_name}' ({product_type})!")
                    st.rerun()
            else:
                st.warning("Please provide both an Item ID and Name.")

    elif "6." in admin_action:
        st.markdown("### 🗑️ Delete Item from Catalog")
        item_id_input = st.selectbox("Select Item to Delete", options=list(inventory.keys()), format_func=lambda x: f"{x} - {inventory[x].name}")
        
        if st.button("Permanently Delete Item", type="primary"):
            success, msg = delete_item(inventory, item_id_input)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    elif "7." in admin_action:
        st.markdown("### 🔍 Search Transaction Audit Record")
        search_id = st.text_input("Enter Transaction ID (e.g., A9F321BC):")
        if st.button("Search Audit Log"):
            if search_id:
                found, result = search_transaction_by_id(search_id)
                if found:
                    st.success("Transaction Record Found!")
                    st.code(result)
                else:
                    st.error(result)

    elif "8." in admin_action:
        st.markdown("### 📜 Full Transaction Audit History")
        if not os.path.exists("transaction_log.txt"):
            st.info("No transaction logs recorded yet.")
        else:
            with open("transaction_log.txt", "r", encoding="utf-8") as file:
                log_contents = file.read()
            st.code(log_contents, language="text")


# 5. SIDEBAR CART, RECEIPT GENERATOR & POLYMORPHIC CHECKOUT
with st.sidebar:
    st.header("🛒 Active Shopping Basket")
    st.divider()
    
    if not cart.items:
        st.info("Your shopping cart is empty.")
    else:
        for entry in cart.items:
            item = entry["item"]
            qty = entry["quantity"]
            line_cost = item.price * qty
            
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"**{item.name}** (x{qty})")
                st.caption(f"${item.price:.2f} ea | Total: ${line_cost:.2f}")
            with c2:
                if st.button("🗑️", key=f"rem_{item.item_id}"):
                    cart.remove_item(item.item_id, quantity_to_remove=qty)
                    st.toast(f"Removed {item.name} from cart.")
                    st.rerun()
            st.divider()

        subtotal = cart.calculate_subtotal()
        final_total = calc_price(subtotal, order_total=subtotal)
        
        st.metric("Subtotal", f"${subtotal:.2f}")
        st.metric("Final Total (Tax incl.)", f"${final_total:.2f}")

        with st.expander("📄 View Itemized Receipt Preview"):
            for receipt_line in cart.stream_receipt_lines():
                st.text(f"> {receipt_line}")
        
        if st.button("🧹 Clear Cart", use_container_width=True):
            cart.clear()
            st.toast("Cart cleared and stock restored!")
            st.rerun()
            
        st.divider()
        st.subheader("💳Payment Portal")
        
        client_name = st.text_input("Student Name", value="Oluwapelumi Bamidele")
        pay_method = st.selectbox(
            "Payment Strategy",
            ["Cash Payment", "Credit/Debit Card", "Mobile Money (OPay/MoMo)"]
        )
        
        card_num = ""
        momo_phone = ""
        momo_provider = "OPay"
        
        if pay_method == "Credit/Debit Card":
            card_num = st.text_input("Card Number", value="4111222233334444")
        elif pay_method == "Mobile Money (OPay/MoMo)":
            momo_phone = st.text_input("Phone Number", value="08098765432")
            momo_provider = st.selectbox("Provider", ["OPay", "PalmPay", "MTN MoMo"])

        confirm_checkout = st.checkbox("Confirm order details & proceed")

        if st.button("🚀 Complete Order & Checkout", type="primary", use_container_width=True):
            if not confirm_checkout:
                st.warning("Please check 'Confirm order details & proceed' before checking out.")
            else:
                if pay_method == "Credit/Debit Card":
                    processor = CardPayment(card_num)
                elif pay_method == "Mobile Money (OPay/MoMo)":
                    processor = MobileMoneyPayment(momo_phone, provider=momo_provider)
                else:
                    processor = CashPayment()

                # --- PUT YOUR CODE BLOCK RIGHT HERE ---
                try:
                    final_paid = execute_streamlit_checkout(client_name, cart, processor)
                    
                    # This creates a floating success notification that stays visible for a few seconds
                    st.toast(f"🎉 Payment Successful! Paid ${final_paid:.2f}", icon="✅")
                    st.balloons()
                    
                    cart.items.clear()
                    
                    # Optional: short delay if you want time to read it before clearing/rerunning
                    import time
                    time.sleep(1.5)
                    st.rerun()
                    
                except Exception as err:
                    st.error(f"Payment Failure: {err}")