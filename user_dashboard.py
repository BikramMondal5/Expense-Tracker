import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import config
from tkinter import messagebox

class UserDashboard:
    def __init__(self, root, auth_manager, app_instance):
        self.root = root
        self.auth_manager = auth_manager
        self.app_instance = app_instance

        # Color scheme
        self.PRIMARY_COLOR = config.PRIMARY_COLOR
        self.SECONDARY_COLOR = config.SECONDARY_COLOR
        self.ACCENT_COLOR = config.ACCENT_COLOR
        self.BG_LIGHT = config.BG_LIGHT
        self.TEXT_DARK = config.TEXT_DARK
        self.TEXT_LIGHT = config.TEXT_LIGHT
        self.WHITE = config.WHITE
        self.SUCCESS = config.SUCCESS
        self.ERROR = config.ERROR

    def clear_frame(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_add_transaction_modal(self):
        messagebox.showinfo("Add Transaction", "Add new transaction functionality coming soon!")

    def display_dashboard(self):
        self.clear_frame()
        main_dashboard_frame = tk.Frame(self.root, bg=self.BG_LIGHT)
        main_dashboard_frame.pack(fill=tk.BOTH, expand=True)

        # Header Frame
        header_frame = tk.Frame(main_dashboard_frame, bg=self.PRIMARY_COLOR, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        header_left_frame = tk.Frame(header_frame, bg=self.PRIMARY_COLOR)
        header_left_frame.pack(side=tk.LEFT, padx=10)

        menu_icon = tk.Label(header_left_frame, text="☰", font=("Segoe UI", 20), bg=self.PRIMARY_COLOR, fg=self.WHITE)
        menu_icon.pack(side=tk.LEFT, padx=5)

        home_label = tk.Label(header_left_frame, text="Home", font=("Segoe UI", 16, "bold"), bg=self.PRIMARY_COLOR, fg=self.WHITE)
        home_label.pack(side=tk.LEFT, padx=10)

        header_right_frame = tk.Frame(header_frame, bg=self.PRIMARY_COLOR)
        header_right_frame.pack(side=tk.RIGHT, padx=10)

        notification_icon = tk.Label(header_right_frame, text="🔔", font=("Segoe UI", 20), bg=self.PRIMARY_COLOR, fg=self.WHITE)
        notification_icon.pack(side=tk.RIGHT, padx=5)

        # Navigation Tabs
        nav_frame = tk.Frame(main_dashboard_frame, bg=self.PRIMARY_COLOR)
        nav_frame.pack(fill=tk.X)

        self.accounts_btn = tk.Button(
            nav_frame,
            text="ACCOUNTS",
            font=("Segoe UI", 12, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE,
            activebackground=self.PRIMARY_COLOR,
            activeforeground=self.WHITE,
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: self.show_tab("accounts")
        )
        self.accounts_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.budgets_goals_btn = tk.Button(
            nav_frame,
            text="BUDGETS & GOALS",
            font=("Segoe UI", 12, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.TEXT_LIGHT,
            activebackground=self.PRIMARY_COLOR,
            activeforeground=self.WHITE,
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: self.show_tab("budgets_goals")
        )
        self.budgets_goals_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.tab_indicator = tk.Frame(nav_frame, height=3, bg=self.ACCENT_COLOR)

        # Content Frame (scrollable)
        content_canvas = tk.Canvas(main_dashboard_frame, bg=self.BG_LIGHT, highlightthickness=0)
        content_scrollbar = ttk.Scrollbar(main_dashboard_frame, orient="vertical", command=content_canvas.yview)
        content_scrollable_frame = tk.Frame(content_canvas, bg=self.BG_LIGHT)

        content_scrollable_frame.bind(
            "<Configure>",
            lambda e: content_canvas.configure(
                scrollregion=content_canvas.bbox("all")
            )
        )

        content_canvas.create_window((0, 0), window=content_scrollable_frame, anchor="nw")
        content_canvas.configure(yscrollcommand=content_scrollbar.set)

        content_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame to hold tab content
        self.tab_content_frame = tk.Frame(content_scrollable_frame, bg=self.BG_LIGHT)
        self.tab_content_frame.pack(fill=tk.BOTH, expand=True)

        # Initialize with accounts tab visible
        self.show_tab("accounts")

        # Floating Action Button (FAB)
        fab = tk.Button(
            main_dashboard_frame,
            text="+",
            font=("Segoe UI", 24, "bold"),
            bg=self.ACCENT_COLOR,
            fg=self.WHITE,
            relief=tk.FLAT,
            width=2,
            height=1,
            command=self.show_add_transaction_modal # To be implemented
        )
        fab.place(relx=0.95, rely=0.95, anchor=tk.SE) # Position at bottom right

    def show_tab(self, tab_name):
        # Clear existing tab content
        for widget in self.tab_content_frame.winfo_children():
            widget.destroy()

        # Reset button styles
        self.accounts_btn.config(fg=self.TEXT_LIGHT)
        self.budgets_goals_btn.config(fg=self.TEXT_LIGHT)

        if tab_name == "accounts":
            self.accounts_btn.config(fg=self.WHITE)
            self.tab_indicator.place(x=self.accounts_btn.winfo_x(), y=self.accounts_btn.winfo_y() + self.accounts_btn.winfo_height() - 3, width=self.accounts_btn.winfo_width())
            self.create_accounts_tab(self.tab_content_frame) # To be implemented
        elif tab_name == "budgets_goals":
            self.budgets_goals_btn.config(fg=self.WHITE)
            self.tab_indicator.place(x=self.budgets_goals_btn.winfo_x(), y=self.budgets_goals_btn.winfo_y() + self.budgets_goals_btn.winfo_height() - 3, width=self.budgets_goals_btn.winfo_width())
            self.create_budgets_goals_tab(self.tab_content_frame) # To be implemented
        
        # Update tab indicator position dynamically (after initial placement for correct coordinates)
        self.accounts_btn.update_idletasks()
        self.budgets_goals_btn.update_idletasks()

        if tab_name == "accounts":
            self.tab_indicator.place(x=self.accounts_btn.winfo_x(), y=self.accounts_btn.winfo_y() + self.accounts_btn.winfo_height() - 3, width=self.accounts_btn.winfo_width())
        elif tab_name == "budgets_goals":
            self.tab_indicator.place(x=self.budgets_goals_btn.winfo_x(), y=self.budgets_goals_btn.winfo_y() + self.budgets_goals_btn.winfo_height() - 3, width=self.budgets_goals_btn.winfo_width())
    
    def create_accounts_tab(self, parent_frame):
        # Accounts Header
        accounts_header_frame = tk.Frame(parent_frame, bg=self.BG_LIGHT)
        accounts_header_frame.pack(fill=tk.X, pady=(10, 5), padx=10)

        list_accounts_label = tk.Label(accounts_header_frame, text="List of accounts", font=("Segoe UI", 14, "bold"), bg=self.BG_LIGHT, fg=self.TEXT_DARK)
        list_accounts_label.pack(side=tk.LEFT, padx=5)

        settings_icon = tk.Label(accounts_header_frame, text="⚙️", font=("Segoe UI", 14), bg=self.BG_LIGHT, fg=self.TEXT_DARK, cursor="hand2")
        settings_icon.pack(side=tk.RIGHT, padx=5)

        # Accounts Cards Frame
        accounts_cards_frame = tk.Frame(parent_frame, bg=self.BG_LIGHT)
        accounts_cards_frame.pack(fill=tk.X, pady=5, padx=10)

        # Cash Account Card
        cash_card = tk.Frame(accounts_cards_frame, bg=self.PRIMARY_COLOR, padx=15, pady=15, width=200, height=100)
        cash_card.pack(side=tk.LEFT, padx=5, pady=5)
        cash_card.pack_propagate(False)

        cash_label = tk.Label(cash_card, text="Cash", font=("Segoe UI", 12, "bold"), bg=self.PRIMARY_COLOR, fg=self.WHITE)
        cash_label.pack(anchor="nw")

        cash_balance = self.auth_manager.get_current_user_data().get('cash_balance', 0.0)
        currency_symbol = self.auth_manager.get_current_user_data().get('currency_symbol', '₹')
        cash_value_label = tk.Label(cash_card, text=f"{currency_symbol} {cash_balance:.2f}", font=("Segoe UI", 18, "bold"), bg=self.PRIMARY_COLOR, fg=self.WHITE)
        cash_value_label.pack(anchor="nw", pady=5)

        # Add Account Button
        add_account_btn = tk.Button(
            accounts_cards_frame,
            text="ADD ACCOUNT",
            font=("Segoe UI", 12, "bold"),
            bg=self.WHITE,
            fg=self.PRIMARY_COLOR,
            activebackground=self.BG_LIGHT,
            activeforeground=self.PRIMARY_COLOR,
            relief=tk.FLAT,
            bd=1,
            highlightbackground=self.PRIMARY_COLOR,
            highlightthickness=1,
            padx=15,
            pady=15,
            cursor="hand2",
            command=lambda: messagebox.showinfo("Add Account", "Add new account functionality coming soon!")
        )
        add_account_btn.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Account Detail Button
        account_detail_btn = tk.Button(
            parent_frame,
            text="ACCOUNT DETAIL",
            font=("Segoe UI", 10, "bold"),
            bg=self.BG_LIGHT,
            fg=self.TEXT_DARK,
            activebackground=self.BG_LIGHT,
            activeforeground=self.TEXT_DARK,
            relief=tk.FLAT,
            bd=1,
            highlightbackground="#e0e0e0",
            highlightthickness=1,
            padx=10,
            pady=5,
            cursor="hand2",
            command=lambda: messagebox.showinfo("Account Detail", "Account detail functionality coming soon!")
        )
        account_detail_btn.pack(pady=10, padx=10, anchor="nw")

        # Expenses Structure Section (Pie Chart)
        expenses_frame = tk.Frame(parent_frame, bg=self.BG_LIGHT, bd=1, relief=tk.SOLID, highlightbackground="#e0e0e0", highlightthickness=1)
        expenses_frame.pack(fill=tk.X, padx=10, pady=10)

        expenses_header = tk.Frame(expenses_frame, bg=self.WHITE)
        expenses_header.pack(fill=tk.X, pady=5, padx=10)

        expenses_title = tk.Label(expenses_header, text="Expenses structure", font=("Segoe UI", 12, "bold"), bg=self.WHITE, fg=self.TEXT_DARK)
        expenses_title.pack(side=tk.LEFT, pady=5)

        expenses_menu_icon = tk.Label(expenses_header, text="⋮", font=("Segoe UI", 14), bg=self.WHITE, fg=self.TEXT_DARK, cursor="hand2")
        expenses_menu_icon.pack(side=tk.RIGHT, pady=5)

        last_30_days_label = tk.Label(expenses_frame, text="LAST 30 DAYS", font=("Segoe UI", 9), bg=self.WHITE, fg=self.TEXT_LIGHT)
        last_30_days_label.pack(anchor="w", padx=15)

        total_expenses_label = tk.Label(expenses_frame, text="₹1,728.00", font=("Segoe UI", 20, "bold"), bg=self.WHITE, fg=self.TEXT_DARK)
        total_expenses_label.pack(anchor="w", padx=15, pady=(0, 10))

        # Pie Chart
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100, facecolor=self.WHITE)
        data = [853, 25, 850] # Sample data
        labels = ['Food & Drinks', 'Shopping', 'Bar, cafe']
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1'] # Sample colors

        wedges, texts, autotexts = ax.pie(data, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))
        ax.set_aspect("equal")
        ax.set_title("All ₹1,728", color=self.TEXT_DARK, font='Segoe UI', fontsize=12)
        
        # Draw a white circle in the middle to make it a donut chart
        centre_circle = plt.Circle((0,0),0.60,fc='white')
        fig.gca().add_artist(centre_circle)
        
        # Legend below the chart
        legend_labels = [f'{l} ({d})' for l, d in zip(labels, data)]
        ax.legend(wedges, legend_labels, loc="lower center", bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False, fontsize=8)

        canvas = FigureCanvasTkAgg(fig, master=expenses_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        show_more_btn = tk.Button(
            expenses_frame,
            text="SHOW MORE",
            font=("Segoe UI", 10, "bold"),
            bg=self.WHITE,
            fg=self.PRIMARY_COLOR,
            activebackground=self.BG_LIGHT,
            activeforeground=self.PRIMARY_COLOR,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=lambda: messagebox.showinfo("Show More", "Show more expenses functionality coming soon!")
        )
        show_more_btn.pack(pady=(0, 10))

        # Last Records Overview Section
        last_records_frame = tk.Frame(parent_frame, bg=self.BG_LIGHT, bd=1, relief=tk.SOLID, highlightbackground="#e0e0e0", highlightthickness=1)
        last_records_frame.pack(fill=tk.X, padx=10, pady=10)

        last_records_header = tk.Frame(last_records_frame, bg=self.WHITE)
        last_records_header.pack(fill=tk.X, pady=5, padx=10)

        last_records_title = tk.Label(last_records_header, text="Last records overview", font=("Segoe UI", 12, "bold"), bg=self.WHITE, fg=self.TEXT_DARK)
        last_records_title.pack(side=tk.LEFT, pady=5)

        last_records_menu_icon = tk.Label(last_records_header, text="⋮", font=("Segoe UI", 14), bg=self.WHITE, fg=self.TEXT_DARK, cursor="hand2")
        last_records_menu_icon.pack(side=tk.RIGHT, pady=5)

        last_30_days_records_label = tk.Label(last_records_frame, text="LAST 30 DAYS", font=("Segoe UI", 9), bg=self.WHITE, fg=self.TEXT_LIGHT)
        last_30_days_records_label.pack(anchor="w", padx=15, pady=(0, 5))

        # Sample Records
        records = [
            {"category": "Electronics, accessories", "amount": "-₹853.00", "account": "Cash", "date": "Today"},
            {"category": "Groceries", "amount": "-₹25.00", "account": "Cash", "date": "Today"},
            {"category": "Bar, cafe", "amount": "-₹850.00", "account": "Cash", "date": "Today"},
        ]

        for record in records:
            record_frame = tk.Frame(last_records_frame, bg=self.WHITE, pady=5)
            record_frame.pack(fill=tk.X, padx=15, pady=2)

            category_icon = tk.Label(record_frame, text="💻", font=("Segoe UI", 14), bg=self.WHITE)
            category_icon.pack(side=tk.LEFT)

            details_frame = tk.Frame(record_frame, bg=self.WHITE)
            details_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

            category_label = tk.Label(details_frame, text=record['category'], font=("Segoe UI", 11, "bold"), bg=self.WHITE, fg=self.TEXT_DARK, anchor="w")
            category_label.pack(fill=tk.X)

            account_date_label = tk.Label(details_frame, text=f"{record['account']} • {record['date']}", font=("Segoe UI", 9), bg=self.WHITE, fg=self.TEXT_LIGHT, anchor="w")
            account_date_label.pack(fill=tk.X)

            amount_label = tk.Label(record_frame, text=record['amount'], font=("Segoe UI", 11, "bold"), bg=self.WHITE, fg=self.ERROR, anchor="e")
            amount_label.pack(side=tk.RIGHT)
        
        show_more_records_btn = tk.Button(
            last_records_frame,
            text="SHOW MORE",
            font=("Segoe UI", 10, "bold"),
            bg=self.WHITE,
            fg=self.PRIMARY_COLOR,
            activebackground=self.BG_LIGHT,
            activeforeground=self.PRIMARY_COLOR,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=lambda: messagebox.showinfo("Show More", "Show more records functionality coming soon!")
        )
        show_more_records_btn.pack(pady=(10, 10))

        # Balance Trend Section (Line Chart)
        balance_trend_frame = tk.Frame(parent_frame, bg=self.BG_LIGHT, bd=1, relief=tk.SOLID, highlightbackground="#e0e0e0", highlightthickness=1)
        balance_trend_frame.pack(fill=tk.X, padx=10, pady=10)

        balance_trend_header = tk.Frame(balance_trend_frame, bg=self.WHITE)
        balance_trend_header.pack(fill=tk.X, pady=5, padx=10)

        balance_trend_title = tk.Label(balance_trend_header, text="Balance Trend", font=("Segoe UI", 12, "bold"), bg=self.WHITE, fg=self.TEXT_DARK)
        balance_trend_title.pack(side=tk.LEFT, pady=5)

        balance_trend_menu_icon = tk.Label(balance_trend_header, text="⋮", font=("Segoe UI", 14), bg=self.WHITE, fg=self.TEXT_DARK, cursor="hand2")
        balance_trend_menu_icon.pack(side=tk.RIGHT, pady=5)

        balance_today_frame = tk.Frame(balance_trend_frame, bg=self.WHITE)
        balance_today_frame.pack(fill=tk.X, padx=15, pady=5)

        balance_today_label = tk.Label(balance_today_frame, text="TODAY", font=("Segoe UI", 9), bg=self.WHITE, fg=self.TEXT_LIGHT)
        balance_today_label.pack(side=tk.LEFT)

        balance_vs_past_label = tk.Label(balance_today_frame, text="vs past period", font=("Segoe UI", 9), bg=self.WHITE, fg=self.TEXT_LIGHT)
        balance_vs_past_label.pack(side=tk.RIGHT)

        balance_value_frame = tk.Frame(balance_trend_frame, bg=self.WHITE)
        balance_value_frame.pack(fill=tk.X, padx=15, pady=(0, 10))

        currency_symbol = self.auth_manager.get_current_user_data().get('currency_symbol', '₹')
        current_balance = self.auth_manager.get_current_user_data().get('cash_balance', 0.0)
        balance_amount_label = tk.Label(balance_value_frame, text=f"{currency_symbol}{current_balance:.2f}", font=("Segoe UI", 20, "bold"), bg=self.WHITE, fg=self.TEXT_DARK)
        balance_amount_label.pack(side=tk.LEFT)

        percentage_change_label = tk.Label(balance_value_frame, text="-58%", font=("Segoe UI", 14, "bold"), bg=self.WHITE, fg=self.ERROR)
        percentage_change_label.pack(side=tk.RIGHT)

        # Line Chart
        fig2, ax2 = plt.subplots(figsize=(4, 2.5), dpi=100, facecolor=self.WHITE)
        dates = ['Sep 16', 'Sep 26', 'Oct 6']
        values = [3000, 2500, 1272] # Sample data

        ax2.plot(dates, values, marker='o', color=self.PRIMARY_COLOR, linestyle='-')
        ax2.fill_between(dates, values, color=self.PRIMARY_COLOR, alpha=0.2)
        ax2.set_ylabel('Amount', fontsize=8)
        ax2.tick_params(axis='x', labelsize=8)
        ax2.tick_params(axis='y', labelsize=8)
        ax2.grid(True, linestyle='--', alpha=0.7)

        canvas2 = FigureCanvasTkAgg(fig2, master=balance_trend_frame)
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    
    def create_budgets_goals_tab(self, parent_frame):
        # Placeholder for Budgets & Goals tab content
        label = tk.Label(parent_frame, text="Budgets & Goals Tab Content", bg=self.BG_LIGHT, font=("Segoe UI", 16))
        label.pack(pady=50)
