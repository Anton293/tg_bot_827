import time
import os
import sys
import datetime


def count_seconds_to_next_day(hh, mm, ss):
    today_time = datetime.datetime.today()
    next_day = datetime.datetime(2023, 1, 1, hh, mm, ss)
    delta_time = next_day - today_time
    return delta_time.seconds


#print((count_seconds_to_next_day(12, 25, 0))/3600)
#print(type(datetime.datetime.today().strftime("%H")))


sys.path.insert(0, "res/root")
from data_users import data


data.TODAY = int(time.strftime("%w", time.localtime()))-1
if data.TODAY == 5 or data.TODAY == -1:
    data.TODAY = 0


#################################


arr_starting_events_in_chat = set()


def check_chat(update):
    id_chat = update.message.chat.id
    id_user = eval(str(update.message))['from']['id']

    if id_chat in arr_starting_events_in_chat:
        update.message.reply_text("События уже запущены!")
        return False
    elif os.getenv("ADMIN_ID") == str(id_user):
        arr_starting_events_in_chat.add(id_chat)
        return True


def warning_of_couple(update):
    """function send data and time of couple"""
    time_begin_couples = data.arr_time_couple

    if check_chat(update) is True:
        bool_init = True
        while True:
            for i, couple in enumerate(time_begin_couples):
                time.sleep(2)
                hours = int(datetime.datetime.today().strftime("%H"))
                def func(arr): return list(map(int, arr.split(":")))
                couple_time = list(map(func, couple.split("=>")))
                def count_to_time_this_couple(): return count_seconds_to_next_day(couple_time[0][0], couple_time[0][1], 0)

                print(f"До {i+1}-й пари залишилось -> {(count_to_time_this_couple()/60)} хвилин.")
                if 3600 > count_to_time_this_couple() > 0:#скільки залишилось до пари щоб поставить таймер(налаштування, для ініціалізації)
                    update.message.reply_text(f"To next couple [{count_to_time_this_couple()/60} mm] Initialisation success!")
                    time.sleep(int(count_to_time_this_couple()))
                if 60 > count_to_time_this_couple() > -60:
                    update.message.reply_text(f"!!!====={couple_time[0]}=====!!!")
                    #краще тут організувати час ожидания до наступної пари

                if len(time_begin_couples) < i+2:#потрібно реорганізувати кінець
                    print("sleep to next day!")
                    time.sleep(int(count_seconds_to_next_day(8, 0, 0)))
