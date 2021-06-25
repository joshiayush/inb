__name__ = "messages"
__package__ = "messages"


class ConsoleMessages(object):
    ENABLED = True

    @staticmethod
    def enable_console_message() -> None:
        ConsoleMessages.ENABLED = True

    @staticmethod
    def disable_console_message() -> None:
        ConsoleMessages.ENABLED = False
