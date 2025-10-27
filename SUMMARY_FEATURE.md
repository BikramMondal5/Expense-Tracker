# ✨ AI Summary Feature

## Overview
The AI Summary feature is an intelligent expense analysis tool that helps users understand their spending behavior, identify areas for improvement, and receive personalized financial recommendations.

## Features

### 1. **Interactive AI Chat Interface**
- Chat with an AI assistant about your expenses
- Ask questions in natural language
- Get instant insights and recommendations

### 2. **Quick Prompts**
Four pre-built suggestion prompts for quick analysis:
- **📊 Weekly Summary**: Analyze expenses from the last 7 days
- **📅 Monthly Overview**: Get a comprehensive 30-day spending report
- **💡 Saving Tips**: Receive personalized recommendations to save money
- **📈 Spending Trends**: Understand your spending patterns over time

### 3. **Smart Analysis**
The AI automatically analyzes your transaction data and provides:
- Total spending breakdowns
- Category-wise analysis
- Budget comparisons
- Spending trends
- Personalized saving tips

## How to Use

### Accessing the Feature
1. Click on "✨ Summary" in the left sidebar
2. The Summary screen opens with the constant navbar and sidebar

### Using Quick Prompts
1. Click on any of the 4 quick prompt cards on the left
2. The prompt is automatically sent to the AI
3. View the response in the chat area

### Asking Custom Questions
1. Type your question in the text input at the bottom
2. Press Enter or click "Send ➤"
3. The AI will analyze your data and respond

### Example Questions You Can Ask
- "How much did I spend on food this week?"
- "What are my top spending categories?"
- "How can I reduce my entertainment expenses?"
- "Am I staying within my budget?"
- "Show me my spending trends"
- "Analyze my transport expenses"

## AI Capabilities

### Weekly Summary
- Total spent in the last 7 days
- Number of transactions
- Average spending per day
- Top spending category
- Budget comparison

### Monthly Overview
- 30-day spending total
- Transaction count
- Daily average
- Top 5 categories with percentages
- Budget status

### Saving Tips
The AI provides personalized recommendations based on your spending:
- **Food**: Meal planning suggestions if >30% of spending
- **Entertainment**: Free alternatives if >20% of spending
- **Shopping**: 24-hour rule suggestion if >25% of spending
- **Transport**: Carpooling/public transit tips if >25% of spending

### Spending Trends
- Compares recent vs. older spending
- Identifies increase/decrease patterns
- Provides percentage change
- Suggests areas for optimization

### Category Analysis
- Deep dive into specific categories
- Transaction count and averages
- Category-specific tips

## Technical Details

### File Structure
```
summary_screen.py          # Main Summary feature implementation
user_dashboard.py          # Updated with Summary navigation
```

### Dependencies
The feature uses existing project dependencies:
- `tkinter` - UI framework
- `datetime` - Date/time handling
- `json` - Data parsing
- `config` - App configuration

### Data Source
- Pulls transaction data from `users.json`
- Analyzes expenses stored in user's expense array
- Uses user's currency and budget settings

## Design

### Color Scheme
- Maintains consistency with the app's existing design
- User messages: Primary color (blue)
- AI messages: Accent color
- Cards: Light background with hover effects

### Layout
- **Left Panel**: Quick prompt cards (300px fixed width)
- **Right Panel**: Chat interface (expandable)
- **Header**: "✨ AI Expense Summary" title with description
- **Input Area**: Multi-line text input with send button

## Future Enhancements

Potential improvements for the AI Summary feature:
1. **Real AI Integration**: Connect to OpenAI GPT API for more sophisticated responses
2. **Visual Charts**: Add graphs and charts in chat responses
3. **Export Insights**: Allow users to save or export AI recommendations
4. **Scheduled Reports**: Weekly/monthly automated summaries via email
5. **Goal Setting**: AI-powered financial goal recommendations
6. **Predictive Analysis**: Forecast future spending based on trends
7. **Multi-language Support**: AI responses in different languages
8. **Voice Input**: Voice-to-text for asking questions

## Note on AI Implementation

The AI now uses **Google Gemini AI API** for real-time intelligent responses! 🚀

### How It Works:
1. **User Data Isolation**: Only fetches data for the logged-in user (e.g., abc@gmail.com)
2. **Comprehensive Analysis**: Sends detailed expense summary to Gemini API
3. **Intelligent Responses**: Gemini generates personalized, context-aware insights
4. **Natural Language**: Understands questions in plain English
5. **Privacy First**: Your data is only sent during active chat sessions

### Benefits:
- ✅ **Real AI Intelligence**: Powered by Google's latest AI model
- ✅ **Contextual Understanding**: Understands complex questions
- ✅ **Personalized Advice**: Tailored to YOUR specific spending patterns
- ✅ **Natural Conversations**: Chat naturally like with a financial advisor
- ✅ **Always Learning**: Benefits from Gemini's continuous improvements

### Setup Required:
1. Install package: `pip install google-generativeai`
2. Get API key from: https://makersuite.google.com/app/apikey
3. Add to `gemini_config.py`: `GEMINI_API_KEY = "your-key-here"`
4. Start chatting!

### Example Conversations:

**User**: "How much did I spend on food this month?"  
**Gemini AI**: "Hi! Let me check your food expenses for the last 30 days... 🍽️

Based on your transaction data, you've spent ₹8,450 on food across 15 transactions. That's about ₹563 per day on average.

Breaking it down:
• Restaurants: ₹5,200 (62%)
• Groceries: ₹3,250 (38%)

This accounts for 42% of your monthly budget. I'd recommend:
1. Try meal prepping 2-3 days a week to reduce restaurant visits
2. Shop with a grocery list to avoid impulse purchases
3. Potential savings: ₹2,000-2,500/month

Keep tracking! You're doing great! 💪"

**User**: "What should I focus on to save money?"  
**Gemini AI**: "Great question! After analyzing your spending patterns, here are my top 3 recommendations: 💡

1️⃣ **Entertainment (28% of budget)** - You're spending ₹2,800/month here
   → Consider free events, library, or rotate subscriptions
   → Potential savings: ₹800-1,000/month

2️⃣ **Transport (22% of budget)** - ₹2,200/month on commute
   → Try carpooling 2-3 days/week
   → Monthly pass might be cheaper than daily tickets
   → Potential savings: ₹400-600/month

3️⃣ **Impulse purchases** - I noticed 8 small purchases under ₹200
   → Implement the 24-hour rule before buying
   → Could save: ₹300-400/month

Total potential savings: ₹1,500-2,000/month! 🎉

Start with one category and build from there. Which one would you like to tackle first?"

For detailed setup instructions, see `GEMINI_INTEGRATION.md`
