import telegram
import os
import datetime
from threading import Thread
import time
import functools

# Создаем объект бота с помощью токена
bot = telegram.Bot(token=os.getenv('TOKEN'))
# Выводим информацию о каждом обновлении
#updates = bot.get_updates()
message = bot.send_message(text="text", chat_id=983486538)
print(message)
print(message.message_id)


def count_seconds_to_next_day(hh, mm, ss):
    today = datetime.datetime.today()
    today_time = today.replace(hour=hh, minute=mm, second=ss, microsecond=0)
    delta_time = today_time - today
    if delta_time.total_seconds() < 0:
        # Если заданное время уже прошло в текущем дне, добавляем один день
        today_time += datetime.timedelta(days=1)
        delta_time = today_time - today
    return delta_time.total_seconds()


def search_event(array_times, during=1):
    def decorator_search_event(function):
        @functools.wraps(function)
        def wrapper_search_event(*args, **kwargs):
            while True:
                arr = [count_seconds_to_next_day(i[0], i[1], 0) for i in array_times]
                seconds_to_event = min(arr)
                event_id = arr.index(seconds_to_event)
                time.sleep(count_seconds_to_next_day(array_times[event_id][0], array_times[event_id][1], 0) - during)
                function(event_id, *args, **kwargs)
                break
        return wrapper_search_event
    return decorator_search_event


@search_event([[8, 0], [9, 35], [10, 0], [11, 25], [14, 0], [21, 0]], during=5)
def send_message_me(events_id):
    array_items = ["L-тироксин (1 таблетка)", "Сніданок", "Хофітол", "Вітаміни та обід", "Хофітол", "Хофітол"]
    text = f"Увага, зараз: {array_items[events_id]}"
    chat_id = 983486538
    message_data = bot.send_message(text=text, chat_id=chat_id)
    bot.delete_message(chat_id=chat_id, message_id=message_data.message_id - 1)


@search_event([[8, 0], [11, 0], [13, 0], [17, 0], [20, 0]], during=60*5)
def send_message_mather(events_id):
    array_items = ["Сніданок", "Перекус", "Обід", "Другий перекус", "Вечеря"]
    text = f"За 5 хвилин: {array_items[events_id]}"
    chat_id = 5762049455
    message_data = bot.send_message(text=text, chat_id=chat_id)
    bot.delete_message(chat_id=chat_id, message_id=message_data.message_id-1)


Thread(target=send_message_me).start()
Thread(target=send_message_mather).start()
