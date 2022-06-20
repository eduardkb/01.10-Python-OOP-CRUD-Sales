import pathlib
import os

iniSettings = {
    "updated_from_file": False,
    "ini_file_exists": True,
    "database": "file",
    "filedb_path": "./resources/FileDB/",
    "filedb_extension": "tdb",
}


def fUpdate_INI_Settings():
    global iniSettings
    # default INI settings:
    #       "updated_from_file": False,
    #       "ini_file_exists": True,
    #       "database": "File",
    #       "filedb_path": ".\\FileDB\\",
    #       "filedb_extension": "tdb",

    if iniSettings["updated_from_file"]:
        return

    if (not iniSettings["ini_file_exists"]) or (not verify_if_file_exists(r"resources/settings.ini")):
        iniSettings["ini_file_exists"] = False
        return

    with open("resources/settings.ini", 'r') as file:
        list_lines = file.readlines()

    for line in list_lines:
        line = line.strip()
        if line != '' and line[0] != '#':
            values = line.split("=")
            if len(values) > 1:
                iniSettings[(values[0].strip()).lower()] = (
                    values[1].strip()).lower()

    iniSettings["updated_from_file"] = True


def clear_scren():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def verify_if_file_exists(path: str):
    file = pathlib.Path(path)
    return True if file.is_file() else False
