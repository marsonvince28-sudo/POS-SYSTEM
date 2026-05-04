import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

# ---------- Data Storage ----------
DATA_FILE = "pos_data.json"

def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"users": {}, "products": [], "transactions": []}
    return {"users": {}, "products": [], "transactions": []}

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Initialize data
saved_data = load_data()

# User Database
USERS = saved_data.get("users", {})
if not USERS:
    USERS = {
        "cashier1": {"password": "cash123", "role": "cashier"},
        "manager1": {"password": "mgr123", "role": "manager"},
        "admin1": {"password": "admin123", "role": "admin"},
    }

# Products Database - CENTRALIZED
PRODUCTS = saved_data.get("products", [])
if not PRODUCTS:
    PRODUCTS = [
        {"name": "Apple", "price": 10.00},
        {"name": "Banana", "price": 15.00},
        {"name": "Orange", "price": 20.00},
        {"name": "Grape", "price": 25.00},
        {"name": "Watermelon", "price": 30.00},
        {"name": "Kiwi", "price": 35.00},
        {"name": "Strawberry", "price": 40.00},
        {"name": "Mango", "price": 45.00},
        {"name": "Pineapple", "price": 50.00},
        {"name": "Peach", "price": 28.00},
        {"name": "Cherry", "price": 60.00},
        {"name": "Blueberry", "price": 55.00},
        {"name": "Broccoli", "price": 22.00},
        {"name": "Carrot", "price": 12.00},
        {"name": "Tomato", "price": 18.00},
        {"name": "Cucumber", "price": 15.00},
        {"name": "Bell Pepper", "price": 25.00},
        {"name": "Lettuce", "price": 20.00},
        {"name": "Garlic", "price": 8.00},
        {"name": "Onion", "price": 10.00},
        {"name": "Milk (1L)", "price": 45.00},
        {"name": "Cheese (250g)", "price": 85.00},
        {"name": "Eggs (6pcs)", "price": 55.00},
        {"name": "Ice Cream", "price": 70.00},
        {"name": "Coffee", "price": 120.00},
        {"name": "Tea", "price": 95.00},
        {"name": "Soda", "price": 35.00},
        {"name": "Juice", "price": 50.00},
        {"name": "Bread", "price": 40.00},
        {"name": "Croissant", "price": 55.00},
        {"name": "Cookies", "price": 65.00},
        {"name": "Chocolate Bar", "price": 45.00},
        {"name": "Pretzel", "price": 30.00},
        {"name": "Donut", "price": 35.00},
        {"name": "Sandwich", "price": 80.00},
    ]

# Transactions Database - CENTRALIZED
TRANSACTIONS = saved_data.get("transactions", [])

# ---------- Login Window ----------
class LoginWindow:
    def __init__(self):
        self.login_root = tk.Tk()
        self.login_root.title("POS Login - Vrejj Convenience Store")
        self.login_root.geometry("450x350")
        self.login_root.resizable(False, False)
        self.login_root.configure(bg="#f0f2f5")

        self.login_root.update_idletasks()
        x = (self.login_root.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.login_root.winfo_screenheight() // 2) - (350 // 2)
        self.login_root.geometry(f"+{x}+{y}")

        # Header
        tk.Label(self.login_root, text="🏪 VREJJ CONVENIENCE STORE", 
                 font=("Segoe UI", 16, "bold"),
                 bg="#f0f2f5", fg="#1e2a3a").pack(pady=20)
        tk.Label(self.login_root, text="Point of Sale System", 
                 font=("Segoe UI", 10),
                 bg="#f0f2f5", fg="#64748b").pack(pady=(0, 20))

        # Login Frame
        frame = tk.Frame(self.login_root, bg="#f0f2f5")
        frame.pack(pady=20)

        tk.Label(frame, text="Username:", font=("Segoe UI", 11), 
                 bg="#f0f2f5").grid(row=0, column=0, padx=5, pady=10, sticky="e")
        self.username_entry = tk.Entry(frame, font=("Segoe UI", 11), width=20)
        self.username_entry.grid(row=0, column=1, padx=5, pady=10)
        self.username_entry.focus()

        tk.Label(frame, text="Password:", font=("Segoe UI", 11), 
                 bg="#f0f2f5").grid(row=1, column=0, padx=5, pady=10, sticky="e")
        self.password_entry = tk.Entry(frame, font=("Segoe UI", 11), width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=10)

        self.message_var = tk.StringVar()
        tk.Label(self.login_root, textvariable=self.message_var, fg="red", 
                 bg="#f0f2f5", font=("Segoe UI", 9)).pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(self.login_root, bg="#f0f2f5")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="🔑 Login", command=self.validate_login, 
                  bg="#3b82f6", fg="white", font=("Segoe UI", 10, "bold"), 
                  padx=30, pady=8, relief="flat").pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="❌ Exit", command=self.login_root.destroy, 
                  bg="#ef4444", fg="white", font=("Segoe UI", 10, "bold"), 
                  padx=30, pady=8, relief="flat").pack(side="left", padx=10)

        self.login_root.bind("<Return>", lambda e: self.validate_login())

    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if username in USERS and USERS[username]["password"] == password:
            role = USERS[username]["role"]
            self.login_root.destroy()
            root = tk.Tk()
            app = ModernPOS(root, username, role)
            app.run()
        else:
            self.message_var.set("❌ Invalid username or password")

# ---------- Main POS System ----------
class ModernPOS:
    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role
        self.root.title(f"🏪 VREJJ POS - {role.upper()} Dashboard - {username}")
        self.root.geometry("1300x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg="#ffffff")

        # Colors & Fonts
        self.BG_PRIMARY = "#1e2a3a"
        self.BG_SECONDARY = "#ffffff"
        self.BG_MAIN = "#ffffff"
        self.ACCENT = "#3b82f6"
        self.DANGER = "#ef4444"
        self.SUCCESS = "#10b981"
        self.WARNING = "#f59e0b"
        self.INFO = "#8b5cf6"

        self.FONT_TITLE = ("Segoe UI", 20, "bold")
        self.FONT_HEADING = ("Segoe UI", 14, "bold")
        self.FONT_REGULAR = ("Segoe UI", 11)
        self.FONT_BUTTON = ("Segoe UI", 10, "bold")
        self.FONT_SMALL = ("Segoe UI", 9)

        self.setup_styles()

        # Cart and transaction data
        self.cart = []
        self.tax_rate = tk.DoubleVar(value=10.0)
        self.discount_percent = tk.DoubleVar(value=0.0)
        self.cash_tendered = tk.DoubleVar(value=0.0)
        
        self.products = PRODUCTS
        self.transactions = TRANSACTIONS

        self.setup_ui()
        self.update_cart_ui()
        self.bind_shortcuts()

    def save_all_data(self):
        """Save all data to file"""
        data = {
            "users": USERS,
            "products": PRODUCTS,
            "transactions": TRANSACTIONS
        }
        save_data(data)

    def refresh_products_display(self):
        """Refresh the products grid"""
        self.filter_products()
        self.root.update_idletasks()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.BG_MAIN)
        style.configure("Left.TFrame", background=self.BG_PRIMARY)

    def setup_ui(self):
        # ========== LEFT PANEL (ORDER SUMMARY) ==========
        self.left_frame = ttk.Frame(self.root, style="Left.TFrame", width=400)
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(False)

        # Header
        header_left = tk.Frame(self.left_frame, bg=self.BG_PRIMARY, height=80)
        header_left.pack(fill="x")
        tk.Label(header_left, text="🛍️ ORDER SUMMARY", 
                font=self.FONT_TITLE, fg="white", bg=self.BG_PRIMARY).pack(pady=20)

        # Scrollable cart
        cart_container = ttk.Frame(self.left_frame)
        cart_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.cart_canvas = tk.Canvas(cart_container, bg=self.BG_SECONDARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(cart_container, orient="vertical", command=self.cart_canvas.yview)
        self.cart_inner = tk.Frame(self.cart_canvas, bg=self.BG_SECONDARY)
        self.canvas_window = self.cart_canvas.create_window((0, 0), window=self.cart_inner, anchor="nw")

        self.cart_canvas.configure(yscrollcommand=scrollbar.set)
        self.cart_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.cart_inner.bind("<Configure>", lambda e: self.cart_canvas.configure(
            scrollregion=self.cart_canvas.bbox("all")))
        self.cart_canvas.bind("<Configure>", lambda e: self.cart_canvas.itemconfig(
            self.canvas_window, width=e.width))
        self.cart_canvas.bind_all("<MouseWheel>", lambda e: self.cart_canvas.yview_scroll(
            int(-1*(e.delta/120)), "units"))

        # Bottom panel
        bottom_left = tk.Frame(self.left_frame, bg=self.BG_PRIMARY)
        bottom_left.pack(fill="x", side="bottom", pady=10)

        # Tax & discount controls (only for manager/admin)
        if self.role in ["manager", "admin"]:
            settings_frame = tk.Frame(bottom_left, bg=self.BG_PRIMARY)
            settings_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(settings_frame, text="Tax %:", fg="white", bg=self.BG_PRIMARY, 
                    font=self.FONT_REGULAR).grid(row=0, column=0, padx=2)
            self.tax_spin = tk.Spinbox(settings_frame, from_=0, to=100, increment=1, 
                                       textvariable=self.tax_rate, width=8, 
                                       font=self.FONT_REGULAR, command=self.update_cart_ui)
            self.tax_spin.grid(row=0, column=1, padx=2)

            tk.Label(settings_frame, text="Discount %:", fg="white", bg=self.BG_PRIMARY, 
                    font=self.FONT_REGULAR).grid(row=0, column=2, padx=5)
            self.disc_spin = tk.Spinbox(settings_frame, from_=0, to=100, increment=1, 
                                        textvariable=self.discount_percent, width=8, 
                                        font=self.FONT_REGULAR, command=self.update_cart_ui)
            self.disc_spin.grid(row=0, column=3, padx=2)

        # Total label
        self.total_var = tk.StringVar(value="Total: ₱0.00")
        total_label = tk.Label(bottom_left, textvariable=self.total_var, 
                               font=("Segoe UI", 16, "bold"),
                               fg="white", bg=self.BG_PRIMARY)
        total_label.pack(pady=(5, 5))

        # Cash tendered
        cash_frame = tk.Frame(bottom_left, bg=self.BG_PRIMARY)
        cash_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(cash_frame, text="💰 Cash Tendered:", fg="white", bg=self.BG_PRIMARY, 
                font=self.FONT_REGULAR).pack(side="left")
        self.cash_entry = tk.Entry(cash_frame, textvariable=self.cash_tendered, 
                                   width=20, font=("Segoe UI", 12))
        self.cash_entry.pack(side="left", padx=5)
        self.change_var = tk.StringVar(value="Change: ₱0.00")
        tk.Label(cash_frame, textvariable=self.change_var, fg="#86efac", 
                bg=self.BG_PRIMARY, font=self.FONT_REGULAR).pack(side="left", padx=10)

        # Action buttons
        btn_frame = tk.Frame(bottom_left, bg=self.BG_PRIMARY)
        btn_frame.pack(pady=10)
        
        clear_btn = tk.Button(btn_frame, text="🗑️ Clear Cart", font=self.FONT_BUTTON, 
                              bg="#334155", fg="white", relief="flat", padx=15, pady=5, 
                              command=self.confirm_clear)
        clear_btn.pack(side="left", padx=5)
        
        self.checkout_btn = tk.Button(btn_frame, text="✅ Checkout", font=self.FONT_BUTTON, 
                                      bg=self.SUCCESS, fg="white", relief="flat", padx=15, pady=5, 
                                      command=self.show_receipt)
        self.checkout_btn.pack(side="left", padx=5)
        
        logout_btn = tk.Button(btn_frame, text="🚪 Logout", font=self.FONT_BUTTON, 
                               bg=self.WARNING, fg="white", relief="flat", padx=15, pady=5, 
                               command=self.logout)
        logout_btn.pack(side="left", padx=5)

        # ========== RIGHT PANEL (PRODUCTS) ==========
        self.right_frame = ttk.Frame(self.root, style="TFrame")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        header_right = tk.Frame(self.right_frame, bg=self.BG_MAIN)
        header_right.pack(fill="x", pady=(0, 15))

        role_titles = {
            "cashier": "👤 CASHIER DASHBOARD",
            "manager": "📊 MANAGER DASHBOARD",
            "admin": "🔧 ADMIN DASHBOARD"
        }
        
        tk.Label(header_right, text=role_titles.get(self.role, "DASHBOARD"), 
                font=self.FONT_TITLE, fg="#0f172a", bg=self.BG_MAIN).pack(anchor="w")
        tk.Label(header_right, text=f"Logged in as: {self.username} ({self.role}) | Centralized POS System", 
                font=self.FONT_SMALL, fg="#64748b", bg=self.BG_MAIN).pack(anchor="w")

        # Search bar
        search_frame = tk.Frame(header_right, bg=self.BG_MAIN)
        search_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(search_frame, text="🔍 Search:", font=self.FONT_REGULAR, 
                bg=self.BG_MAIN).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_products())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                                font=self.FONT_REGULAR, width=30)
        search_entry.pack(side="left", padx=10)

        # Role-specific buttons
        if self.role in ["manager", "admin"]:
            tk.Button(search_frame, text="📊 Sales Report", font=self.FONT_BUTTON,
                     bg=self.WARNING, fg="white", relief="flat", padx=10, pady=3,
                     command=self.show_sales_report).pack(side="right", padx=5)
        
        if self.role == "admin":
            tk.Button(search_frame, text="🔧 Admin Panel", font=self.FONT_BUTTON,
                     bg=self.ACCENT, fg="white", relief="flat", padx=10, pady=3,
                     command=self.open_admin_panel).pack(side="right", padx=5)
            
            tk.Button(search_frame, text="📈 Analytics", font=self.FONT_BUTTON,
                     bg=self.INFO, fg="white", relief="flat", padx=10, pady=3,
                     command=self.show_analytics).pack(side="right", padx=5)

        # Products grid
        self.products_canvas = tk.Canvas(self.right_frame, bg=self.BG_MAIN, highlightthickness=0)
        products_scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", 
                                           command=self.products_canvas.yview)
        self.products_inner = tk.Frame(self.products_canvas, bg=self.BG_MAIN)
        self.products_canvas.create_window((0, 0), window=self.products_inner, anchor="nw")
        self.products_canvas.configure(yscrollcommand=products_scrollbar.set)
        self.products_canvas.pack(side="left", fill="both", expand=True)
        products_scrollbar.pack(side="right", fill="y")

        self.products_inner.bind("<Configure>", lambda e: self.products_canvas.configure(
            scrollregion=self.products_canvas.bbox("all")))
        self.products_canvas.bind("<Configure>", lambda e: self.products_canvas.itemconfig(
            "all", width=e.width))

        self.filter_products()

    def filter_products(self):
        """Filter and display products based on search"""
        for widget in self.products_inner.winfo_children():
            widget.destroy()

        search_term = self.search_var.get().lower()
        filtered = [p for p in PRODUCTS if search_term in p["name"].lower()]

        width = self.products_canvas.winfo_width() if self.products_canvas.winfo_width() > 100 else 600
        cols = max(2, min(5, width // 200))
        
        for i in range(cols):
            self.products_inner.columnconfigure(i, weight=1)

        row, col = 0, 0
        for prod in filtered:
            card = tk.Frame(self.products_inner, bg=self.BG_SECONDARY, relief="raised", bd=1,
                           highlightbackground="#e2e8f0", highlightthickness=1)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            tk.Label(card, text="🛒", font=("Segoe UI", 30), 
                    bg=self.BG_SECONDARY).pack(pady=(10, 0))
            
            tk.Label(card, text=prod["name"], font=("Segoe UI", 12, "bold"),
                    bg=self.BG_SECONDARY, fg="#1e293b", wraplength=150).pack(pady=(5, 2))
            
            tk.Label(card, text=f"₱{prod['price']:.2f}", font=("Segoe UI", 14),
                    bg=self.BG_SECONDARY, fg=self.ACCENT).pack(pady=(0, 5))
            
            qty_frame = tk.Frame(card, bg=self.BG_SECONDARY)
            qty_frame.pack(pady=(0, 5))
            
            qty_var = tk.StringVar(value="1")
            qty_spin = tk.Spinbox(qty_frame, from_=1, to=99, width=5, 
                                  textvariable=qty_var, font=self.FONT_SMALL)
            qty_spin.pack(side="left", padx=5)
            
            add_btn = tk.Button(card, text="➕ Add to Cart", font=self.FONT_BUTTON,
                               bg="black", fg="white", relief="flat", padx=15, pady=4,
                               command=lambda p=prod, var=qty_var: self.add_to_cart_with_qty(p["name"], p["price"], int(var.get())))
            add_btn.pack(pady=(0, 10))

            card.bind("<Enter>", lambda e, c=card: self.on_card_enter(c))
            card.bind("<Leave>", lambda e, c=card: self.on_card_leave(c))

            col += 1
            if col >= cols:
                col = 0
                row += 1

    def on_card_enter(self, card):
        card.configure(bg="#f8fafc", highlightbackground="#cbd5e1")
        for child in card.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg="#f8fafc")

    def on_card_leave(self, card):
        card.configure(bg=self.BG_SECONDARY, highlightbackground="#e2e8f0")
        for child in card.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=self.BG_SECONDARY)

    def add_to_cart_with_qty(self, name, price, quantity):
        for item in self.cart:
            if item["name"] == name:
                item["quantity"] += quantity
                self.update_cart_ui()
                return
        self.cart.append({"name": name, "price": price, "quantity": quantity})
        self.update_cart_ui()

    def update_quantity(self, index, delta):
        if 0 <= index < len(self.cart):
            new_qty = self.cart[index]["quantity"] + delta
            if new_qty <= 0:
                self.cart.pop(index)
            else:
                self.cart[index]["quantity"] = new_qty
            self.update_cart_ui()

    def set_quantity(self, index, value):
        try:
            qty = int(value)
            if qty <= 0:
                self.cart.pop(index)
            else:
                self.cart[index]["quantity"] = qty
            self.update_cart_ui()
        except ValueError:
            pass

    def remove_item(self, index):
        if 0 <= index < len(self.cart):
            self.cart.pop(index)
            self.update_cart_ui()

    def clear_cart(self):
        self.cart.clear()
        self.cash_tendered.set(0.0)
        self.discount_percent.set(0.0)
        self.update_cart_ui()

    def confirm_clear(self):
        if self.cart and messagebox.askyesno("Clear Cart", "Are you sure you want to remove all items?"):
            self.clear_cart()

    def update_cart_ui(self):
        for widget in self.cart_inner.winfo_children():
            widget.destroy()

        if not self.cart:
            ttk.Label(self.cart_inner, text="🛒 Cart is empty", font=("Segoe UI", 12),
                      foreground="#94a3b8", background=self.BG_SECONDARY).pack(pady=40)
        else:
            for idx, item in enumerate(self.cart):
                frame = tk.Frame(self.cart_inner, bg=self.BG_SECONDARY)
                frame.pack(fill="x", padx=10, pady=6)

                subtotal = item["price"] * item["quantity"]
                info = f"{item['name']}  x{item['quantity']}  @ ₱{item['price']:.2f}  = ₱{subtotal:.2f}"
                tk.Label(frame, text=info, font=self.FONT_REGULAR, 
                        bg=self.BG_SECONDARY, anchor="w").pack(side="left", fill="x", expand=True)

                ctrl = tk.Frame(frame, bg=self.BG_SECONDARY)
                ctrl.pack(side="right")

                tk.Button(ctrl, text="−", font=("Segoe UI", 12, "bold"), width=2,
                         bg="#f1f5f9", relief="flat", 
                         command=lambda i=idx: self.update_quantity(i, -1)).pack(side="left")
                
                qty_var = tk.StringVar(value=str(item["quantity"]))
                spin = tk.Spinbox(ctrl, from_=1, to=999, width=3, textvariable=qty_var,
                                 font=self.FONT_REGULAR, 
                                 command=lambda i=idx, var=qty_var: self.set_quantity(i, var.get()))
                spin.pack(side="left", padx=4)
                qty_var.trace("w", lambda *args, i=idx, var=qty_var: self.set_quantity(i, var.get()))
                
                tk.Button(ctrl, text="+", font=("Segoe UI", 12, "bold"), width=2,
                         bg="#f1f5f9", relief="flat", 
                         command=lambda i=idx: self.update_quantity(i, 1)).pack(side="left")
                
                tk.Button(ctrl, text="✕", font=("Segoe UI", 10, "bold"), width=2,
                         bg=self.BG_SECONDARY, fg=self.DANGER, relief="flat",
                         command=lambda i=idx: self.remove_item(i)).pack(side="left", padx=5)

        subtotal = sum(item["price"] * item["quantity"] for item in self.cart)
        tax_amount = subtotal * (self.tax_rate.get() / 100)
        discount_amount = subtotal * (self.discount_percent.get() / 100)
        total = subtotal + tax_amount - discount_amount

        if self.role == "cashier":
            self.total_var.set(f"Total: ₱{total:.2f}")
        else:
            self.total_var.set(f"Sub: ₱{subtotal:.2f}  Tax: ₱{tax_amount:.2f}  Disc: -₱{discount_amount:.2f}\nTotal: ₱{total:.2f}")

        cash = self.cash_tendered.get()
        change = cash - total if cash > total else 0
        self.change_var.set(f"Change: ₱{change:.2f}" if change > 0 else "⚠️ Insufficient cash")

        self.cart_inner.update_idletasks()
        self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))

    def show_receipt(self):
        """Display receipt and complete transaction - FIXED VERSION"""
        if not self.cart:
            messagebox.showwarning("Empty Cart", "No items to checkout.")
            return

        subtotal = sum(item["price"] * item["quantity"] for item in self.cart)
        tax = subtotal * (self.tax_rate.get() / 100)
        discount = subtotal * (self.discount_percent.get() / 100)
        total = subtotal + tax - discount
        cash = self.cash_tendered.get()
        
        # Check if cash is sufficient
        if cash < total:
            messagebox.showerror("Payment Error", f"Insufficient cash. Total is ₱{total:.2f}, you entered ₱{cash:.2f}.")
            return
        
        change = cash - total

        # Save transaction to CENTRALIZED transactions
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total,
            "subtotal": subtotal,
            "tax": tax,
            "discount": discount,
            "item_count": sum(item["quantity"] for item in self.cart),
            "items": self.cart.copy(),
            "cashier": self.username,
            "role": self.role
        }
        TRANSACTIONS.append(transaction)
        self.save_all_data()

        # Generate receipt
        receipt_no = datetime.now().strftime("%Y%m%d%H%M%S")
        receipt_lines = []
        receipt_lines.append("=" * 50)
        receipt_lines.append("          🏪 VREJJ CONVENIENCE STORE")
        receipt_lines.append("         PATAG BULUA, CAGAYAN DE ORO CITY")
        receipt_lines.append("           CEL: 0926-332-0708")
        receipt_lines.append("=" * 50)
        receipt_lines.append(f"Receipt No: {receipt_no}")
        receipt_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        receipt_lines.append(f"Cashier: {self.username} ({self.role})")
        receipt_lines.append("-" * 50)
        receipt_lines.append(f"{'Item':<22} {'Qty':>4} {'Price':>8} {'Total':>10}")
        receipt_lines.append("-" * 50)

        for item in self.cart:
            line_total = item["price"] * item["quantity"]
            name = item["name"][:20] + ".." if len(item["name"]) > 22 else item["name"]
            receipt_lines.append(f"{name:<22} {item['quantity']:>4}  ₱{item['price']:>6.2f}  ₱{line_total:>8.2f}")

        receipt_lines.append("-" * 50)
        receipt_lines.append(f"{'Subtotal':<38} ₱{subtotal:>8.2f}")
        receipt_lines.append(f"{'Tax (' + str(self.tax_rate.get()) + '%):':<38} ₱{tax:>8.2f}")
        if discount > 0:
            receipt_lines.append(f"{'Discount (' + str(self.discount_percent.get()) + '%):':<38} -₱{discount:>7.2f}")
        receipt_lines.append(f"{'TOTAL':<38} ₱{total:>8.2f}")
        receipt_lines.append("-" * 50)
        receipt_lines.append(f"{'Cash Tendered':<38} ₱{cash:>8.2f}")
        receipt_lines.append(f"{'Change Due':<38} ₱{change:>8.2f}")
        receipt_lines.append("=" * 50)
        receipt_lines.append("       Thank you for shopping with us!")
        receipt_lines.append("              Have a great day!")
        receipt_lines.append("=" * 50)

        receipt_text = "\n".join(receipt_lines)

        # Create receipt window
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Receipt")
        receipt_window.geometry("550x600")
        receipt_window.configure(bg="#f8fafc")

        # Make sure receipt window is on top
        receipt_window.transient(self.root)
        receipt_window.grab_set()
        receipt_window.focus_force()

        # Text frame with scrollbars
        text_frame = tk.Frame(receipt_window, bg="#f8fafc")
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        text_widget = tk.Text(text_frame, wrap="none", font=("Courier New", 10), 
                              bg="white", fg="#1e293b")
        scrollbar_y = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        scrollbar_x = ttk.Scrollbar(receipt_window, orient="horizontal", command=text_widget.xview)
        text_widget.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        text_widget.insert("1.0", receipt_text)
        text_widget.configure(state="disabled")

        # Buttons
        btn_frame = tk.Frame(receipt_window, bg="#f8fafc")
        btn_frame.pack(fill="x", pady=10)

        def close_receipt():
            receipt_window.destroy()
            self.clear_cart()
            messagebox.showinfo("Success", "✅ Transaction completed successfully!")

        def print_receipt():
            self.root.clipboard_clear()
            self.root.clipboard_append(receipt_text)
            messagebox.showinfo("Receipt", "✅ Receipt copied to clipboard! You can paste it anywhere to print.")

        tk.Button(btn_frame, text="🖨️ Print / Copy", command=print_receipt, 
                 bg="#3b82f6", fg="white", font=self.FONT_BUTTON, padx=15, pady=5, 
                 relief="flat").pack(side="left", padx=10)
        tk.Button(btn_frame, text="❌ Close", command=close_receipt, 
                 bg="#ef4444", fg="white", font=self.FONT_BUTTON, padx=15, pady=5, 
                 relief="flat").pack(side="right", padx=10)

        # Center the receipt window
        receipt_window.update_idletasks()
        x = (receipt_window.winfo_screenwidth() // 2) - (receipt_window.winfo_width() // 2)
        y = (receipt_window.winfo_screenheight() // 2) - (receipt_window.winfo_height() // 2)
        receipt_window.geometry(f"+{x}+{y}")

    def show_sales_report(self):
        if not TRANSACTIONS:
            messagebox.showinfo("Sales Report", "No sales recorded yet.")
            return
        
        total_sales = sum(t["total"] for t in TRANSACTIONS)
        avg_sale = total_sales / len(TRANSACTIONS) if TRANSACTIONS else 0
        total_items = sum(t["item_count"] for t in TRANSACTIONS)
        
        report_window = tk.Toplevel(self.root)
        report_window.title("Sales Report")
        report_window.geometry("600x500")
        report_window.configure(bg="#f8fafc")
        
        report_text = tk.Text(report_window, wrap="word", font=("Courier New", 10))
        scrollbar = ttk.Scrollbar(report_window, orient="vertical", command=report_text.yview)
        report_text.configure(yscrollcommand=scrollbar.set)
        report_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        report_content = f"""
{'='*50}
📊 CENTRALIZED SALES REPORT
{'='*50}

Total Transactions: {len(TRANSACTIONS)}
Total Revenue: ₱{total_sales:,.2f}
Average Sale: ₱{avg_sale:,.2f}
Total Items Sold: {total_items}

{'='*50}
📋 TRANSACTION DETAILS
{'='*50}

"""
        for idx, t in enumerate(TRANSACTIONS, 1):
            report_content += f"""
{idx}. {t['date']}
   Items: {t['item_count']}
   Subtotal: ₱{t['subtotal']:.2f}
   Tax: ₱{t['tax']:.2f}
   Discount: ₱{t['discount']:.2f}
   Total: ₱{t['total']:.2f}
   Cashier: {t.get('cashier', 'N/A')}
{'-'*50}
"""
        
        report_text.insert("1.0", report_content)
        report_text.configure(state="disabled")

    def show_analytics(self):
        if not TRANSACTIONS:
            messagebox.showinfo("Analytics", "No data available for analytics.")
            return
        
        total_revenue = sum(t["total"] for t in TRANSACTIONS)
        total_tax = sum(t.get("tax", 0) for t in TRANSACTIONS)
        total_discount = sum(t.get("discount", 0) for t in TRANSACTIONS)
        
        product_sales = {}
        for trans in TRANSACTIONS:
            for item in trans.get("items", []):
                name = item["name"]
                qty = item["quantity"]
                product_sales[name] = product_sales.get(name, 0) + qty
        
        top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
        
        daily_sales = {}
        for trans in TRANSACTIONS:
            date = trans["date"].split()[0]
            daily_sales[date] = daily_sales.get(date, 0) + trans["total"]
        
        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("Business Analytics")
        analytics_window.geometry("600x600")
        analytics_window.configure(bg="#f8fafc")
        
        analytics_text = tk.Text(analytics_window, wrap="word", font=("Courier New", 10))
        scrollbar = ttk.Scrollbar(analytics_window, orient="vertical", command=analytics_text.yview)
        analytics_text.configure(yscrollcommand=scrollbar.set)
        analytics_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        analytics_content = f"""
{'='*50}
📈 BUSINESS ANALYTICS (Centralized Data)
{'='*50}

💰 REVENUE SUMMARY:
   Total Revenue: ₱{total_revenue:,.2f}
   Total Tax Collected: ₱{total_tax:,.2f}
   Total Discounts Given: ₱{total_discount:,.2f}
   Net Revenue: ₱{total_revenue - total_discount:,.2f}

{'='*50}
🏆 TOP 5 BEST SELLING PRODUCTS:
{'='*50}

"""
        for i, (product, qty) in enumerate(top_products, 1):
            analytics_content += f"   {i}. {product:<20} - {qty} units\n"
        
        analytics_content += f"""
{'='*50}
📅 DAILY SALES BREAKDOWN:
{'='*50}

"""
        for date, sales in sorted(daily_sales.items(), reverse=True)[:7]:
            analytics_content += f"   {date}: ₱{sales:,.2f}\n"
        
        analytics_content += f"""
{'='*50}
📊 PERFORMANCE METRICS:
{'='*50}

   Average Daily Revenue: ₱{total_revenue / max(len(daily_sales), 1):,.2f}
   Average Transaction Value: ₱{total_revenue / max(len(TRANSACTIONS), 1):,.2f}
   Total Transactions: {len(TRANSACTIONS)}
"""
        
        analytics_text.insert("1.0", analytics_content)
        analytics_text.configure(state="disabled")

    def open_admin_panel(self):
        if self.role != "admin":
            messagebox.showerror("Access Denied", "Only administrators can access this panel.")
            return
        
        admin_win = tk.Toplevel(self.root)
        admin_win.title("Admin Panel - Centralized Management")
        admin_win.geometry("800x600")
        admin_win.configure(bg=self.BG_MAIN)

        notebook = ttk.Notebook(admin_win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Product management tab
        product_frame = ttk.Frame(notebook)
        notebook.add(product_frame, text="📦 Manage Products (Centralized)")

        tree_frame = tk.Frame(product_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("name", "price")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        tree.heading("name", text="Product Name")
        tree.heading("price", text="Price (₱)")
        tree.column("name", width=300)
        tree.column("price", width=100)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def refresh_products():
            for row in tree.get_children():
                tree.delete(row)
            for p in PRODUCTS:
                tree.insert("", "end", values=(p["name"], f"{p['price']:.2f}"))

        refresh_products()

        form_frame = tk.Frame(product_frame, bg=self.BG_MAIN)
        form_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(form_frame, text="Product Name:", bg=self.BG_MAIN, 
                font=self.FONT_REGULAR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(form_frame, width=25, font=self.FONT_REGULAR)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Price (₱):", bg=self.BG_MAIN, 
                font=self.FONT_REGULAR).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        price_entry = tk.Entry(form_frame, width=10, font=self.FONT_REGULAR)
        price_entry.grid(row=0, column=3, padx=5, pady=5)

        def add_product():
            name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            if not name or not price_str:
                messagebox.showerror("Error", "Please enter name and price")
                return
            try:
                price = float(price_str)
            except ValueError:
                messagebox.showerror("Error", "Price must be a number")
                return
            PRODUCTS.append({"name": name, "price": price})
            refresh_products()
            self.refresh_products_display()
            self.save_all_data()
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"✅ Product '{name}' added to centralized catalog")

        def delete_product():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Select a product to delete")
                return
            item = tree.item(selected[0])
            name = item['values'][0]
            if messagebox.askyesno("Confirm Delete", f"Delete product '{name}'?"):
                for i, p in enumerate(PRODUCTS):
                    if p["name"] == name:
                        PRODUCTS.pop(i)
                        break
                refresh_products()
                self.refresh_products_display()
                self.save_all_data()
                messagebox.showinfo("Success", f"✅ Product '{name}' deleted")

        def update_product():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Select a product to update")
                return
            item = tree.item(selected[0])
            old_name = item['values'][0]
            new_name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            if not new_name or not price_str:
                messagebox.showerror("Error", "Please enter new name and price")
                return
            try:
                new_price = float(price_str)
            except ValueError:
                messagebox.showerror("Error", "Price must be a number")
                return
            for p in PRODUCTS:
                if p["name"] == old_name:
                    p["name"] = new_name
                    p["price"] = new_price
                    break
            refresh_products()
            self.refresh_products_display()
            self.save_all_data()
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"✅ Product updated to '{new_name}'")

        btn_frame = tk.Frame(product_frame, bg=self.BG_MAIN)
        btn_frame.pack(fill="x", pady=10)
        
        tk.Button(btn_frame, text="➕ Add", command=add_product, 
                 bg=self.SUCCESS, fg="white", font=self.FONT_BUTTON, 
                 padx=15, pady=5).pack(side="left", padx=5)
        tk.Button(btn_frame, text="✏️ Update", command=update_product, 
                 bg=self.ACCENT, fg="white", font=self.FONT_BUTTON, 
                 padx=15, pady=5).pack(side="left", padx=5)
        tk.Button(btn_frame, text="❌ Delete", command=delete_product, 
                 bg=self.DANGER, fg="white", font=self.FONT_BUTTON, 
                 padx=15, pady=5).pack(side="left", padx=5)

        tk.Label(product_frame, text="⚠️ Products are CENTRALIZED - changes reflect for ALL users",
                font=self.FONT_SMALL, fg=self.INFO, bg=self.BG_MAIN).pack(pady=5)

        # User management tab
        user_frame = ttk.Frame(notebook)
        notebook.add(user_frame, text="👥 Manage Users")
        
        tk.Label(user_frame, text="User Accounts Management", font=self.FONT_HEADING,
                bg=self.BG_MAIN).pack(pady=10)
        
        user_tree_frame = tk.Frame(user_frame)
        user_tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        user_tree = ttk.Treeview(user_tree_frame, columns=("username", "role", "password"), 
                                 show="headings", height=10)
        user_tree.heading("username", text="Username")
        user_tree.heading("role", text="Role")
        user_tree.heading("password", text="Password")
        user_tree.column("username", width=150)
        user_tree.column("role", width=100)
        user_tree.column("password", width=120)
        
        user_scrollbar = ttk.Scrollbar(user_tree_frame, orient="vertical", command=user_tree.yview)
        user_tree.configure(yscrollcommand=user_scrollbar.set)
        user_tree.pack(side="left", fill="both", expand=True)
        user_scrollbar.pack(side="right", fill="y")

        def refresh_users():
            for row in user_tree.get_children():
                user_tree.delete(row)
            for u, data in USERS.items():
                user_tree.insert("", "end", values=(u, data["role"], "*" * len(data["password"])))

        refresh_users()

        add_user_frame = tk.Frame(user_frame, bg=self.BG_MAIN)
        add_user_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(add_user_frame, text="Username:", font=self.FONT_REGULAR,
                bg=self.BG_MAIN).grid(row=0, column=0, padx=5, pady=5)
        new_user_entry = tk.Entry(add_user_frame, width=15, font=self.FONT_REGULAR)
        new_user_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_user_frame, text="Password:", font=self.FONT_REGULAR,
                bg=self.BG_MAIN).grid(row=0, column=2, padx=5, pady=5)
        new_pass_entry = tk.Entry(add_user_frame, width=15, show="*", font=self.FONT_REGULAR)
        new_pass_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(add_user_frame, text="Role:", font=self.FONT_REGULAR,
                bg=self.BG_MAIN).grid(row=0, column=4, padx=5, pady=5)
        role_combo = ttk.Combobox(add_user_frame, values=["cashier", "manager", "admin"], 
                                  width=10)
        role_combo.grid(row=0, column=5, padx=5, pady=5)

        def add_user():
            uname = new_user_entry.get().strip()
            pwd = new_pass_entry.get().strip()
            role = role_combo.get()
            if not uname or not pwd or not role:
                messagebox.showerror("Error", "All fields required")
                return
            if uname in USERS:
                messagebox.showerror("Error", "Username already exists")
                return
            USERS[uname] = {"password": pwd, "role": role}
            refresh_users()
            self.save_all_data()
            new_user_entry.delete(0, tk.END)
            new_pass_entry.delete(0, tk.END)
            role_combo.set("")
            messagebox.showinfo("Success", f"✅ User '{uname}' added")

        def delete_user():
            selected = user_tree.selection()
            if not selected:
                messagebox.showerror("Error", "Select a user to delete")
                return
            item = user_tree.item(selected[0])
            username = item['values'][0]
            if username == self.username:
                messagebox.showerror("Error", "Cannot delete your own account")
                return
            if messagebox.askyesno("Confirm Delete", f"Delete user '{username}'?"):
                del USERS[username]
                refresh_users()
                self.save_all_data()
                messagebox.showinfo("Success", f"✅ User '{username}' deleted")

        tk.Button(add_user_frame, text="➕ Add User", command=add_user, 
                 bg=self.SUCCESS, fg="white", font=self.FONT_BUTTON, 
                 padx=15, pady=5).grid(row=1, column=0, columnspan=3, pady=10)
        tk.Button(add_user_frame, text="❌ Delete User", command=delete_user, 
                 bg=self.DANGER, fg="white", font=self.FONT_BUTTON, 
                 padx=15, pady=5).grid(row=1, column=3, columnspan=3, pady=10)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.save_all_data()
            self.root.destroy()
            login = LoginWindow()
            login.login_root.mainloop()

    def bind_shortcuts(self):
        self.root.bind("<Control-c>", lambda e: self.confirm_clear())
        self.root.bind("<Control-x>", lambda e: self.show_receipt())
        self.root.bind("<F1>", lambda e: self.show_sales_report() if self.role in ["manager", "admin"] else None)

    def run(self):
        self.root.mainloop()

# ---------- Run the Application ----------
if __name__ == "__main__":
    login = LoginWindow()
    login.login_root.mainloop()
