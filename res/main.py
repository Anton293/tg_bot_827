"""chat bot"""
from threading import Thread

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="res/bd/.env")


from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Updater, CallbackContext

from root.data_users import data
from events import time_couple, events

from user_commands import default_commads, callbackquerybutton
from admin_commands import admin_command


########################################################################
#                               events                                 #
########################################################################


def begin_events():
    """begin events for bot"""
    Thread(target=time_couple.time_read).start()


#begin_events()

########################################################################
#                               START BOT                              #
########################################################################


def keyboard_events(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if "week" in query.data:
        callbackquerybutton.processing_keyboard_week(update, query, query.data.replace("week_", ""))
        return
    return


def main():
    updater = Updater(os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("get_week", callbackquerybutton.get_button_options))
    dispatcher.add_handler(CommandHandler("send_chat", admin_command.send_chat))
    dispatcher.add_handler(CommandHandler("ls_chat", admin_command.ls_chat))

    dispatcher.add_handler(CommandHandler("start", default_commads.start))
    dispatcher.add_handler(CommandHandler("help", default_commads.help))
    dispatcher.add_handler(MessageHandler(Filters.text, events.text))

    dispatcher.add_handler(CallbackQueryHandler(keyboard_events))

    #dispatcher.add_error_handler(default_commads.error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
