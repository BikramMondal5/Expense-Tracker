import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import config
from datetime import datetime, timedelta
import json
import google.generativeai as genai
from gemini_config import GEMINI_API_KEY
import re

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

class SummaryScreen:
    def __init__(self, parent_frame, auth_manager, dashboard_instance):
        self.parent_frame = parent_frame
        self.auth_manager = auth_manager
        self.dashboard = dashboard_instance
        
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
        
        # Fonts
        self.FONT_HEADER = ("Segoe UI", 24, "bold")
        self.FONT_SUBHEADER = ("Segoe UI", 16, "bold")
        self.FONT_BODY = ("Segoe UI", 11)
        self.FONT_CAPTION = ("Segoe UI", 9)
        
        # Chat history
        self.chat_history = []
        
        # Initialize Gemini model
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        self.create_summary_screen()
    
    def create_summary_screen(self):
        """Create the AI Summary screen with chat interface"""
        # Clear parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = tk.Frame(self.parent_frame, bg=self.WHITE)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.WHITE, pady=20)
        header_frame.pack(fill=tk.X, padx=30)
        
        tk.Label(
            header_frame,
            text="✨ AI Expense Summary",
            font=self.FONT_HEADER,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(anchor="w")
        
        tk.Label(
            header_frame,
            text="Get insights and recommendations about your spending habits",
            font=self.FONT_BODY,
            bg=self.WHITE,
            fg=self.TEXT_LIGHT
        ).pack(anchor="w", pady=(5, 0))
        
        # Content area with two columns
        content_frame = tk.Frame(main_container, bg=self.WHITE)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Left side - Suggestion prompts
        left_frame = tk.Frame(content_frame, bg=self.WHITE, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_frame.pack_propagate(False)
        
        tk.Label(
            left_frame,
            text="Quick Prompts",
            font=self.FONT_SUBHEADER,
            bg=self.WHITE,
            fg=self.TEXT_DARK
        ).pack(anchor="w", pady=(0, 15))
        
        # Suggestion prompt buttons
        suggestions = [
            {
                "icon": "📊",
                "title": "Weekly Summary",
                "prompt": "Summarize my expenses from the last week"
            },
            {
                "icon": "📅",
                "title": "Monthly Overview",
                "prompt": "Give me a monthly overview of my spending"
            },
            {
                "icon": "💡",
                "title": "Saving Tips",
                "prompt": "What areas can I improve to save more money?"
            },
            {
                "icon": "📈",
                "title": "Spending Trends",
                "prompt": "Analyze my spending trends and patterns"
            }
        ]
        
        for suggestion in suggestions:
            self._create_suggestion_card(left_frame, suggestion)
        
        # Right side - Chat interface
        right_frame = tk.Frame(content_frame, bg=self.WHITE)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat display area
        chat_container = tk.Frame(right_frame, bg=self.WHITE, relief=tk.SOLID, bd=1)
        chat_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Chat history display
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=self.FONT_BODY,
            bg=self.BG_LIGHT,
            fg=self.TEXT_DARK,
            relief=tk.FLAT,
            padx=15,
            pady=15,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for different message types
        self.chat_display.tag_config("user", foreground=self.PRIMARY_COLOR, font=("Segoe UI", 11, "bold"), justify=tk.RIGHT)
        self.chat_display.tag_config("user_content", justify=tk.RIGHT, rmargin=10, lmargin1=250, 
                                     background="#FFE5EC", spacing1=8, spacing3=8)
        self.chat_display.tag_config("ai", foreground=self.ACCENT_COLOR, font=("Segoe UI", 11, "bold"), justify=tk.LEFT)
        self.chat_display.tag_config("ai_content", justify=tk.LEFT, lmargin1=10)
        self.chat_display.tag_config("timestamp", foreground=self.TEXT_LIGHT, font=("Segoe UI", 9))
        
        # Configure markdown formatting tags
        self.chat_display.tag_config("bold", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("italic", font=("Segoe UI", 11, "italic"))
        self.chat_display.tag_config("heading1", font=("Segoe UI", 18, "bold"), foreground=self.TEXT_DARK, spacing1=10, spacing3=5)
        self.chat_display.tag_config("heading2", font=("Segoe UI", 16, "bold"), foreground=self.TEXT_DARK, spacing1=8, spacing3=4)
        self.chat_display.tag_config("heading3", font=("Segoe UI", 14, "bold"), foreground=self.TEXT_DARK, spacing1=6, spacing3=3)
        self.chat_display.tag_config("code", font=("Consolas", 10), background="#f0f0f0", foreground="#d63031")
        self.chat_display.tag_config("code_block", font=("Consolas", 10), background="#f5f5f5", foreground="#2d3436", lmargin1=20, lmargin2=20, spacing1=5, spacing3=5)
        self.chat_display.tag_config("bullet", lmargin1=20, lmargin2=40, spacing1=2)
        self.chat_display.tag_config("number", lmargin1=20, lmargin2=40, spacing1=2)
        self.chat_display.tag_config("blockquote", lmargin1=20, lmargin2=20, foreground=self.TEXT_LIGHT, font=("Segoe UI", 11, "italic"))
        self.chat_display.tag_config("link", foreground="#0984e3", underline=True)
        
        # Input area
        input_frame = tk.Frame(right_frame, bg=self.WHITE)
        input_frame.pack(fill=tk.X)
        
        # Text input with border
        input_container = tk.Frame(input_frame, bg=self.TEXT_LIGHT, relief=tk.SOLID, bd=1)
        input_container.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0, 10))
        
        self.message_entry = tk.Text(
            input_container,
            height=3,
            font=self.FONT_BODY,
            bg=self.WHITE,
            fg=self.TEXT_DARK,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.message_entry.pack(fill=tk.BOTH, expand=True)
        self.message_entry.insert("1.0", "Ask me anything about your expenses...")
        self.message_entry.config(fg=self.TEXT_LIGHT)
        
        # Bind focus events for placeholder
        self.message_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.message_entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.message_entry.bind("<Return>", lambda e: self._send_message() if not e.state & 0x1 else None)
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="Send ➤",
            font=("Segoe UI", 11, "bold"),
            bg=self.PRIMARY_COLOR,
            fg=self.WHITE,
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor="hand2",
            command=self._send_message
        )
        send_btn.pack(side=tk.RIGHT)
        
        # Add welcome message
        self._add_ai_message("Hello! I'm your AI expense assistant. I can help you analyze your spending, provide insights, and offer personalized recommendations. Try asking me about your expenses or use one of the quick prompts on the left!")
    
    def _create_suggestion_card(self, parent, suggestion):
        """Create a suggestion prompt card"""
        card = tk.Frame(parent, bg=self.BG_LIGHT, relief=tk.FLAT, cursor="hand2")
        card.pack(fill=tk.X, pady=5)
        
        # Inner padding
        inner = tk.Frame(card, bg=self.BG_LIGHT)
        inner.pack(fill=tk.BOTH, padx=15, pady=12)
        
        # Icon and title
        header = tk.Frame(inner, bg=self.BG_LIGHT)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=suggestion["icon"],
            font=("Segoe UI", 16),
            bg=self.BG_LIGHT
        ).pack(side=tk.LEFT, padx=(0, 8))
        
        tk.Label(
            header,
            text=suggestion["title"],
            font=("Segoe UI", 11, "bold"),
            bg=self.BG_LIGHT,
            fg=self.TEXT_DARK
        ).pack(side=tk.LEFT)
        
        # Hover effects
        def on_enter(e):
            card.config(bg=self.PRIMARY_COLOR)
            inner.config(bg=self.PRIMARY_COLOR)
            header.config(bg=self.PRIMARY_COLOR)
            for child in header.winfo_children():
                child.config(bg=self.PRIMARY_COLOR, fg=self.WHITE)
        
        def on_leave(e):
            card.config(bg=self.BG_LIGHT)
            inner.config(bg=self.BG_LIGHT)
            header.config(bg=self.BG_LIGHT)
            for child in header.winfo_children():
                child.config(bg=self.BG_LIGHT, fg=self.TEXT_DARK)
        
        def on_click(e):
            self._use_suggestion(suggestion["prompt"])
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", on_click)
        inner.bind("<Button-1>", on_click)
        header.bind("<Button-1>", on_click)
        for child in header.winfo_children():
            child.bind("<Button-1>", on_click)
    
    def _on_entry_focus_in(self, event):
        """Handle focus in event for message entry"""
        if self.message_entry.get("1.0", "end-1c") == "Ask me anything about your expenses...":
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.config(fg=self.TEXT_DARK)
    
    def _on_entry_focus_out(self, event):
        """Handle focus out event for message entry"""
        if not self.message_entry.get("1.0", "end-1c").strip():
            self.message_entry.insert("1.0", "Ask me anything about your expenses...")
            self.message_entry.config(fg=self.TEXT_LIGHT)
    
    def _use_suggestion(self, prompt):
        """Use a suggestion prompt"""
        self.message_entry.delete("1.0", tk.END)
        self.message_entry.insert("1.0", prompt)
        self.message_entry.config(fg=self.TEXT_DARK)
        self._send_message()
    
    def _send_message(self):
        """Send a message and get AI response"""
        message = self.message_entry.get("1.0", "end-1c").strip()
        
        if not message or message == "Ask me anything about your expenses...":
            return
        
        # Clear input
        self.message_entry.delete("1.0", tk.END)
        
        # Add user message
        self._add_user_message(message)
        
        # Show "Thinking..." indicator
        self._add_ai_message("💭 Analyzing your expenses...")
        self.parent_frame.update()
        
        # Generate AI response in background
        try:
            response = self._generate_ai_response(message)
            # Remove the "Thinking..." message
            self.chat_history.pop()
            self._update_last_ai_message(response)
        except Exception as e:
            self.chat_history.pop()
            self._update_last_ai_message(f"❌ Sorry, I encountered an error: {str(e)}\n\nPlease try again or rephrase your question.")
    
    def _update_last_ai_message(self, new_message):
        """Update the last AI message in the chat display with markdown rendering"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Find and delete the last AI message
        content = self.chat_display.get("1.0", tk.END)
        lines = content.split('\n')
        
        # Find the last "AI Assistant" line
        last_ai_index = -1
        for i in range(len(lines) - 1, -1, -1):
            if "AI Assistant" in lines[i]:
                last_ai_index = i
                break
        
        if last_ai_index >= 0:
            # Delete from that line to the end
            self.chat_display.delete(f"{last_ai_index + 1}.0", tk.END)
            
            # Add the new message with markdown rendering
            timestamp = datetime.now().strftime("%I:%M %p")
            self.chat_display.insert(tk.END, "✨ AI Assistant", "ai")
            self.chat_display.insert(tk.END, f" • {timestamp}\n", ("timestamp", "ai"))
            
            # Render markdown-formatted message
            self._render_markdown(new_message)
            
            self.chat_history.append({"role": "ai", "message": new_message, "timestamp": timestamp})
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def _generate_ai_response(self, user_message):
        """Generate AI response using Google Gemini based on user's expense data"""
        # Get current user's email (the logged-in user)
        current_user_email = self.auth_manager.current_user
        
        if not current_user_email:
            return "❌ Error: No user is currently logged in. Please log in to access your expense data."
        
        # Get user data for the logged-in user only
        user_data = self.auth_manager.get_current_user_data()
        if not user_data:
            return f"❌ Error: Could not retrieve data for user {current_user_email}. Please make sure you're logged in."
        
        # Extract user's expense data
        expenses = user_data.get("expenses", [])
        currency_code = user_data.get("currency", "USD")
        currency_symbol = self.dashboard.CURRENCY_SYMBOLS.get(currency_code, "$")
        monthly_budget = user_data.get("monthly_budget", 0)
        user_name = user_data.get("name", "User")
        
        # Prepare expense data summary for AI
        expense_summary = self._prepare_expense_data_for_ai(expenses, currency_code, currency_symbol, monthly_budget)
        
        # Create the prompt for Gemini
        system_context = f"""You are an intelligent financial advisor assistant helping {user_name} manage their personal expenses.

User Information:
- Email: {current_user_email}
- Currency: {currency_code} ({currency_symbol})
- Monthly Budget: {currency_symbol}{monthly_budget:,.2f}

{expense_summary}

Your role is to:
1. Analyze the user's spending patterns and provide actionable insights
2. Answer questions about their expenses clearly and concisely
3. Provide personalized recommendations to help them save money
4. Be encouraging and supportive while being honest about their spending habits
5. Use emojis to make responses more engaging
6. Format responses with clear sections and bullet points when appropriate

Guidelines:
- Keep responses concise but informative (aim for 150-300 words)
- Always reference specific numbers from their data
- Provide practical, actionable advice
- Be positive and encouraging
- Use the correct currency symbol ({currency_symbol})

IMPORTANT - Formatting Instructions:
- Use markdown formatting in your responses
- Use **bold** for emphasis on important numbers or key points
- Use bullet points (- or •) for lists
- Use numbered lists (1. 2. 3.) for step-by-step recommendations
- Use ### for section headings when breaking down complex responses
- Use emojis at the start of sections or key points for visual appeal
- Example format:
  
  ### 📊 Your Weekly Summary
  
  **Total Spent**: {currency_symbol}1,234.56
  
  **Top Categories**:
  - Food: {currency_symbol}450 (36%)
  - Transport: {currency_symbol}320 (26%)
  
  **💡 Recommendations**:
  1. Try meal prepping to reduce food costs
  2. Consider carpooling for transport savings
"""

        user_prompt = f"User Question: {user_message}"
        
        # Generate response using Gemini
        try:
            # Create chat instance
            chat = self.model.start_chat(history=[])
            
            # Send the context and user question
            full_prompt = f"{system_context}\n\n{user_prompt}"
            response = chat.send_message(full_prompt)
            
            return response.text
            
        except Exception as e:
            # Fallback to basic response if API fails
            return f"⚠️ I'm having trouble connecting to the AI service right now.\n\nError: {str(e)}\n\nPlease check your internet connection and try again."
    
    def _prepare_expense_data_for_ai(self, expenses, currency_code, currency_symbol, monthly_budget):
        """Prepare expense data in a format suitable for AI analysis"""
        if not expenses:
            return "Transaction Data: No expenses recorded yet."
        
        # Calculate various statistics
        total_expenses = sum(float(exp.get("amount", 0)) for exp in expenses)
        transaction_count = len(expenses)
        
        # Category breakdown
        categories = {}
        for exp in expenses:
            cat = exp.get("category", "Unknown")
            amount = float(exp.get("amount", 0))
            categories[cat] = categories.get(cat, 0) + amount
        
        # Account breakdown
        accounts = {}
        for exp in expenses:
            acc = exp.get("account", "Unknown")
            amount = float(exp.get("amount", 0))
            accounts[acc] = accounts.get(acc, 0) + amount
        
        # Time-based analysis
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        weekly_expenses = []
        monthly_expenses = []
        
        for exp in expenses:
            try:
                exp_date = datetime.fromisoformat(exp.get("timestamp", exp.get("date", "")))
                if exp_date >= week_ago:
                    weekly_expenses.append(exp)
                if exp_date >= month_ago:
                    monthly_expenses.append(exp)
            except:
                continue
        
        weekly_total = sum(float(exp.get("amount", 0)) for exp in weekly_expenses)
        monthly_total = sum(float(exp.get("amount", 0)) for exp in monthly_expenses)
        
        # Recent transactions (last 5)
        sorted_expenses = sorted(expenses, key=lambda x: x.get("timestamp", x.get("date", "")), reverse=True)
        recent_5 = sorted_expenses[:5]
        
        # Format the data summary
        summary = f"""Transaction Data Summary:

Overall Statistics:
- Total Transactions: {transaction_count}
- Total Spent (All Time): {currency_symbol}{total_expenses:,.2f}
- Last 7 Days: {currency_symbol}{weekly_total:,.2f} ({len(weekly_expenses)} transactions)
- Last 30 Days: {currency_symbol}{monthly_total:,.2f} ({len(monthly_expenses)} transactions)

Category Breakdown:"""
        
        for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
            summary += f"\n- {cat}: {currency_symbol}{amount:,.2f} ({percentage:.1f}%)"
        
        summary += f"\n\nAccount Breakdown:"
        for acc, amount in sorted(accounts.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
            summary += f"\n- {acc}: {currency_symbol}{amount:,.2f} ({percentage:.1f}%)"
        
        summary += f"\n\nRecent Transactions (Last 5):"
        for i, exp in enumerate(recent_5, 1):
            amount = float(exp.get("amount", 0))
            category = exp.get("category", "Unknown")
            date = exp.get("date", "Unknown")
            account = exp.get("account", "Unknown")
            summary += f"\n{i}. {currency_symbol}{amount:,.2f} - {category} - {date} ({account})"
        
        if monthly_budget > 0:
            remaining = monthly_budget - monthly_total
            percentage_used = (monthly_total / monthly_budget * 100) if monthly_budget > 0 else 0
            summary += f"\n\nBudget Status (30 days):"
            summary += f"\n- Budget: {currency_symbol}{monthly_budget:,.2f}"
            summary += f"\n- Spent: {currency_symbol}{monthly_total:,.2f} ({percentage_used:.1f}%)"
            summary += f"\n- Remaining: {currency_symbol}{remaining:,.2f}"
        
        return summary
    
    def _render_markdown(self, text):
        """Render markdown-formatted text to the chat display with proper formatting"""
        # Split text into lines for processing
        lines = text.split('\n')
        i = 0
        in_code_block = False
        code_block_content = []
        
        while i < len(lines):
            line = lines[i]
            
            # Handle code blocks (```)
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_content = []
                else:
                    # End of code block
                    in_code_block = False
                    if code_block_content:
                        self.chat_display.insert(tk.END, '\n'.join(code_block_content) + '\n', "code_block")
                    code_block_content = []
                i += 1
                continue
            
            if in_code_block:
                code_block_content.append(line)
                i += 1
                continue
            
            # Handle headings
            if line.startswith('### '):
                self.chat_display.insert(tk.END, line[4:] + '\n', "heading3")
            elif line.startswith('## '):
                self.chat_display.insert(tk.END, line[3:] + '\n', "heading2")
            elif line.startswith('# '):
                self.chat_display.insert(tk.END, line[2:] + '\n', "heading1")
            
            # Handle bullet points
            elif line.strip().startswith('- ') or line.strip().startswith('• '):
                bullet_text = line.strip()[2:]
                formatted_text = self._format_inline_markdown(bullet_text)
                self.chat_display.insert(tk.END, '• ', "bullet")
                self._insert_formatted_text(formatted_text, "bullet")
                self.chat_display.insert(tk.END, '\n')
            
            # Handle numbered lists
            elif re.match(r'^\d+\.\s', line.strip()):
                match = re.match(r'^(\d+)\.\s(.+)', line.strip())
                if match:
                    num, text = match.groups()
                    formatted_text = self._format_inline_markdown(text)
                    self.chat_display.insert(tk.END, f'{num}. ', "number")
                    self._insert_formatted_text(formatted_text, "number")
                    self.chat_display.insert(tk.END, '\n')
            
            # Handle blockquotes
            elif line.strip().startswith('> '):
                quote_text = line.strip()[2:]
                self.chat_display.insert(tk.END, quote_text + '\n', "blockquote")
            
            # Handle horizontal rules
            elif line.strip() in ['---', '***', '___']:
                self.chat_display.insert(tk.END, '─' * 50 + '\n')
            
            # Handle regular text with inline formatting
            else:
                if line.strip():  # Only process non-empty lines
                    formatted_text = self._format_inline_markdown(line)
                    self._insert_formatted_text(formatted_text)
                self.chat_display.insert(tk.END, '\n')
            
            i += 1
    
    def _format_inline_markdown(self, text):
        """Parse inline markdown formatting and return formatted segments"""
        segments = []
        i = 0
        current_text = ""
        
        while i < len(text):
            # Bold (**text** or __text__)
            if text[i:i+2] == '**' or text[i:i+2] == '__':
                if current_text:
                    segments.append(('normal', current_text))
                    current_text = ""
                
                # Find closing
                end_marker = text[i:i+2]
                end_pos = text.find(end_marker, i+2)
                if end_pos != -1:
                    bold_text = text[i+2:end_pos]
                    segments.append(('bold', bold_text))
                    i = end_pos + 2
                    continue
            
            # Italic (*text* or _text_)
            elif text[i] in ['*', '_'] and (i == 0 or text[i-1] not in ['*', '_']):
                if current_text:
                    segments.append(('normal', current_text))
                    current_text = ""
                
                # Find closing
                end_pos = text.find(text[i], i+1)
                if end_pos != -1 and (end_pos == len(text)-1 or text[end_pos+1] not in ['*', '_']):
                    italic_text = text[i+1:end_pos]
                    segments.append(('italic', italic_text))
                    i = end_pos + 1
                    continue
            
            # Inline code (`code`)
            elif text[i] == '`':
                if current_text:
                    segments.append(('normal', current_text))
                    current_text = ""
                
                # Find closing
                end_pos = text.find('`', i+1)
                if end_pos != -1:
                    code_text = text[i+1:end_pos]
                    segments.append(('code', code_text))
                    i = end_pos + 1
                    continue
            
            # Links [text](url)
            elif text[i] == '[':
                bracket_end = text.find(']', i)
                if bracket_end != -1 and bracket_end + 1 < len(text) and text[bracket_end + 1] == '(':
                    paren_end = text.find(')', bracket_end + 2)
                    if paren_end != -1:
                        if current_text:
                            segments.append(('normal', current_text))
                            current_text = ""
                        
                        link_text = text[i+1:bracket_end]
                        segments.append(('link', link_text))
                        i = paren_end + 1
                        continue
            
            current_text += text[i]
            i += 1
        
        if current_text:
            segments.append(('normal', current_text))
        
        return segments
    
    def _insert_formatted_text(self, segments, base_tag=None):
        """Insert formatted text segments into the chat display"""
        for format_type, text in segments:
            if format_type == 'bold':
                self.chat_display.insert(tk.END, text, ("bold", base_tag) if base_tag else "bold")
            elif format_type == 'italic':
                self.chat_display.insert(tk.END, text, ("italic", base_tag) if base_tag else "italic")
            elif format_type == 'code':
                self.chat_display.insert(tk.END, text, ("code", base_tag) if base_tag else "code")
            elif format_type == 'link':
                self.chat_display.insert(tk.END, text, ("link", base_tag) if base_tag else "link")
            else:
                self.chat_display.insert(tk.END, text, base_tag)
    
    def _add_user_message(self, message):
        """Add user message to chat display aligned to the right with pink background"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%I:%M %p")
        
        self.chat_display.insert(tk.END, "\n" if self.chat_history else "")
        self.chat_display.insert(tk.END, "You", "user")
        self.chat_display.insert(tk.END, f" • {timestamp}\n", ("timestamp", "user"))
        
        # Add padding with spaces and newlines for the pink background box effect
        padded_message = f"  {message}  "
        self.chat_display.insert(tk.END, padded_message + "\n", "user_content")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        self.chat_history.append({"role": "user", "message": message, "timestamp": timestamp})
    
    def _add_ai_message(self, message):
        """Add AI message to chat display with markdown rendering aligned to the left"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%I:%M %p")
        
        self.chat_display.insert(tk.END, "\n" if self.chat_history else "")
        self.chat_display.insert(tk.END, "✨ AI Assistant", "ai")
        self.chat_display.insert(tk.END, f" • {timestamp}\n", ("timestamp", "ai"))
        
        # Render markdown-formatted message
        self._render_markdown(message)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        self.chat_history.append({"role": "ai", "message": message, "timestamp": timestamp})


def display_summary_screen(root, auth_manager, dashboard_instance):
    """Display the summary screen"""
    # Clear the root and recreate the dashboard structure
    for widget in root.winfo_children():
        widget.destroy()
    
    # Unbind any global mouse wheel events from the previous screen
    root.unbind_all("<MouseWheel>")
    
    # Main container
    main_container = tk.Frame(root, bg=dashboard_instance.BG_LIGHT)
    main_container.pack(fill=tk.BOTH, expand=True)
    
    # Configure grid for main_container
    main_container.grid_rowconfigure(0, weight=0)  # Header
    main_container.grid_rowconfigure(1, weight=1)  # Content and sidebar
    main_container.grid_columnconfigure(0, weight=0)  # Sidebar
    main_container.grid_columnconfigure(1, weight=1)  # Content
    
    # ===== FULL-WIDTH HEADER =====
    header_frame = tk.Frame(main_container, bg=dashboard_instance.PRIMARY_COLOR)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
    dashboard_instance._create_header(header_frame)

    # ===== LEFT SIDEBAR =====
    dashboard_instance._create_sidebar(main_container)

    # ===== CONTENT FRAME =====
    content_frame = tk.Frame(main_container, bg=dashboard_instance.BG_LIGHT)
    content_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
    
    # Create summary screen in the content area
    SummaryScreen(content_frame, auth_manager, dashboard_instance)
