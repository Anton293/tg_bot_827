import json


def admin_command(command):
    admins_list = [983486538, 5741678605]

    def wrapper(update, context):
        if update.message.chat.id in admins_list:
            command(update, context)

    return wrapper


def read_file(src):
    with open(src, "r", encoding="UTF-8") as f:
        return f.read().split("\n")
