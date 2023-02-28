import time
import os
import sys
import datetime

#sys.path.insert(0, "/")
from root.data_users import data


data.TODAY = int(time.strftime("%w", time.localtime()))-1
week_number = datetime.datetime.today().isocalendar()[1]
if data.TODAY == 5 or data.TODAY == -1:
    data.TODAY = 0


arr_starting_events_in_chat = set()


def count_seconds_to_next_day(hh, mm, ss):
    today_time = datetime.datetime.today()
    next_day = datetime.datetime(2023, 1, 1, hh, mm, ss)
    delta_time = next_day - today_time
    return delta_time.seconds


def warning_of_couple(update, time_begin_couples):
    """function send data and time of couple"""
    while True:
        for i, couple in enumerate(time_begin_couples):
            time.sleep(2)
            couple_time = list(map(lambda arr: list(map(int, arr.split(":"))), couple.split("=>")))
            def count_to_time_this_couple(): return count_seconds_to_next_day(couple_time[0][0], couple_time[0][1], 0)

            print(f"До {i+1}-й пари залишилось -> {(count_to_time_this_couple()/60)} хвилин.")
            if 3600 > count_to_time_this_couple() > 0:#скільки залишилось до пари щоб поставить таймер(налаштування, для ініціалізації)
                update.message.reply_text(f"To next couple [{count_to_time_this_couple()/60} mm] Initialisation success!")
                time.sleep(int(count_to_time_this_couple()))

            if 60 > count_to_time_this_couple() > -60:
                update.message.reply_text(f"[{couple_time[0][0]}:{couple_time[0][1]}] Бот работает в тестовом режиме, сейчас по таблице пара (№{i+1})! Неделя({week_number})")

            if len(time_begin_couples) < i+2:
                print("sleep to next day!")
                time.sleep(int(count_seconds_to_next_day(8, 0, 0)))


def check_before_start_function_warning_of_couple(update):
    """check user"""
    id_chat = update.message.chat.id
    id_user = eval(str(update.message))['from']['id']

    if id_chat in arr_starting_events_in_chat:
        update.message.reply_text("События уже запущены!")

    elif len(arr_starting_events_in_chat) > 100:#не обязательно!
        update.message.reply_text("Ой... Уже запущено слишком много собитий.")

    elif os.getenv("ADMIN_ID") == str(id_user) or False:#-не только админ
        arr_starting_events_in_chat.add(id_chat)
        warning_of_couple(update, data.arr_time_couple)
