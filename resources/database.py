"""
TODO TODO
Urgent
--
Not Urgent:
-- file -- (acentuaçao nao grava e nao lê) (Encodeng utf-8 ???)
"""
import resources.ekbMod as ekbMod
import os
import sqlite3

###################################################################
# SQL ENTRY FUNCTIONS


def fSql_create_Table(table_name, headers):
    ekbMod.fUpdate_INI_Settings()

    if ekbMod.iniSettings["database"] == "file":
        result = fFile_create_table(table_name, headers)
        return result
    if ekbMod.iniSettings["database"] == "sqlite":
        result = fSQLite_create_table(table_name, headers)
        return result

    raise Exception("Database parameters incorrect")


def fSql_add(table_name, newValues):
    ekbMod.fUpdate_INI_Settings()

    if ekbMod.iniSettings["database"] == "file":
        result = fFile_add(table_name, newValues)
        return result
    if ekbMod.iniSettings["database"] == "sqlite":
        result = fSQLite_add(table_name, newValues)
        return result

    raise Exception("No database to read from")


def fSql_read_all(table_name):
    ekbMod.fUpdate_INI_Settings()

    if ekbMod.iniSettings["database"] == "file":
        result = fFile_read_all(table_name)
        return result
    if ekbMod.iniSettings["database"] == "sqlite":
        result = fSQLite_read_all(table_name)
        return result

    raise Exception("No database to read from")


def fsql_read_one(table_name, table_column, searchValue):
    ekbMod.fUpdate_INI_Settings()

    if ekbMod.iniSettings["database"] == "file":
        result = fFile_read_one(table_name, table_column, searchValue)
        return result
    if ekbMod.iniSettings["database"] == "sqlite":
        result = fSQLite_read_one(table_name, table_column, searchValue)
        return result

    raise Exception("No database to read from")


def fsql_update_line(table_name, table_column, searchValue, newValues):
    ekbMod.fUpdate_INI_Settings()

    if ekbMod.iniSettings["database"] == "file":
        result = fFile_update_line(
            table_name, table_column, searchValue, newValues)
        return result
    if ekbMod.iniSettings["database"] == "sqlite":
        result = fSQLite_update_line(
            table_name, table_column, searchValue, newValues)
        return result

    raise Exception("No database to read from")


def fsql_delete_line(table_name, table_column, searchValue):
    ekbMod.fUpdate_INI_Settings()

    if ekbMod.iniSettings["database"] == "file":
        result = fFile_delete_line(table_name, table_column, searchValue)
        return result
    if ekbMod.iniSettings["database"] == "sqlite":
        result = fSQLite_delete_line(table_name, table_column, searchValue)
        return result

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

    db_path = ekbMod.iniSettings["sqlite_path"]
    db_name = ekbMod.iniSettings["sqlite_db_name"]
    db_exten = ekbMod.iniSettings["sqlite_db_extension"]
    db_file = str(db_path + db_name + db_exten)

    bExists = ekbMod.verify_if_file_exists(db_file)
    if not bExists:
        if not os.path.exists(ekbMod.iniSettings["sqlite_path"]):
            os.makedirs(ekbMod.iniSettings["sqlite_path"])

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
    db_path = ekbMod.iniSettings["sqlite_path"]
    db_name = ekbMod.iniSettings["sqlite_db_name"]
    db_exten = ekbMod.iniSettings["sqlite_db_extension"]
    db_file = str(db_path + db_name + db_exten)

    conn = fSQLit_create_conenction(table_name, db_file)

    # generating tuple only with values to add
    lValues = list(newValues.values())
    data_tuple = tuple(lValues)

    # adding correct number of ?
    sSpaces = ''
    for i in range(len(lValues)):
        sSpaces += ' ?,'
    sSpaces = sSpaces[:-1]

    # separate columns
    lCol = list(newValues.keys())
    sColumns = ""
    for val in lCol:
        sColumns += f" {val},"
    sColumns = sColumns[:-1]

    sSql = f"insert into {table_name} ({sColumns}) Values ({sSpaces});"

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sSql, data_tuple)
            conn.commit()
        except Exception as e:
            conn.close()
            raise Exception("SQL-06, Error while writing to database:", e)
    else:
        conn.close()
        raise Exception("SQL-05, Connection to database lost")

    conn.close()
    return True


def fSQLite_read_all(table_name):
    db_path = ekbMod.iniSettings["sqlite_path"]
    db_name = ekbMod.iniSettings["sqlite_db_name"]
    db_exten = ekbMod.iniSettings["sqlite_db_extension"]
    db_file = str(db_path + db_name + db_exten)

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


def fSQLite_read_one(table_name, table_column, searchValue):
    db_path = ekbMod.iniSettings["sqlite_path"]
    db_name = ekbMod.iniSettings["sqlite_db_name"]
    db_exten = ekbMod.iniSettings["sqlite_db_extension"]
    db_file = str(db_path + db_name + db_exten)

    conn = fSQLit_create_conenction(table_name, db_file)

    sSql = f"select * from {table_name} where {table_column} = {searchValue};"

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


def fSQLite_update_line(
        table_name, table_column, searchValue, newValues):

    db_path = ekbMod.iniSettings["sqlite_path"]
    db_name = ekbMod.iniSettings["sqlite_db_name"]
    db_exten = ekbMod.iniSettings["sqlite_db_extension"]
    db_file = str(db_path + db_name + db_exten)

    conn = fSQLit_create_conenction(table_name, db_file)

    # put the SET SQL clausule in a string
    sSet = ''
    for key, val in newValues.items():
        sSet += f" '{key}'=?,"
    sSet = sSet.strip()
    sSet = sSet[:-1]

    # create tuple with values to change
    tValues = tuple(list(newValues.values()))

    sSql = f"UPDATE {table_name} SET {sSet} WHERE {table_column} = '{searchValue}';"

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sSql, tValues)
            conn.commit()
        except Exception as e:
            conn.close()
            raise Exception("SQL-06, Error while updating table:", e)
    else:
        conn.close()
        raise Exception("SQL-05, Connection to database lost")

    conn.close()
    return True


def fSQLite_delete_line(table_name, table_column, searchValue):
    db_path = ekbMod.iniSettings["sqlite_path"]
    db_name = ekbMod.iniSettings["sqlite_db_name"]
    db_exten = ekbMod.iniSettings["sqlite_db_extension"]
    db_file = str(db_path + db_name + db_exten)

    conn = fSQLit_create_conenction(table_name, db_file)
    #sSql = f"DELETE FROM {table_name} WHERE {table_column} = '{searchValue}';"
    sSql = f"DELETE FROM {table_name} WHERE {table_column} = ?;"

    tValue = tuple()
    tValue += (searchValue,)

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sSql, tValue)
            conn.commit()
        except Exception as e:
            conn.close()
            raise Exception("SQL-06, Error while updating table:", e)
    else:
        conn.close()
        raise Exception("SQL-05, Connection to database lost")

    conn.close()
    return True
###################################################################
# FILE MANAGEMENT FUNCTIONS


def fFile_create_table(table_name: str, headers):
    # fix table name and headers to lower()
    table_name = table_name.lower()
    headers = [(x.split(":")[0]).lower() for x in headers]

    # get file name
    sFileName = f'{ekbMod.iniSettings["filedb_path"]}{table_name}.{ekbMod.iniSettings["filedb_extension"]}'
    bExists = ekbMod.verify_if_file_exists(sFileName)
    if bExists:
        return True
    else:
        if not os.path.exists(ekbMod.iniSettings["filedb_path"]):
            os.makedirs(ekbMod.iniSettings["filedb_path"])

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
    sFileName = f'{ekbMod.iniSettings["filedb_path"]}{table_name}.{ekbMod.iniSettings["filedb_extension"]}'
    bExists = ekbMod.verify_if_file_exists(sFileName)
    if not bExists:
        raise FileNotFoundError("SQL-02, Table name not found.")

    aHeaders = []
    with open(sFileName, 'r') as file:
        fLines = file.readlines()

    # read header
    if len(fLines) > 0:
        aHeaders = fLines[0]
        aHeaders = aHeaders.replace("\n", "")
        aHeaders = aHeaders.split(",")
        aHeaders = [x.lower() for x in aHeaders]

    # setup dictionary with lower case
    newValuesLow = {}
    for key, value in newValues.items():
        newValuesLow[key.lower()] = value
    lDictKeys = list(newValuesLow.keys())
    lDictKeys = [x.lower() for x in lDictKeys]

    # if no ID argumen read all ID's from file and find max ID
    if not ('id' in lDictKeys) and 'id' in aHeaders:
        # search ID position
        iPosID = 0
        for i, val in enumerate(aHeaders):
            if val == 'id':
                iPosID = i
                break
        maxId = 1
        # serach max id in file
        for i in range(1, len(fLines)):
            aLine = fLines[i]
            aLine = aLine.replace("\n", "")
            aLine = aLine.split(",")
            if maxId < int(aLine[iPosID]):
                maxId = int(aLine[iPosID])
        # put ID + 1 in dictionarys
        newValuesLow['id'] = maxId+1
        lDictKeys.append('id')

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
    sFileName = f'{ekbMod.iniSettings["filedb_path"]}{table_name}.{ekbMod.iniSettings["filedb_extension"]}'
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
    sFileName = f'{ekbMod.iniSettings["filedb_path"]}{table_name}.{ekbMod.iniSettings["filedb_extension"]}'
    bExists = ekbMod.verify_if_file_exists(sFileName)
    if not bExists:
        raise FileNotFoundError("SQL-02, Table name not found.")

    items = []
    # reading file
    searchValue = str(searchValue)
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
    sFileName = f'{ekbMod.iniSettings["filedb_path"]}{table_name}.{ekbMod.iniSettings["filedb_extension"]}'
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
    searchValue = str(searchValue)
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
    sFileName = f'{ekbMod.iniSettings["filedb_path"]}{table_name}.{ekbMod.iniSettings["filedb_extension"]}'
    bExists = ekbMod.verify_if_file_exists(sFileName)
    if not bExists:
        raise FileNotFoundError("SQL-02, Table name not found.")

    # read all lines
    with open(sFileName, 'r') as file:
        all_file_lines = file.readlines()

    stemp = all_file_lines[0].replace('\n', '')
    stemp = stemp.split(',')
    # return position of search column
    iCol = fFile_Search_column(stemp, table_column)

    # search lines to delete
    searchValue = str(searchValue)
    aToDelete = []
    for i, line in enumerate(all_file_lines):
        if i > 0:
            stemp = line.replace('\n', '')
            sTemp = stemp.split(',')
            if sTemp[iCol].lower() == searchValue.lower():
                aToDelete.append(i)

    # return false if nothing to delete
    if len(aToDelete) == 0:
        return False

    # delete lines from object with all lines
    aToDelete = aToDelete[::-1]
    for item in aToDelete:
        all_file_lines.pop(item)

    # remove \n from last line in object if last line was deleted
    if all_file_lines[len(all_file_lines)-1].find('\n') >= 0:
        temp = all_file_lines.pop()
        temp = temp.replace('\n', '')
        all_file_lines.append(temp)

    # write list with deleted entries to file
    with open(sFileName, "w") as outfile:
        outfile.writelines(all_file_lines)

    # return true for lines deleted
    return True

###################################################################
# GENERAL FUNCTIONS


def fFile_Search_column(columns, searchValue):
    # returns column position or exception
    for i, str in enumerate(columns):
        if str.lower() == searchValue.lower():
            # column found. store position
            return i
    raise ValueError("SQL-01: Column to search not found.")


###################################################################
# TESTING


if __name__ == "__main__":
    # DATABASE CRUD EXAMPLES
    ekbMod.clear_scren()
    try:

        op = 7
        a = ""
        if op == 1:  # -- CREATE DB and tables
            aHeaders = ["Id:integer PRIMARY KEY", "Name:text",
                        "age:integer", "heigth:real", "address:text", "CPF:text"]
            a = fSql_create_Table("cliente", aHeaders)
            aHeaders = ["Id:integer PRIMARY KEY", "Name:text",
                        "salary:real", "sells:ïnteger"]
            a = fSql_create_Table("vendedor", aHeaders)
        elif op == 2:  # -- ADD with all fields
            dictAdd = {"ID": 4, "name": "Kelson",
                       "age": 44, "heigth": 4.44, "address": "Avenida", "CPF": "444444"}
            a = fSql_add("cliente", dictAdd)
            dictAdd = {"ID": 4, "name": "Xena",
                       "salary": 4400, "sells": 140}
            a = fSql_add("vendedor", dictAdd)
        elif op == 3:  # -- ADD with some fields
            dictAdd = {"name": "Basel", "country": "Brasil",
                       "city": "Curitiba", "date_nasc": "10/06/2022"}
            a = fSql_add("client", dictAdd)
            dictAdd = {"name": "Nóia",
                       "manager": "Pó", "active": "False"}
            a = fSql_add("retailer", dictAdd)
        elif op == 4:  # -- Read One Example
            a = fsql_read_one("Cliente", "id", 1)
        elif op == 5:  # -- Read ALL Example
            a = fSql_read_all("cliente")
            print("Cliente:", a)
            a = fSql_read_all("vendedor")
            print("vendedor:", a)
            a = True
        elif op == 6:  # -- update one or many example
            dictUpdate = {"id": 2, "NamE": "Tanos", "sells": 999}
            a = fsql_update_line("vendedor", "id", 2, dictUpdate)
        elif op == 7:  # -- Delete Example (one or many)
            a = fsql_delete_line("client", "id", 5)
        else:  # default
            a = "No valid option entered"

        print(a)
    except ValueError as error:
        print('Caught error:', error)
    except FileNotFoundError as error:
        print('Caught error:', error)
    except Exception as error:
        print('Caught error:', error)

    print('END')
