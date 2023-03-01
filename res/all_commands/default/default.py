"""users commands default"""
from telegram import Bot
from root.default import admin_command, read_file
bot = Bot(token="5652605903:AAHDahj8anS6YLrVpgF3LN2cJFiqdINfMf0")


admins_list = [983486538, 5741678605]


@admin_command
def help(update, _):
    update.message.reply_text(f"команди нет")


def error(update, context):
    print(f"Update {update} ///// cause error: {context.error}")


def start(update, _):
    bot.send_message(983486538, f"[{update.message.chat.username}|{update.message.chat.id}]\n New user {update.message}!")
    bot.send_message(5741678605, f"[{update.message.chat.username}|{update.message.chat.id}]\n New user {update.message}!")
    update.message.reply_text(f"""
    Привет, тут регистация в TikTok House! Мы будем рады увидеть тебя в нашей группе, чтобы поделиться нашими общими интересами и хобби. Наша группа - это место, где можно обмениваться мнениями, идеями и мыслями друг о друге. Но снаначала раскажите немного осебе!
""")


list_users = []


@admin_command
def get_list_chat_users(update, _):
    if update.message.chat.type == 'private':
        update.message.reply_text("\n".join(list_users))


def check_message(update):
    BAD_WORDS = read_file("res/bd/default/bad_word.txt")
    # Получаем текст сообщения
    message_text = update.message.text

    # Проверяем наличие запрещенных слов в сообщении
    for word in BAD_WORDS:
        if word in message_text:
            # Если найдено запрещенное слово, удаляем сообщение
            update.message.delete()
            # Отправляем уведомление об удалении сообщения
            update.bot.send_message(-1001605339520, 'Сообщение было удалено, так как содержит запрещенное слово.')


def text(update, _):
    try:
        if update.message.chat.type == 'private' and update.message.chat.id not in admins_list:
            list_users.append(update.message.chat.id)
            bot.send_message(983486538, f"[{update.message.chat.username}|{update.message.chat.id}]\n{update.message.text}")
            bot.send_message(5741678605, f"[{update.message.chat.username}|{update.message.chat.id}]\n{update.message.text}")

        if update.message.chat.id == -1001605339520 or update.message.chat.id == 983486538:
            check_message(update)
    except AttributeError as e:
        print("Возникла ошибка text(update, _) \n")


@admin_command
def reply_user(update, _):
    if update.message.chat.type == 'private' and update.message.chat.id in admins_list:
        try:
            res = update.message.text.split()
            bot.send_message(int(res[1]), " ".join(res[2:]))
        except IndexError:
            update.message.reply_text("Используйте: /reply_user <user_id> <message>")
        except:
            print(f"Возникла непредвиденная ошибка в функции reply_user() в default.py")


def get_chat(update, _):
    print(update.message.chat.id)
    print(update)
    chat_id = -1001605339520
    user_id = 5510301889
