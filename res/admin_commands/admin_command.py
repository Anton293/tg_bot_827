import sys
import asyncio
sys.path.insert(0, "res")
from data_users import data
import bot


def send_chat(update, _):
    arr = update.message.text.split(" ")
    asyncio.run(bot.text_send(int(arr[1]), f"{' '.join(arr[2:])}"))

