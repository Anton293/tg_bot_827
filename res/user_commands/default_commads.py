"""users commands default"""
import sys
sys.path.insert(0, "res")
from data_users import data
import bot


def help(update, _):
    update.message.reply_text(f"help")


def error(update, _):
    print("ERROR")


def start(update, _):#error
    update.message.reply_text(f"Hi")
    if update.message.chat.type == "private":
        if data.users['TABLE_USERS_ID']:
            data.users = set()
        data.users['TABLE_USERS_ID'].add(update.message.chat.id)
        bot.send_message(0, f"[{update.message.chat.id}] new user!")
        update.message.reply_text(f"hello new user!")
    elif update.message.chat.type == "supergroup":
        update.message.reply_text(f"hello supergroup!")
    elif update.message.chat.type == "group":
        update.message.reply_text(f"hello group!")
