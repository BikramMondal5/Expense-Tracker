import json
import os
import hashlib
import re
from datetime import datetime
import config

class AuthManager:
    def __init__(self):
        self.users_file = config.USERS_FILE
        self.users = {}
        self.current_user = None
        self.load_users()

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

    def login(self, email, password):
        """Handle login logic"""
        if not email or not password:
            return False, "Please fill in all fields", None
        
        if email not in self.users:
            return False, "Email not found. Please sign up first.", None
        
        hashed_password = self.hash_password(password)
        if self.users[email]["password"] != hashed_password:
            return False, "Incorrect password", None
        
        self.current_user = email
        return True, f"Welcome back, {self.users[email]['name']}!", self.users[email]['name']

    def signup(self, name, email, password, confirm_password, terms_agreed):
        """Handle signup logic"""
        # Validation
        if not name or not email or not password or not confirm_password:
            return False, "Please fill in all fields"
        
        if not terms_agreed:
            return False, "Please agree to Terms & Conditions"
        
        if not self.validate_email(email):
            return False, "Please enter a valid email address"
        
        if email in self.users:
            return False, "Email already registered"
        
        if password != confirm_password:
            return False, "Passwords do not match"
        
        valid, message = self.validate_password(password)
        if not valid:
            return False, message
        
        # Create new user
        self.users[email] = {
            "name": name,
            "password": self.hash_password(password),
            "created_at": datetime.now().isoformat(),
            "monthly_budget": None,
            "currency": None,
            "cash_balance": None
        }
        
        self.save_users()
        self.current_user = email
        
        return True, f"Welcome {name}! Let's set up your account."

    def onboard_user(self, monthly_budget, currency_full):
        """Handle combined monthly budget and currency input"""
        try:
            if monthly_budget == "0" or monthly_budget == "":
                budget_value = 0.0
            else:
                budget_value = float(monthly_budget.replace(",", ""))
            
            if budget_value < 0:
                return False, "Monthly budget cannot be negative"
        except ValueError:
            return False, "Please enter a valid number for monthly budget"
        
        currency_code = currency_full.split(" - ")[0]
        
        self.users[self.current_user]["monthly_budget"] = budget_value
        self.users[self.current_user]["currency"] = currency_code
        self.users[self.current_user]["cash_balance"] = 0.0 
        self.save_users()
        
        user_name = self.users[self.current_user]["name"]
        return True, f"Great job, {user_name}! 🎉\n\nYour account is all set up.\nRedirecting to dashboard."

    def get_current_user_data(self):
        return self.users.get(self.current_user)

    def logout(self):
        self.current_user = None
