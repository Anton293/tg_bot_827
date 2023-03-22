"""/start"""
import sqlite3
from root.default import admin_command, read_file, test_time_start, AppendToFileDAta, send_all_admin_message, config


def add_record_to_database(user_id, username, first_name, database):
    # Подключаемся к базе данных
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Проверяем, есть ли уже запись с таким ID в базе данных
    c.execute("SELECT COUNT(*) FROM records WHERE id=?", (user_id,))
    count = c.fetchone()[0]
    if count > 0:
        conn.close()
        return True

    # Если записи с таким ID еще нет, то добавляем новую запись в базу данных
    c.execute("INSERT INTO records (id, username, first_name) VALUES (?, ?, ?)", (user_id, username, first_name))
    conn.commit()
    conn.close()
    return False


@test_time_start
class Command(object):
    call_name = "start"
    description = "start command"

    def __init__(self):
        self.array_print_command = []

    def call_command(self, update, context):
        """command TG bot: /start """
        chat_data = update.message.chat
        user_data = update.message.from_user
        if add_record_to_database(chat_data.id, user_data.username, user_data.first_name, "res/db/default/records.db") is False:
            result_text = f"👋[@{user_data.username}|{chat_data.id}] New user {user_data.first_name}!"
            send_all_admin_message(result_text)

        for send_text in config['commands']['start']['texts']:
            update.message.reply_text(send_text)


command = Command()
