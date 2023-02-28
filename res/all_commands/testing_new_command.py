from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll, Bot
from telegram.ext import Updater

# Создание бота
updater = Updater(token="5652605903:AAHDahj8anS6YLrVpgF3LN2cJFiqdINfMf0")

# Получение объекта чата группы по ID
chat_id = -1603853876
chat_obj = updater.bot.get_chat(chat_id)
print(chat_obj)

# Создание кнопок для опроса
buttons = [
    [InlineKeyboardButton("Чорний 1", callback_data="option1"),
     InlineKeyboardButton("Чорний 2", callback_data="option2")],
    [InlineKeyboardButton("Много  3", callback_data="option3")]
]
reply_markup = InlineKeyboardMarkup(buttons)

# Создание объекта опроса
question = "Какой ваш любимый цвет?"
options = ["серий", "красний", "просто тестирую бота"]
allows_multiple_answers = True
poll = chat_obj.send_poll(question=question, options=options, allows_multiple_answers=allows_multiple_answers, reply_markup=reply_markup)

# Печать ссылки на опрос для удобства пользователей
poll_link = f"https://t.me/{updater.bot.username}?start={poll.id}"
print(f"Ссылка на опрос: {poll_link}")
