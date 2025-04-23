import os


def get_hook_dirs():
    """
    Retrieve the directory path where pyinstaller will look for hooks.

    Returns:
        list: A list with the directory path of the hooks.
    """

    return [os.path.dirname(__file__)]


def get_PyInstaller_tests():
    """
    Retrieve the directory path where pyinstaller will look for test hooks.

    These paths are then passed to pytest for test discovery. This allows both
    testing by this package and by PyInstaller.

    Returns:
        list: A list with the directory path of the test hooks.
    """

    return [os.path.dirname(__file__)]
