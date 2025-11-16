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
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
            for user_email in self.users:
                if "bank_balance" not in self.users[user_email]:
                    self.users[user_email]["bank_balance"] = 0.0
                if "credit_card_balance" not in self.users[user_email]:
                    self.users[user_email]["credit_card_balance"] = 0.0
                if "cash_balance" not in self.users[user_email]:
                    self.users[user_email]["cash_balance"] = 0.0
            self.save_users()
        else:
            self.users = {}

    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_password(self, password):
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit"
        return True, "Valid"

    def login(self, email, password):
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
            "cash_balance": 0.0,
            "bank_balance": 0.0,
            "credit_card_balance": 0.0,
            "expenses": []
        }
        
        self.save_users()
        self.current_user = email
        
        return True, f"Welcome {name}! Let's set up your account."

    def onboard_user(self, monthly_budget, currency_full):
        
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
        
        # Get existing budget, if any
        existing_budget = self.users[self.current_user].get("monthly_budget", 0.0) or 0.0
        
        # Add new budget to existing budget instead of replacing
        new_total_budget = existing_budget + budget_value
        
        self.users[self.current_user]["monthly_budget"] = new_total_budget
        self.users[self.current_user]["currency"] = currency_code
        
        if "cash_balance" not in self.users[self.current_user]:
            self.users[self.current_user]["cash_balance"] = 0.0
        if "bank_balance" not in self.users[self.current_user]:
            self.users[self.current_user]["bank_balance"] = 0.0
        if "credit_card_balance" not in self.users[self.current_user]:
            self.users[self.current_user]["credit_card_balance"] = 0.0
        self.save_users()
        
        user_name = self.users[self.current_user]["name"]
        
        # Provide different messages based on whether this is initial setup or adding to budget
        if existing_budget == 0:
            return True, f"Great job, {user_name}! 🎉\n\nYour account is all set up.\nRedirecting to dashboard."
        else:
            return True, f"Budget updated successfully! 🎉\n\nAdded {budget_value:.2f} to your budget.\nNew total budget: {new_total_budget:.2f}"

    def get_current_user_data(self):
        return self.users.get(self.current_user)

    def logout(self):
        self.current_user = None
