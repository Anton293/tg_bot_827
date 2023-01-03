import json


dr = "res/bd/"


def read_file(src):
    with open(src, "r", encoding="UTF-8") as f:
        return json.loads(f.read())



def write_file(src, data_in_json) -> None:
    try:
        write_in_file = open(src, "w", encoding="UTF-8")
        json.dump(data_in_json, write_in_file, indent=2)
        write_in_file.close()
    except IOError:
        print(f"[error] Неудалося создать/записать файл: {src}")
    finally:
        pass





class Databasebot():
    def __init__(self):
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
        self.arr_days_week = ['Понеділок', "Вівторок", "Середа", "Четверг", "Пятниця"]
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

    def read_this_file(self, name_file):
        try:
            if name_file == "users":
                self.users = read_file(dr+"users.json")
            elif name_file == "settings":
                self.settings = read_file(dr+"settings.json")
        except IOError:
            print("error reading files!")

    def write_this_file(self, name_file):
        if name_file == "users":
            write_file(dr+"users.json", self.users)
        elif name_file == "settings":
            write_file(dr+"settings.json", self.settings)


data = Databasebot()

