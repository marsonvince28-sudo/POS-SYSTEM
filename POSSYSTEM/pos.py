import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Setup ----------
root = tk.Tk()
root.title("✦ POINT OF SALE SYSTEM ✦")
root.geometry("980x680")
root.minsize(800, 550)
root.configure(bg="#f0f2f5")

# ---------- Style Configuration ----------
style = ttk.Style()
style.theme_use("clam")

# Configure colors and fonts
BG_PRIMARY = "#1e2a3a"      # dark sidebar
BG_SECONDARY = "#ffffff"    # white cards
BG_MAIN = "#f8fafc"         # main background
ACCENT = "#3b82f6"          # bright blue
ACCENT_HOVER = "#2563eb"
DANGER = "#ef4444"
SUCCESS = "#10b981"

root.configure(bg=BG_MAIN)

# Fonts
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_HEADING = ("Segoe UI", 14, "bold")
FONT_REGULAR = ("Segoe UI", 11)
FONT_BUTTON = ("Segoe UI", 10, "bold")

# ttk styles
style.configure("TFrame", background=BG_MAIN)
style.configure("Left.TFrame", background=BG_PRIMARY)
style.configure("Card.TFrame", background=BG_SECONDARY, relief="flat", borderwidth=0)
style.configure("Product.TButton", font=FONT_BUTTON, background=BG_SECONDARY, 
                foreground="#1e293b", borderwidth=0, focuscolor="none", padding=12)
style.map("Product.TButton",
          background=[("active", "#e2e8f0")],
          foreground=[("active", "#0f172a")])
style.configure("Action.TButton", font=FONT_BUTTON, padding=8)
style.configure("Danger.TButton", font=FONT_BUTTON, background=DANGER, foreground="white")
style.map("Danger.TButton",
          background=[("active", "#dc2626")])
style.configure("Success.TButton", font=FONT_BUTTON, background=SUCCESS, foreground="white")
style.map("Success.TButton",
          background=[("active", "#059669")])
style.configure("Total.TLabel", font=("Segoe UI", 18, "bold"), foreground="#0f172a", background=BG_SECONDARY)
style.configure("Heading.TLabel", font=FONT_HEADING, foreground="#334155", background=BG_SECONDARY)

# ---------- Data ----------
products = [
    {"name": "🍎 Apple", "price": 10.00},
    {"name": "🍌 Banana", "price": 15.00},
    {"name": "🍊 Orange", "price": 20.00},
    {"name": "🍇 Grape", "price": 25.00},
    {"name": "🍉 Watermelon", "price": 30.00},
    {"name": "🥝 Kiwi", "price": 35.00},
    {"name": "🍓 Strawberry", "price": 40.00},
    {"name": "🥭 Mango", "price": 45.00}
]

cart = []  # each item: {"name": str, "price": float, "quantity": int}

# ---------- Functions ----------
def add_to_cart(product_name, product_price):
    """Add product to cart (or increase quantity)"""
    for item in cart:
        if item["name"] == product_name:
            item["quantity"] += 1
            update_cart_ui()
            return
    cart.append({"name": product_name, "price": product_price, "quantity": 1})
    update_cart_ui()

def update_quantity(index, delta):
    """Change quantity of cart item at index by delta (1 or -1)"""
    if 0 <= index < len(cart):
        new_qty = cart[index]["quantity"] + delta
        if new_qty <= 0:
            cart.pop(index)
        else:
            cart[index]["quantity"] = new_qty
        update_cart_ui()

def remove_item(index):
    """Remove cart item at given index"""
    if 0 <= index < len(cart):
        cart.pop(index)
        update_cart_ui()

def clear_cart():
    """Remove all items from cart"""
    cart.clear()
    update_cart_ui()

def checkout():
    """Simulate checkout process"""
    if not cart:
        messagebox.showwarning("Empty Cart", "No items in cart to checkout!")
        return
    total = sum(item["price"] * item["quantity"] for item in cart)
    msg = f"Order placed successfully!\n\nTotal amount: ${total:.2f}\n\nThank you for shopping!"
    messagebox.showinfo("Checkout", msg)
    clear_cart()

def update_cart_ui():
    """Rebuild cart display and update total"""
    # Clear inner frame
    for widget in order_inner_frame.winfo_children():
        widget.destroy()
    
    if not cart:
        empty_label = ttk.Label(order_inner_frame, text="🛒 Cart is empty", 
                                font=("Segoe UI", 12), foreground="#94a3b8", background=BG_SECONDARY)
        empty_label.pack(pady=40)
    else:
        # Display each cart item
        for idx, item in enumerate(cart):
            item_frame = tk.Frame(order_inner_frame, bg=BG_SECONDARY, relief="flat", bd=0)
            item_frame.pack(fill="x", padx=12, pady=6)
            
            # Left side: name, price, quantity
            info_text = f"{item['name']}  x{item['quantity']}  @ ${item['price']:.2f}"
            info_label = tk.Label(item_frame, text=info_text, font=FONT_REGULAR, 
                                  bg=BG_SECONDARY, fg="#1e293b", anchor="w")
            info_label.pack(side="left", fill="x", expand=True)
            
            # Right side: control buttons
            btn_frame = tk.Frame(item_frame, bg=BG_SECONDARY)
            btn_frame.pack(side="right")
            
            # Minus button
            minus_btn = tk.Button(btn_frame, text="−", font=("Segoe UI", 12, "bold"),
                                  width=3, bg="#f1f5f9", fg="#475569", relief="flat",
                                  activebackground="#e2e8f0", command=lambda i=idx: update_quantity(i, -1))
            minus_btn.pack(side="left", padx=2)
            
            # Quantity
            qty_label = tk.Label(btn_frame, text=str(item["quantity"]), font=FONT_REGULAR,
                                 bg=BG_SECONDARY, fg="#0f172a", width=3)
            qty_label.pack(side="left", padx=4)
            
            # Plus button
            plus_btn = tk.Button(btn_frame, text="+", font=("Segoe UI", 12, "bold"),
                                 width=3, bg="#f1f5f9", fg="#475569", relief="flat",
                                 activebackground="#e2e8f0", command=lambda i=idx: update_quantity(i, 1))
            plus_btn.pack(side="left", padx=2)
            
            # Remove button
            remove_btn = tk.Button(btn_frame, text="✕", font=("Segoe UI", 10, "bold"),
                                   width=3, bg=BG_SECONDARY, fg=DANGER, relief="flat",
                                   activebackground="#fee2e2", command=lambda i=idx: remove_item(i))
            remove_btn.pack(side="left", padx=5)
    
    # Update total
    total = sum(item["price"] * item["quantity"] for item in cart)
    total_var.set(f"Total: ${total:.2f}")
    
    # Update scroll region after layout
    order_inner_frame.update_idletasks()
    order_canvas.configure(scrollregion=order_canvas.bbox("all"))
    # Adjust inner frame width to canvas
    order_canvas.itemconfig(canvas_window_id, width=order_canvas.winfo_width())

# ---------- UI Layout ----------
# MAIN LEFT PANEL (Order Summary)
left_frame = ttk.Frame(root, style="Left.TFrame", width=360)
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)

# Header in left panel
header_left = tk.Frame(left_frame, bg=BG_PRIMARY, height=70)
header_left.pack(fill="x")
tk.Label(header_left, text="🛍️ ORDER SUMMARY", font=FONT_TITLE, 
         fg="white", bg=BG_PRIMARY).pack(pady=15)

# Scrollable cart area
order_list_frame = ttk.Frame(left_frame)
order_list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

order_canvas = tk.Canvas(order_list_frame, bg=BG_SECONDARY, highlightthickness=0)
order_scrollbar = ttk.Scrollbar(order_list_frame, orient="vertical", command=order_canvas.yview)

order_inner_frame = tk.Frame(order_canvas, bg=BG_SECONDARY)
canvas_window_id = order_canvas.create_window((0, 0), window=order_inner_frame, anchor="nw")

order_canvas.configure(yscrollcommand=order_scrollbar.set)
order_canvas.pack(side="left", fill="both", expand=True)
order_scrollbar.pack(side="right", fill="y")

# Update scroll region when inner frame changes
def on_inner_frame_configure(event):
    order_canvas.configure(scrollregion=order_canvas.bbox("all"))
order_inner_frame.bind("<Configure>", on_inner_frame_configure)

# Update canvas width when resized
def on_canvas_configure(event):
    order_canvas.itemconfig(canvas_window_id, width=event.width)
order_canvas.bind("<Configure>", on_canvas_configure)

# Mousewheel scrolling
def on_mousewheel(event):
    order_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
order_canvas.bind_all("<MouseWheel>", on_mousewheel)

# Total and action buttons at bottom of left panel
bottom_left = tk.Frame(left_frame, bg=BG_PRIMARY, height=130)
bottom_left.pack(fill="x", side="bottom")

total_var = tk.StringVar(value="Total: $0.00")
total_label = tk.Label(bottom_left, textvariable=total_var, font=("Segoe UI", 18, "bold"),
                       fg="white", bg=BG_PRIMARY)
total_label.pack(pady=(15, 10))

btn_frame = tk.Frame(bottom_left, bg=BG_PRIMARY)
btn_frame.pack(pady=5)

clear_btn = tk.Button(btn_frame, text="🗑️ Clear Cart", font=FONT_BUTTON, bg="#334155", fg="white",
                      relief="flat", padx=20, pady=5, activebackground="#475569", command=clear_cart)
clear_btn.pack(side="left", padx=10)

checkout_btn = tk.Button(btn_frame, text="✅ Checkout", font=FONT_BUTTON, bg=SUCCESS, fg="white",
                         relief="flat", padx=20, pady=5, activebackground="#059669", command=checkout)
checkout_btn.pack(side="left", padx=10)

# ---------- RIGHT PANEL (Products) ----------
right_frame = ttk.Frame(root, style="TFrame")
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Header
header_right = tk.Frame(right_frame, bg=BG_MAIN)
header_right.pack(fill="x", pady=(0, 15))
tk.Label(header_right, text="✨ PRODUCTS MENU", font=FONT_TITLE, 
         fg="#0f172a", bg=BG_MAIN).pack(anchor="w")
tk.Label(header_right, text="Click on any item to add to cart", 
         font=("Segoe UI", 10), fg="#64748b", bg=BG_MAIN).pack(anchor="w")

# Products grid
products_frame = tk.Frame(right_frame, bg=BG_MAIN)
products_frame.pack(fill="both", expand=True)

# Configure grid columns
for i in range(3):
    products_frame.columnconfigure(i, weight=1)

row, col = 0, 0
for product in products:
    # Card frame
    card = tk.Frame(products_frame, bg=BG_SECONDARY, relief="raised", bd=1, highlightbackground="#e2e8f0", highlightthickness=1)
    card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
    
    # Product name
    name_label = tk.Label(card, text=product["name"], font=("Segoe UI", 13, "bold"),
                          bg=BG_SECONDARY, fg="#1e293b")
    name_label.pack(pady=(15, 5))
    
    # Price
    price_label = tk.Label(card, text=f"${product['price']:.2f}", font=("Segoe UI", 12),
                           bg=BG_SECONDARY, fg="#3b82f6")
    price_label.pack(pady=(0, 10))
    
    # Add button
    add_btn = tk.Button(card, text="➕ Add to Cart", font=FONT_BUTTON,
                        bg=ACCENT, fg="white", relief="flat", padx=15, pady=5,
                        activebackground=ACCENT_HOVER,
                        command=lambda p=product: add_to_cart(p["name"], p["price"]))
    add_btn.pack(pady=(0, 15))
    
    # Hover effect on card
    def on_enter(e, card=card):
        card.configure(bg="#f8fafc", highlightbackground="#cbd5e1")
        for child in card.winfo_children():
            child.configure(bg="#f8fafc")
    def on_leave(e, card=card):
        card.configure(bg=BG_SECONDARY, highlightbackground="#e2e8f0")
        for child in card.winfo_children():
            child.configure(bg=BG_SECONDARY)
    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)
    
    col += 1
    if col >= 3:
        col = 0
        row += 1

# Initialize empty cart display
update_cart_ui()

# ---------- Run Application ----------
root.mainloop()