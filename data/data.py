import sqlite3
import os

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_user_data(user_id, username):
    user_data_path = f"data/users/{user_id}.sqlite"
    ensure_directory_exists("data/users")
    conn = sqlite3.connect(user_data_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)''')
    cursor.execute('''INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)''', (user_id, username))
    conn.commit()
    conn.close()

def save_listing(sell_type, username, user_id, price, subscriber_count):
    if sell_type == "Channel":
        folder_name = "data/channels"
    elif sell_type == "Group":
        folder_name = "data/groups"
    elif sell_type == "Bot":
        folder_name = "data/bots"
    else:
        raise ValueError("Invalid sell type")

    ensure_directory_exists(folder_name)
    
    conn = sqlite3.connect(f"{folder_name}/{sell_type.lower()}.sqlite")
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {sell_type.lower()}s (username TEXT PRIMARY KEY, owner_id INTEGER, price TEXT, subscriber_count INTEGER)''')
    cursor.execute(f'''INSERT OR REPLACE INTO {sell_type.lower()}s (username, owner_id, price, subscriber_count) VALUES (?, ?, ?, ?)''', (username, user_id, price, subscriber_count))
    conn.commit()
    conn.close()

    user_data_path = f"data/users/{user_id}.sqlite"
    conn = sqlite3.connect(user_data_path)
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {sell_type.lower()}s (username TEXT PRIMARY KEY, price TEXT, subscriber_count INTEGER, owner_username TEXT)''')
    
    owner_username = get_owner_username(user_id)  # Function to retrieve the owner's username

    cursor.execute(f'''INSERT OR REPLACE INTO {sell_type.lower()}s (username, price, subscriber_count, owner_username) VALUES (?, ?, ?, ?)''', (username, price, subscriber_count, owner_username))
    conn.commit()
    conn.close()

    ensure_directory_exists("data/usernames")
    conn = sqlite3.connect("data/usernames/usernames.sqlite")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usernames (username TEXT PRIMARY KEY, owner_id INTEGER, price TEXT, owner_username TEXT)''')
    cursor.execute('''INSERT OR REPLACE INTO usernames (username, owner_id, price, owner_username) VALUES (?, ?, ?, ?)''', (username, user_id, price, owner_username))
    conn.commit()
    conn.close()

def get_owner_username(user_id):
    return "username"  
