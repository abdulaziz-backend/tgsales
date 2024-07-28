from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

async def get_subscriber_count(bot: Bot, username: str) -> int:
    try:
        chat = await bot.get_chat(username)
        return chat.members_count if hasattr(chat, 'members_count') else 0
    except TelegramAPIError as e:
        print(f"Failed to get subscriber count: {e}")
        return 0
