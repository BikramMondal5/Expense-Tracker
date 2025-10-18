import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Wedge
import config
from tkinter import messagebox
from datetime import datetime, timedelta
import math

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
        self.FONT_BODY = (config.FONT_PRIMARY, 11)
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
        messagebox.showinfo("Add Transaction", "Add new transaction functionality coming soon!")

    def show_add_income_modal(self):
        messagebox.showinfo("Add Income", "Add new income functionality coming soon!")

    def show_add_budget_modal(self):
        messagebox.showinfo("Add Budget", "Add new budget functionality coming soon!")
    
    def _create_shadow_card(self, parent, bg_color=None):
        """Create a card frame with shadow effect"""
        if bg_color is None:
            bg_color = self.WHITE
        
        shadow_frame = tk.Frame(parent, bg="#DDDDDD")
        card_frame = tk.Frame(shadow_frame, bg=bg_color, padx=16, pady=16)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        return shadow_frame, card_frame

    def display_dashboard(self):
        """Display the refined, single-screen dashboard"""
        self.clear_frame()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.BG_LIGHT)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid for main_container: sidebar (column 0) and content (column 1)
        main_container.grid_columnconfigure(0, weight=0) # Sidebar will have fixed width
        main_container.grid_columnconfigure(1, weight=1) # Content will expand
        main_container.grid_rowconfigure(0, weight=1)

        # ===== LEFT SIDEBAR =====
        self._create_sidebar(main_container)

        # ===== CONTENT FRAME =====
        content_frame = tk.Frame(main_container, bg=self.BG_LIGHT)
        content_frame.grid(row=0, column=1, sticky="nsew")

        # ===== FULL-WIDTH HEADER =====
        self._create_header(content_frame)
        
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
        columns_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=12)
        
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
        
        # Left: App title with icon
        left_frame = tk.Frame(header, bg=self.PRIMARY_COLOR)
        left_frame.pack(side=tk.LEFT, padx=24, pady=12)
        
        tk.Label(
            left_frame,
            text="💰 Personal Expense Tracker",
            font=self.FONT_XL,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        ).pack(side=tk.LEFT)
        
        # Center: Current date
        center_frame = tk.Frame(header, bg=self.PRIMARY_COLOR)
        center_frame.pack(side=tk.LEFT, expand=True)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        tk.Label(
            center_frame,
            text=current_date,
            font=self.FONT_BODY,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        ).pack()
        
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
        
        currency = self.auth_manager.get_current_user_data().get('currency_symbol', '₹')
        
        # Card 1: This Week's Spend
        self._create_mini_card(
            snapshot_frame, 0,
            icon="📅",
            label="This Week",
            value=f"{currency}1,234",
            trend="↑ 12%",
            trend_color=self.ERROR
        )
        
        # Card 2: This Month's Spend
        self._create_mini_card(
            snapshot_frame, 1,
            icon="📆",
            label="This Month",
            value=f"{currency}5,678",
            trend="↓ 8%",
            trend_color=self.SUCCESS
        )
        
        # Card 3: Average Daily Spend
        self._create_mini_card(
            snapshot_frame, 2,
            icon="📊",
            label="Avg Daily",
            value=f"{currency}189",
            trend="Last 30 days",
            trend_color=self.TEXT_LIGHT
        )
        
        # Card 4: Total Balance
        self._create_mini_card(
            snapshot_frame, 3,
            icon="💰",
            label="Total Balance",
            value=f"{currency}12,456",
            trend="All Accounts",
            trend_color=self.SUCCESS
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
        currency = self.auth_manager.get_current_user_data().get('currency_symbol', '₹')
        
        value_frame = tk.Frame(card_frame, bg=self.WHITE)
        value_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(
            value_frame,
            text=f"{currency}8,924",
            font=self.FONT_KPI,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(side=tk.LEFT)
        
        tk.Label(
            value_frame,
            text="vs previous 30 days: -15%",
            font=self.FONT_CAPTION,
            bg=self.WHITE,
            fg=self.SUCCESS
        ).pack(side=tk.LEFT, padx=12)
        
        # Trend Chart
        chart_frame = tk.Frame(card_frame, bg=self.WHITE)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        fig, ax = plt.subplots(figsize=(6, 2.5), dpi=100, facecolor='white')
        
        # Sample data
        days = list(range(1, 31))
        expenses = [200 + (i % 7) * 50 + (i % 3) * 30 for i in days]
        
        ax.plot(days, expenses, color=self.PRIMARY_COLOR, linewidth=2)
        ax.fill_between(days, expenses, alpha=0.3, color=self.ACCENT_COLOR)
        ax.set_xlabel('Day of Month', fontsize=9, color=self.TEXT_LIGHT)
        ax.set_ylabel('Amount', fontsize=9, color=self.TEXT_LIGHT)
        ax.grid(True, linestyle='--', alpha=0.3, color=self.TEXT_LIGHT)
        ax.tick_params(labelsize=8, colors=self.TEXT_LIGHT)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
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
        
        # Chart on left
        chart_frame = tk.Frame(content_frame, bg=self.WHITE)
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Sample data
        categories = list(self.CATEGORY_COLORS.keys())
        values = [35, 25, 15, 12, 8, 5]
        colors = list(self.CATEGORY_COLORS.values())
        currency = self.auth_manager.get_current_user_data().get('currency_symbol', '₹')
        
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
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_weight('bold')
        
        # Center circle for donut effect
        centre_circle = plt.Circle((0, 0), 0.60, fc='white')
        fig.gca().add_artist(centre_circle)
        
        # Total in center
        ax.text(0, 0, f'{currency}8,924', ha='center', va='center',
                fontsize=14, weight='bold', color=self.TEXT_DARK)
        ax.text(0, -0.15, 'Total', ha='center', va='center',
                fontsize=9, color=self.TEXT_LIGHT)
        
        ax.axis('equal')
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Legend on right
        legend_frame = tk.Frame(content_frame, bg=self.WHITE)
        legend_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(12, 0))
        
        tk.Label(
            legend_frame,
            text="Breakdown",
            font=self.FONT_SUBHEADER,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(anchor="w", pady=(0, 8))
        
        for category, value, color in zip(categories, values, colors):
            item_frame = tk.Frame(legend_frame, bg=self.WHITE)
            item_frame.pack(fill=tk.X, pady=3)
            
            # Color tag
            color_tag = tk.Label(item_frame, text="  ", bg=color, width=2)
            color_tag.pack(side=tk.LEFT, padx=(0, 8))
            
            # Category name
            tk.Label(
                item_frame,
                text=category,
                font=self.FONT_CAPTION,
                bg=self.WHITE,
                fg=self.TEXT_DARK,
                anchor="w"
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Percentage
            tk.Label(
                item_frame,
                text=f"{value}%",
                font=self.FONT_CAPTION,
                bg=self.WHITE,
                fg=self.TEXT_LIGHT
            ).pack(side=tk.RIGHT)
    
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
        scrollbar = ttk.Scrollbar(carousel_container, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg=self.BG_LIGHT)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.TOP, fill=tk.X, expand=True)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        currency = self.auth_manager.get_current_user_data().get('currency_symbol', '₹')
        cash_balance = self.auth_manager.get_current_user_data().get('cash_balance', 0.0)
        
        # Account cards
        self._create_account_card(scrollable_frame, "Cash", "💵", f"{currency}{cash_balance:.2f}", 
                                   "▲ 5%", self.PRIMARY_COLOR, self.SECONDARY_COLOR)
        self._create_account_card(scrollable_frame, "Bank", "🏦", f"{currency}5,234.56", 
                                   "▲ 2%", "#66BB6A", "#4CAF50")
        self._create_account_card(scrollable_frame, "Credit Card", "💳", f"{currency}2,150.00", 
                                   "▼ 10%", "#FFA726", "#FF9800")
        
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
    
    def _create_account_card(self, parent, account_type, icon, balance, trend, color1, color2):
        """Create an individual account card with gradient background"""
        # Note: Tkinter doesn't support gradients natively, so we'll use a solid color
        card_frame = tk.Frame(parent, bg=color1, width=200, height=120, bd=0, relief=tk.FLAT)
        card_frame.pack(side=tk.LEFT, padx=8)
        card_frame.pack_propagate(False)
        
        # Add padding frame
        content_frame = tk.Frame(card_frame, bg=color1)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)
        
        # Icon
        tk.Label(
            content_frame,
            text=icon,
            font=self.FONT_KPI,
            bg=color1,
            fg=self.WHITE
        ).pack(anchor="nw")
        
        # Type
        tk.Label(
            content_frame,
            text=account_type,
            font=self.FONT_CAPTION,
            bg=color1,
            fg=self.WHITE
        ).pack(anchor="nw", pady=(4, 8))
        
        # Balance
        tk.Label(
            content_frame,
            text=balance,
            font=self.FONT_VALUE,
            bg=color1,
            fg=self.WHITE
        ).pack(anchor="w")
        
        # Trend
        tk.Label(
            content_frame,
            text=trend,
            font=self.FONT_CAPTION,
            bg=color1,
            fg=self.WHITE
        ).pack(anchor="sw", side=tk.BOTTOM)
        
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
        currency = self.auth_manager.get_current_user_data().get('currency_symbol', '₹')
        monthly_budget = self.auth_manager.get_current_user_data().get('monthly_budget', 10000)
        spent_amount = 6800
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
            text=f"{currency}{spent_amount:,.2f}",
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
            text=f"{currency}{monthly_budget:,.2f}",
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
            text=f"{currency}{remaining:,.2f}",
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
            font=self.FONT_HEADER,
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
        
        search_icon = tk.Label(search_frame, text="🔍", font=self.FONT_MD, bg="#F7F8FA")
        search_icon.pack(side=tk.LEFT, padx=8)
        
        self.search_entry = tk.Entry(
            search_frame,
            font=self.FONT_BODY,
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
        style.configure("Transactions.Treeview", 
                       background=self.WHITE,
                       foreground=self.TEXT_DARK,
                       rowheight=40,
                       fieldbackground=self.WHITE,
                       borderwidth=0)
        style.configure("Transactions.Treeview.Heading",
                       background=self.BG_LIGHT,
                       foreground=self.TEXT_DARK,
                       font=self.FONT_SUBHEADER)
        
        columns = ("Date", "Category", "Amount")
        self.transactions_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Transactions.Treeview",
            height=6
        )
        
        for col in columns:
            self.transactions_tree.heading(col, text=col, anchor=tk.W)
            if col == "Amount":
                self.transactions_tree.column(col, anchor=tk.E, width=100)
            else:
                self.transactions_tree.column(col, anchor=tk.W, width=120)
        
        # Sample data
        sample_transactions = [
            ("Oct 18", "🍔 Food", f"-₹150.00", "food"),
            ("Oct 17", "🚌 Transport", f"-₹50.00", "transport"),
            ("Oct 16", "💸 Salary", f"+₹5,000.00", "income"),
            ("Oct 15", "🎬 Entertainment", f"-₹300.00", "entertainment"),
            ("Oct 14", "🛒 Shopping", f"-₹700.00", "shopping"),
            ("Oct 13", "💡 Utilities", f"-₹400.00", "utilities"),
        ]
        
        for item in sample_transactions:
            self.transactions_tree.insert("", "end", values=item[:-1], tags=(item[-1],))
        
        # Configure tags for color-coding
        self.transactions_tree.tag_configure("food", foreground=self.CATEGORY_COLORS['Food'])
        self.transactions_tree.tag_configure("transport", foreground=self.CATEGORY_COLORS['Transport'])
        self.transactions_tree.tag_configure("income", foreground=self.SUCCESS)
        self.transactions_tree.tag_configure("entertainment", foreground=self.CATEGORY_COLORS['Entertainment'])
        self.transactions_tree.tag_configure("shopping", foreground=self.CATEGORY_COLORS['Shopping'])
        self.transactions_tree.tag_configure("utilities", foreground=self.CATEGORY_COLORS['Utilities'])
        
        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # View all link
        view_all = tk.Label(
            card_frame,
            text="View All Transactions →",
            font=self.FONT_BODY,
            bg=self.WHITE,
            fg=self.PRIMARY_COLOR,
            cursor="hand2"
        )
        view_all.pack(pady=(8, 0))
        view_all.bind("<Button-1>", lambda e: messagebox.showinfo("View All", "Full transaction list coming soon!"))
    
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
        
        # Top 3 categories
        top_categories = [
            ("🥇", "🍔 Food", "₹3,120", 35, self.CATEGORY_COLORS['Food']),
            ("🥈", "🚌 Transport", "₹2,230", 25, self.CATEGORY_COLORS['Transport']),
            ("🥉", "🎬 Entertainment", "₹1,340", 15, self.CATEGORY_COLORS['Entertainment']),
        ]
        
        for rank, category, amount, percentage, color in top_categories:
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
                text=f"{percentage}% of total",
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
        self.fab_menu_visible = False
        
        # Container for FAB and sub-buttons
        fab_container = tk.Frame(parent, bg=self.BG_LIGHT)
        fab_container.place(relx=0.95, rely=0.93, anchor=tk.SE)
        
        # Sub-buttons frame (initially hidden)
        self.fab_sub_frame = tk.Frame(fab_container, bg=self.BG_LIGHT)
        
        # Sub-buttons
        sub_buttons = [
            ("💸", "Add Expense", self.ERROR, self.show_add_transaction_modal),
            ("💰", "Add Income", self.SUCCESS, self.show_add_income_modal),
            ("🎯", "Add Budget", self.PRIMARY_COLOR, self.show_add_budget_modal),
        ]
        
        for icon, text, color, command in reversed(sub_buttons):
            btn_shadow, btn_card = self._create_shadow_card(self.fab_sub_frame, self.WHITE)
            btn_shadow.pack(pady=4)
            
            btn_content = tk.Frame(btn_card, bg=self.WHITE)
            btn_content.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(
                btn_content,
                text=icon,
                font=self.FONT_XXL,
                bg=self.WHITE,
                fg=color
            ).pack(side=tk.LEFT, padx=8)
            
            tk.Label(
                btn_content,
                text=text,
                font=self.FONT_BODY,
                bg=self.WHITE,
                fg=self.TEXT_DARK
            ).pack(side=tk.LEFT, padx=8)
            
            btn_card.bind("<Button-1>", lambda e, cmd=command: cmd())
            btn_card.bind("<Enter>", lambda e, bc=btn_card: bc.config(bg="#F0F0F0"))
            btn_card.bind("<Leave>", lambda e, bc=btn_card: bc.config(bg=self.WHITE))
        
        # Main FAB button
        fab_button = tk.Label(
            fab_container,
            text="➕",
            font=self.FONT_KPI,
            bg=self.ACCENT_COLOR,
            fg=self.WHITE,
            width=2,
            height=1,
            cursor="hand2",
            bd=0,
            relief=tk.FLAT
        )
        fab_button.pack()
        
        def toggle_fab_menu(e=None):
            if self.fab_menu_visible:
                self.fab_sub_frame.pack_forget()
                fab_button.config(text="➕")
                self.fab_menu_visible = False
            else:
                self.fab_sub_frame.pack(side=tk.TOP, pady=(0, 8))
                fab_button.config(text="✕")
                self.fab_menu_visible = True
        
        fab_button.bind("<Button-1>", toggle_fab_menu)
        
        # Hover effect
        def on_fab_enter(e):
            fab_button.config(bg=self.SECONDARY_COLOR)
        
        def on_fab_leave(e):
            fab_button.config(bg=self.ACCENT_COLOR)
        
        fab_button.bind("<Enter>", on_fab_enter)
        fab_button.bind("<Leave>", on_fab_leave)

    def _create_sidebar(self, parent):
        """Create the left sidebar with profile, navigation, and settings"""
        sidebar_width = 280
        sidebar_frame = tk.Frame(parent, bg=self.WHITE, width=sidebar_width)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
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

        profile_icon = tk.Label(
            profile_frame,
            text="👤",
            font=self.FONT_3XL,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        )
        profile_icon.pack(anchor="w")

        user_name = self.auth_manager.get_current_user_data().get('name', 'User')
        profile_name = tk.Label(
            profile_frame,
            text=user_name.capitalize(),
            font=self.FONT_XXL,
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        )
        profile_name.pack(anchor="w", pady=(10, 0))

        tk.Label(
            profile_frame,
            text="My Wallet",
            font=self.FONT_BODY,
            bg=self.PRIMARY_COLOR,
            fg="#d8e0f0"
        ).pack(anchor="w")

        # Navigation Links
        nav_frame = tk.Frame(scrollable_sidebar_frame, bg=self.WHITE, padx=10, pady=10)
        nav_frame.pack(fill=tk.BOTH, expand=True)

        nav_items_top = [
            ("⬆️", "Get Premium"),
            ("🏦", "Bank Sync"),
            ("⬇️", "Imports"),
        ]
        self._create_nav_section(nav_frame, nav_items_top, section_title=None)

        tk.Frame(nav_frame, bg=self.BG_LIGHT, height=1).pack(fill=tk.X, pady=10)

        nav_items_main = [
            ("🏠", "Home"),
            ("📋", "Records"),
            ("📈", "Investments", "New"),
            ("📊", "Statistics", "New"),
            ("🗓️", "Planned payments"),
            ("💰", "Budgets"),
            ("📉", "Debts"),
            ("🎯", "Goals"),
            ("💼", "Wallet for your business", "New"),
        ]
        self._create_nav_section(nav_frame, nav_items_main, section_title=None)

        tk.Frame(nav_frame, bg=self.BG_LIGHT, height=1).pack(fill=tk.X, pady=10)

        nav_items_more = [
            ("🛒", "Shopping lists"),
            ("🛡️", "Warranties"),
            ("💳", "Loyalty cards"),
            ("💱", "Currency rates"),
            ("👥", "Group sharing"),
            ("•••", "Others"),
        ]
        self._create_nav_section(nav_frame, nav_items_more, section_title=None)

        tk.Frame(nav_frame, bg=self.BG_LIGHT, height=1).pack(fill=tk.X, pady=10)

        # Settings and Utilities
        settings_frame = tk.Frame(scrollable_sidebar_frame, bg=self.WHITE, padx=10, pady=10)
        settings_frame.pack(fill=tk.X, expand=True)

        settings_items = [
            ("🌚", "Dark mode", "toggle"),
            ("🙈", "Hide Amounts", "toggle"),
            ("✉️", "Invite friends"),
            ("💖", "Follow us"),
            ("❓", "Help"),
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
            item_frame.bind("<Button-1>", lambda e, txt=text: messagebox.showinfo("Sidebar", f"{txt} clicked!"))

    # OLD METHODS - TO BE REMOVED OR KEPT FOR COMPATIBILITY
    def toggle_sidebar(self):
        """Legacy method - no longer used in new dashboard"""
        pass
    
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
