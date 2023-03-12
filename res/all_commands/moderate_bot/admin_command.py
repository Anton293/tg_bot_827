import sys
import asyncio

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="res/db/.env")

from telegram import Bot
bot = Bot(token=os.getenv('TOKEN'))

from root.default import admin_command, read_file
from root.data_users import data, config, write_json_in_file
config = config.global_configuration_server
storage_command = data.data_commands['default']


def set_database(update, _):
    pass


@admin_command
def get_database(update, context):
    """get document from database in my chat"""
    update.message.reply_text(f"Вигружаю вам базу данних, ето займет немного времени...")
    chat_id = update.message.chat_id
    document = open('res/bd/database.xlsx', 'rb')
    context.bot.send_document(chat_id, document)


@admin_command
def get_rule_group(update, _):
    update.message.reply_text(read_file("res/db/default/role_group.txt"))


#################################################


@admin_command
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)


@admin_command
def stop_all_chat_moderators(update, _):
    """stop all chat and send message"""
    storage_command['data_messages_admin_user'] = []
    storage_command['data_messages_other_user'] = []
    for admin_id in storage_command['data_messages_admin_user']:
        bot.send_message(admin_id, "Всі чати були завершені, але за бажанням"
                                   " ви можете продовжити розмову відмінивши її та почавши заново")
    update.message.reply_text("chats by stoped in admins")


@admin_command
def reply_user(update, _) -> None:
    """reply user on message used id"""
    if update.message.chat.type == 'private':
        try:
            res = update.message.text.split()
            bot.send_message(int(res[1]), " ".join(res[2:]))
        except (IndexError, ValueError):
            update.message.reply_text("Используйте: /reply_user <user_id> <message>")
        except:
            print(f"Возникла непредвиденная ошибка в функции reply_user() в default.py -> {update.message}")


#################################################


@admin_command
def help_admin(update, _):
    update.message.reply_text(f"{data.text_help_admin}")


def head_function_register_command_admin(dispatcher, CommandHandler):
    data.text_help_admin = ""
    arr = [
        ("set_database", "set_database", "set database in exel table(неработает)"),
        ("get_database", "get_database", "get database in exel table"),
        ("restart_program", "restart_program", "Перезапускает скрипт бота"),
        ("reply_user", "restart_program", "Отправляет собеседнику сообщение, используйте: /reply_user <user_id> <message>"),
        ("help_admin", "help_admin", "Список команд админов"),
        ("get_rule_group", "get_rule_group", "(Команда не для управления) Нужна для администрирувания групи и показивает заданние текст")
    ]
    for command, function, description in arr:
        if True:
            dispatcher.add_handler(CommandHandler(command, eval(function)))
            data.text_help_admin += f"/{command} - {description}\n"
