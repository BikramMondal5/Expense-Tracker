"""
Modern Login/Signup Modal with Interactive UI and Onboarding Flow
Built with Python Tkinter with smooth animations and professional styling
"""

import tkinter as tk
from tkinter import messagebox

import config # Import config module
from auth_manager import AuthManager # Import AuthManager
from ui_manager import UIManager # Import UIManager

class LoginSignupApp:
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Color scheme - Modern gradient colors (now loaded from config)
        self.PRIMARY_COLOR = config.PRIMARY_COLOR
        self.SECONDARY_COLOR = config.SECONDARY_COLOR
        self.ACCENT_COLOR = config.ACCENT_COLOR
        self.BG_LIGHT = config.BG_LIGHT
        self.TEXT_DARK = config.TEXT_DARK
        self.TEXT_LIGHT = config.TEXT_LIGHT
        self.WHITE = config.WHITE
        self.SUCCESS = config.SUCCESS
        self.ERROR = config.ERROR
        
        # Remove default window styling
        self.root.configure(bg=self.BG_LIGHT)
        
        # Initialize AuthManager
        self.auth_manager = AuthManager()
        
        # Initialize UIManager
        self.ui_manager = UIManager(root, self.auth_manager, self) # Pass self for screen transitions
        
        # Show login screen
        self.ui_manager.show_login_screen()
    
    # These methods will now be handled by UIManager, but we need to keep the handlers for callbacks
    def handle_login(self, email, password):
        success, message, user_name = self.auth_manager.login(email, password)
        if success:
            messagebox.showinfo("Success", message)
            self.ui_manager.show_dashboard() # Call UIManager's show_dashboard
        else:
            messagebox.showerror("Error", message)

    def handle_signup(self, name, email, password, confirm_password, terms_agreed):
        success, message = self.auth_manager.signup(name, email, password, confirm_password, terms_agreed)
        if success:
            messagebox.showinfo("Success", message)
            self.ui_manager.show_onboarding_screen() # Call UIManager's show_onboarding_screen
        else:
            messagebox.showerror("Error", message)
    
    def handle_onboarding_data(self, monthly_budget, currency_full):
        success, message = self.auth_manager.onboard_user(monthly_budget, currency_full)
        if success:
            messagebox.showinfo("Setup Complete!", message)
            self.ui_manager.show_dashboard() # Call UIManager's show_dashboard
        else:
            messagebox.showerror("Error", message)

    def show_login_screen(self):
        self.ui_manager.show_login_screen()

    def show_signup_screen(self):
        self.ui_manager.show_signup_screen()

    def show_onboarding_screen(self):
        self.ui_manager.show_onboarding_screen()

    def show_dashboard(self):
        self.ui_manager.show_dashboard()

def main():
    """Main function"""
    root = tk.Tk()
    app = LoginSignupApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()