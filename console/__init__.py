__name__ = "Console"
__package__ = "Console"


class Theme(object):
    PARROT = True

    @staticmethod
    def enable_theme_parrot() -> None:
        Theme.PARROT = True

    @staticmethod
    def disable_theme_parrot() -> None:
        Theme.PARROT = False
