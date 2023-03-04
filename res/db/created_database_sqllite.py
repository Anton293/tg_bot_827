import sqlite3


def create_table():
    conn = sqlite3.connect('default/messages.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  message TEXT,
                  username TEXT,
                  date TEXT,
                  chat_id INTEGER)''')
    conn.commit()
    conn.close()


def insert_message(user_id, message, date_time, username, chat_id):
    """add message in database messages.db"""
    conn = sqlite3.connect('res/db/default/messages.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (user_id, message, username, date, chat_id) VALUES (?, ?, ?, ?, ?)",
              (user_id, message, username, date_time, chat_id))
    conn.commit()
    conn.close()


create_table()
