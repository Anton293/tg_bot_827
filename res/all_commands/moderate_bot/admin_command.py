import sys
import asyncio
import os

from root.data_users import data


def send_chat(update, _):
    arr = update.message.text.split(" ")
    asyncio.run(bot.text_send(int(arr[1]), f"{' '.join(arr[2:])}"))


def check_on_admin(update):
    id_chat = update.message.chat.id
    id_user = eval(str(update.message))['from']['id']
    if os.getenv("ADMIN_ID") == str(id_user):
        return True


def set_database(update, _):
    pass


def get_database(update, context):
    """get document from database in my chat"""
    update.message.reply_text(f"Вигружаю вам базу данних, ето займет немного времени...")
    chat_id = update.message.chat_id
    document = open('res/bd/database.xlsx', 'rb')
    context.bot.send_document(chat_id, document)


def help_admin(update, _):
    update.message.reply_text(f"{data.text_help_admin}")


def head_function_register_command_admin(dispatcher, CommandHandler):
    data.text_help_admin = ""
    arr = [
        ("set_database", "set_database", "set database in exel table(неработает)"),
        ("get_database", "get_database", "get database in exel table"),
        ("help_admin", "help_admin", "list command admin")
    ]
    for command, function, description in arr:
        dispatcher.add_handler(CommandHandler(command, eval(function)))
        data.text_help_admin += f"/{command} - {description}\n"
