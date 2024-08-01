from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.keyboards import start, choose
from app.utils import get_subscriber_count, is_owner
from data.data import save_user_data, save_listing

router = Router()

class SellState(StatesGroup):
    waiting_for_type = State()
    waiting_for_username = State()
    waiting_for_price = State()
    waiting_for_agreement = State()  # New state for terms of use agreement

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    save_user_data(user_id, username)
    
    greeting_message = (
        "👋 Welcome to Our Bot!\n\n"
        "👀 Easily buy or sell channels and groups with confidence. Trusted by 1,400 users, our bot has facilitated nearly 100 successful trades. "
        "🔓 You can securely transact using TON, with $BLAZE support coming soon.\n\n"
        "✨ If you need assistance, simply send the /help command.\n\n"
    )
    
    terms_of_use = (
        "📜 Terms of Use:\n\n"
        "Failure to Transfer Ownership:\n"
        "If you do not transfer ownership of your channel, group, or bot to the buyer after they have paid you, you will be fined 3 TON. "
        "If this happens more than 3 times, you will be banned from using the bot and fined 10 TON. Failure to pay the fine will result in serious consequences.\n\n"
        "Listing for Sale:\n"
        "You must be the owner of a username, channel, group, or bot to list it for sale.\n\n"
        "Getting Help:\n"
        "If you need help, type the /help command.\n\n"
        "🔒 Privacy and Security:\n"
        "All transactions are secure and anonymous.\n\n"
        "⚖️ Payment Terms:\n"
        "A 15% commission fee is charged for every transaction.\n\n"
        "By using this bot, you agree to these terms. Your security and convenience are our priority! 😊"
    )
    
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Agree✅", callback_data="agree_terms")]
        ]
    )
    await message.answer(greeting_message)
    await message.answer(terms_of_use, reply_markup=inline_kb)
    await state.set_state(SellState.waiting_for_agreement)

@router.callback_query(SellState.waiting_for_agreement, lambda call: call.data == "agree_terms")
async def handle_agreement(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Thank you for agreeing to the terms. You can now use the bot.", reply_markup=start())
    await state.clear()

@router.message(Command("help"))
async def help_command(message: Message):
    help_text = """
    /start - Welcome to Our Bot!
    /help - Here are the available commands:
    
    📜 Terms of Use:
    📲 Telegram Bot for buying or selling channels, groups, and bots.
    
    Failure to Transfer Ownership:
    If you do not transfer ownership of your channel, group, or bot to the buyer after they have paid you, you will be fined 3 TON.
    If this happens more than 3 times, you will be banned from using the bot and fined 10 TON. Failure to pay the fine will result in serious consequences.
    
    Listing for Sale:
    You must be the owner of a username, channel, group, or bot to list it for sale.
    
    Getting Help:
    If you need help, type the /help command.
    
    🔒 Privacy and Security:
    All transactions are secure and anonymous.
    
    ⚖️ Payment Terms:
    A 15% commission fee is charged for every transaction.
    
    By using this bot, you agree to these terms. Your security and convenience are our priority! 😊
    """
    await message.answer(help_text)

@router.message(lambda message: message.text == "🏷Sell Usernames")
async def handle_sell_usernames(message: types.Message, state: FSMContext):
    await message.answer("🆗 Choose the option to list your username on the market. Don’t forget! You can only sell if you are the owner of the group, channel, or bot. 🚀", reply_markup=choose())
    await state.set_state(SellState.waiting_for_type)

@router.message(SellState.waiting_for_type)
async def handle_sell_type(message: types.Message, state: FSMContext):
    sell_type = message.text
    if sell_type not in ["Channel", "Group", "Bot"]:
        await message.answer("Please choose a valid option: Channel, Group, or Bot.", reply_markup=choose())
        return
    
    await state.update_data(sell_type=sell_type)
    await message.answer(f"Please send the username of the {sell_type.lower()}.")
    await state.set_state(SellState.waiting_for_username)

@router.message(SellState.waiting_for_username)
async def handle_sell_username(message: types.Message, state: FSMContext, bot: Bot):
    username = message.text
    user_id = message.from_user.id
    sell_type = (await state.get_data())['sell_type']
    
    if not await is_owner(username, user_id, bot):
        await message.answer("You must be the owner of the group or channel to sell it.")
        return
    
    subscriber_count = await get_subscriber_count(username, bot)
    await state.update_data(username=username, subscriber_count=subscriber_count)
    await message.answer("What is the price in TON?")
    await state.set_state(SellState.waiting_for_price)

@router.message(SellState.waiting_for_price)
async def handle_sell_price(message: types.Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer("Please enter a valid price.")
        return
    
    await state.update_data(price=price)
    user_data = await state.get_data()
    sell_type = user_data['sell_type']
    username = user_data['username']
    subscriber_count = user_data['subscriber_count']
    user_id = message.from_user.id
    
    save_listing(sell_type, username, user_id, price, subscriber_count)
    await message.answer(f"Your {sell_type.lower()} has been listed for sale at {price} TON.", reply_markup=start())
    await state.clear()


@router.message(lambda message: message.text == "📞Contact")
async def contact(message: types.Message):
    contact_message = (
        "To connect with us, please visit the following links:\n\n"
        "🌟 [Ablaze Coder](https://t.me/ablaze_coder)\n"
        "✨ [Jalloliddin](https://t.me/darkweb_JF)"
    )
    await message.answer(contact_message, reply_markup=start())
