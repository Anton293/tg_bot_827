import json
from re import findall
import os

from telegram.error import BadRequest
from telegram import Bot

import logging
logger = logging.getLogger(__name__)

from root.data_users import config, write_json_in_file
from root.default import test_time_start

config = config.global_configuration_server
bot = Bot(token=os.getenv('TOKEN'))


@test_time_start
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


@test_time_start
class CheckMessage(object):
    def __init__(self):
        self.config = {}
        self.list_last_messages = [] #список последних сообщений для иследования
        self.list_count_message_users_private_chat = [] #защита бота от спама в приватних сообщениях

        self.list_bad_words = []
        self.list_violators = []
        self.dict_replace_letters = []
        self.array_adverting_banned_words = []

    @test_time_start
    def initialisation(self) -> None:
        """initialisation component and save file in var"""
        self.config = config['check_messages']

        self.list_bad_words = read_file(self.config['bad_words_file_path']).split("\n")
        self.list_violators = json.loads(read_file(self.config['violators_file_path']))
        self.dict_replace_letters = json.loads(read_file(self.config['replace_letters_file_path']))
        self.array_adverting_banned_words = [
            "t.me/+", "скидка", "скидки",
            "заказать", "скидочка", "заказывайте",
            "подписывайтеся", "подпишитесь", "регистрируйтесь",
            "подпишись", " вот мой ", "переходи"
        ]

    @test_time_start
    def check_message_on_adverting(self, message: str) -> bool:
        """check associate text adverting in message"""
        message_lower_word = message.lower()
        for banned_word in self.array_adverting_banned_words:
            if banned_word in message_lower_word:
                return True
        return False

    @test_time_start
    def check_message_on_bad_words(self, message_text: str) -> bool:
        """search bad words in message"""
        message_lower_text = message_text.lower()
        if any([1024 >= ord(char) <= 1111 for char in message_lower_text]):
            message_lower_text = ''.join(self.dict_replace_letters.get(c, c) for c in message_lower_text)

        for banned_word in self.list_bad_words:
            if banned_word in message_lower_text:
                return True
        return False

    @test_time_start
    def check_message_on_spam(self, user_id: int, message: str) -> bool:
        """antispam"""
        clean_message = message.strip(". <>,0- _+=?\n").lower()
        self.list_last_messages.append((user_id, clean_message))

        amount_same_messages = 0
        for old_user_id, old_message in self.list_last_messages:
            if clean_message == old_message and user_id == old_user_id:
                amount_same_messages += 1

        if len(self.list_last_messages) > self.config['max_research_last_messages']:
            del self.list_last_messages[0]

        if amount_same_messages >= self.config['max_same_messages']:
            return True
        return False

    @test_time_start
    def check_message_on_caps(self, message: str):
        clean_message = message.strip(". <>,0- _+=?\n")
        if len(clean_message) <= 3:
            return False

        number_upper_char = 0
        for char in clean_message:
            if char.isupper():
                number_upper_char += 1

        if self.config['min_number_of_capital_letters'] < number_upper_char >= int(len(clean_message) * self.config['max_uppercase_ratio']):
            return True
        return False

    @test_time_start
    def check_message_on_manu_smiles(self, message: str):
        smiles = findall("[\U00010000-\U0010ffff]", message)
        if len(smiles) >= self.config['max_manu_smiles']:
            return True
        return False

    @test_time_start
    def count_violators(self, update, group_id: int, user_id: int):
        MAX_VIOLATIONS = 5
        ROLE_GROUP_FILE_PATH = "res/db/default/role_group.txt"
        # Ищем пользователя в списке нарушителей
        for i, item in enumerate(self.list_violators):
            if item[0] == user_id:
                if item[1] >= MAX_VIOLATIONS:
                    # Если пользователь нарушил правила более MAX_VIOLATIONS раз, кикаем его из чата
                    try:
                        bot.kick_chat_member(chat_id=group_id, user_id=user_id)
                    except BadRequest as e:
                        logger.exception(f"Failed to kick user {user_id}: {e}")
                        #bot.send_message(group_id, f"Failed to kick user {user_id}: {e}")
                        return -1
                    logger.info(f"Kicked user {user_id}")
                    bot.send_message(group_id, f"User {user_id} has been kicked for violating the rules.")
                    return -1
                # Увеличиваем количество нарушений у пользователя
                self.list_violators[i][1] = item[1] + 1
                write_json_in_file(self.list_violators, self.config['violators_file_path'])
                logger.info(f"User {user_id} has {item[1]} violations")
                return item[1]

        # Если пользователя нет в списке нарушителей, добавляем его туда
        self.list_violators.append([user_id, 1])
        bot.send_message(group_id, read_file(ROLE_GROUP_FILE_PATH))
        write_json_in_file(self.list_violators, self.config['violators_file_path'])
        logger.info(f"User {user_id} has been added to the violators list")
        return 1

    @test_time_start
    def head_violators_function(self, update, chat_id: int, user_id: int):
        first_name = update.message.from_user.first_name
        try:
            number_violators = self.count_violators(update, chat_id, user_id)
            print(number_violators)
            if update.message.chat.type != "private" and number_violators != -1:
                bot.send_message(update.message.chat.id, f'Нарушения {number_violators} из 5. Сообщение от пользователя {first_name} было удалено, такое поведения непреемливое у нас.')
            else:
                return None
        except BadRequest as e:
            print(f"Error: {e}")

    @test_time_start
    def check_messages_on_banned_content(self, update):
        try:
            text_messages = update.message.text
            user_id = update.message.from_user.id
            chat_id = update.message.chat.id
            chat_type = update.message.chat.type
        except AttributeError as e:
            print(f"Attribute error: {e}")
            return None
        get_chat_rule = {}
        for chat_rule in self.config['chats']:
            if chat_rule['chat_id'] == chat_id:
                get_chat_rule = chat_rule.copy()
                break
            elif chat_rule['chat_id'] == chat_type:
                get_chat_rule = chat_rule.copy()
                break

        if get_chat_rule == {}:
            return None
        elif user_id in config['moderators'] and get_chat_rule['immunity_of_moderators']:
            return None
        elif user_id in config['super_admin']:
            return None

        if "spam" in get_chat_rule["check_list"]:
            if self.check_message_on_spam(user_id, text_messages) is True:
                self.head_violators_function(update, chat_id, user_id)
                return f"Не спамте пожалуйста"

        if "smiles" in get_chat_rule['check_list']:
            if self.check_message_on_manu_smiles(text_messages) is True:
                return f"Слишком много емодзи"

        if "smiles" in get_chat_rule['check_list']:
            if self.check_message_on_adverting(text_messages) is True:
                self.head_violators_function(update, chat_id, user_id)
                return f"Реклама запрещена"

        if "caps" in get_chat_rule['check_list']:
            if self.check_message_on_caps(text_messages) is True:
                return "Слишком много капса в сообщении"

        if "bad_words" in get_chat_rule['check_list']:
            if self.check_message_on_bad_words(text_messages) is True:
                self.head_violators_function(update, chat_id, user_id)
                return f"Сообщение несет агрессию. Будьте вежливы и терпеливы."


check_messages = CheckMessage()
check_messages.initialisation()
