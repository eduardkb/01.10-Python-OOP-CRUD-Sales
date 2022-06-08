from ast import Raise
import ekbMod
import os
import sqlite3

ekbMod.clear_scren()

iniSettings = {
    "updated_from_file": False,
    "ini_file_exists": True,
    "database": "File",
    "filedb_path": ".\\FileDB\\",
    "filedb_extension": "tdb",
}

###################################################################
# SQL ENTRY FUNCTIONS


def fSql_create_Table(table_name, headers):
    global iniSettings
    fUpdate_INI_Settings()

    if iniSettings["database"] == "file":
        result = fFile_create_table(table_name, headers)
        return result
    if iniSettings["database"] == "sqlite":
        result = fSQLite_create_table(table_name, headers)
        return result

    raise Exception("No database to read from")


def fSql_add(table_name, newValues):
    global iniSettings
    fUpdate_INI_Settings()

    if iniSettings["database"] == "file":
        result = fFile_add(table_name, newValues)
        return result
    if iniSettings["database"] == "sqlite":
        result = fSQLite_add(table_name, newValues)
        return result

    raise Exception("No database to read from")


def fSql_read_all(table_name):
    global iniSettings
    fUpdate_INI_Settings()

    if iniSettings["database"] == "file":
        result = fFile_read_all(table_name)
        return result
    if iniSettings["database"] == "sqlite":
        result = fSQLite_read_all(table_name)
        return result

    raise Exception("No database to read from")


def fsql_read_one(table_name, table_column, searchValue):
    global iniSettings
    fUpdate_INI_Settings()

    if iniSettings["database"] == "file":
        result = fFile_read_one(table_name, table_column, searchValue)
        return result
    if iniSettings["database"] == "sqlite":
        # TODO TODO -- develop sqlite function
        return [1, 2, 3]

    raise Exception("No database to read from")


def fsql_update_line(table_name, table_column, searchValue, newValues):
    global iniSettings
    fUpdate_INI_Settings()

    if iniSettings["database"] == "file":
        result = fFile_update_line(
            table_name, table_column, searchValue, newValues)
        return result
    if iniSettings["database"] == "sqlite":
        # TODO TODO -- develop sqlite function
        return [1, 2, 3]

    raise Exception("No database to read from")


def fsql_delete_line(table_name, table_column, searchValue):
    global iniSettings
    fUpdate_INI_Settings()

    if iniSettings["database"] == "file":
        result = fFile_delete_line(table_name, table_column, searchValue)
        return result
    if iniSettings["database"] == "sqlite":
        # TODO TODO -- develop sqlite function
        return [1, 2, 3]

    raise Exception("No database to read from")


###################################################################
# SQLite MANAGEMENT FUNCTIONS
def fSQLit_create_conenction(table_name, fileName):
    conn = None
    try:
        conn = sqlite3.connect(fileName)
        return conn
    except Exception:
        raise Exception("SQL-03, Not able to open database file.")

    return conn


def fSQLite_create_table(table_name: str, headers):
    global iniSettings

    db_path = iniSettings["sqlite_path"]
    db_file = str(db_path + table_name + iniSettings["sqlite_db_extension"])

    bExists = ekbMod.verify_if_file_exists(db_file)
    if not bExists:
        if not os.path.exists(iniSettings["sqlite_path"]):
            os.makedirs(iniSettings["sqlite_path"])

    conn = fSQLit_create_conenction(table_name, db_file)

    # Build SQL
    sSql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for val in headers:
        items = val.split(":")
        if len(items) != 2:
            conn.close()
            raise Exception("SQL-04, Table input parameters incorrect.")
        sSql += f"{items[0].lower().strip()} {items[1].lower().strip()},"

    sSql = sSql[:-1]
    sSql += ");"
    # execute sql
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sSql)
        except Exception as e:
            conn.close()
            raise Exception("SQL-06, Error while writing to database")
    else:
        conn.close()
        raise Exception("SQL-05, Connection to database lost")

    conn.close()
    return True


def fSQLite_add(table_name, newValues):
    global iniSettings

    db_file = str(iniSettings["sqlite_path"] +
                  table_name + iniSettings["sqlite_db_extension"])
    conn = fSQLit_create_conenction(table_name, db_file)

    sSql = "insert into cliente Values (?,?,?,?,?,?);"

    data_tuple = ()
    lValues = list(newValues.values())
    for val in lValues:
        data_tuple += (f'{val}',)

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sSql, data_tuple)
            conn.commit()
        except Exception as e:
            conn.close()
            raise Exception("SQL-06, Error while writing to database:")
    else:
        conn.close()
        raise Exception("SQL-05, Connection to database lost")

    conn.close()
    return True


def fSQLite_read_all(table_name):
    global iniSettings

    db_file = str(iniSettings["sqlite_path"] +
                  table_name + iniSettings["sqlite_db_extension"])
    conn = fSQLit_create_conenction(table_name, db_file)

    sSql = f"select * from {table_name};"

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sSql)
            rows = c.fetchall()
        except Exception as e:
            conn.close()
            raise Exception("SQL-07, Error while reading database:", e)
    else:
        conn.close()
        raise Exception("SQL-05, Connection to database lost")

    conn.close()
    return rows

###################################################################
# FILE MANAGEMENT FUNCTIONS


def fFile_create_table(table_name: str, headers):
    # fix table name and headers to lower()
    table_name = table_name.lower()
    headers = [x.lower() for x in headers]

    # get file name
    sFileName = f'{iniSettings["filedb_path"]}{table_name}.{iniSettings["filedb_extension"]}'
    bExists = ekbMod.verify_if_file_exists(sFileName)
    if bExists:
        raise FileNotFoundError("SQL-03, Table already exists.")
    else:
        if not os.path.exists(iniSettings["filedb_path"]):
            os.makedirs(iniSettings["filedb_path"])

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
    sFileName = f'{iniSettings["filedb_path"]}{table_name}.{iniSettings["filedb_extension"]}'
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
    sFileName = f'{iniSettings["filedb_path"]}{table_name}.{iniSettings["filedb_extension"]}'
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
    sFileName = f'{iniSettings["filedb_path"]}{table_name}.{iniSettings["filedb_extension"]}'
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
    sFileName = f'{iniSettings["filedb_path"]}{table_name}.{iniSettings["filedb_extension"]}'
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
    sFileName = f'{iniSettings["filedb_path"]}{table_name}.{iniSettings["filedb_extension"]}'
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


def fUpdate_INI_Settings():
    global iniSettings
    # default INI settings:
    #       "updated_from_file": False,
    #       "ini_file_exists": True,
    #       "database": "File",
    #       "filedb_path": ".\\FileDB\\",
    #       "filedb_extension": "tdb",

    if (not iniSettings["ini_file_exists"]) or (not ekbMod.verify_if_file_exists("settings.ini")):
        iniSettings["ini_file_exists"] = False
        return

    with open("settings.ini", 'r') as file:
        list_lines = file.readlines()

    for line in list_lines:
        line = line.strip()
        if line != '' and line[0] != '#':
            values = line.split("=")
            if len(values) > 1:
                iniSettings[(values[0].strip()).lower()] = (
                    values[1].strip()).lower()

    iniSettings["updated_from_file"] = True


def fFile_Search_column(columns, searchValue):
    # returns column position or exception
    for i, str in enumerate(columns):
        if str.lower() == searchValue.lower():
            # column found. store position
            return i
    raise ValueError("SQL-01: Column to search not found.")


###################################################################
# TESTING
# TODO TODO
# -- SQLLITE -- add has to be with full sql. add one and add all are same function

# DATABASE CRUD EXAMPLES
try:
    op = 5
    a = ""

    match op:

        case 1:  # -- create table
            # for File DB:
            # aHeaders = ["Id", "Name", "Age", "Heigth", "Num"]
            # for SQLite DB:
            aHeaders = ["Id:integer PRIMARY KEY", "Name:text",
                        "age:integer", "heigth:real", "address:text", "CPF:text"]
            a = fSql_create_Table("cliente", aHeaders)
            aHeaders = ["Id:integer PRIMARY KEY", "Name:text",
                        "salary:real", "sells:ïnteger"]
            a = fSql_create_Table("vendedor", aHeaders)
        case 2:  # -- ADD with all fields
            dictAdd = {"ID": 3, "name": "Aldo",
                       "age": 44, "heigth": 2.33, "address": "Alameda", "CPF": "444444"}
            a = fSql_add("cliente", dictAdd)
        case 3:  # -- ADD with some fields
            dictAdd = {"ID": 12, "name": "Gustav", "age": 55}
            a = fSql_add("crew", dictAdd)
        case 4:  # -- Read One Example
            a = fsql_read_one("crew", "Id", "1")
        case 5:  # -- Read ALL Example
            a = fSql_read_all("cliente")
        case 6:  # -- update one or many example
            dictUpdate = {"NAME": "Hugo", "heigth": 160}
            a = fsql_update_line("crew", "ID", "1", dictUpdate)
        case 7:  # -- Delete Example (one or many)
            a = fsql_delete_line("crew", "id", "14")
        case _:  # case default
            a = "No valid option entered"

    print(a)
except ValueError as error:
    print('Caught error:', error)
except FileNotFoundError as error:
    print('Caught error:', error)
except Exception as error:
    print('Caught error:', error)

print('END')
