"""users commands default"""
import sqlite3
import json
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, error
from root.default import admin_command, read_file

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="res/db/.env")

from root.data_users import data, config, write_json_in_file
config = config.global_configuration_server
storage_command = data.data_commands['default']

bot = Bot(token=os.getenv('TOKEN'))


####################################################################
#                           moderate users                         #
####################################################################


@admin_command
def help(update, _):
    update.message.reply_text(f"Команда help пустая;)")


def processing_error(update, context):
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


def send_all_admin_message(msg: str, button=None) -> None:
    """send all admins message"""
    if button is not None:
        for i, admin_id in enumerate(config['moderators'].copy()):
            try:
                bot.send_message(admin_id, msg, reply_markup=button)
            except:
                print(f"Chat not found: {admin_id}")
                config['moderators'].remove(admin_id)
    else:
        for i, admin_id in enumerate(config['moderators'].copy()):
            try:
                bot.send_message(int(admin_id), msg)
            except:
                print(f"Chat not found: {admin_id}")
                config['moderators'].remove(admin_id)


def start(update, _):
    """command TG bot: /start """
    get_data = update.message
    if True or add_record_to_database(get_data.chat.id, get_data.chat.username, get_data.from_user.first_name, "res/db/default/records.db") is False:
        result_text = f"👋[@{get_data.chat.username}|{get_data.chat.id}] New user {get_data.from_user.first_name}!"
        send_all_admin_message(result_text)
        update.message.reply_text(f"""
            Привет, тут регистация в TikTok House! Мы будем рады увидеть тебя в нашей группе, чтобы поделиться нашими общими интересами и хобби.
            Наша группа - это место, где можно обмениваться мнениями, идеями и мыслями друг о друге. Но снаначала раскажите немного осебе!""")
        update.message.reply_text("Напиши через кому: Имя, страна, день рождения(день/месяц), количество лет")
    else:
        update.message.reply_text("Я тебе уже отправил соощение, теперь ти если ещо ненаписал(а)")


list_users = []

BAD_WORDS_LIST = read_file("res/db/default/bad_word.txt").split("\n")
read_file_violators = json.loads(read_file("res/db/default/violators.json"))


def filter_messages(message_text: str, LIST_BANNED_WORDS: list) -> bool:
    """check banned word in message"""
    for word in LIST_BANNED_WORDS:
        if word in message_text:
            return True
    return False


def count_violators(group_id: int, user_id: int):
    for i, item in enumerate(read_file_violators):
        if item[0] == user_id:
            if item[1] >= 5:
                try:
                    bot.kick_chat_member(chat_id=group_id, user_id=user_id)
                except error.BadRequest as e:
                    print(f"User {user_id} -> {e}")
                return -1
            read_file_violators[i][1] = item[1]+1
            write_json_in_file(read_file_violators, "res/db/default/violators.json")
            return item[1]
    read_file_violators.append([user_id, 1])
    bot.send_message(group_id, read_file("res/db/default/role_group.txt"))
    write_json_in_file(read_file_violators, "res/db/default/violators.json")
    return 1


def check_message_on_bad_word(update):
    """filter message on bad word"""
    text_message = update.message.text

    if filter_messages(text_message.lower(), BAD_WORDS_LIST) is True:
        from_user = update.message.from_user
        #добавить запись нарушителя в бд и проверить сколько раз он уже нарушил + написать количество нарушений пользователя
        res = count_violators(update.message.chat.id, from_user.id)
        name_violators = from_user.username
        if name_violators:
            name_violators = from_user.first_name

        print(f"[info]Aggresion messages by user {name_violators} -> {text_message}")

        try:
            update.message.delete()
            if update.message.chat.type != "private":
                bot.send_message(update.message.chat.id, f'Нарушения {res} из 5. Сообщение от пользователя {name_violators} было удалено, так как содержит запрещенное слово или контекст.')
            else:
                bot.send_message(update.message.chat.id, f'Сообщение несет агрессию. Будьте вежливы и терпеливы.')
        except error.BadRequest as e:
            print(f"Error: {e}")
        return True
    return False


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
        print(f"admin send message -> {id_other_user} -> {update.message.text}")
    except (ValueError, AttributeError):
        pass


def create_button(button_name, button_data):
    button_reply = [
        [InlineKeyboardButton(button_name, callback_data=button_data)]
    ]
    reply_markup = InlineKeyboardMarkup(button_reply)
    return reply_markup


def result_check_bad_words(update) -> bool:
    try:
        if update.message.chat.id in config['chats_have_filters_bad_word'] or update.message.chat.type in config['chats_have_filters_bad_word']:
            return check_message_on_bad_word(update)
    except TypeError as e:
        print(f"Error type -> begin_check_bad_words(): {e}")
    return False


#######################################################


def text(update, _) -> None:
    """get and processing text in TG bot"""
    append_to_array_messages("res/db/default/messages.json", {"message": str(update.message)})
    admin_send_message_in_virtual_chat_user(update)

    if result_check_bad_words(update) is True:
        return None

    try:
        check_type_chat = update.message.chat.type == 'private'
        check_on_admin = update.message.from_user.id in config['moderators']
        if check_type_chat is True and check_on_admin is False:
            list_users.append(update.message.chat.id)
            username = update.message.chat.username
            chat_id = update.message.chat.id
            msg = update.message.text
            reply_markup = create_button("💌Почати чат💌", f"reply_user_active:{chat_id}")

            if str(chat_id) in storage_command['data_messages_other_user']:
                try:
                    position_other_id = storage_command['data_messages_other_user'].index(str(chat_id))
                    id_admin_user = storage_command['data_messages_admin_user'][position_other_id]
                    #тут можно разместить команди для конкретного пользователя
                    bot.send_message(int(id_admin_user), f"[@{username}]\n{msg}")
                except ValueError:
                    print(f"снова возникла ошипка -> ValueError: {chat_id} is not in list")
            else:
                send_all_admin_message(f"[@{username}|{chat_id}]\n{msg}", reply_markup)

    except AttributeError as e:
        print("Error function `text(update, _)` in `default/default.py`\n", e)


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


@admin_command
def stop_all_chat_moderators(update, _):
    """stop all chat and send message"""
    storage_command['data_messages_admin_user'] = []
    storage_command['data_messages_other_user'] = []
    for admin_id in storage_command['data_messages_admin_user']:
        bot.send_message(admin_id, "Всі чати були завершені, але за бажанням ви можете продовжити розмову")
    update.message.reply_text("chats by stoped in admins")


@admin_command
def get_rule_group(update, _):
    update.message.reply_text(read_file("res/db/default/role_group.txt"))


##########################################


def get_username_by_user_id(user_id: int) -> str:
    """get telegram username by user id"""
    chat = bot.get_chat(user_id)
    return chat.username


def get_chat(update, _):
    """get meta-data message chats"""
    print(update.message.chat.id)
    print(update)
