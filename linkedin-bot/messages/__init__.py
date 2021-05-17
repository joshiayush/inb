__name__ = "Messages"
__package__ = "Messages"


class ConsoleMessages(object):
    ENABLED = True

    @staticmethod
    def enable_console_message() -> None:
        ConsoleMessages.ENABLED = True

    @staticmethod
    def disable_console_message() -> None:
        ConsoleMessages.ENABLED = False
