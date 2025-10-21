import tkinter as tk
from tkinter import ttk
from datetime import datetime

class RecordsScreen:
    def __init__(self, root, auth_manager, dashboard_instance):
        self.root = root
        self.auth_manager = auth_manager
        self.dashboard_instance = dashboard_instance

        self.user_data = self.auth_manager.get_current_user_data()
        self.user_expenses = self.user_data.get('expenses', [])
        self.currency_code = self.user_data.get('currency', 'INR')
        
        self.CURRENCY_SYMBOLS = {
            "INR": "₹",
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "JPY": "¥",
            "AUD": "A$"
        }
        self.currency_symbol = self.CURRENCY_SYMBOLS.get(self.currency_code, '₹')

        self.primary_color = "#3498db" # Example color, you can get from config
        self.text_dark = "#333333"
        self.bg_light = "#f2f2f2"

        self.display_records()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def display_records(self):
        self.clear_frame()

        main_frame = tk.Frame(self.root, bg=self.bg_light)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = tk.Frame(main_frame, bg=self.primary_color)
        header_frame.pack(fill=tk.X)

        back_button = tk.Button(
            header_frame,
            text="← Back to Dashboard",
            command=self.dashboard_instance.display_dashboard,
            font=("Segoe UI", 12, "bold"),
            bg=self.primary_color,
            fg="white",
            relief=tk.FLAT,
            bd=0
        )
        back_button.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(
            header_frame,
            text="All Transactions",
            font=("Segoe UI", 18, "bold"),
            bg=self.primary_color,
            fg="white"
        ).pack(side=tk.LEFT, expand=True, pady=10)

        # Search and Filter (Placeholder for now)
        search_frame = tk.Frame(main_frame, bg=self.bg_light, padx=10, pady=10)
        search_frame.pack(fill=tk.X)

        tk.Label(search_frame, text="🔍 Search:", bg=self.bg_light, fg=self.text_dark).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=40, bd=1, relief=tk.SOLID)
        self.search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.search_entry.bind("<KeyRelease>", self.filter_transactions)

        # Transactions Table
        table_frame = tk.Frame(main_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("Date", "Category", "Account", "Amount")
        self.transactions_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=20 # Adjust height as needed
        )

        for col in columns:
            self.transactions_tree.heading(col, text=col, anchor=tk.W)
            if col == "Amount":
                self.transactions_tree.column(col, anchor=tk.E, width=100)
            else:
                self.transactions_tree.column(col, anchor=tk.W, width=150)

        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.populate_transactions_tree(self.user_expenses)

    def populate_transactions_tree(self, expenses_to_display):
        # Clear existing items
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        if not expenses_to_display:
            self.transactions_tree.insert("", "end", values=("", "No transactions to display", "", ""))
            return
        
        # Sort transactions by timestamp (most recent first)
        sorted_transactions = sorted(expenses_to_display, key=lambda x: datetime.fromisoformat(x['timestamp']), reverse=True)

        for expense in sorted_transactions:
            display_date = datetime.fromisoformat(expense['date']).strftime("%Y-%m-%d")
            category = expense['category'].capitalize()
            account = expense['account'].capitalize()
            amount = f"-{self.currency_symbol}{expense['amount']:,.2f}"
            self.transactions_tree.insert("", "end", values=(display_date, category, account, amount))

    def filter_transactions(self, event=None):
        search_term = self.search_entry.get().lower()
        filtered_expenses = []
        for expense in self.user_expenses:
            if search_term in str(expense['amount']).lower() or \
               search_term in expense['category'].lower() or \
               search_term in expense['account'].lower() or \
               search_term in expense['date'].lower():
                filtered_expenses.append(expense)
        self.populate_transactions_tree(filtered_expenses)

def display_records_screen(root, auth_manager, dashboard_instance):
    RecordsScreen(root, auth_manager, dashboard_instance)