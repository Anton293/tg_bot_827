"""
Лутче бота запускать в терменале

pip install python-telegram-bot==13.15
"""
import asyncio
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, error
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Updater, CallbackContext


def create_button(name_button: str, callback_data):
    button_reply = [[InlineKeyboardButton(name_button, callback_data=callback_data)]]
    reply_markup = InlineKeyboardMarkup(button_reply)
    return reply_markup


def start(update, context):
    update.message.reply_text("hello!")


def text(update, context):
    print(update.message.text)
    print(update.message.chat.id)
    print(update.message.from_user.id)
    print(update.message.from_user.first_name)


def test(update, context):
    update.message.reply_text("Click on button", reply_markup=create_button("button", "click_user"))


def keyboard_events(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_name = query.from_user.first_name
    if query.data == "click_user":
        try:
            query.edit_message_text(f"Click button: {user_name}", reply_markup=create_button("button", "click_user"))
        except error.BadRequest as e:
            print(e)


async def main():
    updater = Updater("YOUR TELEGRAM TOKEN", use_context=True)#os.getenv('TOKEN')
    dispatcher = updater.dispatcher

    #init commands
    dispatcher.add_handler(CommandHandler("start", start)) #/start
    dispatcher.add_handler(CommandHandler("test", test)) #/test
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    dispatcher.add_handler(CallbackQueryHandler(keyboard_events))

    # Start polling
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    asyncio.run(main())
