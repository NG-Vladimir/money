from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Функция для добавления транзакции
def add_transaction(trans_type, amount, category, comment):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO transactions (type, amount, category, comment, date) VALUES (?, ?, ?, ?, ?)",
                   (trans_type, amount, category, comment, date))
    conn.commit()
    conn.close()

# Функция для получения истории транзакций
def get_transactions():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT type, amount, category, comment, date FROM transactions ORDER BY date DESC")
    transactions = cursor.fetchall()
    conn.close()
    return transactions

# Главная страница
@app.route('/')
def index():
    return render_template("index.html")

# API для добавления транзакции
@app.route('/add_transaction', methods=['POST'])
def handle_add_transaction():
    data = request.json
    add_transaction(data['type'], data['amount'], data['category'], data.get('comment', ''))
    return jsonify({"status": "success"})

# API для получения истории
@app.route('/get_transactions', methods=['GET'])
def handle_get_transactions():
    transactions = get_transactions()
    return jsonify(transactions)

# API для удаления всех транзакций (если нужно)
@app.route('/delete_all', methods=['POST'])
def delete_all_transactions():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Все транзакции удалены"})

if __name__ == '__main__':
    app.run(debug=True)
