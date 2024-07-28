from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_choice_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Channel")],
            [KeyboardButton(text="Group")],
            [KeyboardButton(text="Bot")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_edit_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Channel")],
            [KeyboardButton(text="Group")],
            [KeyboardButton(text="Bot")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_edit_options_keyboard(user_info):
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    for line in user_info.split('\n'):
        if line:
            info_type = line.split(' ')[0]
            inline_keyboard.add(
                InlineKeyboardButton(f"Edit {info_type}", callback_data=f"edit_{info_type.lower()}"),
                InlineKeyboardButton(f"Delete {info_type}", callback_data=f"delete_{info_type.lower()}")
            )
    return inline_keyboard
