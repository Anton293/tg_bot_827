"""users commands default"""
import sqlite3
import json
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from root.default import admin_command, read_file

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="res/db/.env")

from root.data_users import data
storage_command = data.data_commands['default']

bot = Bot(token=os.getenv('TOKEN'))
admins_list = [983486538, 5741678605]


####################################################################
#                           moderate users                         #
####################################################################


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


def send_all_admin_message(msg: str, button="") -> None:
    """send all admins message"""
    for admin_id in admins_list:
        bot.send_message(admin_id, msg, reply_markup=button)


def start(update, _):
    """command TG bot: /start """
    get_data = update.message
    if add_record_to_database(get_data.chat.id, get_data.chat.username, get_data.from_user.first_name, "res/db/default/records.db") is False:
        result_text = f"👋[@{get_data.chat.username}|{get_data.chat.id}] New user {get_data.from_user.first_name}!"
        send_all_admin_message(result_text)
        update.message.reply_text(f"""
            Привет, тут регистация в TikTok House! Мы будем рады увидеть тебя в нашей группе, чтобы поделиться нашими общими интересами и хобби.
            Наша группа - это место, где можно обмениваться мнениями, идеями и мыслями друг о друге. Но снаначала раскажите немного осебе!""")
        update.message.reply_text("Напиши через кому: Имя, страна, день рождения(день/месяц), количество лет")
    else:
        update.message.reply_text("Я тебе уже отправил соощение, теперь ти если ещо ненаписал(а)")


list_users = []


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


def append_to_array_messages(file_name: str, new_element: dict) -> None:
    """add to array messages in file"""
    # Загрузить массив из файла
    with open(file_name, 'r') as f:
        data = json.load(f)

    # Добавить элемент в массив
    data.append(new_element)

    # Сохранить обновленный массив в файл
    with open(file_name, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def admin_send_message_in_virtual_chat_user(update):
    try:
        position_admin_id = storage_command['data_messages_admin_user'].index(update.message.chat.id)
        id_other_user = storage_command['data_messages_other_user'][position_admin_id]
        bot.send_message(id_other_user, update.message.text)
        print(f"bot send message -> {id_other_user} -> {update.message.text}")
    except (ValueError, AttributeError):
        pass


def create_button(button_name, button_data):
    button_reply = [
        [InlineKeyboardButton(button_name, callback_data=button_data)]
    ]
    reply_markup = InlineKeyboardMarkup(button_reply)
    return reply_markup

#######################################################


def text(update, _):
    """get and processing text in TG bot"""
    #print(f"[text]боту написал {update.message.chat.username} -> {update.message.text}")
    append_to_array_messages("res/db/default/messages.json", {"message": str(update.message)})
    admin_send_message_in_virtual_chat_user(update)

    try:
        if update.message.chat.type == 'private' and update.message.chat.id not in admins_list:
            list_users.append(update.message.chat.id)
            username = update.message.chat.username
            chat_id = update.message.chat.id
            msg = update.message.text
            reply_markup = create_button("💌Почати чат💌", f"reply_user_active:{chat_id}")

            if str(chat_id) in storage_command['data_messages_other_user']:
                try:
                    position_other_id = storage_command['data_messages_other_user'].index(chat_id)
                    id_admin_user = storage_command['data_messages_admin_user'][position_other_id]
                    #тут можно разместить команди для конкретного пользователя
                    bot.send_message(int(id_admin_user), f"[@{username}]\n{msg}")
                except ValueError:
                    print(f"снова возникла ошипка -> ValueError: {chat_id} is not in list")
            else:
                bot.send_message(983486538, f"[@{username}|{chat_id}]\n{msg}", reply_markup=reply_markup)
                bot.send_message(5741678605, f"[@{username}|{chat_id}]\n{msg}", reply_markup=reply_markup)

        if update.message.chat.id in [-1001605339520, 983486538]:
            check_message(update)
    except AttributeError as e:
        print("Error function `text(update, _)` in `default/default.py`\n", e)


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


@admin_command
def stoped_all_chat_moderators(update, _):
    """stop all chat and send message"""
    storage_command['data_messages_admin_user'] = []
    storage_command['data_messages_other_user'] = []
    update.message.reply_text("chats by stoped in admins")
##########################################


def get_username_by_user_id(user_id: int) -> str:
    """get telegram username by user id"""
    chat = bot.get_chat(user_id)
    return chat.username


def get_chat(update, _):
    """get meta-data message chats"""
    print(update.message.chat.id)
    print(update)
