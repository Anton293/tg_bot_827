import sqlite3
import json


def green(text):
    return "\033[32m" + text + "\033[0m"

def red(text):
    return "\033[31m" + text + "\033[0m"

def yellow(text):
    return "\033[33m" + text + "\033[0m"


def find_keys_with_path(json_obj, path):
    keys = []
    for key, value in json_obj.items():
        if path in key:
            keys.append((key, value))
        if isinstance(value, dict):
            keys.extend(find_keys_with_path(value, path))
    return keys


def create_table(src):
    conn = sqlite3.connect(src)
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


# ищем все ключи, содержащие "path" в названии
json_data = json.loads(open("res/config.json", "r").read())
keys = find_keys_with_path(json_data, "file_path")

# выводим значение найденных ключей
for key, value in keys:
    if ".json" in value:
        try:
            json.loads(open(value, "r").read())
            print(green(f"File found -> {value}"))
        except (ValueError, IOError):
            print(red(f"File not found -> {value}"))
            open(value, "w").write("[]")

    elif ".txt" in value:
        try:
            open(value, "r").read()
            print(green(f"File found -> {value}"))
        except (ValueError, IOError):
            print(red(f"File not found -> {value}"))
            if data_file := input(yellow(f"Enter data in file -> {value}:\n")):
                open(value, "w").write(data_file)
            else:
                print(red(f"[WARNING] File not created ->->-> {value}"))

    elif ".db" in value:
        try:
            open(value, "r").read()
            print(green(f"File found -> {value}"))
        except (ValueError, IOError):
            print(red(f"[WARNING] File `sqlLite` not found -> {value}"))
            if "y" in input("Would you like to create a file?(yes/no)\n>\n").lower():
                print(yellow("Attempt to create a database, be sure to test its functionality."))
                create_table(value)
            else:
                print(red("[WARNING] passed..."))

    elif ".xlsx" in value:
        try:
            open(value, "r").read()
            print(green(f"File found -> {value}"))
        except (ValueError, IOError):
            print(red(f"[WARNING] File `xlsx` not found -> {value}"))
