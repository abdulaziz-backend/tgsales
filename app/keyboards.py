from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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
            [KeyboardButton(text="🗞Channel"), KeyboardButton(text="💬Group")],
            [KeyboardButton(text="🤖Bot")],
        ],
        resize_keyboard=True
    )

def pricing_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="10 $BLAZE", callback_data="buy_blaze_10"),
             InlineKeyboardButton(text="20 $BLAZE", callback_data="buy_blaze_20")],
            [InlineKeyboardButton(text="50 $BLAZE", callback_data="buy_blaze_50"),
             InlineKeyboardButton(text="100 $BLAZE", callback_data="buy_blaze_100")],
            [InlineKeyboardButton(text="150 $BLAZE", callback_data="buy_blaze_150"),
             InlineKeyboardButton(text="200 $BLAZE", callback_data="buy_blaze_200")]
        ]
    )

def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Add Listing"), KeyboardButton(text="Remove Listing")],
            [KeyboardButton(text="View All Listings"), KeyboardButton(text="Manage Users")],
            [KeyboardButton(text="Back to Main Menu")]
        ],
        resize_keyboard=True
    )

