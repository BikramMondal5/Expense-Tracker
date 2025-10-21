import tkinter as tk
from tkinter import messagebox
import config
from datetime import datetime
from tkcalendar import Calendar

def display_add_expense_screen(root, auth_manager, dashboard_instance):
    """Displays the add expense screen as a modal popup."""
    # Create a modal window (Toplevel)
    modal = tk.Toplevel(root)
    modal.title("Add Expense")
    modal.geometry("450x600")
    modal.resizable(False, False)
    
    # Make it modal
    modal.transient(root)
    modal.grab_set()
    
    # Center the modal on screen
    modal.update_idletasks()
    x = modal.winfo_screenwidth() - 450 - 20  # 20px padding from right edge
    y = modal.winfo_screenheight() - 600 - 170 # Increased padding from bottom
    modal.geometry(f"450x600+{x}+{y}")

    # Main container with light blue background
    main_frame = tk.Frame(modal, bg="#00BFFF")
    main_frame.pack(fill=tk.BOTH, expand=True)
    main_frame.grid_rowconfigure(0, weight=5) # Reduced weight for blue section
    main_frame.grid_rowconfigure(1, weight=5) # Increased weight for keypad section
    main_frame.grid_columnconfigure(0, weight=1)

    # Blue section frame to hold all top elements
    blue_section_frame = tk.Frame(main_frame, bg="#00BFFF")
    blue_section_frame.grid(row=0, column=0, sticky="nsew")

    # Top section with amount display
    top_section = tk.Frame(blue_section_frame, bg="#00BFFF")
    top_section.pack(fill=tk.X)

    # New frame to hold calendar, amount, and currency on the same row
    top_header_row_frame = tk.Frame(blue_section_frame, bg="#00BFFF")
    top_header_row_frame.pack(fill=tk.X, pady=(10, 0)) # Reduced top padding here

    # Back button (calendar icon)
    date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d")) # Initialize with current date

    def show_calendar_modal():
        calendar_modal = tk.Toplevel(modal)
        calendar_modal.title("Select Date")
        calendar_modal.transient(modal)
        calendar_modal.grab_set()
        
        cal = Calendar(calendar_modal, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=20)

        def set_date():
            selected_date = cal.selection_get()
            date_var.set(selected_date.strftime("%Y-%m-%d"))
            date_label.config(text=date_var.get()) # Update the date label
            calendar_modal.destroy()

        tk.Button(calendar_modal, text="Select Date", command=set_date).pack(pady=10)

    back_btn = tk.Label(
        top_header_row_frame, # Packed in the new header row
        text="📅", # Changed to calendar icon
        font=("Segoe UI Emoji", 20),
        bg="#00BFFF",
        fg="white",
        cursor="hand2"
    )
    back_btn.pack(side=tk.LEFT, anchor="nw", padx=20, pady=0) # Aligned left, no vertical padding
    back_btn.bind("<Button-1>", lambda e: show_calendar_modal()) # Bind to show_calendar_modal

    # Amount display frame (now within top_header_row_frame)
    amount_display_frame = tk.Frame(top_header_row_frame, bg="#00BFFF")
    amount_display_frame.pack(side=tk.RIGHT, expand=True, padx=(0,20)) # Packed right within header row

    amount_value_label = tk.Label(
        amount_display_frame,
        text="0",
        font=("Segoe UI", 60, "bold"),
        bg="#00BFFF",
        fg="white"
    )
    amount_value_label.pack(side=tk.LEFT, expand=True)

    # Get user's currency
    user_data = auth_manager.get_current_user_data()
    currency_code = user_data.get('currency', 'INR')
    
    amount_currency_label = tk.Label(
        amount_display_frame,
        text=currency_code,
        font=("Segoe UI", 24, "bold"),
        bg="#00BFFF",
        fg="white"
    )
    amount_currency_label.pack(side=tk.LEFT, padx=(10, 0))

    # Current Date display (remains below, but adjust padding)
    date_label = tk.Label(
        blue_section_frame,
        textvariable=date_var, # Use StringVar for dynamic update
        font=("Segoe UI", 12),
        bg="#00BFFF",
        fg="white"
    )
    date_label.pack(pady=(0, 15)) # Added bottom padding for spacing

    # Account and Category selection section
    selection_frame = tk.Frame(blue_section_frame, bg="#00BFFF")
    selection_frame.pack(fill=tk.X, pady=(0, 15)) # Added bottom padding here

    # Account selector
    account_frame = tk.Frame(selection_frame, bg="#00BFFF")
    account_frame.pack(side=tk.LEFT, expand=True, padx=20)

    account_label = tk.Label(
        account_frame,
        text="Account",
        font=("Segoe UI", 10),
        bg="#00BFFF",
        fg="white"
    )
    account_label.pack()

    account_var = tk.StringVar(value="CASH")
    account_options = ["CASH", "BANK", "CREDIT CARD", "WALLET"]
    
    account_display = tk.Label(
        account_frame,
        text=account_var.get(),
        font=("Segoe UI", 14, "bold"),
        bg="#00BFFF",
        fg="white",
        cursor="hand2"
    )
    account_display.pack(pady=(5, 0))

    # Category selector
    category_frame = tk.Frame(selection_frame, bg="#00BFFF")
    category_frame.pack(side=tk.LEFT, expand=True, padx=20)

    category_label = tk.Label(
        category_frame,
        text="Category",
        font=("Segoe UI", 10),
        bg="#00BFFF",
        fg="white"
    )
    category_label.pack()

    category_var = tk.StringVar(value="FUEL")
    category_options = ["FOOD", "TRANSPORT", "FUEL", "ENTERTAINMENT", "UTILITIES", "SHOPPING", "OTHERS"]
    
    category_display = tk.Label(
        category_frame,
        text=category_var.get(),
        font=("Segoe UI", 14, "bold"),
        bg="#00BFFF",
        fg="white",
        cursor="hand2"
    )
    category_display.pack(pady=(5, 0))

    # Simple dropdown functionality for account
    def show_account_menu(event):
        menu = tk.Menu(modal, tearoff=0, font=("Segoe UI", 10))
        for option in account_options:
            menu.add_command(
                label=option,
                command=lambda opt=option: [account_var.set(opt), account_display.config(text=opt)]
            )
        menu.post(event.x_root, event.y_root)

    # Simple dropdown functionality for category
    def show_category_menu(event):
        menu = tk.Menu(modal, tearoff=0, font=("Segoe UI", 10))
        for option in category_options:
            menu.add_command(
                label=option,
                command=lambda opt=option: [category_var.set(opt), category_display.config(text=opt)]
            )
        menu.post(event.x_root, event.y_root)

    account_display.bind("<Button-1>", show_account_menu)
    category_display.bind("<Button-1>", show_category_menu)

    def open_templates_modal():
        pass

    # Templates button
    templates_btn = tk.Button(
        blue_section_frame,
        text="TEMPLATES",
        font=("Segoe UI", 10, "bold"),
        bg="#00BFFF",
        fg="white",
        relief=tk.FLAT,
        bd=0,
        cursor="hand2",
        activebackground="#00BFFF",
        activeforeground="white",
        command=open_templates_modal
    )
    templates_btn.pack(pady=(0, 15)) # Added bottom padding here

    # Function to update the amount display
    def update_amount_display(value):
        current_text = amount_value_label.cget("text")
        # Ensure only one decimal point
        if "." in current_text and value == ".":
            return
        # Prevent leading zero unless it's a decimal
        if current_text == "0" and value != ".":
            amount_value_label.config(text=value)
        elif len(current_text) < 12:  # Limit input length
            amount_value_label.config(text=current_text + value)
    
    # Function to delete the last character
    def delete_last_char():
        current_text = amount_value_label.cget("text")
        if len(current_text) > 1:
            amount_value_label.config(text=current_text[:-1])
        else:
            amount_value_label.config(text="0")

    # Numeric Keypad Section
    keypad_container = tk.Frame(main_frame, bg="lightgray")
    keypad_container.grid(row=1, column=0, sticky="nsew")

    # Keypad frame with light gray background
    keypad_frame = tk.Frame(keypad_container, bg="#F0F0F0")
    keypad_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

    keys = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [".", "0", "⌫",]
    ]

    # Function to handle key presses
    def on_key_press(key):
        if key == "⌫":
            delete_last_char()
        elif key in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            update_amount_display(key)

    # Function to simulate button press visual feedback
    # def on_key_enter(e):
    #     if e.widget.cget("text") in ["÷", "×", "-", "+"]:
    #         e.widget['background'] = "#D0D0D0"
    #     else:
    #         e.widget['background'] = "#E0E0E0"

    # def on_key_leave(e):
    #     if e.widget.cget("text") in ["÷", "×", "-", "+"]:
    #         e.widget['background'] = "#3591e2" # Blue for operators
    #     elif e.widget.cget("text") == "⌫":
    #         e.widget['background'] = "#FF6B6B"  # Light red for backspace
    #     elif e.widget.cget("text") == ".":
    #         e.widget['background'] = "#C0C0C0"
    #     else:
    #         e.widget['background'] = "#E0E0E0"


    def process_expense():
        try:
            amount = float(amount_value_label.cget("text"))
            if amount <= 0:
                messagebox.showwarning("Invalid Amount", "Amount must be greater than zero.")
                return

            # Get expense details
            account = account_var.get()
            category = category_var.get()
            date = date_var.get() # Get the selected date
            
            # Here you would typically save to the auth_manager
            # For now, we'll show a success message and go back to dashboard
            user_data = auth_manager.get_current_user_data()
            
            # Initialize expenses list if it doesn't exist
            if 'expenses' not in user_data:
                user_data['expenses'] = []
            
            # Create expense entry
            expense_entry = {
                'amount': amount,
                'category': category,
                'account': account,
                'date': date, # Store the selected date
                'timestamp': f"{date} {datetime.now().strftime('%H:%M:%S')}"
            }
            
            user_data['expenses'].append(expense_entry)
            
            # Update cash balance
            if account == "CASH": # Assuming only CASH affects cash_balance for now
                user_data['cash_balance'] -= amount
            elif account == "BANK":
                user_data['bank_balance'] -= amount
            elif account == "CREDIT CARD":
                user_data['credit_card_balance'] -= amount

            auth_manager.save_users()
            
            messagebox.showinfo("Success", f"Expense of {currency_code} {amount} added successfully!")
            modal.destroy()
            dashboard_instance.display_dashboard()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create keypad buttons
    for r_idx, row in enumerate(keys):
        keypad_frame.grid_rowconfigure(r_idx, weight=1)
        
        for c_idx, key in enumerate(row):
            keypad_frame.grid_columnconfigure(c_idx, weight=1)

            # Determine button color based on key type
            # All numeric and functional keys will have a consistent light grey background and dark text.
            bg_color = "#E0E0E0"
            fg_color = "#333333"
            active_bg_color = "#D0D0D0"
            active_fg_color = "#333333"

            # Specific styling for backspace (X) for visual distinction, if desired, otherwise it will match numbers
            if key == "⌫":
                bg_color = "#E0E0E0"  # Keep consistent with other keys
                fg_color = "#333333" # Dark text for backspace symbol
                active_bg_color = "#FF8F8F" # Slightly redder on hover for delete action
                active_fg_color = "white"

            key_button = tk.Button(
                keypad_frame,
                text=key,
                font=("Segoe UI", 24),
                bg=bg_color,
                fg=fg_color,
                activebackground=active_bg_color,
                activeforeground=active_fg_color,
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                command=lambda k=key: on_key_press(k)
            )
            key_button.grid(row=r_idx, column=c_idx, sticky="nsew", padx=1, pady=1)
    
    # Submit button - now in a separate row at the bottom
    keypad_frame.grid_rowconfigure(len(keys), weight=1) # Configure the new row
    submit_button = tk.Button(
        keypad_frame,
        text="Submit",
        font=("Segoe UI", 24, "bold"),
        bg="#5C6BC0",
        fg="white",
        activebackground="#4A5B9C",
        activeforeground="white",
        relief=tk.FLAT,
        bd=0,
        cursor="hand2",
        command=lambda: process_expense()
    )
    submit_button.grid(row=len(keys), column=0, columnspan=3, sticky="nsew", padx=1, pady=1)

def display_onboarding_screen(root, auth_manager, app_instance, primary_color, secondary_color, accent_color, bg_light, text_dark, text_light, white, success, error):
    """Displays the combined onboarding screen for monthly budget and currency."""
    # Clear existing widgets from root
    for widget in root.winfo_children():
        widget.destroy()

    # Main container
    main_frame = tk.Frame(root, bg="#EEF2FF")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Center content container
    center_frame = tk.Frame(main_frame, bg="#FFFFFF")
    center_frame.place(relx=0.5, rely=0.5, anchor="center", width=500)



    # Content padding frame
    content_frame = tk.Frame(center_frame, bg=white)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

    # Icon
    icon_frame = tk.Frame(content_frame, bg="#FFFFFF", width=80, height=80)
    icon_frame.pack(pady=(10, 20))
    icon_frame.pack_propagate(False)
    icon_frame.layer = True
    icon_frame.config(highlightbackground="#E2E8F0", highlightthickness=1, borderwidth=0, relief=tk.SOLID)


    onboarding_icon_label = tk.Label(
        icon_frame,
        text="🚀",  # Rocket icon for onboarding
        font=("Segoe UI Emoji", 30),
        bg="#FFFFFF",
        fg="#6366F1"
    )
    onboarding_icon_label.place(relx=0.5, rely=0.5, anchor="center")

    # Title
    title_label = tk.Label(
        content_frame,
        text="Set up Your Monthly Budget",
        font=("Segoe UI", 22, "bold"),
        bg="#FFFFFF",
        fg="#1E293B"
    )
    title_label.pack(pady=(10, 5))

    # Subtitle
    subtitle_label = tk.Label(
        content_frame,
        text="Let's set your monthly budget and preferred currency.",
        font=("Segoe UI", 12),
        bg="#FFFFFF",
        fg="#64748B",
        wraplength=400
    )
    subtitle_label.pack(pady=(0, 30))

    # Currency selector
    currency_frame = tk.Frame(content_frame, bg=white)
    currency_frame.pack(fill=tk.X, pady=(10, 5))
    
    currency_label = tk.Label(
        currency_frame,
        text="Target Currency",
        font=("Segoe UI", 11, "bold"),
        bg="#FFFFFF",
        fg="#1E293B"
    )
    currency_label.pack(anchor="w")
    
    currency_options = ["INR - Indian Rupee (₹)", "USD - US Dollar ($)", "EUR - Euro (€)", 
                      "GBP - British Pound (£)", "JPY - Japanese Yen (¥)", "AUD - Australian Dollar ($)"]
    currency_var = tk.StringVar(value=currency_options[0])
    
    currency_menu_frame = tk.Frame(content_frame, bg="#F8FAFC", relief=tk.FLAT, bd=0)
    currency_menu_frame.pack(fill=tk.X, pady=(5, 10))
    
    currency_menu = tk.OptionMenu(
        currency_menu_frame,
        currency_var,
        *currency_options
    )
    currency_menu.config(
        font=("Segoe UI", 11),
        bg="#F8FAFC",
        fg="#1E293B",
        activebackground="#E2E8F0",
        activeforeground="#1E293B",
        relief=tk.FLAT,
        bd=0,
        highlightthickness=0,
        width=35,
        anchor="w"
    )
    currency_menu.pack(fill=tk.X, ipady=8)

    # Monthly Budget Input
    budget_display_frame = tk.Frame(content_frame, bg="#F8FAFC", height=60)
    budget_display_frame.pack(fill=tk.X, pady=(10, 15))
    budget_display_frame.pack_propagate(False)

    budget_value_label = tk.Label(
        budget_display_frame,
        text="0",
        font=("Segoe UI", 32, "bold"),
        bg="#F8FAFC",
        fg="#111827"
    )
    budget_value_label.pack(side=tk.LEFT, padx=(20, 0), expand=True, fill=tk.BOTH)

    budget_currency_code_label = tk.Label(
        budget_display_frame,
        text="INR",
        font=("Segoe UI", 16),
        bg="#F8FAFC",
        fg="#111827"
    )
    budget_currency_code_label.pack(side=tk.LEFT, padx=(0, 10))

    clear_budget_btn = tk.Label(
        budget_display_frame,
        text="✕",
        font=("Segoe UI", 16, "bold"),
        bg="#FEE2E2",
        fg="#B91C1C",
        cursor="hand2"
    )
    clear_budget_btn.pack(side=tk.RIGHT, padx=(0, 15))
    clear_budget_btn.bind("<Button-1>", lambda e: budget_value_label.config(text="0"))
    
    # Function to update the prominent budget display
    def update_budget_display(value):
        # Ensure only one decimal point
        if "." in budget_value_label.cget("text") and value == ".":
            return
        # Prevent leading zero unless it's a decimal
        if budget_value_label.cget("text") == "0" and value != ".":
            budget_value_label.config(text=value)
        elif len(budget_value_label.cget("text")) < 12: # Limit input length
            budget_value_label.config(text=budget_value_label.cget("text") + value)
    
    # Function to delete the last character
    def delete_last_char():
        current_text = budget_value_label.cget("text")
        if len(current_text) > 1:
            budget_value_label.config(text=current_text[:-1])
        else:
            budget_value_label.config(text="0")

    # Update currency display when selection changes
    def update_currency_display(*args):
        selected = currency_var.get()
        currency_code = selected.split(" - ")[0]
        budget_currency_code_label.config(text=currency_code)
    
    currency_var.trace("w", update_currency_display)
    update_currency_display() # Initialize currency display

    # Numeric Keypad
    keypad_frame = tk.Frame(content_frame, bg="#FFFFFF")
    keypad_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))

    keys = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        [".", "0", "⌫"]
    ]

    def on_enter(e):
        e.widget['background'] = "#C7D2FE"

    def on_leave(e):
        e.widget['background'] = "#E0E7FF"

    def complete_onboarding(budget, currency):
        try:
            monthly_budget = float(budget)
            if monthly_budget <= 0:
                messagebox.showwarning("Invalid Budget", "Monthly budget must be greater than zero.")
                return

            currency_symbol = currency.split('(')[1].split(')')[0]
            currency_code = currency.split(' - ')[0]

            success, message = auth_manager.onboard_user(budget, currency_var.get())
            
            if success:
                messagebox.showinfo("Setup Complete", message)
                app_instance.show_dashboard()
            else:
                messagebox.showerror("Error", message)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the budget.")
        except IndexError:
            messagebox.showerror("Invalid Currency", "Please select a valid currency.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    for r_idx, row in enumerate(keys):
        keypad_frame.grid_rowconfigure(r_idx, weight=1)
        for c_idx, key in enumerate(row):
            keypad_frame.grid_columnconfigure(c_idx, weight=1)

            key_button = tk.Button(
                keypad_frame,
                text=key,
                font=("Segoe UI", 22, "bold"),
                bg="#E0E7FF",
                fg="#312E81",
                activebackground="#C7D2FE",
                activeforeground="#312E81",
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                command=lambda k=key: update_budget_display(k) if k != "⌫" else delete_last_char()
            )
            key_button.grid(row=r_idx, column=c_idx, sticky="nsew", padx=8, pady=8)
            key_button.bind("<Enter>", on_enter)
            key_button.bind("<Leave>", on_leave)

            if key == "⌫":
                key_button.config(fg="#312E81")

    # Complete Setup Button
    complete_setup_btn = tk.Button(
        content_frame,
        text="Complete Setup",
        font=("Segoe UI", 14, "bold"),
        bg="#3591e2",
        fg="white",
        activebackground="#2c79c1",
        activeforeground="white",
        relief=tk.FLAT,
        bd=0,
        cursor="hand2",
        command=lambda: complete_onboarding(budget_value_label.cget("text"), currency_var.get())
    )
    complete_setup_btn.pack(fill=tk.X, ipady=12, pady=(20, 0))
