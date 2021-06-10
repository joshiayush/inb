import os


def get_javascript(file_path: str = '') -> str:
    """Function get_javascript() returns the javascript of a given file.

    :Args:
        - file_path: {str} file's path absolute/relative.

    :Returns:
        - {str} javascript code.

    :Usage:
        - _javascript = get_javascript(./index.js)
    """
    with open(file_path, "r") as _js:
        return _js.read()
