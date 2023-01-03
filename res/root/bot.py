import asyncio
from aiogram import Bot
import os


bot = Bot(token=os.getenv('TOKEN'))


async def text_send(chat_id, text):
    await bot.send_message(chat_id, text)


def send_message(chat_id, message):
    asyncio.run(text_send(chat_id, message))
