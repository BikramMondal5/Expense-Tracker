import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Wedge
import config
from tkinter import messagebox
from datetime import datetime, timedelta
import math
import add_expenses # Import the new module
import records_screen # Import the new module for all transactions
from all_transactions_screen import display_all_transactions_screen
from onboarding_screen import display_onboarding_screen

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
        
        self.CURRENCY_SYMBOLS = {
            "INR": "₹",
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "JPY": "¥",
            "AUD": "A$"
        }
        
        # Extended color palette for categories
        self.CATEGORY_COLORS = {
            'Food': '#FF6B6B',
            'Transport': '#4ECDC4',
            'Entertainment': '#45B7D1',
            'Utilities': '#FFC107',
            'Shopping': '#9C27B0',
            'Others': '#95A5A6'
        }

        # Fonts - Updated hierarchy
        self.FONT_CAPTION = (config.FONT_PRIMARY, 9)
        self.FONT_BODY = (config.FONT_PRIMARY, 11, "bold") # Made font bold
        self.FONT_SM = (config.FONT_PRIMARY, 11)
        self.FONT_MD = (config.FONT_PRIMARY, 12)
        self.FONT_SUBHEADER = (config.FONT_PRIMARY, 12, "bold")
        self.FONT_HEADER = (config.FONT_PRIMARY, 14, "bold")
        self.FONT_LG = (config.FONT_PRIMARY, 14, "bold")
        self.FONT_VALUE = (config.FONT_PRIMARY, 18, "bold")
        self.FONT_KPI = (config.FONT_PRIMARY, 24, "bold")
        self.FONT_XL = (config.FONT_PRIMARY, 16, "bold")
        self.FONT_XXL = (config.FONT_PRIMARY, 20, "bold")
        self.FONT_3XL = (config.FONT_PRIMARY, 24, "bold")
        self.FONT_TITLE = (config.FONT_PRIMARY, 24, "bold")

        self.dark_mode_enabled = tk.BooleanVar(value=False)
        self.hide_amounts_enabled = tk.BooleanVar(value=False)

    def _calculate_expense_summary(self, expenses, days=30):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days - 1)

        # Filter expenses for summary statistics (total spent, categories) within the specified days and up to now
        summary_filtered_expenses = [exp for exp in expenses if start_date <= datetime.fromisoformat(exp['date']) <= end_date]

        total_spent = sum(item['amount'] for item in summary_filtered_expenses)
        
        category_breakdown = {}
        for item in summary_filtered_expenses:
            category = item['category'].capitalize() # Ensure consistent capitalization
            category_breakdown[category] = category_breakdown.get(category, 0) + item['amount']

        # Sort categories by amount spent for consistent display
        sorted_categories = sorted(category_breakdown.items(), key=lambda item: item[1], reverse=True)

        # For recent transactions, sort all expenses by timestamp and take the latest 6, without date range filtering.
        # This ensures newly added (past or future) transactions appear if they are truly the most recent additions.
        all_expenses_sorted_by_timestamp = sorted(expenses, key=lambda x: datetime.fromisoformat(x['timestamp']), reverse=True)
        recent_transactions = all_expenses_sorted_by_timestamp[:6]

        return total_spent, sorted_categories, recent_transactions

    def toggle_dark_mode(self):
        """Toggle dark mode"""
        self.dark_mode_enabled.set(not self.dark_mode_enabled.get())
        if self.dark_mode_enabled.get():
            messagebox.showinfo("Dark Mode", "Dark mode enabled (UI colors not yet implemented).")
        else:
            messagebox.showinfo("Dark Mode", "Dark mode disabled.")

    def toggle_hide_amounts(self):
        """Toggle hiding of amounts"""
        self.hide_amounts_enabled.set(not self.hide_amounts_enabled.get())
        if self.hide_amounts_enabled.get():
            messagebox.showinfo("Hide Amounts", "Amounts are now hidden.")
        else:
            messagebox.showinfo("Hide Amounts", "Amounts are now visible.")

    def clear_frame(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_add_transaction_modal(self):
        add_expenses.display_add_expense_screen(self.root, self.auth_manager, self)

    def show_add_income_modal(self):
        # TODO: Implement add income screen
        from tkinter import messagebox
        messagebox.showinfo("Coming Soon", "Add Income feature will be implemented soon!")

    def show_budget_window(self):
        """Show the budget setup window (same as onboarding)"""
        display_onboarding_screen(
            self.root, 
            self.auth_manager, 
            self,
            self.PRIMARY_COLOR,
            self.SECONDARY_COLOR,
            self.ACCENT_COLOR,
            self.BG_LIGHT,
            self.TEXT_DARK,
            self.TEXT_LIGHT,
            self.WHITE,
            self.SUCCESS,
            self.ERROR
        )
        
    def show_add_budget_modal(self):
        # Open the budget window (re-uses onboarding logic)
        self.show_budget_window()
        
    def show_edit_budget_modal(self):
        """Open a modal to edit the user's monthly budget and currency."""
        user_data = self.auth_manager.get_current_user_data() or {}
        current_budget = user_data.get('monthly_budget', 0.0) or 0.0
        current_currency = user_data.get('currency', 'INR')

        modal = tk.Toplevel(self.root)
        modal.title("Edit Monthly Budget")
        modal.geometry("420x300")
        modal.resizable(False, False)
        modal.transient(self.root)
        modal.grab_set()

        # Center modal
        modal.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 420) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 300) // 2
        modal.geometry(f"420x300+{x}+{y}")

        frame = tk.Frame(modal, bg=self.WHITE, padx=16, pady=12)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Monthly Budget", font=self.FONT_HEADER, bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w")
        tk.Label(frame, text="Set or update your monthly budget and currency.", font=self.FONT_SM, bg=self.WHITE, fg=self.TEXT_LIGHT).pack(anchor="w", pady=(0,8))

        # Currency selector
        currency_options = [
            "INR - Indian Rupee (₹)", "USD - US Dollar ($)", "EUR - Euro (€)",
            "GBP - British Pound (£)", "JPY - Japanese Yen (¥)", "AUD - Australian Dollar ($)"
        ]
        # Prefer the verbose option (e.g. "INR - Indian Rupee (₹)") if available
        default_currency_option = next((opt for opt in currency_options if opt.startswith(current_currency)), currency_options[0])
        currency_var = tk.StringVar(value=default_currency_option)
        currency_menu = tk.OptionMenu(frame, currency_var, *currency_options)
        currency_menu.config(font=self.FONT_SM, bd=0, relief=tk.FLAT)
        currency_menu.pack(fill=tk.X, pady=(6, 12))

        # Budget entry
        tk.Label(frame, text="Amount", font=self.FONT_SUBHEADER, bg=self.WHITE, fg=self.TEXT_DARK).pack(anchor="w")
        budget_var = tk.StringVar(value=f"{current_budget:.2f}" if current_budget else "0")
        budget_entry = tk.Entry(frame, textvariable=budget_var, font=(config.FONT_PRIMARY, 16), bd=1, relief=tk.SOLID)
        budget_entry.pack(fill=tk.X, pady=(6, 12))

        button_frame = tk.Frame(frame, bg=self.WHITE)
        button_frame.pack(fill=tk.X, pady=(6,0))

        def apply_budget():
            val = budget_var.get().strip()
            if val == "":
                messagebox.showerror("Error", "Please enter a budget amount")
                return
            # Allow commas
            try:
                # Accept values like "1,000" or "1000.50"
                parsed = float(val.replace(",", ""))
                if parsed < 0:
                    messagebox.showerror("Error", "Budget cannot be negative")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for budget")
                return

            # Use the same format as onboarding: currency full string
            success, msg = self.auth_manager.onboard_user(val, currency_var.get())
            if success:
                messagebox.showinfo("Success", msg)
                modal.destroy()
                # Refresh dashboard to reflect new budget values
                self.display_dashboard()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(button_frame, text="Cancel", font=self.FONT_SM, bg=self.BG_LIGHT, fg=self.TEXT_DARK, relief=tk.FLAT, command=modal.destroy).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Save", font=self.FONT_SM, bg=self.PRIMARY_COLOR, fg=self.WHITE, relief=tk.FLAT, command=apply_budget).pack(side=tk.RIGHT)

    def _create_shadow_card(self, parent, bg_color=None):
        """Create a card frame with shadow effect"""
        if bg_color is None:
            bg_color = self.WHITE
        
        shadow_frame = tk.Frame(parent, bg="#DDDDDD")
        card_frame = tk.Frame(shadow_frame, bg=bg_color, padx=10, pady=10) # Reduced internal padding
        card_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        return shadow_frame, card_frame

    def display_dashboard(self):
        """Display the refined, single-screen dashboard"""
        self.auth_manager.load_users() # Ensure latest data is loaded
        self.clear_frame()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.BG_LIGHT)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid for main_container: header (row 0), sidebar (row 1, column 0) and content (row 1, column 1)
        main_container.grid_rowconfigure(0, weight=0) # Header will have fixed height
        main_container.grid_rowconfigure(1, weight=1) # Content and sidebar will expand
        main_container.grid_columnconfigure(0, weight=0) # Sidebar will have fixed width
        main_container.grid_columnconfigure(1, weight=1) # Content will expand
        
        # ===== FULL-WIDTH HEADER =====
        header_frame = tk.Frame(main_container, bg=self.PRIMARY_COLOR)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self._create_header(header_frame)

        # ===== LEFT SIDEBAR =====
        self._create_sidebar(main_container)

        # ===== CONTENT FRAME =====
        content_frame = tk.Frame(main_container, bg=self.BG_LIGHT)
        content_frame.grid(row=1, column=1, sticky="nsew", padx=(57, 0))

        
        # ===== SCROLLABLE CONTENT AREA =====
        content_canvas = tk.Canvas(content_frame, bg=self.BG_LIGHT, highlightthickness=0)
        content_scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=content_canvas.yview)
        scrollable_frame = tk.Frame(content_canvas, bg=self.BG_LIGHT)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: content_canvas.configure(scrollregion=content_canvas.bbox("all"))
        )
        
        content_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        content_canvas.configure(yscrollcommand=content_scrollbar.set)
        
        content_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            content_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        content_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # ===== QUICK SNAPSHOT ROW =====
        self._create_quick_snapshot(scrollable_frame)
        
        # ===== TWO-COLUMN LAYOUT =====
        columns_frame = tk.Frame(scrollable_frame, bg=self.BG_LIGHT)
        columns_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=6) # Reduced padding to decrease card area size
        
        # Configure columns: 60% left, 40% right
        columns_frame.grid_columnconfigure(0, weight=60, minsize=400)
        columns_frame.grid_columnconfigure(1, weight=40, minsize=300)
        
        # Left column
        left_column = tk.Frame(columns_frame, bg=self.BG_LIGHT)
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        
        # Right column
        right_column = tk.Frame(columns_frame, bg=self.BG_LIGHT)
        right_column.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        
        # ===== LEFT COLUMN CONTENT =====
        # 1. Total Expense KPI Card
        self._create_total_expense_kpi(left_column)
        
        # 2. Expense Breakdown Pie Chart
        self._create_expense_breakdown_pie(left_column)
        
        # 3. Accounts Carousel
        self._create_accounts_carousel(left_column)
        
        # ===== RIGHT COLUMN CONTENT =====
        # 1. Budget Progress Widget
        self._create_budget_progress(right_column)
        
        # 2. Recent Transactions Table
        self._create_recent_transactions(right_column)
        
        # 3. Top 3 Categories
        self._create_top_categories(right_column)
        
        # ===== FLOATING ACTION BUTTON =====
        self._create_fab(main_container)
    
    def _create_header(self, parent):
        """Create the full-width header"""
        header = tk.Frame(parent, bg=self.PRIMARY_COLOR, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        header.config(highlightbackground=self.BG_LIGHT, highlightthickness=1)
        
        # Left: Project Logo
        left_logo_frame = tk.Frame(header, bg=self.PRIMARY_COLOR)
        left_logo_frame.pack(side=tk.LEFT, padx=24, pady=12) # Proper left padding
        
        tk.Label(
            left_logo_frame,
            text="📈", # Placeholder for logo
            font=self.FONT_XXL,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        ).pack(side=tk.LEFT)
        
        # Project Name
        tk.Label(
            left_logo_frame,
            text="MyWallet", # Changed from "WalletWise"
            font=self.FONT_XL,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        ).pack(side=tk.LEFT, padx=(5,0)) # Added left padding for spacing
        
        # Center: App title and Current date
        center_frame = tk.Frame(header, bg=self.PRIMARY_COLOR)
        center_frame.pack(side=tk.LEFT, expand=True)
        
        # App Title
        tk.Label(
            center_frame,
            text="💰 Personal Expense Tracker",
            font=self.FONT_XL,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        ).pack(pady=(0, 5)) # Removed explicit left padding to allow dynamic centering
        
        # Current date
        # Removed current date label
        # current_date = datetime.now().strftime("%B %d, %Y")
        # tk.Label(
        #     center_frame,
        #     text=current_date,
        #     font=self.FONT_BODY,
        #     bg=self.PRIMARY_COLOR,
        #     fg=self.WHITE
        # ).pack()
        
        # Right: Notification & User avatar
        right_frame = tk.Frame(header, bg=self.PRIMARY_COLOR)
        right_frame.pack(side=tk.RIGHT, padx=24, pady=12)
        
        # Notification icon
        notif_icon = tk.Label(
            right_frame,
            text="🔔",
            font=self.FONT_XXL,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE,
            cursor="hand2"
        )
        notif_icon.pack(side=tk.LEFT, padx=8)
        
        # User avatar
        user_name = self.auth_manager.get_current_user_data().get('name', 'User')
        user_icon = tk.Label(
            right_frame,
            text="👤",
            font=self.FONT_XXL,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE,
            cursor="hand2"
        )
        user_icon.pack(side=tk.LEFT, padx=8)
        
        user_label = tk.Label(
            right_frame,
            text=user_name,
            font=self.FONT_BODY,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        )
        user_label.pack(side=tk.LEFT, padx=(0, 8))
    
    def _create_quick_snapshot(self, parent):
        """Create the quick snapshot row with 4 mini-cards"""
        snapshot_frame = tk.Frame(parent, bg=self.BG_LIGHT)
        snapshot_frame.pack(fill=tk.X, padx=24, pady=24)
        
        # Configure 4 equal columns
        for i in range(4):
            snapshot_frame.grid_columnconfigure(i, weight=1, uniform="snapshot")
        
        user_data = self.auth_manager.get_current_user_data()
        user_expenses = user_data.get('expenses', [])
        currency_code = user_data.get('currency', 'INR')
        currency_symbol = self.CURRENCY_SYMBOLS.get(currency_code, '₹')

        # This Week's Spend
        weekly_spent, _, _ = self._calculate_expense_summary(user_expenses, days=7)
        
        # This Month's Spend
        monthly_spent, _, _ = self._calculate_expense_summary(user_expenses, days=30)

        # Average Daily Spend (Last 30 Days)
        if user_expenses:
            total_spent_30_days, _, _ = self._calculate_expense_summary(user_expenses, days=30)
            avg_daily_spend = total_spent_30_days / 30
        else:
            avg_daily_spend = 0.0

        # Get monthly budget and current month's expenses
        monthly_budget = user_data.get('monthly_budget', 0.0)
        today = datetime.now()
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_expenses = sum(expense['amount'] for expense in user_expenses
                                  if datetime.fromisoformat(expense['timestamp']) >= start_of_month)
        
        # Calculate remaining budget for this month
        remaining_budget = monthly_budget - current_month_expenses

        # Card 1: This Week's Spend
        self._create_mini_card(
            snapshot_frame, 0,
            icon="📅",
            label="This Week",
            value=f"{currency_symbol}{weekly_spent:,.2f}",
            trend="", # No dynamic trend for now
            trend_color=self.ERROR
        )
        
        # Card 2: This Month's Spend
        self._create_mini_card(
            snapshot_frame, 1,
            icon="📆",
            label="This Month",
            value=f"{currency_symbol}{monthly_spent:,.2f}",
            trend="", # No dynamic trend for now
            trend_color=self.SUCCESS
        )
        
        # Card 3: Average Daily Spend
        self._create_mini_card(
            snapshot_frame, 2,
            icon="📊",
            label="Avg Daily",
            value=f"{currency_symbol}{avg_daily_spend:,.2f}",
            trend="Last 30 days",
            trend_color=self.TEXT_LIGHT
        )
        
        # Card 4: Remaining Budget
        self._create_mini_card(
            snapshot_frame, 3,
            icon="💰",
            label="Remaining Budget",
            value=f"{currency_symbol}{remaining_budget:,.2f}",
            trend="This Month",
            trend_color=self.SUCCESS if remaining_budget >= 0 else self.ERROR
        )
    
    def _create_mini_card(self, parent, column, icon, label, value, trend, trend_color):
        """Create a mini-card for quick snapshot"""
        shadow_frame, card_frame = self._create_shadow_card(parent)
        shadow_frame.grid(row=0, column=column, padx=6, pady=6, sticky="nsew")
        
        # Icon
        tk.Label(
            card_frame,
            text=icon,
            font=self.FONT_XXL,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(pady=(0, 8))
        
        # Label
        tk.Label(
            card_frame,
            text=label,
            font=self.FONT_BODY,
            bg=self.WHITE,
            fg=self.TEXT_LIGHT
        ).pack()
        
        # Value
        tk.Label(
            card_frame,
            text=value,
            font=self.FONT_VALUE,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(pady=(4, 4))
        
        # Trend
        tk.Label(
            card_frame,
            text=trend,
            font=self.FONT_CAPTION,
            bg=self.WHITE,
            fg=trend_color
        ).pack()
        
        # Hover effect
        def on_enter(e):
            shadow_frame.config(bg="#CCCCCC")
        def on_leave(e):
            shadow_frame.config(bg="#DDDDDD")
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
    
    def _create_total_expense_kpi(self, parent):
        """Create the Total Expense KPI card with trend chart"""
        shadow_frame, card_frame = self._create_shadow_card(parent)
        shadow_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.WHITE)
        header_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(
            header_frame,
            text="Total Expense - Last 30 Days",
            font=self.FONT_HEADER,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(side=tk.LEFT)
        
        # KPI Value
        user_data = self.auth_manager.get_current_user_data()
        user_expenses = user_data.get('expenses', [])
        currency_code = user_data.get('currency', 'INR')
        currency_symbol = self.CURRENCY_SYMBOLS.get(currency_code, '₹')
        
        total_spent_30_days, _, _ = self._calculate_expense_summary(user_expenses, days=30)

        value_frame = tk.Frame(card_frame, bg=self.WHITE)
        value_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(
            value_frame,
            text=f"{currency_symbol}{total_spent_30_days:,.2f}",
            font=self.FONT_KPI,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(side=tk.LEFT)
        
        # Placeholder for trend comparison - dynamic calculation would be complex
        # For now, it will remain static or show a default message
        tk.Label(
            value_frame,
            text="", # Removed dynamic trend calculation
            font=self.FONT_CAPTION,
            bg=self.WHITE,
            fg=self.SUCCESS
        ).pack(side=tk.LEFT, padx=12)
        
        # Trend Chart
        chart_frame = tk.Frame(card_frame, bg=self.WHITE)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        fig, ax = plt.subplots(figsize=(6, 2.5), dpi=100, facecolor='white')
        
        # Generate daily expenses for the last 30 days
        daily_expenses = { (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"): 0.0 for i in range(30) }
        for expense in user_expenses:
            date_str = expense['date']
            if date_str in daily_expenses:
                daily_expenses[date_str] += expense['amount']
        
        # Sort by date and get values
        sorted_dates = sorted(daily_expenses.keys())
        expenses_data = [daily_expenses[date] for date in sorted_dates]
        days = list(range(1, 31))

        ax.plot(days, expenses_data, color=self.PRIMARY_COLOR, linewidth=2)
        ax.fill_between(days, expenses_data, alpha=0.3, color=self.ACCENT_COLOR)
        ax.set_xlabel('Day of Month', fontsize=9, color=self.TEXT_LIGHT)
        ax.set_ylabel('Amount', fontsize=9, color=self.TEXT_LIGHT)
        ax.grid(True, linestyle='--', alpha=0.3, color=self.TEXT_LIGHT)
        ax.tick_params(labelsize=8, colors=self.TEXT_LIGHT)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _create_expense_breakdown_pie(self, parent):
        """Create the Expense Breakdown pie chart card"""
        shadow_frame, card_frame = self._create_shadow_card(parent)
        shadow_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.WHITE)
        header_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(
            header_frame,
            text="Expense Categories",
            font=self.FONT_HEADER,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(side=tk.LEFT)
        
        # Container for chart and legend
        content_frame = tk.Frame(card_frame, bg=self.WHITE)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chart on top
        chart_frame = tk.Frame(content_frame, bg=self.WHITE)
        chart_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Get dynamic data
        user_data = self.auth_manager.get_current_user_data()
        user_expenses = user_data.get('expenses', [])
        currency_code = user_data.get('currency', 'INR')
        currency_symbol = self.CURRENCY_SYMBOLS.get(currency_code, '₹')

        total_spent_30_days, category_breakdown, _ = self._calculate_expense_summary(user_expenses, days=30)

        if total_spent_30_days == 0:
            # Handle case with no expenses
            categories = ["No Expenses"]
            values = [1]
            colors = ["#E0E0E0"]
            total_display_amount = f"{currency_symbol}0.00"
        else:
            categories = [cat for cat, amount in category_breakdown]
            values = [amount for cat, amount in category_breakdown]
            # Assign colors, cycle through CATEGORY_COLORS or use a default if not found
            colors = [self.CATEGORY_COLORS.get(cat, self.CATEGORY_COLORS['Others']) for cat in categories]
            total_display_amount = f"{currency_symbol}{total_spent_30_days:,.2f}"
        
        fig, ax = plt.subplots(figsize=(4, 3.5), dpi=100, facecolor='white')
        
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops=dict(width=0.4, edgecolor='white')
        )
        
        # Style the percentage text
        for autotext in autotexts:
            autotext.set_color(self.TEXT_DARK) # Changed to TEXT_DARK (black)
            autotext.set_fontsize(9)
            autotext.set_weight('bold')
        
        # Center circle for donut effect
        centre_circle = plt.Circle((0, 0), 0.60, fc='white')
        fig.gca().add_artist(centre_circle)
        
        # Total in center
        ax.text(0, 0, total_display_amount, ha='center', va='center',
                fontsize=14, weight='bold', color=self.TEXT_DARK)
        ax.text(0, -0.15, 'Total', ha='center', va='center',
                fontsize=9, color=self.TEXT_LIGHT)
        
        ax.axis('equal')
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Legend below chart
        legend_frame = tk.Frame(content_frame, bg=self.WHITE)
        legend_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(12, 0)) # Positioned below
        
        # Arrange items horizontally with wrap-like effect
        row_num = 0
        col_num = 0
        max_cols = 6 # Changed to 6 items per row
        
        for category, value, color in zip(categories, values, colors):
            item_frame = tk.Frame(legend_frame, bg=self.WHITE)
            item_frame.grid(row=row_num, column=col_num, sticky="w", padx=5, pady=3)
            
            # Color tag (now a circle on canvas)
            color_canvas = tk.Canvas(item_frame, width=16, height=16, bg=self.WHITE, highlightthickness=0)
            color_canvas.pack(side=tk.LEFT, padx=(0, 8), pady=0) # Adjust pady if needed
            color_canvas.create_oval(2, 2, 14, 14, fill=color, outline="", width=0)
            
            # Category name
            tk.Label(
                item_frame,
                text=category,
                font=self.FONT_BODY, # Increased font size
                bg=self.WHITE,
                fg=self.TEXT_DARK,
                anchor="w"
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

            col_num += 1
            if col_num >= max_cols:
                col_num = 0
                row_num += 1
    
    def _create_accounts_carousel(self, parent):
        """Create the accounts carousel"""
        # Header
        header_frame = tk.Frame(parent, bg=self.BG_LIGHT)
        header_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(
            header_frame,
            text="My Accounts",
            font=self.FONT_HEADER,
            bg=self.BG_LIGHT,
            fg=self.TEXT_DARK
        ).pack(side=tk.LEFT)
        
        # Scrollable carousel frame
        carousel_container = tk.Frame(parent, bg=self.BG_LIGHT)
        carousel_container.pack(fill=tk.X)
        
        canvas = tk.Canvas(carousel_container, bg=self.BG_LIGHT, height=140, highlightthickness=0)
        # scrollbar = ttk.Scrollbar(carousel_container, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg=self.BG_LIGHT)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=None) # Remove horizontal scrollbar
        
        canvas.pack(side=tk.TOP, fill=tk.X, expand=True)
        # scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        currency_code = self.auth_manager.get_current_user_data().get('currency', 'INR')
        currency_symbol = self.CURRENCY_SYMBOLS.get(currency_code, '₹')
        cash_balance = self.auth_manager.get_current_user_data().get('cash_balance', 0.0)
        bank_balance = self.auth_manager.get_current_user_data().get('bank_balance', 0.0)
        credit_card_balance = self.auth_manager.get_current_user_data().get('credit_card_balance', 0.0)
        
        # Account cards
        self._create_account_card(scrollable_frame, "Cash", "💵", f"{currency_symbol}{cash_balance:.2f}", 
                                   "", self.PRIMARY_COLOR, self.SECONDARY_COLOR, vertical_offset=0)
        self._create_account_card(scrollable_frame, "Bank", "🏦", f"{currency_symbol}{bank_balance:.2f}", 
                                   "", "#66BB6A", "#4CAF50", vertical_offset=0)
        self._create_account_card(scrollable_frame, "Credit Card", "💳", f"{currency_symbol}{credit_card_balance:.2f}", 
                                   "", "#FFA726", "#FF9800", vertical_offset=6) # Increased downward shift further
        
        # Add Account button
        add_btn_frame = tk.Frame(scrollable_frame, bg=self.BG_LIGHT, 
                                width=200, height=120, bd=2, relief=tk.SOLID,
                                highlightbackground=self.ACCENT_COLOR,
                                highlightthickness=2)
        add_btn_frame.pack(side=tk.LEFT, padx=8)
        add_btn_frame.pack_propagate(False)
        
        tk.Label(
            add_btn_frame,
            text="➕",
            font=self.FONT_KPI,
            bg=self.BG_LIGHT,
            fg=self.ACCENT_COLOR
        ).pack(expand=True)
        
        tk.Label(
            add_btn_frame,
            text="Add Account",
            font=self.FONT_BODY,
            bg=self.BG_LIGHT,
            fg=self.TEXT_DARK
        ).pack()
        
        add_btn_frame.bind("<Button-1>", lambda e: messagebox.showinfo("Add Account", "Add account functionality coming soon!"))
        add_btn_frame.bind("<Enter>", lambda e: add_btn_frame.config(bg="#F0F0F0"))
        add_btn_frame.bind("<Leave>", lambda e: add_btn_frame.config(bg=self.BG_LIGHT))
    
    def _create_account_card(self, parent, account_type, icon, balance, trend, color1, color2, vertical_offset=0):
        """Create an individual account card with gradient background"""
        # Note: Tkinter doesn't support gradients natively, so we'll use a solid color
        card_frame = tk.Frame(parent, bg=color1, width=200, height=120, bd=0, relief=tk.FLAT) # Reverted height for better proportion
        card_frame.pack(side=tk.LEFT, padx=8)
        card_frame.pack_propagate(False)
        
        # Add padding frame
        content_frame = tk.Frame(card_frame, bg=color1)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5) # Consistent internal padding
        
        # Configure grid for content_frame
        content_frame.grid_rowconfigure(0, weight=1) # Icon row
        content_frame.grid_rowconfigure(1, weight=1) # Type row
        content_frame.grid_rowconfigure(2, weight=1) # Balance row
        content_frame.grid_rowconfigure(3, weight=1) # Trend row
        content_frame.grid_columnconfigure(0, weight=1)

        # Frame to hold icon and type on the same row
        icon_and_type_frame = tk.Frame(content_frame, bg=color1)
        icon_and_type_frame.grid(row=0, column=0, sticky="nw")
        
        # Icon
        tk.Label(
            icon_and_type_frame,
            text=icon,
            font=self.FONT_XL,
            bg=color1,
            fg=self.WHITE
        ).pack(side=tk.LEFT, anchor="nw")
        
        # Type
        tk.Label(
            icon_and_type_frame,
            text=account_type,
            font=self.FONT_BODY, # Increased font size and weight
            bg=color1,
            fg=self.WHITE
        ).pack(side=tk.LEFT, anchor="center", padx=(5,0), pady=(vertical_offset,0)) # Apply conditional vertical offset
        
        # Balance
        tk.Label(
            content_frame,
            text=balance,
            font=self.FONT_BODY,
            bg=color1,
            fg=self.WHITE
        ).grid(row=1, column=0, sticky="w") # Shifted to row 1
        
        # Trend
        tk.Label(
            content_frame,
            text=trend,
            font=self.FONT_CAPTION,
            bg=color1,
            fg=self.WHITE
        ).grid(row=2, column=0, sticky="sw") # Shifted to row 2
        
        # Hover effect
        def on_enter(e):
            card_frame.config(bg=color2)
            content_frame.config(bg=color2)
            for child in content_frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=color2)
        
        def on_leave(e):
            card_frame.config(bg=color1)
            content_frame.config(bg=color1)
            for child in content_frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=color1)
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        content_frame.bind("<Enter>", on_enter)
        content_frame.bind("<Leave>", on_leave)
    
    def _create_budget_progress(self, parent):
        """Create the budget progress widget with circular progress ring"""
        shadow_frame, card_frame = self._create_shadow_card(parent)
        shadow_frame.pack(fill=tk.X, pady=(0, 12))
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.WHITE)
        header_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(
            header_frame,
            text="Monthly Budget",
            font=self.FONT_HEADER,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(side=tk.LEFT)
        
        # Circular progress
        canvas_size = 160
        canvas_widget = tk.Canvas(card_frame, width=canvas_size, height=canvas_size, 
                                  bg=self.WHITE, highlightthickness=0)
        canvas_widget.pack(pady=12)
        
        center = canvas_size / 2
        radius = 60
        width = 12
        
        # Background circle
        canvas_widget.create_oval(
            center - radius, center - radius,
            center + radius, center + radius,
            outline="#E0E0E0", width=width
        )
        
        # Progress arc
        user_data = self.auth_manager.get_current_user_data()
        user_expenses = user_data.get('expenses', [])
        currency_code = user_data.get('currency', 'INR')
        currency_symbol = self.CURRENCY_SYMBOLS.get(currency_code, '₹')
        monthly_budget = user_data.get('monthly_budget', 0.0)
        
        # Calculate spent amount for the current month
        today = datetime.now()
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        spent_amount = sum(expense['amount'] for expense in user_expenses
                           if datetime.fromisoformat(expense['timestamp']) >= start_of_month and
                           datetime.fromisoformat(expense['timestamp']) <= today)

        percentage = min(100, (spent_amount / monthly_budget) * 100) if monthly_budget > 0 else 0
        
        # Determine color based on percentage
        if percentage <= 80:
            progress_color = self.SUCCESS
        elif percentage <= 100:
            progress_color = "#F39C12"  # Warning orange
        else:
            progress_color = self.ERROR
        
        # Draw arc (starting from top, going clockwise)
        extent = (percentage / 100) * 360
        canvas_widget.create_arc(
            center - radius, center - radius,
            center + radius, center + radius,
            start=90, extent=-extent,
            outline=progress_color, width=width,
            style=tk.ARC
        )
        
        # Center text
        canvas_widget.create_text(
            center, center - 10,
            text=f"{int(percentage)}%",
            font=self.FONT_KPI,
            fill=self.TEXT_DARK
        )
        
        canvas_widget.create_text(
            center, center + 15,
            text="Used",
            font=self.FONT_CAPTION,
            fill=self.TEXT_LIGHT
        )
        
        # Details below ring
        details_frame = tk.Frame(card_frame, bg=self.WHITE)
        details_frame.pack(fill=tk.X, pady=12)
        
        # Spent
        spent_frame = tk.Frame(details_frame, bg=self.WHITE)
        spent_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(
            spent_frame,
            text="Spent:",
            font=self.FONT_BODY,
            bg=self.WHITE,
            fg=self.TEXT_LIGHT
        ).pack(side=tk.LEFT)
        
        tk.Label(
            spent_frame,
            text=f"{currency_symbol}{spent_amount:,.2f}",
            font=self.FONT_VALUE,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(side=tk.RIGHT)
        
        # Total
        total_frame = tk.Frame(details_frame, bg=self.WHITE)
        total_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(
            total_frame,
            text="Budget:",
            font=self.FONT_BODY,
            bg=self.WHITE,
            fg=self.TEXT_LIGHT
        ).pack(side=tk.LEFT)
        
        tk.Label(
            total_frame,
            text=f"{currency_symbol}{monthly_budget:,.2f}",
            font=self.FONT_BODY,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(side=tk.RIGHT)
        
        # Remaining
        remaining = monthly_budget - spent_amount
        remaining_frame = tk.Frame(details_frame, bg=self.WHITE)
        remaining_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(
            remaining_frame,
            text="Remaining:",
            font=self.FONT_BODY,
            bg=self.WHITE,
            fg=self.TEXT_LIGHT
        ).pack(side=tk.LEFT)
        
        tk.Label(
            remaining_frame,
            text=f"{currency_symbol}{remaining:,.2f}",
            font=self.FONT_VALUE,
            bg=self.WHITE,
            fg=self.SUCCESS if remaining >= 0 else self.ERROR
        ).pack(side=tk.RIGHT)
        
        # Status indicator
        if percentage <= 80:
            status_text = "✅ On Track"
            status_color = self.SUCCESS
        elif percentage <= 100:
            status_text = "⚠️ Almost There"
            status_color = "#F39C12"
        else:
            status_text = "🚨 Over Budget"
            status_color = self.ERROR
        
        tk.Label(
            card_frame,
            text=status_text,
            font=self.FONT_SUBHEADER,
            bg=self.WHITE,
            fg=status_color
        ).pack(pady=(8, 0))
    
    def _create_recent_transactions(self, parent):
        """Create the recent transactions table with search"""
        shadow_frame, card_frame = self._create_shadow_card(parent)
        shadow_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.WHITE)
        header_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(
            header_frame,
            text="Recent Transactions",
            font=self.FONT_HEADER, # Already FONT_HEADER, keep as is for consistent header sizing
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(side=tk.LEFT)
        
        tk.Label(
            header_frame,
            text="⋮",
            font=self.FONT_XXL,
            bg=self.WHITE,
            fg=self.TEXT_DARK,
            cursor="hand2"
        ).pack(side=tk.RIGHT)
        
        # Search bar
        search_frame = tk.Frame(card_frame, bg="#F7F8FA", bd=0)
        search_frame.pack(fill=tk.X, pady=(0, 12))
        
        search_icon = tk.Label(search_frame, text="🔍", font=self.FONT_MD, bg="#F7F8FA") # Keep FONT_MD for icon
        search_icon.pack(side=tk.LEFT, padx=8)
        
        self.search_entry = tk.Entry(
            search_frame,
            font=self.FONT_MD, # Increased font size
            bg="#F7F8FA",
            fg=self.TEXT_DARK,
            bd=0,
            relief=tk.FLAT
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), pady=8)
        self.search_entry.insert(0, "Search transactions...")
        
        # Placeholder behavior
        def on_focus_in(e):
            if self.search_entry.get() == "Search transactions...":
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg=self.TEXT_DARK)
        
        def on_focus_out(e):
            if self.search_entry.get() == "":
                self.search_entry.insert(0, "Search transactions...")
                self.search_entry.config(fg=self.TEXT_LIGHT)
        
        self.search_entry.bind("<FocusIn>", on_focus_in)
        self.search_entry.bind("<FocusOut>", on_focus_out)
        self.search_entry.config(fg=self.TEXT_LIGHT)
        
        # Table
        table_frame = tk.Frame(card_frame, bg=self.WHITE)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure treeview style
        style = ttk.Style()
        style.theme_use("default") # Use default theme to avoid issues with custom styles if any
        style.configure("Transactions.Treeview", 
                       background=self.WHITE,
                       foreground=self.TEXT_DARK,
                       rowheight=30, # Reduced row height for better compactness
                       fieldbackground=self.WHITE,
                       borderwidth=0,
                       font=self.FONT_BODY) # Reverted font size for rows
        style.configure("Transactions.Treeview.Heading",
                       background=self.BG_LIGHT,
                       foreground=self.TEXT_DARK,
                       font=self.FONT_SUBHEADER) # Reverted font size for headings
        
        columns = ("Date", "Category", "Amount")
        self.transactions_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Transactions.Treeview",
            height=6 # Reduced height of the card back to original
        )
        
        for col in columns:
            self.transactions_tree.heading(col, text=col, anchor=tk.W)
            if col == "Amount":
                self.transactions_tree.column(col, anchor=tk.E, width=100)
            else:
                self.transactions_tree.column(col, anchor=tk.W, width=120)
        
        # Get dynamic data
        user_data = self.auth_manager.get_current_user_data()
        user_expenses = user_data.get('expenses', [])
        currency_code = user_data.get('currency', 'INR')
        currency_symbol = self.CURRENCY_SYMBOLS.get(currency_code, '₹')

        _, _, recent_transactions = self._calculate_expense_summary(user_expenses, days=365) # Get all recent for table

        # Clear existing items
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        if not recent_transactions:
            self.transactions_tree.insert("", "end", values=("", "No transactions yet", ""))
        else:
            for expense in recent_transactions:
                display_date = datetime.fromisoformat(expense['date']).strftime("%b %d")
                category = expense['category'].capitalize()
                amount = expense['amount']
                # Determine if it's an expense or income (for now, all are expenses)
                amount_text = f"-{currency_symbol}{amount:,.2f}"
                tag = category.lower() # Use lower case for tags
                self.transactions_tree.insert("", "end", values=(display_date, f"● {category}", amount_text), tags=(tag,))
        
        # Configure tags for color-coding
        for category_name, color_hex in self.CATEGORY_COLORS.items():
            self.transactions_tree.tag_configure(category_name.lower(), foreground=color_hex)
        self.transactions_tree.tag_configure("income", foreground=self.SUCCESS) # If income is ever added

        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        # scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.transactions_tree.yview)
        # self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # View all link
        view_all = tk.Label(
            card_frame,
            text="View All Transactions →",
            font=self.FONT_BODY, # Reverted font size
            bg=self.WHITE,
            fg=self.PRIMARY_COLOR,
            cursor="hand2"
        )
        view_all.pack(pady=(8, 0))
        view_all.bind("<Button-1>", lambda e: display_all_transactions_screen(self.root, self.auth_manager, self))
    
    def _create_top_categories(self, parent):
        """Create the top 3 expense categories widget"""
        shadow_frame, card_frame = self._create_shadow_card(parent)
        shadow_frame.pack(fill=tk.X, pady=(0, 12))
        
        # Header
        tk.Label(
            card_frame,
            text="Highest Spenders This Month",
            font=self.FONT_HEADER,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(anchor="w", pady=(0, 12))
        
        # Get dynamic data
        user_data = self.auth_manager.get_current_user_data()
        user_expenses = user_data.get('expenses', [])
        currency_code = user_data.get('currency', 'INR')
        currency_symbol = self.CURRENCY_SYMBOLS.get(currency_code, '₹')

        total_spent_this_month, category_breakdown, _ = self._calculate_expense_summary(user_expenses, days=30)

        top_categories_data = []
        if total_spent_this_month > 0:
            # Get top 3 categories by amount spent this month
            sorted_categories = category_breakdown # Already sorted from _calculate_expense_summary
            for i, (category, amount) in enumerate(sorted_categories[:3]):
                percentage = (amount / total_spent_this_month) * 100
                rank_icon = ["🥇", "🥈", "🥉"][i]
                color = self.CATEGORY_COLORS.get(category, self.CATEGORY_COLORS['Others'])
                top_categories_data.append((rank_icon, f"● {category}", f"{currency_symbol}{amount:,.2f}", percentage, color))
        
        if not top_categories_data:
            tk.Label(
                card_frame,
                text="No expenses recorded this month.",
                font=self.FONT_BODY,
                bg=self.WHITE,
                fg=self.TEXT_LIGHT
            ).pack(anchor="w", pady=10)
        else:
            for rank, category, amount, percentage, color in top_categories_data:
                item_frame = tk.Frame(card_frame, bg=self.WHITE)
                item_frame.pack(fill=tk.X, pady=8)
                
                # Rank badge
                tk.Label(
                    item_frame,
                    text=rank,
                    font=self.FONT_XXL,
                    bg=self.WHITE
                ).pack(side=tk.LEFT, padx=(0, 12))
                
                # Category details
                details_frame = tk.Frame(item_frame, bg=self.WHITE)
                details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                # Category name
                tk.Label(
                    details_frame,
                    text=category,
                    font=self.FONT_SUBHEADER,
                    bg=self.WHITE,
                    fg=self.TEXT_DARK
                ).pack(anchor="w")
                
                # Amount and percentage
                info_frame = tk.Frame(details_frame, bg=self.WHITE)
                info_frame.pack(fill=tk.X, pady=(2, 4))
                
                tk.Label(
                    info_frame,
                    text=amount,
                    font=self.FONT_VALUE,
                    bg=self.WHITE,
                    fg=self.TEXT_DARK
                ).pack(side=tk.LEFT)
                
                tk.Label(
                    info_frame,
                    text=f"{percentage:.1f}% of total",
                    font=self.FONT_CAPTION,
                    bg=self.WHITE,
                    fg=self.TEXT_LIGHT
                ).pack(side=tk.LEFT, padx=8)
                
                # Progress bar
                progress_bg = tk.Frame(details_frame, bg="#E0E0E0", height=4)
                progress_bg.pack(fill=tk.X)
                
                progress_fill = tk.Frame(progress_bg, bg=color, height=4)
                progress_fill.place(relwidth=percentage/100, relheight=1.0)
    
    def _create_fab(self, parent):
        """Create the floating action button group"""
        # Container for FAB and sub-buttons
        fab_container = tk.Frame(parent, bg=self.BG_LIGHT)
        fab_container.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-20, y=-20) # Adjusted position to be more visible
        
        # Main FAB button - now a circular canvas
        fab_canvas_size = 60 # Diameter of the circle
        self.fab_button_canvas = tk.Canvas(
            fab_container,
            width=fab_canvas_size,
            height=fab_canvas_size,
            bg=self.BG_LIGHT, # Background of the canvas itself, outside the circle
            highlightthickness=0,
            cursor="hand2"
        )
        self.fab_button_canvas.pack()

        # Draw the circle
        radius = fab_canvas_size / 2
        center_x = fab_canvas_size / 2
        center_y = fab_canvas_size / 2
        self.fab_circle_item = self.fab_button_canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=self.ACCENT_COLOR,
            outline="",
            width=0
        )

        # Add the plus text
        self.fab_text_item = self.fab_button_canvas.create_text(
            center_x, center_y,
            text="➕",
            font=self.FONT_KPI,
            fill=self.WHITE
        )
        
        self.fab_button_canvas.bind("<Button-1>", lambda e: self.show_add_transaction_modal())
        
        # Hover effect
        def on_fab_enter(e):
            self.fab_button_canvas.itemconfig(self.fab_circle_item, fill=self.SECONDARY_COLOR)
        
        def on_fab_leave(e):
            self.fab_button_canvas.itemconfig(self.fab_circle_item, fill=self.ACCENT_COLOR)
        
        self.fab_button_canvas.bind("<Enter>", on_fab_enter)
        self.fab_button_canvas.bind("<Leave>", on_fab_leave)

    def _create_sidebar(self, parent):
        """Create the left sidebar with profile, navigation, and settings"""
        sidebar_width = 300
        sidebar_frame = tk.Frame(parent, bg=self.WHITE, width=sidebar_width, highlightbackground=self.BG_LIGHT, highlightthickness=1)
        sidebar_frame.grid(row=1, column=0, sticky="nsew")
        sidebar_frame.pack_propagate(False) # Prevent frame from resizing to content

        # Scrollable area for sidebar content
        sidebar_canvas = tk.Canvas(sidebar_frame, bg=self.WHITE, highlightthickness=0)
        sidebar_scrollbar = ttk.Scrollbar(sidebar_frame, orient="vertical", command=sidebar_canvas.yview)
        scrollable_sidebar_frame = tk.Frame(sidebar_canvas, bg=self.WHITE)

        scrollable_sidebar_frame.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )

        sidebar_canvas.create_window((0, 0), window=scrollable_sidebar_frame, anchor="nw")
        sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)

        sidebar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sidebar_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add mouse wheel scrolling to sidebar
        def _on_sidebar_mousewheel(event):
            sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        sidebar_canvas.bind_all("<MouseWheel>", _on_sidebar_mousewheel)

        # Custom style for the switch toggle
        style = ttk.Style()
        style.theme_use('default')
        style.map("Switch.TCheckbutton",
            background=[('active', self.WHITE), ('selected', self.ACCENT_COLOR)],
            foreground=[('selected', self.WHITE)],
            indicatorbackground=[('selected', self.ACCENT_COLOR)],
            indicatorforeground=[('selected', self.WHITE)]
        )

        # Profile Section
        profile_frame = tk.Frame(scrollable_sidebar_frame, bg=self.PRIMARY_COLOR, padx=20, pady=20)
        profile_frame.pack(fill=tk.X)

        # Frame to hold icon and name on the same row
        name_row_frame = tk.Frame(profile_frame, bg=self.PRIMARY_COLOR)
        name_row_frame.pack(fill=tk.X, anchor="w")

        profile_icon = tk.Label(
            name_row_frame,
            text="👤",
            font=self.FONT_3XL,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        )
        profile_icon.pack(side=tk.LEFT, anchor="w")

        user_name = self.auth_manager.get_current_user_data().get('name', 'User')
        profile_name = tk.Label(
            name_row_frame,
            text=user_name.capitalize(),
            font=self.FONT_XXL,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        )
        profile_name.pack(side=tk.LEFT, anchor="w", padx=(10, 0))

        tk.Label(
            profile_frame,
            text="My Wallet",
            font=self.FONT_BODY,
            bg=self.PRIMARY_COLOR,
            fg="#d8e0f0"
        ).pack(anchor="w", pady=(5,0))

        # Navigation Links
        nav_frame = tk.Frame(scrollable_sidebar_frame, bg=self.WHITE, padx=10, pady=10)
        nav_frame.pack(fill=tk.BOTH, expand=True)

        # Removed top 3 nav items: Get Premium, Bank Sync, Imports
        # nav_items_top = [
        #     ("⬆️", "Get Premium"),
        #     ("🏦", "Bank Sync"),
        #     ("⬇️", "Imports"),
        # ]
        # self._create_nav_section(nav_frame, nav_items_top, section_title=None)

        tk.Frame(nav_frame, bg=self.BG_LIGHT, height=1).pack(fill=tk.X, pady=10)

        nav_items_main = [
            ("🏠", "Home"),
            ("📋", "Records"),
            ("💰", "Budgets"),
        ]
        self._create_nav_section(nav_frame, nav_items_main, section_title=None)

        tk.Frame(nav_frame, bg=self.BG_LIGHT, height=1).pack(fill=tk.X, pady=10)

        # Settings and Utilities
        settings_frame = tk.Frame(scrollable_sidebar_frame, bg=self.WHITE, padx=10, pady=10)
        settings_frame.pack(fill=tk.X, expand=True)

        settings_items = [
            ("⚙️", "Settings"),
        ]

        for icon, text, *args in settings_items:
            item_frame = tk.Frame(settings_frame, bg=self.WHITE, cursor="hand2")
            item_frame.pack(fill=tk.X, pady=2)

            tk.Label(
                item_frame,
                text=icon,
                font=self.FONT_MD,
                bg=self.WHITE,
                fg=self.TEXT_DARK
            ).pack(side=tk.LEFT, padx=(0, 8), pady=8)

            tk.Label(
                item_frame,
                text=text,
                font=self.FONT_BODY,
                bg=self.WHITE,
                fg=self.TEXT_DARK
            ).pack(side=tk.LEFT, pady=8, anchor="w")

            if text == "Dark mode":
                toggle_switch = ttk.Checkbutton(item_frame, text="", variable=self.dark_mode_enabled, style="Switch.TCheckbutton", command=self.toggle_dark_mode)
                toggle_switch.pack(side=tk.RIGHT, padx=5)
            elif text == "Hide Amounts":
                toggle_switch = ttk.Checkbutton(item_frame, text="", variable=self.hide_amounts_enabled, style="Switch.TCheckbutton", command=self.toggle_hide_amounts)
                toggle_switch.pack(side=tk.RIGHT, padx=5)
            else:
                pass # No toggle for other items
            
            def on_enter(e, frame=item_frame):
                frame.config(bg=self.BG_LIGHT)
                for child in frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=self.BG_LIGHT)

            def on_leave(e, frame=item_frame):
                frame.config(bg=self.WHITE)
                for child in frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=self.WHITE)
            
            item_frame.bind("<Enter>", on_enter)
            item_frame.bind("<Leave>", on_leave)
            # Only bind Button-1 for non-toggle items
            if text not in ["Dark mode", "Hide Amounts"]:
                item_frame.bind("<Button-1>", lambda e, txt=text: messagebox.showinfo("Sidebar", f"{txt} clicked!"))

    def _create_nav_section(self, parent, items, section_title=None):
        """Helper to create a section of navigation links"""
        if section_title:
            tk.Label(
                parent,
                text=section_title,
                font=self.FONT_SUBHEADER,
                bg=self.WHITE,
                fg=self.TEXT_DARK,
                anchor="w"
            ).pack(fill=tk.X, pady=(10, 5), padx=5)

        for icon, text, *args in items:
            item_frame = tk.Frame(parent, bg=self.WHITE, cursor="hand2")
            item_frame.pack(fill=tk.X, pady=2)

            tk.Label(
                item_frame,
                text=icon,
                font=self.FONT_MD,
                bg=self.WHITE,
                fg=self.TEXT_DARK
            ).pack(side=tk.LEFT, padx=(0, 8), pady=8)

            tk.Label(
                item_frame,
                text=text,
                font=self.FONT_BODY,
                bg=self.WHITE,
                fg=self.TEXT_DARK
            ).pack(side=tk.LEFT, pady=8, anchor="w")

            if "New" in args:
                tk.Label(
                    item_frame,
                    text="New",
                    font=self.FONT_CAPTION,
                    bg=self.ACCENT_COLOR,
                    fg=self.WHITE,
                    padx=5,
                    relief=tk.FLAT,
                    bd=0,
                    anchor="e"
                ).pack(side=tk.RIGHT, padx=5)
            
            def on_enter(e, frame=item_frame):
                frame.config(bg=self.BG_LIGHT)
                for child in frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=self.BG_LIGHT)

            def on_leave(e, frame=item_frame):
                frame.config(bg=self.WHITE)
                for child in frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=self.WHITE)

            item_frame.bind("<Enter>", on_enter)
            item_frame.bind("<Leave>", on_leave)
            
            if text == "Records":
                item_frame.bind("<Button-1>", lambda e: records_screen.display_records_screen(self.root, self.auth_manager, self))
            elif text == "Budgets":
                # Open the budget setup window (same as onboarding)
                item_frame.bind("<Button-1>", lambda e: self.show_budget_window())
            else:
                # Only bind Button-1 for non-toggle items
                if text not in ["Dark mode", "Hide Amounts"]:
                    item_frame.bind("<Button-1>", lambda e, txt=text: messagebox.showinfo("Sidebar", f"{txt} clicked!"))

    # OLD METHODS - TO BE REMOVED OR KEPT FOR COMPATIBILITY
    def toggle_sidebar(self):
        """Legacy method - no longer used in new dashboard"""
        pass
        
    def show_dashboard(self):
        """Refresh and display the dashboard"""
        self.display_dashboard()
    
    def show_tab(self, tab_name):
        """Legacy method - no longer used in new dashboard"""
        pass
    
    def create_home_tab(self, parent_frame):
        """Legacy method - no longer used in new dashboard"""
        pass
    
    def create_accounts_tab(self, parent_frame):
        """Legacy method - no longer used in new dashboard"""
        pass
    
    def create_budgets_goals_tab(self, parent_frame):
        """Legacy method - no longer used in new dashboard"""
        pass
    
    def create_insights_tab(self, parent_frame):
        """Legacy method - no longer used in new dashboard"""
        pass
    
    def _sort_treeview(self, tree, col, reverse):
        """Sort treeview columns"""
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        # Convert amount to float for proper sorting if it's the amount column
        if col == "Amount":
            try:
                l.sort(key=lambda t: float(t[0].replace('₹', '').replace(',', '').replace('+', '').replace('-', '')), reverse=reverse)
            except:
                l.sort(reverse=reverse)

        # rearrange items in sorted order
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)
        
        # reverse sort next time
        tree.heading(col, command=lambda: self._sort_treeview(tree, col, not reverse))
    
    def _filter_treeview(self, event):
        """Filter treeview based on search term"""
        if not hasattr(self, 'transactions_tree'):
            return
            
        search_term = event.widget.get().lower()
        if search_term == "search transactions...":
            return
            
        for item_id in self.transactions_tree.get_children():
            item_values = [str(self.transactions_tree.item(item_id, "values")[col_idx]).lower() 
                          for col_idx in range(len(self.transactions_tree["columns"]))]
            
            if any(search_term in value for value in item_values):
                self.transactions_tree.reattach(item_id, '', tk.END)
            else:
                self.transactions_tree.detach(item_id)
