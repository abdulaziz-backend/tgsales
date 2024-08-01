from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def start():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏷Sell Usernames"), KeyboardButton(text="📊View Listings")],
            [KeyboardButton(text="📞Contact"),
             KeyboardButton(text="ℹ️Help")],
            [KeyboardButton(text="💰My Balance")] 
        ],
        resize_keyboard=True
    )

def choose():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Channel"), KeyboardButton(text="Group")],
            [KeyboardButton(text="Bot")],
        ],
        resize_keyboard=True
    )

def agree_terms_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Agree✅", callback_data="agree_terms")]
        ]
    )

def check_admin_status_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="I've made the bot an admin", callback_data="check_admin_status")]
        ]
    )
