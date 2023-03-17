
class Command(object):
    def __init__(self):
        self.call_name = "test"
        self.description = "test command"

    @staticmethod
    def call_command(update, context):
        update.message.reply_text("test test test")


command = Command()
