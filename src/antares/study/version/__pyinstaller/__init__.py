import os


def get_hook_dirs():
    """
    Retrieve the directory path where pyinstaller will look for hooks.

    Returns:
        list: A list with the directory path of the hooks.
    """

    return [os.path.dirname(__file__)]
