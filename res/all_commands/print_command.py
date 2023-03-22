"""exemples"""
from root.default import user_throttle


class Command(object):
    def __init__(self):
        self.call_name = "test"
        self.description = "test command"

    @staticmethod
    @user_throttle(seconds=5)
    def call_command(update, context):
        context.bot.send_message(update.message.chat.id, "text")
        update.message.reply_text("test test test")


command = Command()
