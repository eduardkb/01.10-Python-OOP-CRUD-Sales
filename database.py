import ekbMod
import os

ekbMod.clear_scren()

# TODO TODO - think how to start iniSettings
iniSettings = {
    "Database": "File",
    "FileDB_path": ".\\FileDB\\",
    "FileDB_extension": "tdb",
}

###################################################################
# SQL ENTRY FUNCTIONS


def fSql_create_Table(table_name, headers):
    if iniSettings["Database"] == "File":
        result = fFile_create_table(table_name, headers)
        return result


def fSql_add(table_name, newValues):
    if iniSettings["Database"] == "File":
        result = fFile_add(table_name, newValues)
        return result


def fSql_read_all(table_name):
    if iniSettings["Database"] == "File":
        result = fFile_read_all(table_name)
        return result


def fsql_read_one(table_name, table_column, searchValue):
    if iniSettings["Database"] == "File":
        result = fFile_read_one(table_name, table_column, searchValue)
        return result


def fsql_update_line(table_name, table_column, searchValue, newValues):
    if iniSettings["Database"] == "File":
        result = fFile_update_line(
            table_name, table_column, searchValue, newValues)
        return result


def fsql_delete_line(table_name, table_column, searchValue):
    if iniSettings["Database"] == "File":
        result = fFile_delete_line(table_name, table_column, searchValue)
        return result


###################################################################
# FILE MANAGEMENT FUNCTIONS

def fFile_create_table(table_name: str, headers):
    # fix table name and headers to lower()
    table_name = table_name.lower()
    headers = [x.lower() for x in headers]

    # get file name
    sFileName = f'{iniSettings["FileDB_path"]}{table_name}.{iniSettings["FileDB_extension"]}'
    bExists = ekbMod.verify_if_file_exists(sFileName)
    if bExists:
        raise FileNotFoundError("SQL-03, Table already exists.")
    else:
        if not os.path.exists(iniSettings["FileDB_path"]):
            os.makedirs(iniSettings["FileDB_path"])

    # generate header string
    sHeader = ""
    for head in headers:
        sHeader += head + ","
    sHeader = sHeader[:-1]

    # Write to file
    with open(sFileName, "a") as outfile:
        outfile.write(sHeader)

    return True


def fFile_add(table_name, newValues):
    sFileName = f'{iniSettings["FileDB_path"]}{table_name}.{iniSettings["FileDB_extension"]}'
    bExists = ekbMod.verify_if_file_exists(sFileName)
    if not bExists:
        raise FileNotFoundError("SQL-02, Table name not found.")

    aHeaders = []
    with open(sFileName, 'r') as file:
        for i, line in enumerate(file):
            if i == 0:
                aHeaders = line
                aHeaders = aHeaders.replace("\n", "")
                aHeaders = aHeaders.split(",")
                aHeaders = [x.lower() for x in aHeaders]
                break

    # setup dictionary with lower case
    newValuesLow = {}
    for key, value in newValues.items():
        newValuesLow[key.lower()] = value
    lDictKeys = list(newValuesLow.keys())
    lDictKeys = [x.lower() for x in lDictKeys]

    # build string to add
    sAdd = "\n"
    for head in aHeaders:
        if head in lDictKeys:
            sAdd += f"{newValuesLow[head]},"
        else:
            sAdd += ","

    sAdd = sAdd[:-1]

    with open(sFileName, "a") as outfile:
        outfile.write(sAdd)

    return True


def fFile_read_all(table_name):

    # verify if table_name (file) exists
    sFileName = f'{iniSettings["FileDB_path"]}{table_name}.{iniSettings["FileDB_extension"]}'
    bExists = ekbMod.verify_if_file_exists(sFileName)
    if not bExists:
        raise FileNotFoundError("SQL-02, Table name not found.")

    lines = []
    # reading file
    with open(sFileName, 'r') as file:
        list_lines = file.readlines()

    sTemp = ''
    for i, line in enumerate(list_lines):
        if i > 0:
            sTemp = line.replace('\n', '')
            sTemp = sTemp.split(',')
            sTemp = tuple(sTemp)
            lines.append(sTemp)

    return lines


def fFile_read_one(table_name, table_column: str, searchValue: str):
    # verify if table_name (file) exists
    sFileName = f'{iniSettings["FileDB_path"]}{table_name}.{iniSettings["FileDB_extension"]}'
    bExists = ekbMod.verify_if_file_exists(sFileName)
    if not bExists:
        raise FileNotFoundError("SQL-02, Table name not found.")

    items = []
    # reading file
    with open(sFileName, 'r') as file:
        for i, line in enumerate(file):
            if i == 0:
                stemp = line.replace('\n', '')
                sTemp = stemp.split(',')
                # search column position
                iCol = fFile_Search_column(sTemp, table_column)
            else:
                stemp = line.replace('\n', '')
                sTemp = stemp.split(',')
                if sTemp[iCol].lower() == searchValue.lower():
                    # value found. add to array as tuple
                    items.append(tuple(sTemp))
    # returning the result array
    return items


def fFile_update_line(table_name, table_column: str, searchValue: str, newValues):
    # verify if table_name (file) exists
    sFileName = f'{iniSettings["FileDB_path"]}{table_name}.{iniSettings["FileDB_extension"]}'
    bExists = ekbMod.verify_if_file_exists(sFileName)
    if not bExists:
        raise FileNotFoundError("SQL-02, Table name not found.")

    # read all lines
    with open(sFileName, 'r') as file:
        lines = file.readlines()

    stemp = lines[0].replace('\n', '')
    sTemp = stemp.split(',')
    # return position of search column
    iCol = fFile_Search_column(sTemp, table_column)

    # search lines to update
    aToUpdate = []
    for i, line in enumerate(lines):
        if i > 0:
            stemp = line.replace('\n', '')
            sTemp = stemp.split(',')
            if sTemp[iCol].lower() == searchValue.lower():
                aToUpdate.append(i)

    # return false if nothing to update
    if len(aToUpdate) == 0:
        return False

    # setup dictionary with lower case
    newValuesLow = {}
    for key, value in newValues.items():
        newValuesLow[key.lower()] = value
    lDictKeys = list(newValuesLow.keys())
    lDictKeys = [x.lower() for x in lDictKeys]

    # update lines
    newLines = ""
    for i, line in enumerate(lines):
        if i == 0:
            aHeaders = line.replace("\n", "")
            aHeaders = aHeaders.split(",")
            aHeaders = [x.lower() for x in aHeaders]
        if i in aToUpdate:
            # line to update
            aLine = line.replace("\n", "")
            aLine = aLine.split(",")
            w = 0
            for j, head in enumerate(aHeaders):
                if head in lDictKeys:
                    newLines += f"{newValuesLow[head]},"
                    w += 1
                else:
                    newLines += f"{aLine[j]},"
            if w != len(newValuesLow):
                raise ValueError("Incorrect column name")
            newLines = newLines[:-1]
            newLines += "\n"
        else:
            # line to maintain
            newLines += line

    # remove new line from end of the file
    if newLines[-1] == "\n":
        newLines = newLines[:-1]

    # write list updating entries to file
    with open(sFileName, "w") as outfile:
        outfile.write(newLines)

    # return true for lines updated
    return True


def fFile_delete_line(table_name, table_column: str, searchValue: str):
    # verify if table_name (file) exists
    sFileName = f'{iniSettings["FileDB_path"]}{table_name}.{iniSettings["FileDB_extension"]}'
    bExists = ekbMod.verify_if_file_exists(sFileName)
    if not bExists:
        raise FileNotFoundError("SQL-02, Table name not found.")

    # read all lines
    with open(sFileName, 'r') as file:
        lines = file.readlines()

    stemp = lines[0].replace('\n', '')
    sTemp = stemp.split(',')
    # return position of search column
    iCol = fFile_Search_column(sTemp, table_column)

    # search lines to delete
    aToDelete = []
    for i, line in enumerate(lines):
        if i > 0:
            stemp = line.replace('\n', '')
            sTemp = stemp.split(',')
            if sTemp[iCol].lower() == searchValue.lower():
                aToDelete.append(i)

    # return false if nothing to delete
    if len(aToDelete) == 0:
        return False

    # write list with deleted entries to file
    with open(sFileName, "w") as outfile:
        for pos, line in enumerate(lines):
            if pos not in aToDelete:
                outfile.write(line)

    # return true for lines deleted
    return True

###################################################################
# GENERAL FUNCTIONS

# returns column position or exception


def fFile_Search_column(columns, searchValue):
    for i, str in enumerate(columns):
        if str.lower() == searchValue.lower():
            # column found. store position
            return i
    raise ValueError("SQL-01: Column to search not found.")


###################################################################
# TESTING
# TODO TODO
# --

# FILE DATABASE CRUD EXAMPLES
try:
    op = 2
    a = ""

    match op:
        # -- create table
        case 1:
            aHeaders = ["ID", "NaME", "AgE", "heigth", "NUM"]
            a = fFile_create_table("CrEW", aHeaders)
        # -- Complete Add
        case 2:
            dictAdd = {"ID": 1, "name": "Eduard",
                       "age": 39, "heigth": 183, "NUM": 7}
            a = fSql_add("crew", dictAdd)
        # -- Incomplete ADD
        case 3:
            dictAdd = {"ID": 12, "name": "Gustav", "age": 55}
            a = fSql_add("crew", dictAdd)

    # -- add

    # -- Read One Example
    # a = fsql_read_one("crew", "Id", "1")
    # -- Read ALL Example
    # a = fSql_read_all("crew")
    # -- update one or many example
    # dictUpdate = {"NAME": "Hugo", "heigth": 160}
    # a = fsql_update_line("crew", "ID", "1", dictUpdate)
    # -- Delete Example (one or many)
    # a = fsql_delete_line("crew", "id", "14")

    print(a)
except ValueError as error:
    print('Caught error:', error)
except FileNotFoundError as error:
    print('Caught error:', error)
except Exception as error:
    print('Caught error:', error)

print('END')
