import sqlite3
import os

def init_db():
    conn = sqlite3.connect('transactions.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            username TEXT,
            owner_id INTEGER,
            price INTEGER,
            subscriber_count INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            code TEXT,
            amount INTEGER,
            completed BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def save_user_data(user_id, username):
    conn = sqlite3.connect('transactions.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)
    ''', (user_id, username))
    conn.commit()
    conn.close()

def save_listing(sell_type, username, owner_id, price, subscriber_count):
    conn = sqlite3.connect('transactions.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO listings (type, username, owner_id, price, subscriber_count)
        VALUES (?, ?, ?, ?, ?)
    ''', (sell_type, username, owner_id, price, subscriber_count))
    conn.commit()
    conn.close()

def get_user_balance_and_orders(user_id):

    conn = sqlite3.connect('transactions.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT balance FROM users WHERE user_id = ?
    ''', (user_id,))
    balance = cursor.fetchone()
    balance = balance[0] if balance else 0

    cursor.execute('''
        SELECT COUNT(*) FROM listings WHERE owner_id = ?
    ''', (user_id,))
    orders = cursor.fetchone()[0]
    
    conn.close()
    return balance, orders

def update_balance(user_id, amount):
    conn = sqlite3.connect('transactions.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET balance = balance + ? WHERE user_id = ?
    ''', (amount, user_id))
    conn.commit()
    conn.close()

init_db()
