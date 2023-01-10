"""events"""
import os
import sys
import asyncio

sys.path.insert(0, "res")
from data_users import data
from bot import bot


######################################################################
#                               text                                 #
######################################################################


def send_msg_me(update, user_from):
    bot.send_message(os.getenv("ADMIN_ID"), f"[{user_from['first_name']}] {update.message.text}")


def text(update, _):
    user_from = eval(str(update.message))['from']
    arr_word = ''

    if update.message.chat.type == 'private' and not os.getenv("ADMIN_ID") == str(user_from['id']):
        data.active_last_user = user_from['id']
        send_msg_me(update, user_from)

    if len(list(set(update.message.text.split(" ")) & set(arr_word))) > 0 and update.message.chat.type != 'private':
        send_msg_me(update, user_from)
