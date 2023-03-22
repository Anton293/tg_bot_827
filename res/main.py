"""
A chat bot.
"""
import os

#default pkg python
from threading import Thread
import asyncio

#pkg telegram bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Updater, CallbackContext

#commands
from all_commands.schedule import time_couple, callbackquerybutton
from all_commands.moderate_bot import admin_command
from all_commands.default import default

#initialisation
from root.data_users import data
storage_command = data.data_commands['default']
bot = Bot(token=os.getenv('TOKEN'))


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


def create_reply_markup_button(name_button, callback_button):
    button_reply = [
        [InlineKeyboardButton(name_button, callback_data=callback_button)]
    ]
    reply_markup = InlineKeyboardMarkup(button_reply)
    return reply_markup


def keyboard_events(update: Update, _: CallbackContext) -> None:
    """callback button"""
    query = update.callback_query
    query.answer()
    if "week" in query.data:
        callbackquerybutton.processing_keyboard_week(update, query, query.data.replace("week_", ""))
        return
    elif "reply" in query.data:
        #get data
        arr_button_back = query.data.split(":")
        other_user_id = arr_button_back[1]
        admin_user_id = query.from_user.id
        if "user_active" in query.data:
            if admin_user_id not in storage_command['data_messages_admin_user']:
                try:
                    position_other_id = storage_command['data_messages_other_user'].index(other_user_id)
                    id_admin_user = storage_command['data_messages_admin_user'][position_other_id]
                    query.message.reply_text(f"[🛑] Пользователь разговоривает с ID:{id_admin_user}")
                except (ValueError, IndexError, AttributeError):
                    #add to global arr
                    storage_command['data_messages_other_user'].append(other_user_id)
                    storage_command['data_messages_admin_user'].append(admin_user_id)

                    #create button
                    reply_markup = create_reply_markup_button("❌Отмена❌", f"reply_user_cancel:{other_user_id}")

                    #update message
                    query.edit_message_text(f"⏰Ви разгавариваете с: \n{query.message.text}", reply_markup=reply_markup)


        elif "reply_user_cancel" in query.data:
            #create button
            reply_markup = create_reply_markup_button("Начать чат", f"reply_user_active:{other_user_id}")

            #update message
            text = "\n".join(query.message.text.split("\n")[1:])
            query.edit_message_text(text, reply_markup=reply_markup)

            #delete in global arr
            try:
                del storage_command['data_messages_other_user'][storage_command['data_messages_admin_user'].index(admin_user_id)]
                storage_command['data_messages_admin_user'].remove(admin_user_id)
                query.message.reply_text(f"[🛑]Общение с участником 👉 @{bot.get_chat(int(other_user_id)).username} окончено!")
            except ValueError:
                pass

    return


async def main():
    updater = Updater(os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    # Initialize admin commands
    path = "res/all_commands"
    for file_command in os.listdir(path):
        if os.path.isdir(os.path.join(path, file_command)) is False:
            module_name = f"all_commands.{file_command[:-3]}"
            try:
                imported_module = __import__(module_name, fromlist=["command"])
                dispatcher.add_handler(CommandHandler(imported_module.command.call_name, imported_module.command.call_command))
                print(f"Запущена команда -> /{imported_module.command.call_name} -> {imported_module.command.description}")
            except (AttributeError, ImportError):
                pass
        else:
            pass

    admin_command.head_function_register_command_admin(dispatcher, CommandHandler)

    # Register command handlers
    dispatcher.add_handler(CommandHandler("get_week", callbackquerybutton.get_button_options))
    dispatcher.add_handler(CommandHandler("start_events", begin_events))
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
    asyncio.run(main())
