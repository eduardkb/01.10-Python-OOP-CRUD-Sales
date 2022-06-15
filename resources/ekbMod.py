import pathlib
import os


def clear_scren():
    os.system("cls")


def verify_if_file_exists(path: str):
    file = pathlib.Path(path)
    return True if file.is_file() else False
