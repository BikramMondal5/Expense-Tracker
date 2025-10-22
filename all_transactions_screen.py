import tkinter as tk
from tkinter import ttk
from datetime import datetime
import config

class AllTransactionsScreen:
    def __init__(self, master, auth_manager, app_instance):
        self.master = master
        self.auth_manager = auth_manager
        self.app_instance = app_instance
        self.window = tk.Toplevel(self.master)
        self.window.title("All Transactions")
        # Make the window full screen
        self.window.state('zoomed') # For Windows. For other OS, might need self.window.attributes('-fullscreen', True)
        # self.window.geometry("800x600") # Remove fixed geometry
        self.window.transient(self.master)
        self.window.grab_set()

        self._create_widgets()
        self._load_transactions()

    def _create_widgets(self):
        # Frame for search and filter
        control_frame = ttk.Frame(self.window, padding="10")
        control_frame.pack(fill=tk.X)

        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._filter_transactions)
        
        # Search button (optional, can be implicit with KeyRelease)
        # ttk.Button(control_frame, text="Search", command=self._filter_transactions).pack(side=tk.LEFT)

        # Treeview for transactions
        self.transactions_tree = ttk.Treeview(self.window, columns=("Date", "Category", "Amount"), show="headings")
        self.transactions_tree.heading("Date", text="Date")
        self.transactions_tree.heading("Category", text="Category")
        self.transactions_tree.heading("Amount", text="Amount")
        self.transactions_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bindings for sorting
        self.transactions_tree.heading("Date", command=lambda: self._sort_column("Date", False))
        self.transactions_tree.heading("Category", command=lambda: self._sort_column("Category", False))
        self.transactions_tree.heading("Amount", command=lambda: self._sort_column("Amount", False))

        # Adjust column widths dynamically
        self.transactions_tree.column("Date", anchor=tk.W, width=150)
        self.transactions_tree.column("Category", anchor=tk.W, width=200)
        self.transactions_tree.column("Amount", anchor=tk.E, width=150)

        # Allow column resizing (already default in ttk.Treeview, but explicitly setting minwidth is good)
        self.transactions_tree.column("Date", minwidth=50)
        self.transactions_tree.column("Category", minwidth=50)
        self.transactions_tree.column("Amount", minwidth=50)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.transactions_tree, orient="vertical", command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _load_transactions(self):
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        user_data = self.auth_manager.get_current_user_data()
        all_expenses = user_data.get('expenses', [])
        currency_code = user_data.get('currency', 'INR')
        currency_symbol = config.CURRENCY_SYMBOLS.get(currency_code, '₹')

        # Sort transactions by date, newest first
        all_expenses.sort(key=lambda x: datetime.fromisoformat(x['date']), reverse=True)

        if not all_expenses:
            self.transactions_tree.insert("", "end", values=("", "No transactions yet", ""))
        else:
            for expense in all_expenses:
                display_date = datetime.fromisoformat(expense['date']).strftime("%Y-%m-%d")
                category = expense['category'].capitalize()
                amount = expense['amount']
                amount_text = f"-{currency_symbol}{amount:,.2f}" # Assuming all are expenses for now
                self.transactions_tree.insert("", "end", values=(display_date, category, amount_text))

    def _filter_transactions(self, event=None):
        search_term = self.search_var.get().lower()

        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        user_data = self.auth_manager.get_current_user_data()
        all_expenses = user_data.get('expenses', [])
        currency_code = user_data.get('currency', 'INR')
        currency_symbol = config.CURRENCY_SYMBOLS.get(currency_code, '₹')

        filtered_expenses = [
            exp for exp in all_expenses
            if search_term in exp.get('category', '').lower() or \
               search_term in str(exp.get('amount', '')).lower() or \
               search_term in exp.get('date', '').lower()
        ]
        
        filtered_expenses.sort(key=lambda x: datetime.fromisoformat(x['date']), reverse=True)

        if not filtered_expenses:
            self.transactions_tree.insert("", "end", values=("", "No matching transactions", ""))
        else:
            for expense in filtered_expenses:
                display_date = datetime.fromisoformat(expense['date']).strftime("%Y-%m-%d")
                category = expense['category'].capitalize()
                amount = expense['amount']
                amount_text = f"-{currency_symbol}{amount:,.2f}"
                self.transactions_tree.insert("", "end", values=(display_date, category, amount_text))

    def _sort_column(self, col, reverse):
        l = [(self.transactions_tree.set(k, col), k) for k in self.transactions_tree.get_children('')]
        
        # Handle date and amount sorting specifically
        if col == "Date":
            l.sort(key=lambda t: datetime.strptime(t[0], "%Y-%m-%d"), reverse=reverse)
        elif col == "Amount":
            # Remove currency symbol and comma for numerical sort
            l.sort(key=lambda t: float(t[0].replace(config.CURRENCY_SYMBOLS.get(self.auth_manager.get_current_user_data().get('currency', 'INR'), '₹'), '').replace(',', '')), reverse=reverse)
        else:
            l.sort(reverse=reverse)

        # rearrange items in sorted order
        for index, (val, k) in enumerate(l):
            self.transactions_tree.move(k, '', index)
        
        # Reverse sort next time
        self.transactions_tree.heading(col, command=lambda: self._sort_column(col, not reverse))

def display_all_transactions_screen(master, auth_manager, app_instance):
    AllTransactionsScreen(master, auth_manager, app_instance)
