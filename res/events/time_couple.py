import time
import os
import sys

sys.path.insert(0, "res/root")
from data_users import data


data.TODAY = int(time.strftime("%w", time.localtime()))-1
arr_starting_events_in_chat = []
if data.TODAY == 5 or data.TODAY == -1:
    data.TODAY = 0

#################################


class Antispam(object):
    def __init__(self):
        self.count_call_function = [i for i in range(15)]
        self.arr_check_start_function_one = []

    def check_one_start(self, id_user: int) -> bool:
        self.arr_check_start_function_one.append(id_user)
        self.count_call_function[self.arr_check_start_function_one.index(id_user)] += 1
        if self.count_call_function[self.arr_check_start_function_one.index(id_user)] > 3:
            return False
        return True


#######################################




def time_read(update):
    id_chat = update.message.chat.id
    id_user = eval(str(update.message))['from']['id']
    if id_chat in arr_starting_events_in_chat and (id_user in data.users['TABLE_USERS'] or os.getenv("ADMIN_ID") == str(id_user)):
        update.message.reply_text("События уже запущены!")
        return
    if id_user in data.users['TABLE_USERS'] or os.getenv("ADMIN_ID") == str(id_user):
        arr_starting_events_in_chat.append(id_chat)
        print(f"[{id_chat}] start events")
        sleep_time = 5
        while True:
            time.sleep(sleep_time)
            local_time_str = time.strftime("%X", time.localtime()).split(":")
            sleep_time = 29
            for i in range(3):
                time_event_str = data.settings['user_settings'][data.user_id_special]['time'][i].split("=>")[0].split(":")
                if time_event_str[0] == local_time_str[0] and int(time_event_str[1]) == int(local_time_str[1])-5:
                    sleep_time = 60*60
                    if True:
                        update.message.reply_text(f'[{":".join(local_time_str)}] Увага, через 5хв буде пара!')
                        time.sleep(60*5)
                        update.message.reply_text(f'[{":".join(local_time_str)}] Увага, почалася пара!')
                        callbackquerybutton.details(update)
                    break
                elif int(local_time_str[0]) >= 14:
                    sleep_time = 24-(int(local_time_str[0])-6)
                    break
                elif int(local_time_str[0]) <= 7:
                    sleep_time = 60*29
                    break
