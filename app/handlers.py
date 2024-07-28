from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.keyboards import get_choice_keyboard, get_edit_keyboard, get_edit_options_keyboard
from data.data import save_user_to_file, save_channel_info, save_group_info, save_bot_info, get_user_info, edit_info, delete_info
from app.utils import get_subscriber_count

router = Router()

class NewUsernameState(StatesGroup):
    choice = State()
    channel_username = State()
    group_username = State()
    bot_username = State()

class EditUsernameState(StatesGroup):
    choose_edit = State()
    new_info = State()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await message.answer(
        "👋 Welcome to Our Bot!\n\n"
        "Easily buy or sell channels and groups with confidence. Trusted by 1,400 users, our bot has facilitated nearly 100 successful trades. "
        "You can securely transact using TON, with $BLAZE support coming soon.\n\n"
        "If you need assistance, simply send the /help command.",
        reply_markup=get_choice_keyboard()
    )
    await state.set_state(NewUsernameState.choice)

@router.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "/start - Welcome to Our Bot!\n"
        "/help - Here is available commands:\n"
        "/myusernames - View Your Listed Usernames\n"
        "/newusername - List Your Channel or Group for Sale\n"
        "/edit - Edit your channel/group info\n"
        "/username - Browse Channels and Groups for Sale"
    )
    await message.answer(help_text)

@router.message(Command("myusernames"))
async def myusernames_command(message: Message):
    user_id = message.from_user.id
    user_info = get_user_info(user_id)
    
    if user_info:
        await message.answer(user_info)
    else:
        await message.answer("You have not listed any usernames for sale.")

@router.message(Command("newusername"))
async def newusername_command(message: Message, state: FSMContext):
    await message.answer("Please choose an option:", reply_markup=get_choice_keyboard())
    await state.set_state(NewUsernameState.choice)

@router.message(NewUsernameState.choice)
async def handle_choice(message: Message, state: FSMContext):
    choice = message.text

    if choice == "Channel":
        await message.answer("OK, Send me your channel username:")
        await state.set_state(NewUsernameState.channel_username)
    elif choice == "Group":
        await message.answer("OK, Send me your group username:")
        await state.set_state(NewUsernameState.group_username)
    elif choice == "Bot":
        await message.answer("OK, Send me your bot username:")
        await state.set_state(NewUsernameState.bot_username)
    else:
        await message.answer("Invalid choice. Please choose 'Channel', 'Group' or 'Bot'.")

@router.message(NewUsernameState.channel_username)
async def handle_channel_username(message: Message, state: FSMContext):
    username = message.text
    subscriber_count = await get_subscriber_count(message.bot, username)

    user_id = message.from_user.id
    save_channel_info(user_id, username, subscriber_count)

    await message.answer("Your channel information has been saved.")
    await state.finish()

@router.message(NewUsernameState.group_username)
async def handle_group_username(message: Message, state: FSMContext):
    username = message.text
    subscriber_count = await get_subscriber_count(message.bot, username)

    user_id = message.from_user.id
    save_group_info(user_id, username, subscriber_count)

    await message.answer("Your group information has been saved.")
    await state.finish()

@router.message(NewUsernameState.bot_username)
async def handle_bot_username(message: Message, state: FSMContext):
    username = message.text
    subscriber_count = await get_subscriber_count(message.bot, username)

    user_id = message.from_user.id
    save_bot_info(user_id, username, subscriber_count)

    await message.answer("Your bot information has been saved.")
    await state.finish()

@router.message(Command("edit"))
async def edit_command(message: Message):
    user_id = message.from_user.id
    user_info = get_user_info(user_id)

    if user_info:
        await message.answer("Please choose what you want to edit:", reply_markup=get_edit_options_keyboard(user_info))
    else:
        await message.answer("You have not listed any usernames for sale.")

@router.callback_query(lambda c: c.data and c.data.startswith('edit_'))
async def process_edit_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    await state.update_data(edit_choice=callback_query.data[5:])
    await callback_query.message.answer(f"OK, send me the new information for your {callback_query.data[5:]}:")
    await state.set_state(EditUsernameState.new_info)

@router.callback_query(lambda c: c.data and c.data.startswith('delete_'))
async def process_delete_callback(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    delete_choice = callback_query.data[7:]
    delete_info(user_id, delete_choice)
    await callback_query.message.answer(f"Your {delete_choice} has been deleted.")

@router.message(EditUsernameState.new_info)
async def handle_new_info(message: Message, state: FSMContext):
    data = await state.get_data()
    edit_choice = data.get("edit_choice")
    new_info = message.text

    user_id = message.from_user.id
    edit_info(user_id, edit_choice, new_info)

    await message.answer(f"Your {edit_choice} information has been updated.")
    await state.finish()
