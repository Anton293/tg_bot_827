"""events"""
import os
import sys
import asyncio

sys.path.insert(0, "res")
from data_users import data
from bot import bot


def text(update, _):
    user_from = eval(str(update.message))['from']
    arr_word = ''
    if len(list(set(update.message.text.split(" ")) & set(arr_word))) > 0 and update.message.chat.type != 'private':
        bot.send_message(os.getenv("ADMIN_ID"), f"[{user_from['first_name']}] {update.message.text}")
    if update.message.chat.type == 'private' and not os.getenv("ADMIN_ID") == str(user_from['id']):
        data.active_last_user = user_from['id']
        bot.send_message(os.getenv("ADMIN_ID"), f"[{user_from['first_name']}] {update.message.text}")
