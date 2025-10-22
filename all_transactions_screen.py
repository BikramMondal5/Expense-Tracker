import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import config
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

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

        # Export button with dropdown
        export_button = ttk.Button(
            control_frame,
            text="Export",
            command=self._show_export_dropdown,
            style="Export.TButton"
        )
        export_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Define style for the Export button
        s = ttk.Style()
        s.configure("Export.TButton",
            background="#2ECC71", # Green background
            foreground="white", # White text
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            focusthickness=0,
            focuscolor="none"
        )
        s.map("Export.TButton",
            background=[('active', "#2ECC71")], # Keep background green on hover
            foreground=[('active', "white")]  # Keep foreground white on hover
        )
        # We can simulate a rounded corner by using a slight padding and the flat relief.
        # The borderwidth=0 and relief='flat' helps remove default borders.
        # For a true border-radius, often an image or canvas drawing is used.
        # Given the request for a 'medium' border radius, a subtle effect is best
        # achieved through careful use of padding and color. For now, the flat relief
        # and padding will give a cleaner, block-like button.

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

    def _export_to_csv(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Transactions as CSV"
            )
            if not file_path:  # User cancelled
                return

            user_data = self.auth_manager.get_current_user_data()
            all_expenses = user_data.get('expenses', [])

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['date', 'category', 'amount', 'account', 'timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for expense in all_expenses:
                    # Ensure all fields are present, add empty string if not
                    row = {key: expense.get(key, '') for key in fieldnames}
                    writer.writerow(row)
            
            tk.messagebox.showinfo("Export Successful", f"Transactions exported to {file_path}")
        except Exception as e:
            tk.messagebox.showerror("Export Error", f"An error occurred during export: {e}")

    def _export_to_pdf(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save Transactions as PDF"
            )
            if not file_path:  # User cancelled
                return

            user_data = self.auth_manager.get_current_user_data()
            all_expenses = user_data.get('expenses', [])
            currency_code = user_data.get('currency', 'INR')
            currency_symbol = config.CURRENCY_SYMBOLS.get(currency_code, '₹')

            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Add title
            story.append(Paragraph("All Transactions", styles['h1']))
            story.append(Paragraph("<br/><br/>", styles['Normal']))

            # Prepare data for table
            data = [["Date", "Category", "Amount", "Account", "Timestamp"]]
            for expense in all_expenses:
                display_date = datetime.fromisoformat(expense['date']).strftime("%Y-%m-%d")
                category = expense['category'].capitalize()
                amount = f"{currency_symbol}{expense['amount']:.2f}"
                account = expense.get('account', 'N/A')
                timestamp = expense.get('timestamp', 'N/A')
                data.append([display_date, category, amount, account, timestamp])

            # Create table style
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(config.PRIMARY_COLOR)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(config.BG_LIGHT)),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ])
            
            # Create table and apply style
            table = Table(data)
            table.setStyle(table_style)
            story.append(table)

            doc.build(story)
            tk.messagebox.showinfo("Export Successful", f"Transactions exported to {file_path}")
        except Exception as e:
            tk.messagebox.showerror("Export Error", f"An error occurred during PDF export: {e}")

    def _show_export_dropdown(self):
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Export to CSV", command=self._export_to_csv)
        menu.add_command(label="Export to PDF", command=self._export_to_pdf)

        # Display the menu at the current mouse position
        try:
            x = self.window.winfo_pointerx()
            y = self.window.winfo_pointery()
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()
        
def display_all_transactions_screen(master, auth_manager, app_instance):
    AllTransactionsScreen(master, auth_manager, app_instance)
