"""default module to bot"""
import functools
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
