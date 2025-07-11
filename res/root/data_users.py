import json
import os

HEAD_CONFIG_PATH = "res/config.json"
HEAD_DIR_COMMANDS = "res/db/"


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file at path: {file_path}")
    except ValueError:
        raise ValueError(f"File error json: {file_path}")
    except IOError as e:
        raise IOError(f"Error file: {e}")


def write_json_in_file(data_in_json: dict, src: str) -> None:
    try:
        with open(src, "w", encoding="UTF-8") as f:
            json.dump(data_in_json, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"[error] Не удалось создать/записать файл: {src}. {e}")


def get_list_dir(path):
    res_list = []
    for d in os.listdir(path):
        if os.path.isdir(os.path.join(path, d)):
            res_list.append(d)
    return res_list


#print(get_list_dir("res/bd"))


class DatabaseBot(object):
    def __init__(self):
        self.data_commands = {}
        self.NAME = "HAI_BOT_518"
        self.DATABASE = []
        self.TODAY = 1
        self.couple = 1
        self.edition_couple = -1
        self.active_last_user = 5164147339
        self.user_id_special = 0
        self.user_id_special_group = []
        self.arr_files_src = ["database.json", "bd.json", "settings.json"]
        self.arr_var_in_self = ["DATABASE", "users", "settings"]
        self.arr_days_week = ['Понеділок', "Вівторок", "Середа", "Четверг", "П'ятниця"]
        self.arr_time_couple = ['08:00=>9:00', '09:00=>10:00', '10:00=>9:00', '11:00=>13:00']
        self.my_msg = ""
        self.users = {
            "TABLE_USERS_ID": [],
            "TABLE_CHANNELS_ID": [],
            "TABLE_ADMINS_ID": []
        }
        self.settings = {
            "send_my_message_new_users": True,
            "send_message_group_me_chat_bot": False,
            "user_settings": [{
                "time": ["08:00=>09:35", "09:50=>11:25", "11:55=>13:30", "14:45=>15:20"],
            }]
        }

    def initialization(self):
        path = HEAD_DIR_COMMANDS
        for command_dir in os.listdir(path):
            if os.path.isdir(os.path.join(path, command_dir)):
                self.data_commands[command_dir] = read_file(path+command_dir+"/data.json")


class Config(object):
    def __init__(self):
        self.global_configuration_server = {}

    def initialization(self):
        self.global_configuration_server = read_file(HEAD_CONFIG_PATH)


data = DatabaseBot()
data.initialization()

config = Config()
config.initialization()
