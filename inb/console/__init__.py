"""Package console provides all the functions to interact with the user using the terminal."""

__name__ = "console"
__package__ = "console"


class Theme(object):
    PARROT = True

    @staticmethod
    def enable_theme_parrot() -> None:
        Theme.PARROT = True

    @staticmethod
    def disable_theme_parrot() -> None:
        Theme.PARROT = False
