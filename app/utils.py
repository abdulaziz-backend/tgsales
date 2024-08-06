import random
import string
from aiogram import Bot

async def is_owner(username, user_id, bot: Bot):
    try:
        chat = await bot.get_chat(username)
        member = await bot.get_chat_member(chat.id, user_id)
        return member.is_chat_owner()
    except:
        return False

async def get_subscriber_count(username, bot: Bot):
    try:
        chat = await bot.get_chat(username)
        return chat.get('members_count', 0)
    except:
        return 0

def generate_random_code(length=4):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
