from aiogram import Router, types, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods import GetUserProfilePhotos, SendPhoto
from app.keyboards import start, choose, pricing_keyboard
from app.utils import get_subscriber_count, is_owner, generate_random_code
from data.data import save_user_data, save_listing, get_user_balance_and_orders, update_balance

router = Router()

class SellState(StatesGroup):
    waiting_for_type = State()
    waiting_for_username = State()
    waiting_for_price = State()
    waiting_for_agreement = State()

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

    await message.answer_photo(photo="https://i.ibb.co/7y4SRLB/pixelcut-export-22.png", caption=greeting_message)
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
        await message.answer("❌ You must be the owner of the group or channel to sell it❗️")
        return
    
    subscriber_count = await get_subscriber_count(username, bot)
    await state.update_data(username=username, subscriber_count=subscriber_count)
    await message.answer("💴What is the price in $BLAZE?\n if you dont know see Your balance.")
    await state.set_state(SellState.waiting_for_price)

@router.message(SellState.waiting_for_price)
async def handle_sell_price(message: types.Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer("❌ Please enter a valid price.")
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

@router.message(lambda message: message.text == "💰My Balance")
async def my_balance(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    balance, orders = get_user_balance_and_orders(user_id)
    response = (
        f"💳 Your balance:\n"
        f"💲 Balance: {balance} $BLAZE\n"
        f"🪪 Your ID: {user_id}\n"
        f"👤 Username: @{message.from_user.username}\n"
    )

    photos = await bot(GetUserProfilePhotos(user_id=user_id))
    if photos.total_count > 0:
        photo = photos.photos[0][0].file_id
        await message.answer_photo(photo=photo, caption=response, reply_markup=pricing_keyboard())
    else:
        await message.answer(response, reply_markup=pricing_keyboard())

@router.callback_query(lambda call: call.data.startswith("buy_blaze_"))
async def handle_pricing_choice(call: CallbackQuery):
    user_id = call.from_user.id
    amount_map = {
        "buy_blaze_10": 5,
        "buy_blaze_20": 10,
        "buy_blaze_50": 25,
        "buy_blaze_100": 50,
        "buy_blaze_150": 75,
        "buy_blaze_200": 100
    }
    amount = amount_map[call.data]
    random_code = generate_random_code()
    response = (
        f" Amount :  {amount} TON💎 \n Add this word as a comment - {random_code}\n "
        f"‼️ If you don't add this, you can't top up your balance.\n\n"
        f"👛Wallet address: `adress`\n\n"
    )
    await call.message.answer(response)

@router.message(F.text == "ℹ️Help")
async def show_help(message: Message):
    help_text = """
Welcome to the $BLAZE Marketplace Bot! 🚀

You can use this bot to buy or sell Telegram channels, groups, and bots with complete security and anonymity.

How to Get Started:
Top Up Your Balance:
To buy any channel, group, or bot, you need to top up your balance.

Currency: $BLAZE
Exchange Rate: 1 $BLAZE = 0.5 TONs
Buying:

Browse available listings.
Choose what you want to purchase.
Complete the transaction using your $BLAZE balance.
Selling:

List your channel, group, or bot for sale.
Wait for interested buyers.
Finalize the sale securely.
Commands:
/start - start bot.
/help - Get this help message.
If you have any questions or need assistance, feel free to contact support!"""
    await message.answer(help_text)
