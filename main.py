"""
Modern Login/Signup Modal with Interactive UI
Built with Python Tkinter with smooth animations and professional styling
"""

import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import hashlib
import re

class LoginSignupApp:
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Color scheme - Modern gradient colors
        self.PRIMARY_COLOR = "#667eea"
        self.SECONDARY_COLOR = "#764ba2"
        self.ACCENT_COLOR = "#f093fb"
        self.BG_LIGHT = "#f5f7fa"
        self.TEXT_DARK = "#2d3748"
        self.TEXT_LIGHT = "#718096"
        self.WHITE = "#ffffff"
        self.SUCCESS = "#48bb78"
        self.ERROR = "#f56565"
        
        # Remove default window styling
        self.root.configure(bg=self.BG_LIGHT)
        
        # Users data file
        self.users_file = "users.json"
        self.load_users()
        
        # Current user
        self.current_user = None
        
        # Show login screen
        self.show_login_screen()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def hash_password(self, password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit"
        return True, "Valid"
    
    def clear_frame(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Display the login screen"""
        self.clear_frame()
        
        # Main container with gradient effect
        main_frame = tk.Frame(self.root, bg=self.BG_LIGHT)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Left side - Branding (50%)
        left_panel = tk.Frame(main_frame, bg=self.PRIMARY_COLOR)
        left_panel.grid(row=0, column=0, sticky="nsew")
        
        # Branding content
        brand_frame = tk.Frame(left_panel, bg=self.PRIMARY_COLOR)
        brand_frame.pack(expand=True)
        
        # Logo/Icon
        logo_label = tk.Label(
            brand_frame,
            text="💰",
            font=("Arial", 80),
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        )
        logo_label.pack(pady=20)
        
        # Brand title
        title_label = tk.Label(
            brand_frame,
            text="Expense Tracker",
            font=("Segoe UI", 36, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        )
        title_label.pack(pady=10)
        
        # Brand subtitle
        subtitle_label = tk.Label(
            brand_frame,
            text="Manage Your Finances Smartly",
            font=("Segoe UI", 14),
            bg=self.PRIMARY_COLOR,
            fg="#d8e0f0"
        )
        subtitle_label.pack(pady=5)
        
        # Features list
        features_label = tk.Label(
            brand_frame,
            text="✓ Track Expenses\n✓ Analyze Spending\n✓ Visualize Data\n✓ Smart Insights",
            font=("Segoe UI", 12),
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE,
            justify=tk.LEFT
        )
        features_label.pack(pady=40)
        
        # Right side - Login form (50%)
        right_panel = tk.Frame(main_frame, bg=self.WHITE)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Form container with padding
        form_container = tk.Frame(right_panel, bg=self.WHITE)
        form_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Form title
        form_title = tk.Label(
            form_container,
            text="Welcome Back",
            font=("Segoe UI", 26, "bold"),
            bg=self.WHITE,
            fg=self.TEXT_DARK
        )
        form_title.pack(pady=(0, 5))
        
        # Form subtitle
        form_subtitle = tk.Label(
            form_container,
            text="Sign in to your account",
            font=("Segoe UI", 12),
            bg=self.WHITE,
            fg=self.TEXT_LIGHT
        )
        form_subtitle.pack(pady=(0, 30))
        
        # Email field
        email_label = tk.Label(
            form_container,
            text="Email Address",
            font=("Segoe UI", 11, "bold"),
            bg=self.WHITE,
            fg=self.TEXT_DARK
        )
        email_label.pack(anchor="w", pady=(10, 5))
        
        email_entry = tk.Entry(
            form_container,
            font=("Segoe UI", 11),
            bg="#f7fafc",
            fg=self.TEXT_DARK,
            relief=tk.FLAT,
            bd=0,
            width=30
        )
        email_entry.pack(fill=tk.X, ipady=12, pady=(0, 15))
        email_entry.insert(0, "")
        
        # Add subtle border effect
        email_border = tk.Frame(form_container, bg="#e2e8f0", height=1)
        email_border.pack(fill=tk.X, pady=(0, 15))
        
        # Password field
        password_label = tk.Label(
            form_container,
            text="Password",
            font=("Segoe UI", 11, "bold"),
            bg=self.WHITE,
            fg=self.TEXT_DARK
        )
        password_label.pack(anchor="w", pady=(10, 5))
        
        password_entry = tk.Entry(
            form_container,
            font=("Segoe UI", 11),
            bg="#f7fafc",
            fg=self.TEXT_DARK,
            relief=tk.FLAT,
            bd=0,
            show="•",
            width=30
        )
        password_entry.pack(fill=tk.X, ipady=12, pady=(0, 15))
        password_entry.insert(0, "")
        
        # Add subtle border effect
        password_border = tk.Frame(form_container, bg="#e2e8f0", height=1)
        password_border.pack(fill=tk.X, pady=(0, 20))
        
        # Remember me checkbox
        remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(
            form_container,
            text="Remember me",
            variable=remember_var,
            font=("Segoe UI", 10),
            bg=self.WHITE,
            fg=self.TEXT_LIGHT,
            activebackground=self.WHITE,
            activeforeground=self.PRIMARY_COLOR,
            selectcolor=self.WHITE,
            relief=tk.FLAT,
            bd=0
        )
        remember_check.pack(anchor="w", pady=(0, 20))
        
        # Login button
        login_btn = tk.Button(
            form_container,
            text="Sign In",
            font=("Segoe UI", 12, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE,
            activebackground=self.SECONDARY_COLOR,
            activeforeground=self.WHITE,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=lambda: self.handle_login(email_entry.get(), password_entry.get())
        )
        login_btn.pack(fill=tk.X, ipady=12, pady=10)
        
        # Hover effect on login button
        def on_enter(e):
            login_btn.config(bg=self.SECONDARY_COLOR)
        
        def on_leave(e):
            login_btn.config(bg=self.PRIMARY_COLOR)
        
        login_btn.bind("<Enter>", on_enter)
        login_btn.bind("<Leave>", on_leave)
        
        # Submit on Enter key
        for _widget in (email_entry, password_entry, form_container):
            _widget.bind("<Return>", lambda e: login_btn.invoke())
        
        # Forgot password link
        forgot_link = tk.Label(
            form_container,
            text="Forgot password?",
            font=("Segoe UI", 10),
            bg=self.WHITE,
            fg=self.PRIMARY_COLOR,
            cursor="hand2"
        )
        forgot_link.pack(pady=15)
        forgot_link.bind("<Button-1>", lambda e: messagebox.showinfo("Info", "Password reset feature coming soon!"))
        
        # Divider
        divider_label = tk.Label(
            form_container,
            text="Don't have an account?",
            font=("Segoe UI", 10),
            bg=self.WHITE,
            fg=self.TEXT_LIGHT
        )
        divider_label.pack(pady=10)
        
        # Signup button (text based)
        signup_link = tk.Label(
            form_container,
            text="Sign Up Here",
            font=("Segoe UI", 11, "bold"),
            bg=self.WHITE,
            fg=self.PRIMARY_COLOR,
            cursor="hand2"
        )
        signup_link.pack()
        signup_link.bind("<Button-1>", lambda e: self.show_signup_screen())
        signup_link.bind("<Enter>", lambda e: signup_link.config(fg=self.ACCENT_COLOR))
        signup_link.bind("<Leave>", lambda e: signup_link.config(fg=self.PRIMARY_COLOR))
    
    def handle_login(self, email, password):
        """Handle login logic"""
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if email not in self.users:
            messagebox.showerror("Error", "Email not found. Please sign up first.")
            return
        
        hashed_password = self.hash_password(password)
        if self.users[email]["password"] != hashed_password:
            messagebox.showerror("Error", "Incorrect password")
            return
        
        self.current_user = email
        messagebox.showinfo("Success", f"Welcome back, {self.users[email]['name']}!")
        self.show_dashboard()
    
    def show_signup_screen(self):
        """Display the signup screen"""
        self.clear_frame()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.BG_LIGHT)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Left side - Branding (50%)
        left_panel = tk.Frame(main_frame, bg=self.SECONDARY_COLOR)
        left_panel.grid(row=0, column=0, sticky="nsew")
        
        # Branding content
        brand_frame = tk.Frame(left_panel, bg=self.SECONDARY_COLOR)
        brand_frame.pack(expand=True)
        
        # Logo/Icon
        logo_label = tk.Label(
            brand_frame,
            text="🚀",
            font=("Arial", 80),
            bg=self.SECONDARY_COLOR,
            fg=self.WHITE
        )
        logo_label.pack(pady=20)
        
        # Brand title
        title_label = tk.Label(
            brand_frame,
            text="Get Started",
            font=("Segoe UI", 36, "bold"),
            bg=self.SECONDARY_COLOR,
            fg=self.WHITE
        )
        title_label.pack(pady=10)
        
        # Brand subtitle
        subtitle_label = tk.Label(
            brand_frame,
            text="Create your account today",
            font=("Segoe UI", 14),
            bg=self.SECONDARY_COLOR,
            fg="#e0d8f0"
        )
        subtitle_label.pack(pady=5)
        
        # Benefits
        benefits_label = tk.Label(
            brand_frame,
            text="✓ Free Account\n✓ Secure & Private\n✓ Easy Setup\n✓ Start Tracking Now",
            font=("Segoe UI", 12),
            bg=self.SECONDARY_COLOR,
            fg=self.WHITE,
            justify=tk.LEFT
        )
        benefits_label.pack(pady=40)
        
        # Right side - Signup form (50%)
        right_panel = tk.Frame(main_frame, bg=self.WHITE)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Scrollable form container
        canvas = tk.Canvas(right_panel, bg=self.WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(right_panel, orient="vertical", command=canvas.yview)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        scrollable_frame = tk.Frame(canvas, bg=self.WHITE)
        
        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", _on_frame_configure)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", _on_canvas_configure)
        
        # Form container with padding
        form_container = tk.Frame(scrollable_frame, bg=self.WHITE)
        form_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Form title
        form_title = tk.Label(
            form_container,
            text="Create Account",
            font=("Segoe UI", 26, "bold"),
            bg=self.WHITE,
            fg=self.TEXT_DARK
        )
        form_title.pack(pady=(0, 5))
        
        # Form subtitle
        form_subtitle = tk.Label(
            form_container,
            text="Join thousands of users managing their expenses",
            font=("Segoe UI", 11),
            bg=self.WHITE,
            fg=self.TEXT_LIGHT
        )
        form_subtitle.pack(pady=(0, 25))
        
        # Full name field
        name_label = tk.Label(
            form_container,
            text="Full Name",
            font=("Segoe UI", 11, "bold"),
            bg=self.WHITE,
            fg=self.TEXT_DARK
        )
        name_label.pack(anchor="w", pady=(10, 5))
        
        name_entry = tk.Entry(
            form_container,
            font=("Segoe UI", 11),
            bg="#f7fafc",
            fg=self.TEXT_DARK,
            relief=tk.FLAT,
            bd=0,
            width=30
        )
        name_entry.pack(fill=tk.X, ipady=12, pady=(0, 15))
        
        name_border = tk.Frame(form_container, bg="#e2e8f0", height=1)
        name_border.pack(fill=tk.X, pady=(0, 15))
        
        # Email field
        email_label = tk.Label(
            form_container,
            text="Email Address",
            font=("Segoe UI", 11, "bold"),
            bg=self.WHITE,
            fg=self.TEXT_DARK
        )
        email_label.pack(anchor="w", pady=(10, 5))
        
        email_entry = tk.Entry(
            form_container,
            font=("Segoe UI", 11),
            bg="#f7fafc",
            fg=self.TEXT_DARK,
            relief=tk.FLAT,
            bd=0,
            width=30
        )
        email_entry.pack(fill=tk.X, ipady=12, pady=(0, 15))
        
        email_border = tk.Frame(form_container, bg="#e2e8f0", height=1)
        email_border.pack(fill=tk.X, pady=(0, 15))
        
        # Password field
        password_label = tk.Label(
            form_container,
            text="Password",
            font=("Segoe UI", 11, "bold"),
            bg=self.WHITE,
            fg=self.TEXT_DARK
        )
        password_label.pack(anchor="w", pady=(10, 5))
        
        password_entry = tk.Entry(
            form_container,
            font=("Segoe UI", 11),
            bg="#f7fafc",
            fg=self.TEXT_DARK,
            relief=tk.FLAT,
            bd=0,
            show="•",
            width=30
        )
        password_entry.pack(fill=tk.X, ipady=12, pady=(0, 5))
        
        password_border = tk.Frame(form_container, bg="#e2e8f0", height=1)
        password_border.pack(fill=tk.X, pady=(0, 10))
        
        # Password requirements
        requirements_label = tk.Label(
            form_container,
            text="• At least 6 characters\n• 1 uppercase letter\n• 1 number",
            font=("Segoe UI", 9),
            bg=self.WHITE,
            fg=self.TEXT_LIGHT,
            justify=tk.LEFT
        )
        requirements_label.pack(anchor="w", pady=(0, 15))
        
        # Confirm password field
        confirm_label = tk.Label(
            form_container,
            text="Confirm Password",
            font=("Segoe UI", 11, "bold"),
            bg=self.WHITE,
            fg=self.TEXT_DARK
        )
        confirm_label.pack(anchor="w", pady=(10, 5))
        
        confirm_entry = tk.Entry(
            form_container,
            font=("Segoe UI", 11),
            bg="#f7fafc",
            fg=self.TEXT_DARK,
            relief=tk.FLAT,
            bd=0,
            show="•",
            width=30
        )
        confirm_entry.pack(fill=tk.X, ipady=12, pady=(0, 15))
        
        confirm_border = tk.Frame(form_container, bg="#e2e8f0", height=1)
        confirm_border.pack(fill=tk.X, pady=(0, 20))
        
        # Terms checkbox
        terms_var = tk.BooleanVar()
        terms_check = tk.Checkbutton(
            form_container,
            text="I agree to Terms & Conditions",
            variable=terms_var,
            font=("Segoe UI", 10),
            bg=self.WHITE,
            fg=self.TEXT_LIGHT,
            activebackground=self.WHITE,
            activeforeground=self.PRIMARY_COLOR,
            selectcolor=self.WHITE,
            relief=tk.FLAT,
            bd=0
        )
        terms_check.pack(anchor="w", pady=(0, 20))
        
        # Signup button
        signup_btn = tk.Button(
            form_container,
            text="Create Account",
            font=("Segoe UI", 12, "bold"),
            bg=self.SECONDARY_COLOR,
            fg=self.WHITE,
            activebackground=self.PRIMARY_COLOR,
            activeforeground=self.WHITE,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=lambda: self.handle_signup(
                name_entry.get(),
                email_entry.get(),
                password_entry.get(),
                confirm_entry.get(),
                terms_var.get()
            )
        )
        signup_btn.pack(fill=tk.X, ipady=12, pady=10)
        
        # Hover effect
        def on_enter(e):
            signup_btn.config(bg=self.PRIMARY_COLOR)
        
        def on_leave(e):
            signup_btn.config(bg=self.SECONDARY_COLOR)
        
        signup_btn.bind("<Enter>", on_enter)
        signup_btn.bind("<Leave>", on_leave)
        
        # Submit on Enter key for signup
        for _widget in (
            name_entry, email_entry, password_entry, confirm_entry, form_container, scrollable_frame
        ):
            _widget.bind("<Return>", lambda e: signup_btn.invoke())
        
        # Login link
        divider_label = tk.Label(
            form_container,
            text="Already have an account?",
            font=("Segoe UI", 10),
            bg=self.WHITE,
            fg=self.TEXT_LIGHT
        )
        divider_label.pack(pady=15)
        
        login_link = tk.Label(
            form_container,
            text="Sign In Here",
            font=("Segoe UI", 11, "bold"),
            bg=self.WHITE,
            fg=self.SECONDARY_COLOR,
            cursor="hand2"
        )
        login_link.pack(pady=(0, 20))
        login_link.bind("<Button-1>", lambda e: self.show_login_screen())
        login_link.bind("<Enter>", lambda e: login_link.config(fg=self.ACCENT_COLOR))
        login_link.bind("<Leave>", lambda e: login_link.config(fg=self.SECONDARY_COLOR))
    
    def handle_signup(self, name, email, password, confirm_password, terms_agreed):
        """Handle signup logic"""
        # Validation
        if not name or not email or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if not terms_agreed:
            messagebox.showerror("Error", "Please agree to Terms & Conditions")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        if email in self.users:
            messagebox.showerror("Error", "Email already registered")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        valid, message = self.validate_password(password)
        if not valid:
            messagebox.showerror("Error", message)
            return
        
        # Create new user
        self.users[email] = {
            "name": name,
            "password": self.hash_password(password),
            "created_at": datetime.now().isoformat()
        }
        
        self.save_users()
        self.current_user = email
        
        messagebox.showinfo("Success", f"Welcome {name}! Account created successfully!")
        self.show_dashboard()
    
    def show_dashboard(self):
        """Show main dashboard (placeholder)"""
        self.clear_frame()
        
        dashboard_frame = tk.Frame(self.root, bg=self.PRIMARY_COLOR)
        dashboard_frame.pack(fill=tk.BOTH, expand=True)
        
        welcome_label = tk.Label(
            dashboard_frame,
            text=f"Welcome, {self.users[self.current_user]['name']}!",
            font=("Segoe UI", 28, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        )
        welcome_label.pack(expand=True)
        
        message_label = tk.Label(
            dashboard_frame,
            text="🎉 Login/Signup Successful!\n\nExpense Tracker Main App Coming Next...",
            font=("Segoe UI", 16),
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE
        )
        message_label.pack(expand=True)
        
        logout_btn = tk.Button(
            dashboard_frame,
            text="Logout",
            font=("Segoe UI", 12, "bold"),
            bg=self.WHITE,
            fg=self.PRIMARY_COLOR,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.show_login_screen,
            padx=40,
            pady=12
        )
        logout_btn.pack(pady=30)


def main():
    """Main function"""
    root = tk.Tk()
    app = LoginSignupApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()