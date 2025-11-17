# 💰📊 MyWallet - Personal Expense Tracker

![Google](https://img.shields.io/badge/Google-%23FFFFFF?logo=google&logoColor=%234285F4)
[![Watch the demo](./public/image9.png)](https://youtu.be/PXE6EQHTw1Q)
A simple yet powerful **Python-based Expense Tracker** that helps you take control of your daily, weekly, and monthly spending habits. Easily add expenses, visualize your spending trends with pie charts, and store all your data locally in a JSON file - all through an intuitive Tkinter GUI.

## `🔵 NOTE: Click the image to play the full video.`

## 🌟 Features

- 🔐 **Secure Authentication** – Modern login/signup system with password hashing.
- 🙋 **User Onboarding** – Smooth onboarding flow for new users to set up their profile.
- 🧾 **Add Daily Expenses** – Quickly log your daily spending with category, date, and notes.  
- 📅 **Monthly & Weekly Insights** – Get automated summaries powered by NumPy & pandas.  
- 🧠 **Smart Data Handling** – All transactions stored locally in a `users.json` file.  
- 📈 **Visual Analytics** – Generate colorful pie charts for category-wise spending using Matplotlib.  
- 💾 **Export to CSV & PDF** – Backup or analyze your expense data anytime.  
- 🪟 **Interactive GUI** – Clean, modern interface built with Tkinter.  
- 🔍 **Filter & Review** – View all transactions, sort them, and export them.
- 🤖 **AI-Powered Summary** - Get an AI-generated summary of your spending habits using Google Gemini.

## 🔗 Important Links
- 👉 You can download the `.exe` file from here: [Google_drive_link](https://drive.google.com/drive/folders/1wcgCqpe0CIqLQTrBpwYuEYCv-gDLuiHy?usp=sharing)
- 👉 You can find the complete project documentation here: [Google_docs](https://docs.google.com/document/d/1ZFZRMg-GMIlJ2pFmr0tnX5mJVxzxQiELcuxvcqypN-Q/edit?usp=sharing)

## 🛠️ Technologies Used

- **Python 3.x** – Core programming language  
- **Tkinter** – GUI framework for user interface  
- **NumPy** – Mathematical operations and calculations  
- **pandas** – Data handling and tabular operations  
- **Matplotlib** – Data visualization and pie charts
- **Google Gemini** - For AI-powered expense summaries.
- **JSON** – For local data storage.

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/BikramMondal5/Expense-Tracker.git
```

2. Navigate to the project directory:
```bash
cd Expense-Tracker
```

3. Install the required depedencies:
```bash
pip install -r requirements.txt
```

4. **Configure Google Gemini API Key**: 
   - Create a `.env` file in the root directory.
   - Add your Google Gemini API key to it like this:
     ```python
     GEMINI_API_KEY = "YOUR_API_KEY"
     ```

5. Run the application:
```bash
python main.py
```

## 🚀 How to Use

- 🚪 **Login/Signup** – Create an account or log in with your credentials.
- 🪙 **Add Expense** – Enter date, category, amount, and note → Click “Add Expense”.
- 📋 **View Summary** – See your total & category-wise spending.
- 📈 **View Chart** – Visualize your expenses with a pie chart.
- 📜 **View All Transactions** - See a detailed list of all your expenses.
- 💾 **Export Data** – Save all transactions to `expenses.csv` or `transactions.pdf`.
- 🤖 **Get AI Summary** - Get a smart summary of your spending habits.
- 🔁 **Restart Anytime** – Data is saved locally in `users.json`.

## 📜 License

This project is licensed under the `MIT License`.
