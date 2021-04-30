import os


def get_javascript(file_path=""):
    """Function get_javascript() returns the javascript of a file specified.

    This function takes the file path as a parameter and checks if it's a absolute path
    or relative to the project's source directory. If the file_path is found to be a
    relative path then this function converts that relative file path to absolute.

    return:
        - javascript of the file specified.
    """
    if file_path == "":
        return

    try:
        if file_path[0] == "." and file_path[1] == "/":
            file_path = os.getcwd() + "/" + file_path[2::]
        elif file_path[0] != "/":
            file_path = os.getcwd() + "/" + file_path
    except IndexError:
        return

    if not file_path.endswith(".js"):
        return

    with open(file_path, "r") as _js:
        return _js.read()
