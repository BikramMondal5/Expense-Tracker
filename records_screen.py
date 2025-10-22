import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import config

# Define periods for filtering
periods = [
    ("7D", "7 Days"),
    ("30D", "30 Days"),
    ("12W", "12 Weeks"),
    ("6M", "6 Months"),
    ("1Y", "1 Year"),
    ("Custom", "Custom")
]

def display_records_screen(root, auth_manager, dashboard_instance):
    """Displays the records screen as a modal popup."""
    print("display_records_screen called!")
    # Create a modal window (Toplevel)
    modal = tk.Toplevel(root)
    modal.title("Records")
    modal.geometry("450x700")
    modal.resizable(False, False)
    
    # Make it modal
    modal.transient(root)
    modal.grab_set()
    
    # Center the modal on screen
    modal.update_idletasks()
    x = (modal.winfo_screenwidth() - 450) // 2
    y = (modal.winfo_screenheight() - 700) // 2
    modal.geometry(f"450x700+{x}+{y}")

    # Main container with primary color background
    main_frame = tk.Frame(modal, bg=config.PRIMARY_COLOR)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Header section
    header_frame = tk.Frame(main_frame, bg=config.PRIMARY_COLOR)
    header_frame.pack(fill=tk.X, padx=20, pady=15)

    # Menu icon (left) - close button
    menu_icon = tk.Label(
        header_frame,
        text="✕",
        font=("Segoe UI", 24, "bold"),
        bg=config.PRIMARY_COLOR,
        fg=config.WHITE,
        cursor="hand2"
    )
    menu_icon.pack(side=tk.LEFT, padx=(0, 10))
    menu_icon.bind("<Button-1>", lambda e: modal.destroy())

    # Title (center)
    title_label = tk.Label(
        header_frame,
        text="Records",
        font=("Segoe UI", 20, "bold"),
        bg=config.PRIMARY_COLOR,
        fg=config.WHITE
    )
    title_label.pack(side=tk.LEFT, expand=True)

    # Search and More icons (right)
    icons_frame = tk.Frame(header_frame, bg=config.PRIMARY_COLOR)
    icons_frame.pack(side=tk.RIGHT)

    search_icon = tk.Label(
        icons_frame,
        text="🔍",
        font=("Segoe UI", 18),
        bg=config.PRIMARY_COLOR,
        fg=config.WHITE,
        cursor="hand2"
    )
    search_icon.pack(side=tk.LEFT, padx=5)

    more_icon = tk.Label(
        icons_frame,
        text="⋮",
        font=("Segoe UI", 24),
        bg=config.PRIMARY_COLOR,
        fg=config.WHITE,
        cursor="hand2"
    )
    more_icon.pack(side=tk.LEFT, padx=5)

    # Time period buttons section
    period_frame = tk.Frame(main_frame, bg=config.PRIMARY_COLOR)
    period_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

    # Variable to track selected period
    selected_period = tk.StringVar(value="1Y")

    def update_period_buttons():
        """Update the appearance of period buttons based on selection"""
        current_period = selected_period.get()
        for btn, period_code in period_buttons:
            btn.configure(
                bg=config.ACCENT_COLOR if period_code == current_period else config.PRIMARY_COLOR,
                fg=config.WHITE
            )

    # Summary section (white card)
    summary_frame = tk.Frame(main_frame, bg=config.WHITE)
    summary_frame.pack(fill=tk.X, padx=15, pady=10)

    # Get user data
    user_data = auth_manager.get_current_user_data()
    currency = user_data.get('currency', 'INR')
    currency_symbol = '₹' if currency == 'INR' else '$'
    expenses = user_data.get('expenses', [])

    # Calculate total for selected period
    total_amount = tk.StringVar(value="0.00")
    period_label_text = tk.StringVar(value="LAST 1 YEAR")

    summary_header = tk.Label(
        summary_frame,
        textvariable=period_label_text,
        font=("Segoe UI", 10, "bold"),
        bg=config.WHITE,
        fg=config.TEXT_LIGHT,
        anchor="w"
    )
    summary_header.pack(fill=tk.X, padx=15, pady=(15, 5))

    summary_amount = tk.Label(
        summary_frame,
        textvariable=total_amount,
        font=("Segoe UI", 24, "bold"),
        bg=config.WHITE,
        fg=config.TEXT_DARK,
        anchor="e"
    )
    summary_amount.pack(fill=tk.X, padx=15, pady=(0, 15))

    # Scrollable transactions list - white container
    list_outer_container = tk.Frame(main_frame, bg=config.BG_LIGHT)
    list_outer_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=0)

    # White background container
    list_container = tk.Frame(list_outer_container, bg=config.WHITE)
    list_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)

    # Canvas for scrolling
    canvas = tk.Canvas(list_container, bg=config.WHITE, highlightthickness=0)
    scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=config.WHITE)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Category icons and colors
    category_icons = {
        'FOOD': '🍔',
        'TRANSPORT': '🚌',
        'FUEL': '⛽',
        'ENTERTAINMENT': '🎬',
        'UTILITIES': '💡',
        'SHOPPING': '🛍️',
        'OTHERS': '📦',
        'Education, development': '🎓',
        'Education': '🎓'
    }

    category_colors = {
        'FOOD': '#FF6B6B',
        'TRANSPORT': '#4ECDC4',
        'FUEL': '#9B59B6',
        'ENTERTAINMENT': '#E74C3C',
        'UTILITIES': '#F39C12',
        'SHOPPING': '#3498DB',
        'OTHERS': '#95A5A6',
        'Education, development': '#2ECC71',
        'Education': '#2ECC71'
    }

    def create_transaction_card(parent, expense_data, month_label=None):
        """Create a transaction card"""
        # Month separator if needed
        if month_label:
            separator = tk.Frame(parent, bg=config.WHITE, height=30)
            separator.pack(fill=tk.X)
            tk.Label(
                separator,
                text=month_label,
                font=("Segoe UI", 12, "bold"),
                bg=config.WHITE,
                fg=config.TEXT_DARK
            ).pack(side=tk.LEFT, padx=15)

        # Transaction card
        card = tk.Frame(parent, bg=config.WHITE, bd=0, relief=tk.FLAT)
        card.pack(fill=tk.X, padx=15, pady=5)

        # Icon circle
        category = expense_data.get('category', 'OTHERS')
        icon = category_icons.get(category, '📦')
        color = category_colors.get(category, '#95A5A6')

        icon_canvas = tk.Canvas(card, width=50, height=50, bg=config.WHITE, highlightthickness=0)
        icon_canvas.pack(side=tk.LEFT, padx=15, pady=15)
        
        # Draw colored circle
        icon_canvas.create_oval(5, 5, 45, 45, fill=color, outline="")
        
        # Add icon text
        icon_canvas.create_text(25, 25, text=icon, font=("Segoe UI", 20))

        # Details frame
        details_frame = tk.Frame(card, bg=config.WHITE)
        details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=15)

        # Category name
        category_display = category.replace('_', ', ').title()
        tk.Label(
            details_frame,
            text=category_display,
            font=("Segoe UI", 13, "bold"),
            bg=config.WHITE,
            fg=config.TEXT_DARK,
            anchor="w"
        ).pack(fill=tk.X)

        # Account type
        account = expense_data.get('account', 'Cash')
        tk.Label(
            details_frame,
            text=account.title(),
            font=("Segoe UI", 11),
            bg=config.WHITE,
            fg=config.TEXT_LIGHT,
            anchor="w"
        ).pack(fill=tk.X)

        # Amount and date
        amount_frame = tk.Frame(card, bg=config.WHITE)
        amount_frame.pack(side=tk.RIGHT, pady=15, padx=15)

        amount = expense_data.get('amount', 0)
        tk.Label(
            amount_frame,
            text=f"{currency_symbol}{amount:.2f}",
            font=("Segoe UI", 13, "bold"),
            bg=config.WHITE,
            fg=config.TEXT_DARK,
            anchor="e"
        ).pack()

        date = expense_data.get('date', '')
        tk.Label(
            amount_frame,
            text=date,
            font=("Segoe UI", 11),
            bg=config.WHITE,
            fg=config.TEXT_LIGHT,
            anchor="e"
        ).pack()

    def filter_expenses_by_period(period, start_date=None, end_date=None):
        """Filter expenses based on selected period"""
        # Clear existing cards
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Calculate date range
        today = datetime.now().date()
        if period == "custom":
            start_range = start_date
            end_range = end_date
        elif period == "7D":
            start_range = today - timedelta(days=7)
            end_range = today
            period_label_text.set("LAST 7 DAYS")
        elif period == "30D":
            start_range = today - timedelta(days=30)
            end_range = today
            period_label_text.set("LAST 30 DAYS")
        elif period == "12W":
            start_range = today - timedelta(weeks=12)
            end_range = today
            period_label_text.set("LAST 12 WEEKS")
        elif period == "6M":
            start_range = today - timedelta(days=180)
            end_range = today
            period_label_text.set("LAST 6 MONTHS")
        elif period == "1Y":
            start_range = today - timedelta(days=365)
            end_range = today
            period_label_text.set("LAST 1 YEAR")

        # Filter and sort expenses
        filtered_expenses = []
        period_total = 0

        for expense in expenses:
            try:
                expense_date = datetime.strptime(expense.get('date', ''), '%Y-%m-%d').date()
                if start_range <= expense_date <= end_range:
                    filtered_expenses.append(expense)
                    period_total += expense.get('amount', 0)
            except ValueError:
                continue  # Skip invalid dates

        # Update total amount
        total_amount.set(f"{currency_symbol}{period_total:.2f}")

        if not filtered_expenses:
            # Show a message if no expenses found
            empty_label = tk.Label(
                scrollable_frame,
                text="No expenses found for this period",
                font=("Segoe UI", 12),
                bg=config.WHITE,
                fg=config.TEXT_DARK
            )
            empty_label.pack(pady=20)
            return

        # Sort expenses by date
        filtered_expenses.sort(key=lambda x: x.get('date', ''), reverse=True)

        # Group by month and create cards
        current_month = None
        for expense in filtered_expenses:
            expense_date = datetime.strptime(expense.get('date', ''), '%Y-%m-%d')
            month_year = expense_date.strftime('%B %Y')

            if month_year != current_month:
                current_month = month_year
                create_transaction_card(scrollable_frame, expense, month_year)
            else:
                create_transaction_card(scrollable_frame, expense)

    def show_custom_date_picker():
        """Show custom date range picker"""
        date_modal = tk.Toplevel(modal)
        date_modal.title("Select Date Range")
        date_modal.geometry("300x200")
        date_modal.resizable(False, False)
        
        # Make it modal
        date_modal.transient(modal)
        date_modal.grab_set()
        
        # Center the modal
        date_modal.update_idletasks()
        x = modal.winfo_x() + (modal.winfo_width() - 300) // 2
        y = modal.winfo_y() + (modal.winfo_height() - 200) // 2
        date_modal.geometry(f"300x200+{x}+{y}")

        # Date picker frame
        picker_frame = tk.Frame(date_modal, bg=config.WHITE)
        picker_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # From date
        tk.Label(picker_frame, text="From:", bg=config.WHITE).pack(anchor="w")
        from_date = DateEntry(picker_frame, width=30, background=config.PRIMARY_COLOR,
                            foreground=config.WHITE, borderwidth=2)
        from_date.pack(fill=tk.X, pady=(0, 10))

        # To date
        tk.Label(picker_frame, text="To:", bg=config.WHITE).pack(anchor="w")
        to_date = DateEntry(picker_frame, width=30, background=config.PRIMARY_COLOR,
                         foreground=config.WHITE, borderwidth=2)
        to_date.pack(fill=tk.X, pady=(0, 20))

        # Buttons frame
        button_frame = tk.Frame(picker_frame, bg=config.WHITE)
        button_frame.pack(fill=tk.X)

        def apply_custom_range():
            """Apply the selected date range and filter expenses"""
            start_date = from_date.get_date()
            end_date = to_date.get_date()
            today = datetime.now().date()
            
            # Validate dates
            if start_date > end_date:
                messagebox.showerror("Error", "Start date cannot be after end date")
                return
                
            # Check for future dates
            if start_date > today or end_date > today:
                messagebox.showinfo("No Data", "No expenses available for future dates")
                period_label_text.set(f"CUSTOM: {start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}")
                total_amount.set(f"{currency_symbol}0.00")
                # Clear existing cards
                for widget in scrollable_frame.winfo_children():
                    widget.destroy()
                selected_period.set("Custom")
                update_period_buttons()
                date_modal.destroy()
                return

            # Filter expenses for the specific period
            filter_expenses_by_period("custom", start_date=start_date, end_date=end_date)
            period_label_text.set(f"CUSTOM: {start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}")
            selected_period.set("Custom")
            update_period_buttons()
            date_modal.destroy()

        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Segoe UI", 12),
            bg=config.BG_LIGHT,
            fg=config.TEXT_DARK,
            relief=tk.FLAT,
            command=date_modal.destroy
        )

        # Apply button
        apply_btn = tk.Button(
            button_frame,
            text="Apply",
            font=("Segoe UI", 12, "bold"),
            bg=config.PRIMARY_COLOR,
            fg=config.WHITE,
            activebackground=config.SECONDARY_COLOR,
            activeforeground=config.WHITE,
            relief=tk.FLAT,
            command=apply_custom_range
        )

        cancel_btn.pack(side=tk.LEFT, padx=5)
        apply_btn.pack(side=tk.RIGHT, padx=5)

    def on_period_select(period):
        """Handle period selection"""
        selected_period.set(period)
        if period == "Custom":
            show_custom_date_picker()
        else:
            filter_expenses_by_period(period)
        update_period_buttons()

    # Create period buttons
    period_buttons = []
    for i, (period_code, period_label) in enumerate(periods):
        btn = tk.Button(
            period_frame,
            text=period_label,
            font=("Segoe UI", 11),
            bg=config.PRIMARY_COLOR,
            fg=config.WHITE,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda p=period_code: on_period_select(p)
        )
        row = i // 3
        col = i % 3
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        period_buttons.append((btn, period_code))

    # Configure grid columns to expand equally
    for i in range(3):
        period_frame.grid_columnconfigure(i, weight=1)

    # Initial load - show 1 year by default
    filter_expenses_by_period("1Y")
    update_period_buttons()