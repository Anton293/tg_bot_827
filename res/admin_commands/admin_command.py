import sys
import asyncio
sys.path.insert(0, "res")
from data_users import data
import bot


def send_chat(update, _):
    arr = update.message.text.split(" ")
    update.message.reply_text(arr[1:])
    asyncio.run(bot.text_send(int(arr[1]), f"{' '.join(arr[2:])}"))


def ls_chat(update, _):
    pass
