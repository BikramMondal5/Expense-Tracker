# 💰📊 Personal Expense Tracker

A simple yet powerful **Python-based Expense Tracker** that helps you take control of your daily, weekly, and monthly spending habits.  
Easily add expenses, visualize your spending trends with pie charts, and store all your data securely in MongoDB - all through an intuitive Tkinter GUI.

## 🌟 Features

- 🧾 **Add Daily Expenses** – Quickly log your daily spending with category, date, and notes.  
- 📅 **Monthly & Weekly Insights** – Get automated summaries powered by NumPy & pandas.  
- 🧠 **Smart Data Handling** – All transactions stored in MongoDB for long-term tracking.  
- 📈 **Visual Analytics** – Generate colorful pie charts for category-wise spending using Matplotlib.  
- 💾 **Export to CSV** – Backup or analyze your expense data anytime.  
- 🪟 **Interactive GUI** – Clean, beginner-friendly interface built with Tkinter.  
- 🔍 **Filter & Review** – View summaries by category or date range.  

## 🛠️ Technologies Used

- 🐍 **Python 3.x** – Core programming language  
- 🪟 **Tkinter** – GUI framework for user interface  
- 🧮 **NumPy** – Mathematical operations and calculations  
- 🧾 **pandas** – Data handling and tabular operations  
- 📊 **Matplotlib** – Data visualization and pie charts  
- 🍃 **MongoDB** – Cloud/local database for storing expenses  

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

4. **Start MongoDB**: For local setup, run MongoDB server → `mongod` or use `MongoDB Atlas` and replace your connection string in the code.

5. Run the application:
```bash
python main.py
```

## 🚀 How to Use

- 🪙 **Add Expense** – Enter date, category, amount, and note → Click “Add Expense”.
- 📋 **View Summary** – See your total & category-wise spending.
- 📈 **View Chart** – Visualize your expenses with a pie chart.
- 💾 **Export Data** – Save all transactions to `expenses.csv`.
- 🔁 **Restart Anytime** – Data stays safe in MongoDB.

## 📜 License

This project is licensed under the `MIT License`.
