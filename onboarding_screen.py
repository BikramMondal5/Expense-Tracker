import tkinter as tk
from tkinter import messagebox
import config

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
