"""
A chat bot.
"""
import os
import json

#default pkg python
import sys
from threading import Thread

#pkg telegram bot
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Updater, CallbackContext

#commands
from all_commands.schedule import time_couple, callbackquerybutton
from all_commands.moderate_bot import admin_command
from all_commands.default import default

#initialisation .env
load_dotenv(dotenv_path="res/bd/.env")


def begin_events(update, _):
    """Begins events for bot."""
    Thread(target=time_couple.check_before_start_function_warning_of_couple, args=(update,)).start()


def call_function(func_str: str):
    """string in function"""
    parts = func_str.split('(')
    name = parts[0]
    args_str = parts[1][:-1]
    args = [a.strip() for a in args_str.split(',')]
    func = globals()[name]
    func(*args)


def keyboard_events(update: Update, _: CallbackContext) -> None:
    """"""
    query = update.callback_query
    query.answer()
    if "week" in query.data:
        callbackquerybutton.processing_keyboard_week(update, query, query.data.replace("week_", ""))
        return
    return


def main():
    updater = Updater(os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    # Initialize admin commands
    admin_command.head_function_register_command_admin(dispatcher, CommandHandler)

    # Register command handlers
    dispatcher.add_handler(CommandHandler("get_week", callbackquerybutton.get_button_options))
    dispatcher.add_handler(CommandHandler("send_chat", admin_command.send_chat))
    dispatcher.add_handler(CommandHandler("start_events", begin_events))
    dispatcher.add_handler(CommandHandler("start", default.start))
    dispatcher.add_handler(CommandHandler("help", default.help))
    dispatcher.add_handler(CommandHandler("reply_user", default.reply_user))
    dispatcher.add_handler(CommandHandler("get_chat", default.get_chat))
    dispatcher.add_handler(CommandHandler("get_list_user", default.list_users))
    dispatcher.add_handler(MessageHandler(Filters.text, default.text))
    dispatcher.add_handler(CallbackQueryHandler(keyboard_events))

    # Register error handler
    #dispatcher.add_error_handler(default.error)

    # Start polling
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()
