"""default module to bot"""
import functools
import time
from root.data_users import config


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


def test(func):
    def yellow(text):
        return "\033[33m" + text + "\033[0m"

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(yellow(f"[info]Function ʼ{func.__name__}ʼ took {(end-start):.8f} seconds to run."))
        return result
    return wrapper
