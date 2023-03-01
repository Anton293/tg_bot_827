"""users commands default"""
import sqlite3
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from root.default import admin_command, read_file

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="res/db/.env")

from root.data_users import data
storage_command = data.data_commands['default']

bot = Bot(token=os.getenv('TOKEN'))
admins_list = [983486538, 5741678605]


@admin_command
def help(update, _):
    update.message.reply_text(f"Команда help пустая;)")


def error(update, context):
    print(f"Update {update} ///// cause error: {context.error}")


def add_record_to_database(id, username, first_name, database):
    # Подключаемся к базе данных
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Проверяем, есть ли уже запись с таким ID в базе данных
    c.execute("SELECT COUNT(*) FROM records WHERE id=?", (id,))
    count = c.fetchone()[0]
    if count > 0:
        conn.close()
        return True

    # Если записи с таким ID еще нет, то добавляем новую запись в базу данных
    c.execute("INSERT INTO records (id, username, first_name) VALUES (?, ?, ?)", (id, username, first_name))
    conn.commit()
    conn.close()
    return False


def start(update, _):
    """command TG bot: /start """
    get_data = update.message
    if add_record_to_database(get_data.chat.id, get_data.chat.username, get_data.from_user.first_name, "res/db/default/records.db") is False:
        result_text = f"[@{get_data.chat.username}|{get_data.chat.id}] New user {get_data.from_user.first_name}!"
        bot.send_message(983486538, result_text)
        bot.send_message(5741678605, result_text)
        update.message.reply_text(f"""
            Привет, тут регистация в TikTok House! Мы будем рады увидеть тебя в нашей группе, чтобы поделиться нашими общими интересами и хобби.
            Наша группа - это место, где можно обмениваться мнениями, идеями и мыслями друг о друге. Но снаначала раскажите немного осебе!""")
    else:
        update.message.reply_text("Я тебе уже отправил соощение, теперь ти если ещо ненаписал(а)")


list_users = []


@admin_command
def get_list_chat_users(update, _):
    """print last chat member id"""
    if update.message.chat.type == 'private':
        update.message.reply_text("\n".join(list_users))


def check_message(update):
    """filter message on bad word"""
    BAD_WORDS = read_file("res/db/default/bad_word.txt")
    # Получаем текст сообщения
    message_text = update.message.text

    # Проверяем наличие запрещенных слов в сообщении
    for word in BAD_WORDS:
        if word in message_text:
            # Если найдено запрещенное слово, удаляем сообщение
            update.message.delete()
            print(update)
            # Отправляем уведомление об удалении сообщения
            update.bot.send_message(-1001605339520, 'Сообщение было удалено, так как содержит запрещенное слово.')


def text(update, _):
    """send text in TG bot"""
    try:
        position_admin_id = storage_command['data_messages_admin_user'].index(update.message.chat.id)
        id_other_user = storage_command['data_messages_other_user'][position_admin_id]
        bot.send_message(id_other_user, update.message.text)
        print(f"ок {id_other_user}")
    except ValueError:
        pass

    try:
        if update.message.chat.type == 'private' and update.message.chat.id not in admins_list:
            list_users.append(update.message.chat.id)
            username = update.message.chat.username
            chat_id = update.message.chat.id
            msg = update.message.text

            button_reply = [
                [InlineKeyboardButton("Ответить на сообщение", callback_data=f"reply_user_active:{chat_id}")]]
            reply_markup = InlineKeyboardMarkup(button_reply)

            if str(chat_id) in storage_command['data_messages_other_user']:
                #тут можно разместить команди для конкретного пользователя
                bot.send_message(983486538, f"[@{username}|{chat_id}]\n{msg}")
                bot.send_message(5741678605, f"[@{username}|{chat_id}]\n{msg}")
            else:
                bot.send_message(983486538, f"[@{username}|{chat_id}]\n{msg}", reply_markup=reply_markup)
                bot.send_message(5741678605, f"[@{username}|{chat_id}]\n{msg}", reply_markup=reply_markup)

        if update.message.chat.id in [-1001605339520, 983486538]:
            check_message(update)
    except AttributeError as e:
        print("Error function `text(update, _)` in `default/default.py`\n")


@admin_command
def reply_user(update, _):
    """reply user on message used id"""
    if update.message.chat.type == 'private' and update.message.chat.id in admins_list:
        try:
            res = update.message.text.split()
            bot.send_message(int(res[1]), " ".join(res[2:]))
        except IndexError:
            update.message.reply_text("Используйте: /reply_user <user_id> <message>")
        except:
            print(f"Возникла непредвиденная ошибка в функции reply_user() в default.py")


##########################################


def get_username_by_user_id(user_id: int) -> str:
    """get telegram username by user id"""
    chat = bot.get_chat(user_id)
    return chat.username


def get_chat(update, _):
    """get meta-data message chats"""
    print(update.message.chat.id)
    print(update)
    chat_id = -1001605339520
    user_id = 5510301889
