import sqlite3
from pytonapi import Tonapi

TONAPI_KEY = "AGXE3X6MI4NK3WIAAAAFAZUNNPDKLRMOCQEAXKFKPNQIIBHSTDR4B6X3EB745OE4WIBRFZQ" 
MY_WALLET_ADDRESS = "UQCNeLkssvBYoENt5FGF9tpZEv7gM2Ivxl9TwONmf_AJdO3V"

tonapi = Tonapi(api_key=TONAPI_KEY)

async def save_transaction(user_id, code, amount):

    conn = sqlite3.connect('transactions.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (user_id, code, amount) 
        VALUES (?, ?, ?)
    ''', (user_id, code, amount))
    conn.commit()
    conn.close()

async def verify_and_update_balance(transaction_hash, user_id, amount):
    """
    Verify the transaction using pytonapi and update the user's balance if the transaction is confirmed.
    """
    try:
        # Use pytonapi to check transaction details
        transaction_info = await tonapi.get_transaction_info(transaction_hash)
        if transaction_info["status"] == "confirmed":
            from data.data import update_balance
            update_balance(user_id, amount)
            conn = sqlite3.connect('transactions.sqlite')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE transactions SET completed = 1 WHERE user_id = ? AND amount = ?
            ''', (user_id, amount))
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        print(f"Error verifying transaction: {e}")
    return False

async def send_ton_transaction(amount_ton, comment):
    """
    Send a TON transaction.
    """
    try:
        transaction_data = {
            "from_address": MY_WALLET_ADDRESS,
            "to_address": MY_WALLET_ADDRESS,  
            "amount": int(amount_ton * 10**9), 
            "comment": comment
        }
        
        transaction_hash = await tonapi.send_transaction(transaction_data)
        return transaction_hash
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None
