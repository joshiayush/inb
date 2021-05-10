__name__ = "Console"
__package__ = "Console"


class Theme(object):
    PARROT = True

    def enable_theme_parrot() -> None:
        Theme.PARROT = True

    def disable_theme_parrot() -> None:
        Theme.PARROT = False
