import telegram
import os
from datetime import datetime, timedelta, time as d_time

# Создаем объект бота с помощью токена
bot = telegram.Bot(token=os.getenv('TOKEN'))

# Открываем голосовой файл
#voice_file = open('path/to/voice_message.ogg', 'rb')

# Отправляем голосовое сообщение в группу
#bot.send_voice(chat_id='GROUP_CHAT_ID', voice=voice_file)


def send_poll():
    bot.send_poll(chat_id=983486538,
                  question="Когда колаб?",
                  options=[
                      "16:45",
                      "18:30",
                      "20:00",
                      "21:00"
                  ],
                  is_anonymous=False,
                  close_date=datetime.now() + timedelta(hours=1))


def count_second_to_time(hours, minutes, seconds):
    now = datetime.now()
    target_time = d_time(hours, minutes, seconds)

    # Создаем объект datetime, объединяя текущую дату и целевое время
    target_datetime = datetime.combine(now.date(), target_time)

    # Если целевое время уже прошло сегодня, добавляем один день
    if now.time() > target_time:
        target_datetime += timedelta(days=1)

    # Считаем оставшееся время в секундах
    remaining_seconds = (target_datetime - now).total_seconds()
    return remaining_seconds


count_second = count_second_to_time(13, 0, 0)
print(count_second)
