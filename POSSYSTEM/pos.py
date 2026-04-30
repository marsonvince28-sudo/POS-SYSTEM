import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ---------- User Database (demo) ----------
USERS = {
    "cashier1": {"password": "cash123", "role": "cashier"},
    "manager1": {"password": "mgr123", "role": "manager"},
    "admin1":   {"password": "admin123", "role": "admin"},
}

# ---------- Login Window ----------
class LoginWindow:
    def __init__(self):
        self.login_root = tk.Tk()
        self.login_root.title("POS Login")
        self.login_root.geometry("400x300")
        self.login_root.resizable(False, False)
        self.login_root.configure(bg="#f0f2f5")

        # Center the window
        self.login_root.update_idletasks()
        x = (self.login_root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.login_root.winfo_screenheight() // 2) - (300 // 2)
        self.login_root.geometry(f"+{x}+{y}")

        # UI elements
        tk.Label(self.login_root, text="POINT OF SALE SYSTEM", font=("Segoe UI", 16, "bold"),
                 bg="#f0f2f5", fg="#1e2a3a").pack(pady=20)
        tk.Label(self.login_root, text="Please log in", font=("Segoe UI", 10),
                 bg="#f0f2f5", fg="#64748b").pack(pady=(0, 20))

        frame = tk.Frame(self.login_root, bg="#f0f2f5")
        frame.pack(pady=10)

        tk.Label(frame, text="Username:", font=("Segoe UI", 11), bg="#f0f2f5").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = tk.Entry(frame, font=("Segoe UI", 11), width=20)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        self.username_entry.focus()

        tk.Label(frame, text="Password:", font=("Segoe UI", 11), bg="#f0f2f5").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = tk.Entry(frame, font=("Segoe UI", 11), width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.message_var = tk.StringVar()
        tk.Label(self.login_root, textvariable=self.message_var, fg="red", bg="#f0f2f5",
                 font=("Segoe UI", 9)).pack(pady=5)

        btn_frame = tk.Frame(self.login_root, bg="#f0f2f5")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Login", command=self.validate_login, bg="#3b82f6", fg="white",
                  font=("Segoe UI", 10, "bold"), padx=20, pady=5, relief="flat").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Exit", command=self.login_root.destroy, bg="#ef4444", fg="white",
                  font=("Segoe UI", 10, "bold"), padx=20, pady=5, relief="flat").pack(side="left", padx=10)

        self.login_root.bind("<Return>", lambda e: self.validate_login())

    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if username in USERS and USERS[username]["password"] == password:
            role = USERS[username]["role"]
            self.login_root.destroy()
            # Launch main POS with role
            root = tk.Tk()
            app = ModernPOS(root, username, role)
            app.run()
        else:
            self.message_var.set("Invalid username or password")

# ---------- Improved POS System with Roles and Logout ----------
class ModernPOS:
    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role
        self.root.title(f"✦ POINT OF SALE SYSTEM - Logged in as: {username} ({role}) ✦")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f0f2f5")

        # Colors & Fonts
        self.BG_PRIMARY = "#1e2a3a"
        self.BG_SECONDARY = "#ffffff"
        self.BG_MAIN = "#f8fafc"
        self.ACCENT = "#3b82f6"
        self.ACCENT_HOVER = "#2563eb"
        self.DANGER = "#ef4444"
        self.SUCCESS = "#10b981"
        self.WARNING = "#f59e0b"

        self.FONT_TITLE = ("Segoe UI", 20, "bold")
        self.FONT_HEADING = ("Segoe UI", 14, "bold")
        self.FONT_REGULAR = ("Segoe UI", 11)
        self.FONT_BUTTON = ("Segoe UI", 10, "bold")
        self.FONT_SMALL = ("Segoe UI", 9)

        self.setup_styles()

        # Products list (editable by admin only)
        self.products = [
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

        self.cart = []          # {name, price, quantity}
        self.tax_rate = tk.DoubleVar(value=10.0)
        self.discount_percent = tk.DoubleVar(value=0.0)
        self.cash_tendered = tk.DoubleVar(value=0.0)

        # For reports: store all completed sales (list of dicts)
        self.transactions = []

        self.setup_ui()
        self.update_cart_ui()
        self.bind_shortcuts()

        # Role-based restrictions
        self.apply_role_restrictions()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.BG_MAIN)
        style.configure("Left.TFrame", background=self.BG_PRIMARY)
        style.configure("Search.TEntry", fieldbackground="white", borderwidth=1)
        style.configure("Total.TLabel", font=("Segoe UI", 18, "bold"), foreground="#0f172a", background=self.BG_SECONDARY)
        style.configure("Heading.TLabel", font=self.FONT_HEADING, foreground="#334155", background=self.BG_SECONDARY)

    def setup_ui(self):
        # ========== LEFT PANEL (ORDER) ==========
        self.left_frame = ttk.Frame(self.root, style="Left.TFrame", width=380)
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(False)

        header_left = tk.Frame(self.left_frame, bg=self.BG_PRIMARY, height=70)
        header_left.pack(fill="x")
        tk.Label(header_left, text="🛍️ ORDER SUMMARY", font=self.FONT_TITLE, fg="white", bg=self.BG_PRIMARY).pack(pady=15)

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

        self.cart_inner.bind("<Configure>", lambda e: self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all")))
        self.cart_canvas.bind("<Configure>", lambda e: self.cart_canvas.itemconfig(self.canvas_window, width=e.width))
        self.cart_canvas.bind_all("<MouseWheel>", lambda e: self.cart_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Bottom panel with totals and payment
        bottom_left = tk.Frame(self.left_frame, bg=self.BG_PRIMARY)
        bottom_left.pack(fill="x", side="bottom", pady=10)

        # Tax & discount row (role-restricted)
        settings_frame = tk.Frame(bottom_left, bg=self.BG_PRIMARY)
        settings_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(settings_frame, text="Tax %:", fg="white", bg=self.BG_PRIMARY, font=self.FONT_SMALL).grid(row=0, column=0, padx=2)
        self.tax_spin = tk.Spinbox(settings_frame, from_=0, to=100, increment=1, textvariable=self.tax_rate, width=5,
                                   font=self.FONT_SMALL, command=self.update_cart_ui)
        self.tax_spin.grid(row=0, column=1, padx=2)
        tk.Label(settings_frame, text="Discount %:", fg="white", bg=self.BG_PRIMARY, font=self.FONT_SMALL).grid(row=0, column=2, padx=5)
        self.disc_spin = tk.Spinbox(settings_frame, from_=0, to=100, increment=1, textvariable=self.discount_percent, width=5,
                                    font=self.FONT_SMALL, command=self.update_cart_ui)
        self.disc_spin.grid(row=0, column=3, padx=2)

        # Total label
        self.total_var = tk.StringVar(value="Total: $0.00")
        total_label = tk.Label(bottom_left, textvariable=self.total_var, font=("Segoe UI", 16, "bold"),
                               fg="white", bg=self.BG_PRIMARY)
        total_label.pack(pady=(5, 5))

        # Cash tendered
        cash_frame = tk.Frame(bottom_left, bg=self.BG_PRIMARY)
        cash_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(cash_frame, text="Cash:", fg="white", bg=self.BG_PRIMARY, font=self.FONT_SMALL).pack(side="left")
        self.cash_entry = tk.Entry(cash_frame, textvariable=self.cash_tendered, width=10, font=self.FONT_REGULAR)
        self.cash_entry.pack(side="left", padx=5)
        self.change_var = tk.StringVar(value="Change: $0.00")
        tk.Label(cash_frame, textvariable=self.change_var, fg="#86efac", bg=self.BG_PRIMARY, font=self.FONT_SMALL).pack(side="left", padx=10)

        # Buttons row (Clear Cart, Checkout, Logout)
        btn_frame = tk.Frame(bottom_left, bg=self.BG_PRIMARY)
        btn_frame.pack(pady=10)
        clear_btn = tk.Button(btn_frame, text="🗑️ Clear Cart", font=self.FONT_BUTTON, bg="#334155", fg="white",
                              relief="flat", padx=15, pady=5, command=self.confirm_clear)
        clear_btn.pack(side="left", padx=5)
        self.checkout_btn = tk.Button(btn_frame, text="✅ Checkout", font=self.FONT_BUTTON, bg=self.SUCCESS, fg="white",
                                      relief="flat", padx=15, pady=5, command=self.show_receipt)
        self.checkout_btn.pack(side="left", padx=5)
        logout_btn = tk.Button(btn_frame, text="🚪 Logout", font=self.FONT_BUTTON, bg=self.WARNING, fg="white",
                               relief="flat", padx=15, pady=5, command=self.logout)
        logout_btn.pack(side="left", padx=5)

        # ========== RIGHT PANEL (PRODUCTS) ==========
        self.right_frame = ttk.Frame(self.root, style="TFrame")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        header_right = tk.Frame(self.right_frame, bg=self.BG_MAIN)
        header_right.pack(fill="x", pady=(0, 15))
        tk.Label(header_right, text="✨ PRODUCTS MENU", font=self.FONT_TITLE, fg="#0f172a", bg=self.BG_MAIN).pack(anchor="w")
        tk.Label(header_right, text="Click on any item or use Ctrl+1..8 (first 8 products)", font=self.FONT_SMALL, fg="#64748b", bg=self.BG_MAIN).pack(anchor="w")

        # Search and extra buttons row
        top_bar = tk.Frame(header_right, bg=self.BG_MAIN)
        top_bar.pack(fill="x", pady=(10, 0))

        search_frame = tk.Frame(top_bar, bg=self.BG_MAIN)
        search_frame.pack(side="left", fill="x", expand=True)
        tk.Label(search_frame, text="🔍 Search:", font=self.FONT_REGULAR, bg=self.BG_MAIN).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_products())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=self.FONT_REGULAR, width=30)
        search_entry.pack(side="left", padx=10)

        # Admin/Manager buttons (report, admin panel)
        self.report_btn = None
        self.admin_panel_btn = None
        if self.role in ["manager", "admin"]:
            self.report_btn = tk.Button(top_bar, text="📊 Sales Report", font=self.FONT_BUTTON,
                                        bg=self.WARNING, fg="white", relief="flat", padx=10, pady=3,
                                        command=self.show_sales_report)
            self.report_btn.pack(side="right", padx=5)
        if self.role == "admin":
            self.admin_panel_btn = tk.Button(top_bar, text="🔧 Admin Panel", font=self.FONT_BUTTON,
                                             bg=self.ACCENT, fg="white", relief="flat", padx=10, pady=3,
                                             command=self.open_admin_panel)
            self.admin_panel_btn.pack(side="right", padx=5)

        # Products grid container
        self.products_canvas = tk.Canvas(self.right_frame, bg=self.BG_MAIN, highlightthickness=0)
        products_scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.products_canvas.yview)
        self.products_inner = tk.Frame(self.products_canvas, bg=self.BG_MAIN)
        self.products_canvas.create_window((0, 0), window=self.products_inner, anchor="nw")
        self.products_canvas.configure(yscrollcommand=products_scrollbar.set)
        self.products_canvas.pack(side="left", fill="both", expand=True)
        products_scrollbar.pack(side="right", fill="y")

        self.products_inner.bind("<Configure>", lambda e: self.products_canvas.configure(scrollregion=self.products_canvas.bbox("all")))
        self.products_canvas.bind("<Configure>", lambda e: self.products_canvas.itemconfig("all", width=e.width))

        self.filter_products()

    def apply_role_restrictions(self):
        """Disable features based on role."""
        if self.role == "cashier":
            # Cashier cannot change tax/discount
            self.tax_spin.config(state="disabled")
            self.disc_spin.config(state="disabled")
        elif self.role == "manager":
            self.tax_spin.config(state="normal")
            self.disc_spin.config(state="normal")
        elif self.role == "admin":
            self.tax_spin.config(state="normal")
            self.disc_spin.config(state="normal")

    # ---------- Logout ----------
    def logout(self):
        """Close the POS window and return to login screen."""
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.root.destroy()
            # Re-open login window
            login = LoginWindow()
            login.login_root.mainloop()

    # ---------- Admin Panel ----------
    def open_admin_panel(self):
        admin_win = tk.Toplevel(self.root)
        admin_win.title("Admin Panel")
        admin_win.geometry("700x500")
        admin_win.configure(bg=self.BG_MAIN)

        notebook = ttk.Notebook(admin_win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Product management tab
        product_frame = ttk.Frame(notebook)
        notebook.add(product_frame, text="Manage Products")

        # Treeview for products
        tree_frame = tk.Frame(product_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        columns = ("name", "price")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        tree.heading("name", text="Product Name")
        tree.heading("price", text="Price ($)")
        tree.column("name", width=250)
        tree.column("price", width=100)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def refresh_products():
            for row in tree.get_children():
                tree.delete(row)
            for p in self.products:
                tree.insert("", "end", values=(p["name"], f"{p['price']:.2f}"))

        refresh_products()

        # Add/Edit product form
        form_frame = tk.Frame(product_frame, bg=self.BG_MAIN)
        form_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(form_frame, text="Name:", bg=self.BG_MAIN).grid(row=0, column=0, padx=5, pady=2, sticky="e")
        name_entry = tk.Entry(form_frame, width=25)
        name_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Price:", bg=self.BG_MAIN).grid(row=0, column=2, padx=5, pady=2, sticky="e")
        price_entry = tk.Entry(form_frame, width=10)
        price_entry.grid(row=0, column=3, padx=5, pady=2)

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
            self.products.append({"name": name, "price": price})
            refresh_products()
            self.filter_products()
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Product '{name}' added")

        def delete_product():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Select a product to delete")
                return
            item = tree.item(selected[0])
            name = item['values'][0]
            if messagebox.askyesno("Confirm Delete", f"Delete product '{name}'?"):
                for i, p in enumerate(self.products):
                    if p["name"] == name:
                        self.products.pop(i)
                        break
                refresh_products()
                self.filter_products()
                messagebox.showinfo("Success", f"Product '{name}' deleted")

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
            for p in self.products:
                if p["name"] == old_name:
                    p["name"] = new_name
                    p["price"] = new_price
                    break
            refresh_products()
            self.filter_products()
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Product updated to '{new_name}'")

        btn_frame = tk.Frame(product_frame, bg=self.BG_MAIN)
        btn_frame.pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Add", command=add_product, bg=self.SUCCESS, fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update", command=update_product, bg=self.ACCENT, fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete", command=delete_product, bg=self.DANGER, fg="white").pack(side="left", padx=5)

        # User management tab (admin only)
        user_frame = ttk.Frame(notebook)
        notebook.add(user_frame, text="Manage Users")
        tk.Label(user_frame, text="User accounts (demo - hardcoded)", font=self.FONT_HEADING).pack(pady=10)
        user_tree = ttk.Treeview(user_frame, columns=("username", "role"), show="headings", height=8)
        user_tree.heading("username", text="Username")
        user_tree.heading("role", text="Role")
        user_tree.pack(fill="both", expand=True, padx=10, pady=5)

        def refresh_users():
            for row in user_tree.get_children():
                user_tree.delete(row)
            for u, data in USERS.items():
                user_tree.insert("", "end", values=(u, data["role"]))

        refresh_users()

        # Add user form (simplified)
        add_user_frame = tk.Frame(user_frame, bg=self.BG_MAIN)
        add_user_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(add_user_frame, text="New Username:").grid(row=0, column=0, padx=5, pady=2)
        new_user_entry = tk.Entry(add_user_frame, width=15)
        new_user_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(add_user_frame, text="Password:").grid(row=0, column=2, padx=5, pady=2)
        new_pass_entry = tk.Entry(add_user_frame, width=15, show="*")
        new_pass_entry.grid(row=0, column=3, padx=5, pady=2)
        tk.Label(add_user_frame, text="Role:").grid(row=0, column=4, padx=5, pady=2)
        role_combo = ttk.Combobox(add_user_frame, values=["cashier", "manager", "admin"], width=10)
        role_combo.grid(row=0, column=5, padx=5, pady=2)

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
            new_user_entry.delete(0, tk.END)
            new_pass_entry.delete(0, tk.END)
            role_combo.set("")
            messagebox.showinfo("Success", f"User '{uname}' added")

        tk.Button(add_user_frame, text="Add User", command=add_user, bg=self.SUCCESS, fg="white").grid(row=0, column=6, padx=10)

    # ---------- Reports ----------
    def show_sales_report(self):
        if not self.transactions:
            messagebox.showinfo("Sales Report", "No sales recorded yet.")
            return

        total_sales = sum(t["total"] for t in self.transactions)
        avg_sale = total_sales / len(self.transactions) if self.transactions else 0
        report = f"===== SALES REPORT =====\nTotal transactions: {len(self.transactions)}\nTotal revenue: ${total_sales:.2f}\nAverage sale: ${avg_sale:.2f}\n\nDetailed list:\n"
        for idx, t in enumerate(self.transactions, 1):
            report += f"{idx}. {t['date']} - ${t['total']:.2f} (items: {t['item_count']})\n"
        messagebox.showinfo("Sales Report", report)

    # ---------- POS Core Methods ----------
    def filter_products(self):
        for widget in self.products_inner.winfo_children():
            widget.destroy()

        search_term = self.search_var.get().lower()
        filtered = [p for p in self.products if search_term in p["name"].lower()]

        width = self.products_canvas.winfo_width() if self.products_canvas.winfo_width() > 100 else 600
        cols = max(2, min(4, width // 220))
        for i in range(cols):
            self.products_inner.columnconfigure(i, weight=1)

        row, col = 0, 0
        for prod in filtered:
            card = tk.Frame(self.products_inner, bg=self.BG_SECONDARY, relief="raised", bd=1,
                            highlightbackground="#e2e8f0", highlightthickness=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            tk.Label(card, text=prod["name"], font=("Segoe UI", 13, "bold"),
                     bg=self.BG_SECONDARY, fg="#1e293b").pack(pady=(12, 5))
            tk.Label(card, text=f"${prod['price']:.2f}", font=("Segoe UI", 12),
                     bg=self.BG_SECONDARY, fg=self.ACCENT).pack(pady=(0, 10))
            add_btn = tk.Button(card, text="➕ Add", font=self.FONT_BUTTON,
                                bg=self.ACCENT, fg="white", relief="flat", padx=15, pady=4,
                                activebackground=self.ACCENT_HOVER,
                                command=lambda p=prod: self.add_to_cart(p["name"], p["price"]))
            add_btn.pack(pady=(0, 12))

            def on_enter(e, c=card):
                c.configure(bg="#f8fafc", highlightbackground="#cbd5e1")
                for child in c.winfo_children():
                    child.configure(bg="#f8fafc")
            def on_leave(e, c=card):
                c.configure(bg=self.BG_SECONDARY, highlightbackground="#e2e8f0")
                for child in c.winfo_children():
                    child.configure(bg=self.BG_SECONDARY)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

            col += 1
            if col >= cols:
                col = 0
                row += 1

    def add_to_cart(self, name, price):
        for item in self.cart:
            if item["name"] == name:
                item["quantity"] += 1
                self.update_cart_ui()
                return
        self.cart.append({"name": name, "price": price, "quantity": 1})
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
                info = f"{item['name']}  x{item['quantity']}  @ ${item['price']:.2f}  = ${subtotal:.2f}"
                tk.Label(frame, text=info, font=self.FONT_REGULAR, bg=self.BG_SECONDARY, anchor="w").pack(side="left", fill="x", expand=True)

                ctrl = tk.Frame(frame, bg=self.BG_SECONDARY)
                ctrl.pack(side="right")

                tk.Button(ctrl, text="−", font=("Segoe UI", 12, "bold"), width=2,
                          bg="#f1f5f9", relief="flat", command=lambda i=idx: self.update_quantity(i, -1)).pack(side="left")
                qty_var = tk.StringVar(value=str(item["quantity"]))
                spin = tk.Spinbox(ctrl, from_=1, to=999, width=3, textvariable=qty_var,
                                  font=self.FONT_REGULAR, command=lambda i=idx, var=qty_var: self.set_quantity(i, var.get()))
                spin.pack(side="left", padx=4)
                qty_var.trace("w", lambda *args, i=idx, var=qty_var: self.set_quantity(i, var.get()))
                tk.Button(ctrl, text="+", font=("Segoe UI", 12, "bold"), width=2,
                          bg="#f1f5f9", relief="flat", command=lambda i=idx: self.update_quantity(i, 1)).pack(side="left")
                tk.Button(ctrl, text="✕", font=("Segoe UI", 10, "bold"), width=2,
                          bg=self.BG_SECONDARY, fg=self.DANGER, relief="flat",
                          command=lambda i=idx: self.remove_item(i)).pack(side="left", padx=5)

        subtotal = sum(item["price"] * item["quantity"] for item in self.cart)
        tax_amount = subtotal * (self.tax_rate.get() / 100)
        discount_amount = subtotal * (self.discount_percent.get() / 100)
        total = subtotal + tax_amount - discount_amount
        self.total_var.set(f"Sub: ${subtotal:.2f}  Tax: ${tax_amount:.2f}  Disc: -${discount_amount:.2f}\nTotal: ${total:.2f}")

        cash = self.cash_tendered.get()
        change = cash - total if cash > total else 0
        self.change_var.set(f"Change: ${change:.2f}" if change > 0 else "Insufficient cash")

        self.cart_inner.update_idletasks()
        self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))

    def show_receipt(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "No items to checkout.")
            return

        subtotal = sum(item["price"] * item["quantity"] for item in self.cart)
        tax = subtotal * (self.tax_rate.get() / 100)
        discount = subtotal * (self.discount_percent.get() / 100)
        total = subtotal + tax - discount
        cash = self.cash_tendered.get()
        change = cash - total if cash >= total else 0

        if cash < total:
            messagebox.showerror("Payment Error", f"Insufficient cash. Total is ${total:.2f}, you entered ${cash:.2f}.")
            return

        # Record transaction
        self.transactions.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total,
            "item_count": len(self.cart)
        })

        receipt_no = datetime.now().strftime("%Y%m%d%H%M%S")
        receipt_lines = []
        receipt_lines.append("=" * 48)
        receipt_lines.append("            VREJJ CONVENIENCE STORE")
        receipt_lines.append("         PATAG BULUA, CAGAYAN DE ORO CITY")
        receipt_lines.append("           CEL: 0926-332-0708")
        receipt_lines.append("=" * 48)
        receipt_lines.append(f"Receipt No: {receipt_no}")
        receipt_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        receipt_lines.append(f"Cashier: {self.username} ({self.role})")
        receipt_lines.append("-" * 48)
        receipt_lines.append(f"{'Item':<22} {'Qty':>4} {'Price':>8} {'Total':>10}")
        receipt_lines.append("-" * 48)

        for item in self.cart:
            line_total = item["price"] * item["quantity"]
            name = item["name"][:20] + ".." if len(item["name"]) > 22 else item["name"]
            receipt_lines.append(f"{name:<22} {item['quantity']:>4}  ${item['price']:>6.2f}  ${line_total:>8.2f}")

        receipt_lines.append("-" * 48)
        receipt_lines.append(f"{'Subtotal':<38} ${subtotal:>8.2f}")
        receipt_lines.append(f"{'Tax (' + str(self.tax_rate.get()) + '%):':<38} ${tax:>8.2f}")
        if discount > 0:
            receipt_lines.append(f"{'Discount (' + str(self.discount_percent.get()) + '%):':<38} -${discount:>7.2f}")
        receipt_lines.append(f"{'TOTAL':<38} ${total:>8.2f}")
        receipt_lines.append("-" * 48)
        receipt_lines.append(f"{'Cash Tendered':<38} ${cash:>8.2f}")
        receipt_lines.append(f"{'Change Due':<38} ${change:>8.2f}")
        receipt_lines.append("=" * 48)
        receipt_lines.append("       Thank you for shopping with us!")
        receipt_lines.append("              Have a great day!")
        receipt_lines.append("=" * 48)

        receipt_text = "\n".join(receipt_lines)

        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Receipt")
        receipt_window.geometry("500x550")
        receipt_window.resizable(False, False)
        receipt_window.configure(bg="#f8fafc")

        text_frame = tk.Frame(receipt_window, bg="#f8fafc")
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        text_widget = tk.Text(text_frame, wrap="none", font=("Courier New", 10), bg="white", fg="#1e293b")
        scrollbar_y = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        scrollbar_x = ttk.Scrollbar(receipt_window, orient="horizontal", command=text_widget.xview)
        text_widget.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        text_widget.insert("1.0", receipt_text)
        text_widget.configure(state="disabled")

        btn_frame = tk.Frame(receipt_window, bg="#f8fafc")
        btn_frame.pack(fill="x", pady=10)

        def close_receipt():
            receipt_window.destroy()
            self.clear_cart()

        def print_receipt():
            self.root.clipboard_clear()
            self.root.clipboard_append(receipt_text)
            messagebox.showinfo("Receipt", "Receipt copied to clipboard! You can paste it anywhere to print.")

        tk.Button(btn_frame, text="Print / Copy", command=print_receipt, bg="#3b82f6", fg="white",
                  font=self.FONT_BUTTON, padx=15, pady=5, relief="flat").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Close", command=close_receipt, bg="#ef4444", fg="white",
                  font=self.FONT_BUTTON, padx=15, pady=5, relief="flat").pack(side="right", padx=10)

        receipt_window.update_idletasks()
        x = (receipt_window.winfo_screenwidth() // 2) - (receipt_window.winfo_width() // 2)
        y = (receipt_window.winfo_screenheight() // 2) - (receipt_window.winfo_height() // 2)
        receipt_window.geometry(f"+{x}+{y}")

    def bind_shortcuts(self):
        for i in range(min(8, len(self.products))):
            self.root.bind(f"<Control-{i+1}>", lambda e, p=self.products[i]: self.add_to_cart(p["name"], p["price"]))

    def run(self):
        self.root.mainloop()

# ---------- Run ----------
if __name__ == "__main__":
    login = LoginWindow()
    login.login_root.mainloop()
