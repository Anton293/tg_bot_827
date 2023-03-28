"""default module to bot"""
import functools
import time
from datetime import datetime, timedelta, time as d_time
from root.data_users import config

import os
from telegram import Bot
bot = Bot(token=os.getenv('TOKEN'))


def admin_command(command):
    """Decorator that checks if the user is an admin and executes the command if they are."""

    @functools.wraps(command)
    def wrapper(update, context, *args, **kwargs):
        """Wrapper function that checks if the user is an admin and executes the command if they are."""
        if update.message.from_user.id in config.global_configuration_server['moderators']:
            return command(update, context, *args, **kwargs)
        else:
            print("[info]Кто-то попитался использовать команду предназначеную для админа")
            print(update.message.from_user.id)
            return None

    return wrapper


def check_on_ban_users(command):
    """Decorator that ban users"""

    @functools.wraps(command)
    def wrapper(update, context, *args, **kwargs):
        """Wrapper function that checks if the user is an admin and executes the command if they are."""
        if update.message.from_user.id not in config.global_configuration_server['ban_users']:
            return command(update, context, *args, **kwargs)
        else:
            print(f"[info]Заблокирований пользователь написал: {update.message.text}")
            return None

    return wrapper


def read_file(file_path: str):
    """Read the file from the given file path and return its contents as a list of strings."""
    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file at path: {file_path}")
    except ValueError:
        raise ValueError(f"File error reading in path: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file: {e}")


def user_throttle(seconds=5):
    def decorator(func):
        last_called = {}

        def wrapper(update, context, *args, **kwargs):
            user_id = update.effective_user.id
            elapsed = time.monotonic() - last_called.get(user_id, 0)
            left_to_wait = seconds - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            last_called[user_id] = time.monotonic()
            return func(update, context, *args, **kwargs)
        return wrapper
    return decorator


def throttle_all_server(seconds=5):
    def decorator(func):
        last_called = [0.0]

        def wrapper(*args, **kwargs):
            elapsed = time.monotonic() - last_called[0]
            left_to_wait = seconds - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            last_called[0] = time.monotonic()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def test_time_start(func):
    def yellow(text):
        return "\033[33m" + text + "\033[0m"

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(yellow(f"[info]Function ʼ{func.__name__}ʼ took {(end-start):.8f} seconds to run."))
        return result
    return wrapper


class AppendToFileDAta(object):
    def __init__(self, point_save=10):
        self.point_save = int(point_save)
        self.count = 0
        self.array_messages = []

    def add(self, file_name: str, message) -> None:
        """add to array messages in file"""
        # Сохранить обновленный массив в файл
        self.count += 1
        try:
            self.array_messages.append(f"{message.from_user.id}::{message.chat.id}::{message.text}".replace("\n", " "))
        except AttributeError:
            pass

        if self.count >= self.point_save:
            with open(file_name, 'a') as f:
                f.write("\n".join(self.array_messages) + "\n")

            self.count = 0
            self.array_messages = []


def send_all_admin_message(msg: str, button=None) -> None:
    """send all admins message"""
    if button is not None:
        for i, admin_id in enumerate(config['moderators'].copy()):
            try:
                bot.send_message(admin_id, msg, reply_markup=button)
            except:
                print(f"Chat not found: {admin_id}")
                config['moderators'].remove(admin_id)
    else:
        for i, admin_id in enumerate(config['moderators'].copy()):
            try:
                bot.send_message(int(admin_id), msg)
            except:
                print(f"Chat not found: {admin_id}")
                config['moderators'].remove(admin_id)


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


config = config.global_configuration_server
