import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ---------- Improved POS System ----------
class ModernPOS:
    def __init__(self, root):
        self.root = root
        self.root.title("✦ POINT OF SALE SYSTEM ✦")
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
        
        # ---------- EXPANDED PRODUCT LIST (30+ items) ----------
        self.products = [
            # Fruits
            {"name": " Apple", "price": 10.00},
            {"name": " Banana", "price": 15.00},
            {"name": " Orange", "price": 20.00},
            {"name": " Grape", "price": 25.00},
            {"name": " Watermelon", "price": 30.00},
            {"name": " Kiwi", "price": 35.00},
            {"name": " Strawberry", "price": 40.00},
            {"name": " Mango", "price": 45.00},
            {"name": " Pineapple", "price": 50.00},
            {"name": " Peach", "price": 28.00},
            {"name": " Cherry", "price": 60.00},
            {"name": " Blueberry", "price": 55.00},
            # Vegetables
            {"name": " Broccoli", "price": 22.00},
            {"name": " Carrot", "price": 12.00},
            {"name": " Tomato", "price": 18.00},
            {"name": " Cucumber", "price": 15.00},
            {"name": " Bell Pepper", "price": 25.00},
            {"name": " Lettuce", "price": 20.00},
            {"name": " Garlic", "price": 8.00},
            {"name": " Onion", "price": 10.00},
            # Dairy & Eggs
            {"name": " Milk (1L)", "price": 45.00},
            {"name": " Cheese (250g)", "price": 85.00},
            {"name": " Eggs (6pcs)", "price": 55.00},
            {"name": " Ice Cream", "price": 70.00},
            # Beverages
            {"name": " Coffee", "price": 120.00},
            {"name": " Tea", "price": 95.00},
            {"name": " Soda", "price": 35.00},
            {"name": " Juice", "price": 50.00},
            # Snacks & Bakery
            {"name": " Bread", "price": 40.00},
            {"name": " Croissant", "price": 55.00},
            {"name": " Cookies", "price": 65.00},
            {"name": " Chocolate Bar", "price": 45.00},
            {"name": " Pretzel", "price": 30.00},
            {"name": " Donut", "price": 35.00},
            {"name": " Sandwich", "price": 80.00},
        ]
        
        self.cart = []  # {name, price, quantity}
        self.tax_rate = tk.DoubleVar(value=10.0)   # 10% tax
        self.discount_percent = tk.DoubleVar(value=0.0)
        self.cash_tendered = tk.DoubleVar(value=0.0)

        self.setup_ui()
        self.update_cart_ui()
        self.bind_shortcuts()

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

        # Header
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

        # Tax & discount row
        settings_frame = tk.Frame(bottom_left, bg=self.BG_PRIMARY)
        settings_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(settings_frame, text="Tax %:", fg="white", bg=self.BG_PRIMARY, font=self.FONT_SMALL).grid(row=0, column=0, padx=2)
        tax_spin = tk.Spinbox(settings_frame, from_=0, to=100, increment=1, textvariable=self.tax_rate, width=5,
                              font=self.FONT_SMALL, command=self.update_cart_ui)
        tax_spin.grid(row=0, column=1, padx=2)
        tk.Label(settings_frame, text="Discount %:", fg="white", bg=self.BG_PRIMARY, font=self.FONT_SMALL).grid(row=0, column=2, padx=5)
        disc_spin = tk.Spinbox(settings_frame, from_=0, to=100, increment=1, textvariable=self.discount_percent, width=5,
                               font=self.FONT_SMALL, command=self.update_cart_ui)
        disc_spin.grid(row=0, column=3, padx=2)

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

        # Buttons
        btn_frame = tk.Frame(bottom_left, bg=self.BG_PRIMARY)
        btn_frame.pack(pady=10)
        clear_btn = tk.Button(btn_frame, text="🗑️ Clear Cart", font=self.FONT_BUTTON, bg="#334155", fg="white",
                              relief="flat", padx=15, pady=5, command=self.confirm_clear)
        clear_btn.pack(side="left", padx=10)
        checkout_btn = tk.Button(btn_frame, text="✅ Checkout", font=self.FONT_BUTTON, bg=self.SUCCESS, fg="white",
                                 relief="flat", padx=15, pady=5, command=self.show_receipt)
        checkout_btn.pack(side="left", padx=10)

        # ========== RIGHT PANEL (PRODUCTS) ==========
        self.right_frame = ttk.Frame(self.root, style="TFrame")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Header + search
        header_right = tk.Frame(self.right_frame, bg=self.BG_MAIN)
        header_right.pack(fill="x", pady=(0, 15))
        tk.Label(header_right, text="✨ PRODUCTS MENU", font=self.FONT_TITLE, fg="#0f172a", bg=self.BG_MAIN).pack(anchor="w")
        tk.Label(header_right, text="Click on any item or use Ctrl+1..8 (first 8 products)", font=self.FONT_SMALL, fg="#64748b", bg=self.BG_MAIN).pack(anchor="w")

        search_frame = tk.Frame(header_right, bg=self.BG_MAIN)
        search_frame.pack(fill="x", pady=(10, 0))
        tk.Label(search_frame, text="🔍 Search:", font=self.FONT_REGULAR, bg=self.BG_MAIN).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_products())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=self.FONT_REGULAR, width=30)
        search_entry.pack(side="left", padx=10)

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

        self.filter_products()  # Initial load

    def filter_products(self):
        # Clear existing widgets
        for widget in self.products_inner.winfo_children():
            widget.destroy()

        search_term = self.search_var.get().lower()
        filtered = [p for p in self.products if search_term in p["name"].lower()]

        # Responsive grid columns
        width = self.products_canvas.winfo_width() if self.products_canvas.winfo_width() > 100 else 600
        cols = max(2, min(4, width // 220))
        for i in range(cols):
            self.products_inner.columnconfigure(i, weight=1)

        row, col = 0, 0
        for idx, prod in enumerate(filtered):
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

            # Hover effects
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

                # Item info + subtotal
                subtotal = item["price"] * item["quantity"]
                info = f"{item['name']}  x{item['quantity']}  @ ${item['price']:.2f}  = ${subtotal:.2f}"
                tk.Label(frame, text=info, font=self.FONT_REGULAR, bg=self.BG_SECONDARY, anchor="w").pack(side="left", fill="x", expand=True)

                # Controls
                ctrl = tk.Frame(frame, bg=self.BG_SECONDARY)
                ctrl.pack(side="right")
                # Minus
                tk.Button(ctrl, text="−", font=("Segoe UI", 12, "bold"), width=2,
                          bg="#f1f5f9", relief="flat", command=lambda i=idx: self.update_quantity(i, -1)).pack(side="left")
                # Quantity spinbox (editable)
                qty_var = tk.StringVar(value=str(item["quantity"]))
                spin = tk.Spinbox(ctrl, from_=1, to=999, width=3, textvariable=qty_var,
                                  font=self.FONT_REGULAR, command=lambda i=idx, var=qty_var: self.set_quantity(i, var.get()))
                spin.pack(side="left", padx=4)
                qty_var.trace("w", lambda *args, i=idx, var=qty_var: self.set_quantity(i, var.get()))
                # Plus
                tk.Button(ctrl, text="+", font=("Segoe UI", 12, "bold"), width=2,
                          bg="#f1f5f9", relief="flat", command=lambda i=idx: self.update_quantity(i, 1)).pack(side="left")
                # Remove
                tk.Button(ctrl, text="✕", font=("Segoe UI", 10, "bold"), width=2,
                          bg=self.BG_SECONDARY, fg=self.DANGER, relief="flat",
                          command=lambda i=idx: self.remove_item(i)).pack(side="left", padx=5)

        # Calculate totals
        subtotal = sum(item["price"] * item["quantity"] for item in self.cart)
        tax_amount = subtotal * (self.tax_rate.get() / 100)
        discount_amount = subtotal * (self.discount_percent.get() / 100)
        total = subtotal + tax_amount - discount_amount
        self.total_var.set(f"Sub: ${subtotal:.2f}  Tax: ${tax_amount:.2f}  Disc: -${discount_amount:.2f}\nTotal: ${total:.2f}")

        # Update change
        cash = self.cash_tendered.get()
        change = cash - total if cash > total else 0
        self.change_var.set(f"Change: ${change:.2f}" if change > 0 else "Insufficient cash")

        # Scroll region
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

        # Generate receipt number (timestamp based)
        receipt_no = datetime.now().strftime("%Y%m%d%H%M%S")

        # Build receipt content with proper monospaced alignment
        receipt_lines = []
        receipt_lines.append("=" * 48)
        receipt_lines.append("            FRESH MART STORE")
        receipt_lines.append("         123 Main Street, Cityville")
        receipt_lines.append("           Tel: (555) 123-4567")
        receipt_lines.append("=" * 48)
        receipt_lines.append(f"Receipt No: {receipt_no}")
        receipt_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        receipt_lines.append("-" * 48)
        receipt_lines.append(f"{'Item':<22} {'Qty':>4} {'Price':>8} {'Total':>10}")
        receipt_lines.append("-" * 48)

        for item in self.cart:
            line_total = item["price"] * item["quantity"]
            # Truncate long names
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

        # Create a custom dialog with monospaced font for perfect alignment
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Receipt")
        receipt_window.geometry("500x550")
        receipt_window.resizable(False, False)
        receipt_window.configure(bg="#f8fafc")

        # Text widget with monospaced font
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

        # Button frame
        btn_frame = tk.Frame(receipt_window, bg="#f8fafc")
        btn_frame.pack(fill="x", pady=10)

        def close_receipt():
            receipt_window.destroy()
            self.clear_cart()

        def print_receipt():
            # Simple print simulation: copy to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(receipt_text)
            messagebox.showinfo("Receipt", "Receipt copied to clipboard! You can paste it anywhere to print.")

        tk.Button(btn_frame, text="Print / Copy", command=print_receipt, bg="#3b82f6", fg="white",
                  font=self.FONT_BUTTON, padx=15, pady=5, relief="flat").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Close", command=close_receipt, bg="#ef4444", fg="white",
                  font=self.FONT_BUTTON, padx=15, pady=5, relief="flat").pack(side="right", padx=10)

        # Center the window
        receipt_window.update_idletasks()
        x = (receipt_window.winfo_screenwidth() // 2) - (receipt_window.winfo_width() // 2)
        y = (receipt_window.winfo_screenheight() // 2) - (receipt_window.winfo_height() // 2)
        receipt_window.geometry(f"+{x}+{y}")

    def bind_shortcuts(self):
        # Bind Ctrl+1 to Ctrl+8 for the first 8 products (for convenience)
        for i in range(min(8, len(self.products))):
            self.root.bind(f"<Control-{i+1}>", lambda e, p=self.products[i]: self.add_to_cart(p["name"], p["price"]))

    def run(self):
        self.root.mainloop()

# ---------- Run ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernPOS(root)
    app.run()
