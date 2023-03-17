import time
import datetime
import itertools


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


def has_latin_chars(text):
    for char in text:
        if 0x0041 <= ord(char) <= 0x005A:
            return True
    return False


set_bad_words = open("res/db/default/bad_word.txt", "r").read().split("\n")


@test
def check_message_on_bad_words(message_text: str) -> bool:
    """search bad words in message"""
    message_lower_word = message_text.lower()
    if any([1024 >= ord(char) <= 1111 for char in message_lower_word]):
        print("yes")
        message_lower_word = ''.join(dict_replace_letters.get(c, c) for c in message_lower_word)

    print(message_lower_word)
    for banned_word in set_bad_words:
        if banned_word in message_lower_word:
            return True
    return False


text = "прbвіт друже, не міг би ти підти звідси naxyй"
for i in range(5000):
    if "spam" in ["spam", "smiles", "caps", "adverting", "bad_words"]:
        print(True)


