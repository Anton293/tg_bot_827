"""users commands default"""
import os
from datetime import datetime, timedelta

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, error

from root.default import admin_command, count_second_to_time, read_file, test_time_start, AppendToFileDAta, send_all_admin_message, config
from all_commands.default.module_checking_message import check_messages
from root.data_users import data

storage_command = data.data_commands['default']
bot = Bot(token=os.getenv('TOKEN'))
####################################################################
#                           moderate users                         #
####################################################################


def processing_error(update, context):
    print(f"Update {update} ///// cause error: {context.error}")


list_users = []#create class
append_data_in_file = AppendToFileDAta(config['point_save_messages'])


@test_time_start
def admin_send_message_in_virtual_chat_user(update):
    try:
        position_admin_id = storage_command['data_messages_admin_user'].index(update.message.chat.id)
        id_other_user = storage_command['data_messages_other_user'][position_admin_id]
        bot.send_message(id_other_user, update.message.text)
        print(f"admin send message -> {id_other_user} -> {update.message.text}")
    except (ValueError, AttributeError):
        pass


def create_button(button_name, button_data):
    button_reply = [
        [InlineKeyboardButton(button_name, callback_data=button_data)]
    ]
    reply_markup = InlineKeyboardMarkup(button_reply)
    return reply_markup


class Huhu(object):
    def __init__(self):
        self.colab = []
        self.array_users = {'Iva', 'Аяна-Vitalina', 'Антон', 'nika'}

    def checking(self, update):
        new_message = update.message.text
        clean_text = new_message.lower().strip(" ,./?<>-=+_")
        if update.message.chat.id == -1001605339520:
            self.array_users.add(update.message.from_user.first_name)
            print(self.array_users)
            if "когда колаб" in clean_text:
                update.message.reply_text("пока ещо незнаю")

    def send_poll(self, update):
        if count_second_to_time(9, 0, 0) < 2*3600:
            bot.send_poll(chat_id=update.message.chat.id, question="Когда колаб?",
                          options=["16:45", "18:30", "20:00", "21:00"],  is_anonymous=False,
                          close_date=datetime.now() + timedelta(hours=1))

    def set_colab(self, update):
        text = update.message.text


huhu = Huhu()
#######################################################


@test_time_start
def text(update, _) -> None:
    """get and processing text in TG bot"""
    new_message = update.message.text
    chat = update.message.chat
    user = update.message.from_user
    append_data_in_file.add("res/db/default/messages.txt", update.message)

    if chat.id in config['ban_users']:
        return None

    if (result := check_messages.check_messages_on_banned_content(update)) is not None:
        print(update.message.text)
        update.message.delete()
        update.message.reply_text(result)
        return None

    admin_send_message_in_virtual_chat_user(update)
    huhu.checking(update)

    try:
        check_type_chat = chat.type == 'private'
        check_on_admin = user.id in config['moderators']
        if check_type_chat is True and check_on_admin is False:
            list_users.append(chat.id)
            username = chat.username
            chat_id = chat.id
            reply_markup = create_button("💌Начать чат💌", f"reply_user_active:{chat_id}")

            if str(chat_id) in storage_command['data_messages_other_user']:
                try:
                    position_other_id = storage_command['data_messages_other_user'].index(str(chat_id))
                    id_admin_user = storage_command['data_messages_admin_user'][position_other_id]
                    #тут можно разместить команди для конкретного пользователя
                    bot.send_message(int(id_admin_user), f"[@{username}]\n{new_message}")
                except ValueError:
                    print(f"снова возникла ошипка -> ValueError: {chat_id} is not in list")
            else:
                send_all_admin_message(f"[@{username}|{chat_id}]\n{new_message}", reply_markup)

    except AttributeError as e:
        print("Error function `text(update, _)` in `default/default.py`\n", e)
        print(update)


##########################################################
#                   specefic command                     #
##########################################################


def get_username_by_user_id(user_id: int) -> str:
    """get telegram username by user id"""
    chat = bot.get_chat(user_id)
    return chat.username


def get_chat(update, _):
    #сделать включение и отключение етой команди с помощью похожей
    """get meta-data message chats"""
    print(update.message.chat.id)
    print(update)
