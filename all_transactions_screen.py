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
        self.window.state('zoomed')
        self.window.transient(self.master)
        self.window.grab_set()

        self._create_widgets()
        self._load_transactions()

    def _create_widgets(self):
        control_frame = ttk.Frame(self.window, padding="10")
        control_frame.pack(fill=tk.X)

        export_button = ttk.Button(
            control_frame,
            text="Export",
            command=self._show_export_dropdown,
            style="Export.TButton"
        )
        export_button.pack(side=tk.RIGHT, padx=(10, 0))

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
            background=[('active', "#2ECC71")],
            foreground=[('active', "white")]
        )

        self.transactions_tree = ttk.Treeview(self.window, columns=("Date", "Category", "Amount"), show="headings")
        self.transactions_tree.heading("Date", text="Date")
        self.transactions_tree.heading("Category", text="Category")
        self.transactions_tree.heading("Amount", text="Amount")
        self.transactions_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.transactions_tree.heading("Date", command=lambda: self._sort_column("Date", False))
        self.transactions_tree.heading("Category", command=lambda: self._sort_column("Category", False))
        self.transactions_tree.heading("Amount", command=lambda: self._sort_column("Amount", False))

        self.transactions_tree.column("Date", anchor=tk.W, width=150)
        self.transactions_tree.column("Category", anchor=tk.W, width=200)
        self.transactions_tree.column("Amount", anchor=tk.E, width=150)

        self.transactions_tree.column("Date", minwidth=50)
        self.transactions_tree.column("Category", minwidth=50)
        self.transactions_tree.column("Amount", minwidth=50)

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

        all_expenses.sort(key=lambda x: datetime.fromisoformat(x['date']), reverse=True)

        if not all_expenses:
            self.transactions_tree.insert("", "end", values=("", "No transactions yet", ""))
        else:
            for expense in all_expenses:
                display_date = datetime.fromisoformat(expense['date']).strftime("%Y-%m-%d")
                category = expense['category'].capitalize()
                amount = expense['amount']
                amount_text = f"-{currency_symbol}{amount:,.2f}"
                self.transactions_tree.insert("", "end", values=(display_date, category, amount_text))

    def _sort_column(self, col, reverse):
        l = [(self.transactions_tree.set(k, col), k) for k in self.transactions_tree.get_children('')]
        
        if col == "Date":
            l.sort(key=lambda t: datetime.strptime(t[0], "%Y-%m-%d"), reverse=reverse)
        elif col == "Amount":
            l.sort(key=lambda t: float(t[0].replace(config.CURRENCY_SYMBOLS.get(self.auth_manager.get_current_user_data().get('currency', 'INR'), '₹'), '').replace(',', '')), reverse=reverse)
        else:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.transactions_tree.move(k, '', index)
        
        self.transactions_tree.heading(col, command=lambda: self._sort_column(col, not reverse))

    def _export_to_csv(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Transactions as CSV"
            )
            if not file_path:
                return

            user_data = self.auth_manager.get_current_user_data()
            all_expenses = user_data.get('expenses', [])

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['date', 'category', 'amount', 'account', 'timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for expense in all_expenses:
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
            if not file_path:
                return

            user_data = self.auth_manager.get_current_user_data()
            all_expenses = user_data.get('expenses', [])
            currency_code = user_data.get('currency', 'INR')
            currency_symbol = config.CURRENCY_SYMBOLS.get(currency_code, '₹')
            
            pdf_currency_prefix = {
                'INR': 'Rs.',
                'USD': '$',
                'EUR': 'EUR',
                'GBP': 'GBP',
                'JPY': 'JPY',
                'AUD': 'A$',
                'CAD': 'C$',
                'CHF': 'CHF',
                'CNY': 'CNY',
                'SEK': 'SEK',
                'NZD': 'NZ$',
                'MXN': 'Mex$',
                'SGD': 'S$',
                'HKD': 'HK$',
                'NOK': 'NOK',
                'KRW': 'KRW',
                'TRY': 'TRY',
                'RUB': 'RUB',
                'BRL': 'R$',
                'ZAR': 'R',
                'AED': 'AED',
                'SAR': 'SAR',
                'QAR': 'QAR',
                'THB': 'THB',
                'MYR': 'RM',
                'IDR': 'Rp',
                'PHP': 'PHP',
                'PLN': 'PLN',
                'DKK': 'DKK',
                'HUF': 'Ft',
                'CZK': 'CZK',
                'ILS': 'ILS',
            }
            pdf_currency = pdf_currency_prefix.get(currency_code, currency_code)

            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("All Transactions", styles['h1']))
            story.append(Paragraph("<br/><br/>", styles['Normal']))

            data = [["Date", "Category", "Amount", "Account", "Timestamp"]]
            for expense in all_expenses:
                display_date = datetime.fromisoformat(expense['date']).strftime("%Y-%m-%d")
                category = expense['category'].capitalize()
                amount = f"{pdf_currency} {expense['amount']:.2f}"
                account = expense.get('account', 'N/A')
                timestamp = expense.get('timestamp', 'N/A')
                data.append([display_date, category, amount, account, timestamp])

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

        try:
            x = self.window.winfo_pointerx()
            y = self.window.winfo_pointery()
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()
        
def display_all_transactions_screen(master, auth_manager, app_instance):
    AllTransactionsScreen(master, auth_manager, app_instance)
