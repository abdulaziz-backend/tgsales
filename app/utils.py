from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

async def get_subscriber_count(bot: Bot, username: str) -> int:
    try:
        chat = await bot.get_chat(username)
        return chat.members_count if hasattr(chat, 'members_count') else 0
    except TelegramAPIError as e:
        print(f"Failed to get subscriber count: {e}")
        return 0

async def is_owner(bot: Bot, username: str, user_id: int) -> bool:
    try:
        chat_member = await bot.get_chat_member(username, user_id)
        return chat_member.status == 'creator'
    except TelegramAPIError as e:
        print(f"Failed to check ownership: {e}")
        return False

async def is_bot_admin(bot: Bot, username: str) -> bool:
    try:
        chat_member = await bot.get_chat_member(username, bot.id)
        return chat_member.status in ['administrator', 'creator']
    except TelegramAPIError as e:
        print(f"Failed to check bot admin status: {e}")
        return False
