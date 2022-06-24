"""
TODO TODO
urgent
-- on table list of clients
    -- phone not being truncated because it is a integer
not urgent
-- for file_DB Windows does not read or write special characters (Encodeng utf-8 ???)
    -- works on linux. when windows fixed, test linux again.

"""

import resources.backend as backend
import resources.ekbMod as ekbMod
bDEBUG = False


######################################################
# CLI - Print Main menu


def fMain_menu():
    op = '0'
    while str(op) != '5':
        fPrint_main_Menu()

        op = input("Select an option: ")
        if op == '1':
            fCreate_database()
        elif op == '2':
            fEnter_client()
        elif op == '3':
            fEnter_Retailer()
        elif op == '4':
            fEnter_Sells()

        if op not in ['1', '2', '3', '4', '5']:
            print("\nINFO: Invalid option.")
            input("Press any key to return.")


def fPrint_main_Menu():
    ekbMod.clear_scren()
    c = chr(176)  # °
    c = chr(187)  # »
    
    print(" "*27 + "╔═══════════════════════╗")
    print(" "*27 + "║   Sales - Main Menu   ║")
    print(" "*27 + "╚═══════════════════════╝")
    print("╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                             ║")
    print(f"║       {c}  1 - Create database                                                ║")
    print(f"║       {c}  2 - Client Registration                                            ║")
    print(f"║       {c}  3 - Retailer Registration                                          ║")
    print(f"║       {c}  4 - Sells Registration                                             ║")
    print(f"║       {c}  5 - Exit                                                           ║")
    print("║                                                                             ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")

######################################################
# CLI - Print SubMenu title


def fPrint_submenu_title(title: str):
    ekbMod.clear_scren()
    title = f"   Submenu - {title}   "
    table = '┄' * len(title)
    print(f"┍{table}┑")
    print(f"┆{title}┆")
    print(f"┕{table}┙")
    print("┄"*80)


def fEnter_client():

    try:
        backend.Client.fRead_all_from_db()
    except Exception as e:
        fPrint_submenu_title("Client Registration")
        print("ERROR: Problem accessing database: ", e)
        input("\nPress any key to return to main menu.")
        return
    op = '0'
    while op != '5':
        fPrint_submenu_title("Client Registration")
        print("1 - List all Clients")
        print("2 - Add a new Client")
        print("3 - Modify a Client")
        print("4 - Delete a Client")
        print("5 - Back to Main Menu")

        op = str(input("Select an option: "))
        if op not in ['1', '2', '3', '4', '5']:
            print("\nINFO: Invalid option.")
            input("Press any key to return.")

        if op == '1':
            fTable_print_items(backend.Client.all_items, "Clients")
            input("\nPress any key to return.")
        elif op == '2':
            fAdd_new("Clients")
            input("Press any key to return.")
        elif op == '3':
            fModify("Clients")
            input("Press any key to return.")
        elif op == '4':
            fDelete_Item("Clients")


def fEnter_Retailer():
    try:
        backend.Retailer.fRead_all_from_db()
    except Exception as e:
        fPrint_submenu_title("Retailer Registration")
        print("ERROR: Problem accessing database: ", e)
        input("\nPress any key to return to main menu.")
        return
    op = '0'
    while op != '5':
        fPrint_submenu_title("Retailer Registration")
        print("1 - List all Retailers")
        print("2 - Add a new Retailer")
        print("3 - Modify a Retailer")
        print("4 - Delete a Retailer")
        print("5 - Back to Main Menu")

        op = str(input("Select an option: "))
        if op not in ['1', '2', '3', '4', '5']:
            print("\nINFO: Invalid option.")
            input("Press any key to return.")

        if op == '1':
            fTable_print_items(backend.Retailer.all_items, "Retailers")
            input("\nPress any key to return.")
        elif op == '2':
            fAdd_new("Retailers")
            input("Press any key to return.")
        elif op == '3':
            fModify("Retailers")
            input("Press any key to return.")
        elif op == '4':
            fDelete_Item("Retailers")


def fEnter_Sells():
    try:
        backend.Sale.fRead_all_from_db()
    except Exception as e:
        fPrint_submenu_title("Sells Registration")
        print("ERROR: Problem accessing database: ", e)
        input("\nPress any key to return to main menu.")
        return
    op = '0'
    while op != '5':
        fPrint_submenu_title("Sells Registration")
        print("1 - List all Sells")
        print("2 - Add a new Sell")
        print("3 - Print sells per retailer")
        print("5 - Back to Main Menu")

        op = str(input("Select an option: "))
        if op not in ['1', '2', '3', '5']:
            print("\nINFO: Invalid option.")
            input("Press any key to return.")

        if op == '1':
            fTable_print_items(backend.Sale.all_items, "Sells")
            input("\nPress any key to return.")
        elif op == '2':
            fAdd_new("Sells")
            input("Press any key to return.")
        elif op == '3':
            fPrintSellSum()
            input("\nPress any key to return.")

######################################################
# General Functions


def fCreate_database():
    global bDEBUG
    fPrint_submenu_title("Create Databases")
    try:
        backend.Client.fCreate_table()
        backend.Retailer.fCreate_table()
        backend.Sale.fCreate_table()

        if bDEBUG:
            objTest_Class = "Client"
            backend.fTest_add(objTest_Class)
            objTest_Class = "Retailer"
            backend.fTest_add(objTest_Class)
            objTest_Class = "Sale"
            backend.fTest_add(objTest_Class)

        print("INFO: All databses created successful if they did not exist.")
    except Exception as e:
        print("ERROR: Database couldn't be created: ", e)

    input("\nPress any key to return to main menu.")

def fTable_print_items(items, table):
    fPrint_submenu_title(f"List of {table}")
    if table == "Clients":
        if len(items) > 0:
            head = ["ID", "CPF", "Name", "Country",
                    "City", "Phone", "Birthday"]
            row = "{id:<4}| {CPF:<10.9}| {Name:<15.14}| {Country:<15.14}| {City:<15.14}| {Phone:<10}| {Birthday:^10.10}".format
            print(row(id=head[0], CPF=head[1], Name=head[2], Country=head[3],
                      City=head[4], Phone=head[5], Birthday=head[6]))
            print("-"*80)
            for tup in items:
                print(row(id=tup.id, CPF=tup.cpf, Name=tup.name, Country=tup.country,
                          City=tup.city, Phone=tup.phone, Birthday=str(tup.date_nasc)))
        else:
            print(f"INFO: {table} table is empty.")
    elif table == "Retailers":
        if len(items) > 0:
            head = ["ID", "CPF", "Name", "Manager", "Salary"]
            row = "{id:<4}| {CPF:<10.10}| {Name:<15.15}| {Manager:<15.15}| {Salary:>10}".format
            print(row(id=head[0], CPF=head[1], Name=head[2], Manager=head[3],
                      Salary=head[4]))
            row = "{id:<4}| {CPF:<10.9}| {Name:<15.14}| {Manager:<15.14}| {Salary:>10,.2F}".format
            print("-"*80)
            for tup in items:
                try:
                    sal = float(tup.salary)
                except Exception:
                    sal = float(0)
                print(row(id=tup.id, CPF=tup.cpf, Name=tup.name, Manager=tup.manager,
                          Salary=sal))
        else:
            fPrint_submenu_title(f"List of {table}")
            print(f"INFO: {table} table is empty.")
    elif table == "Sells":
        if len(items) > 0:
            head = ["ID", "Retailer", "Client", "Item Sold", "Price"]
            row = "{id:<4}| {ret:<15}| {cli:<15}| {item:<20}| {price:>10}".format
            print(row(id=head[0], ret=head[1], cli=head[2], item=head[3],
                      price=head[4]))
            row = "{id:<4}| {ret:<15.14}| {cli:<15.14}| {item:<20.19}| {price:>10,.2f}".format
            print("-"*80)
            for tup in items:
                try:
                    pri = float(tup.price)
                except Exception:
                    pri = float(0)
                print(row(id=tup.id, ret=tup.retailer, cli=tup.client, item=tup.item_sold,
                          price=pri))
        else:
            fPrint_submenu_title(f"List of {table}")
            print(f"INFO: {table} table is empty.")

def fAdd_new(table):
    if table == "Clients":
        fPrint_submenu_title(f"Adding {table}")
        print("Type a value for each field (0 at any field to cancel):")
        val = fValidateClientInput()
        if val == 0:
            print("\nINFO: Adding client was cancelled.")
        else:
            try:
                backend.Client(0, val[0], val[1], val[2],
                               val[3], val[4], val[5])
                print("\nINFO: Successfully added new Client")
            except Exception as e:
                print(f"\nERROR: Could not add new Client: {e}")
    if table == "Retailers":
        fPrint_submenu_title(f"Adding {table}")
        print("Type a value for each field (0 at any field to cancel):")
        val = fValidateRetailerInput()
        if val == 0:
            print("\nINFO: Adding retailer was cancelled.")
        else:
            try:
                backend.Retailer(0, val[0], val[1], val[2],
                                 val[3], val[4])
                print("\nINFO: Successfully added new Retailer")
            except Exception as e:
                print(f"\nERROR: Could not add new Retailer: {e}")
    if table == "Sells":
        iRetID = fGetRetailerID()
        if iRetID != False:
            iCliID = fGetClientID()
            if iCliID != False:
                fPrint_submenu_title(f"Adding {table}")
                dictUpdate = fValidateSellInput()
                if dictUpdate != False:
                    #write sell to database
                    try:
                        backend.Sale(0,iRetID, iCliID, dictUpdate["item"], dictUpdate["price"])
                        print("\nINFO: Sell registered successfully.")
                    except Exception as e:
                        print("\nError. Unable to add sell: ", e)
        
def fValidateClientInput():
    # Init fields: id, cpf, name, country, city, phone, date_nasc
    val = []
    # input and validate CPF
    sCpf = ''
    while sCpf == '' or len(sCpf) <= 5:
        sCpf = input("Client CPF: ")
        if sCpf == '0':
            return 0
        if sCpf == '' or len(sCpf) <= 5:
            print("INFO: Incorrect input. CPF has at least 6 digits.")
    val.append(sCpf)
    # input and validate sName
    sName = ''
    while sName == '' or len(sName) <= 5:
        sName = input("Client Name: ")
        if sName == '0':
            return 0
        if sName == '' or len(sName) <= 5:
            print("INFO: Incorrect input. NAME has to be at least 6 digits long.")
    val.append(sName)
    # input country
    sCountry = input("Client Country: ")
    if sCountry == '0':
        return 0
    val.append(sCountry)
    # input city
    sCity = input("Client City: ")
    if sCity == '0':
        return 0
    val.append(sCity)
    # input phone
    sPhone = input("Client Phone: ")
    if sPhone == '0':
        return 0
    val.append(sPhone)
    # input birthday
    sDate_nasc = input("Client Birthday: ")
    if sDate_nasc == '0':
        return 0
    val.append(sDate_nasc)
    return val

def fValidateRetailerInput():
    # cpf, name, manager, salary, active
    val = []
    # validate CPF
    sCpf = ''
    while sCpf == '' or len(sCpf) <= 5:
        sCpf = input("Retailer CPF: ")
        if sCpf == '0':
            return 0
        if sCpf == '' or len(sCpf) <= 5:
            print("INFO: Incorrect input. CPF has at least 6 digits.")
    val.append(sCpf)
    # validate name
    sName = ''
    while sName == '' or len(sName) <= 5:
        sName = input("Retailer Name: ")
        if sName == '0':
            return 0
        if sName == '' or len(sName) <= 5:
            print("INFO: Incorrect input. NAME has to be at least 6 digits long.")
    val.append(sName)
    # input manager
    sManager = input("Retailer Manager: ")
    if sManager == '0':
        return 0
    val.append(sManager)
    # validate salary
    fSalary = ''
    while fSalary == '':
        fSalary = input("Retailer Salary: ")
        if fSalary == '0':
            return 0
        try:
            fSalary = float(fSalary)
            val.append(fSalary)
        except Exception:
            print('\nINFO: Please enter a number. Ex: 1200.50.')
            fSalary = ''

    # validate active
    fActive = ''
    while fActive not in ['y', 'yes', 'n', 'no', '0']:
        fActive = input("Retailer Active (y/n): ")
        if fActive == '0':
            return 0
        elif fActive in ['y', 'yes']:
            val.append(True)
        elif fActive in ['n', 'no']:
            val.append(False)
        else:
            print("\nInfo: Invalid input. Please type 'y' or 'n'.")

    return val

def fValidateSellInput():
    print("Enter the sell details Below:")
    dictUpdate = {}
   
    # input Item
    sItem = ''
    while sItem == '':
        sItem = input("Type item name (0 to cancel): ")
        sItem = sItem.strip()
        if sItem == '0':
            print("\nINFO: Sell regitration cancelled.")
            return False
        elif len(sItem) < 3:
            print("\nINFO: Item cannot be blank and must have at least 3 characters.")
            sItem = ''
        else:
             dictUpdate["item"] = sItem

    # input Price    
    fPrice = ''
    while fPrice == '':
        fPrice =  input("Type item's price (0 to cancel): ")
        fPrice = fPrice.strip()
        if fPrice == '0':
            print("\nINFO: Sell regitration cancelled.")
            return False
        else:
            try:
                fPrice = float(fPrice)
                dictUpdate["price"] = fPrice
            except Exception as e:
                print("INFO: Invalid number entered. Expected format: 1200.50. ", e)
                fPrice = ''
        
    return dictUpdate

def fGetClientID():
    if len(backend.Client.all_items) < 1:
        fPrint_submenu_title(f"List of Clients")
        print("INFO: There are no Clients to select from. Adding a new sell was cancelled")
        return False
    fTable_print_items(backend.Client.all_items, "Clients")
    iCliID = ''
    while iCliID == '':
        iCliID = input("\nSelect a Client ID for the sell (0 or enter to cancel): ")
        if iCliID == '0' or iCliID == '':
            print("INFO: Adding a new sell was cancelled")
            return False
        try:
            cliOBJ = backend.Client.getObjectByID(iCliID)
            if cliOBJ == 0:
                print("INFO: Invalid ID. Please select an ID from table above.")
                iCliID = ''
            else:
                return iCliID
        except Exception as e:
            print("ERROR: Problem while getting the Client. Try selecting again: ",e)
            iCliID = ''

def fGetRetailerID():
    if len(backend.Retailer.all_items) < 1:
        fPrint_submenu_title(f"List of Retailers")
        print("INFO: There are no Retailers to select from. Adding a new sell was cancelled")
        return False
    fTable_print_items(backend.Retailer.all_items, "Retailers")
    iRetID = ''
    while iRetID == '':
        iRetID = input("\nSelect a Retailer ID for the sell (0 or enter to cancel): ")
        if iRetID == '0' or iRetID == '':
            print("INFO: Adding a new sell was cancelled")
            return False
        try:
            cliOBJ = backend.Retailer.getObjectByID(iRetID)
            if cliOBJ == 0:
                print("INFO: Invalid ID. Please select an ID from table above.")
                iRetID = ''
            else:
                return iRetID
        except Exception as e:
            print("ERROR: Problem while getting the Retailer. Try selecting again: ",e)
            iRetID = ''

def fModify(table):    
    if table == "Clients":
        if len(backend.Client.all_items) > 0:
            op = ''
            while op == '':
                fTable_print_items(backend.Client.all_items, table)
                op = input("\nType a client ID to change (or 0 to cancel): ")
                if op != '0':
                    try:
                        cliOBJ = backend.Client.getObjectByID(op)
                        if cliOBJ == 0:
                            print(
                                "\nERROR: Invalid Client ID entered. Plase select a valid ID.")
                            input("Press any key to continue.")
                            op = ''
                    except Exception as e:
                        print('\nERROR: Unable to get client to update: ', e)

            if op != '0':
                dictUpdate = fValidateClientChange(op, cliOBJ)
                if dictUpdate != 0:
                    try:
                        backend.Client.fUpdate_line(op, dictUpdate)
                        print('\nINFO: Client changed successfully.')
                    except Exception as e:
                        print('\nERROR: Unable to change client: ', e)
                else:
                    print("\nINFO: Changing Client cancelled")
            else:
                print('\nINFO: Modifying Client cancelled.')
        else:
            fPrint_submenu_title(f"List of {table}")
            print('\nINFO: Client table is empty. Nothing to modify.')
    if table == "Retailers":
        if len(backend.Retailer.all_items) > 0:
            op = ''
            while op == '':
                fTable_print_items(backend.Retailer.all_items, table)
                op = input("\nType a retailer ID to change (or 0 to cancel): ")
                if op != '0':
                    try:
                        cliOBJ = backend.Retailer.getObjectByID(op)
                        if cliOBJ == 0:
                            print(
                                "\nERROR: Invalid Retailer ID entered. Plase select a valid ID.")
                            input("Press any key to continue.")
                            op = ''
                    except Exception as e:
                        print('\nERROR: Unable to get retailer to update: ', e)

            if op != '0':
                dictUpdate = fValidateRetailerChange(op, cliOBJ)
                if dictUpdate != 0:
                    try:
                        backend.Retailer.fUpdate_line(op, dictUpdate)
                        print('\nINFO: Retailer changed successfully.')
                    except Exception as e:
                        print('\nERROR: Unable to change retailer: ', e)
                else:
                    print("\nINFO: Changing retailer cancelled")
            else:
                print('\nINFO: Modifying retailer cancelled.')
        else:
            fPrint_submenu_title(f"List of {table}")
            print('\nINFO: Retailer table is empty. Nothing to modify.')

def fValidateClientChange(id, cliOBJ):
    fPrint_submenu_title(f'Updating Client {id}: {cliOBJ.name}')
    # dictUpdate = {"cpf": 999, "name": "Zuleima", "country": "Italy",
    #               "city": "Rome", "phone": 9999, "date_nasc": "11/11/1111"}

    dictUpdate = {}
    print('Enter new value for each field, \nenter to continue with same value or 0 to canecl edit.')

    sCpf = ''
    while sCpf == '' or len(sCpf) <= 5:
        sCpf = input(
            f"\nClient CPF (Currently {cliOBJ.cpf if cliOBJ.cpf != '' else 'EMPTY'}): ")
        sCpf = sCpf.strip()
        if sCpf == '0':
            return 0
        if sCpf == '':
            sCpf = cliOBJ.cpf
        if sCpf == '' or len(sCpf) <= 5:
            print("INFO: Incorrect input. CPF has at least 6 digits.")
    dictUpdate['cpf'] = sCpf
    # input and validate sName
    sName = ''
    while sName == '' or len(sName) <= 5:
        sName = input(
            f"\nClient Name (Currently {cliOBJ.name if cliOBJ.name != '' else 'EMPTY'}): ")
        sName = sName.strip()
        if sName == '0':
            return 0
        if sName == '':
            sName = cliOBJ.name
        if sName == '' or len(sName) <= 5:
            print("INFO: Incorrect input. NAME has to be at least 6 digits long.")
    dictUpdate['name'] = sName
    # input country
    sCountry = input(
        f"\nClient Country (Currently {cliOBJ.country if cliOBJ.country != '' else 'EMPTY'}): ")
    sCountry = sCountry.strip()
    if sCountry == '':
        sCountry = cliOBJ.country
    if sCountry == '0':
        return 0
    dictUpdate['country'] = sCountry
    # input city
    sCity = input(
        f"\nClient City (Currently {cliOBJ.city if cliOBJ.city != '' else 'EMPTY'}): ")
    sCity = sCity.strip()
    if sCity == '':
        sCity = cliOBJ.city
    if sCity == '0':
        return 0
    dictUpdate['city'] = sCity
    # input phone
    sPhone = input(
        f"\nClient Phone (Currently {cliOBJ.phone if cliOBJ.phone != '' else 'EMPTY'}): ")
    sPhone = sPhone.strip()
    if sPhone == '':
        sPhone = cliOBJ.phone
    if sPhone == '0':
        return 0
    dictUpdate['phone'] = sPhone
    # input birthday
    sDate_nasc = input(
        f"\nClient Country (Currently {cliOBJ.date_nasc if cliOBJ.date_nasc != '' else 'EMPTY'}): ")
    sDate_nasc = sDate_nasc.strip()
    if sDate_nasc == '':
        sDate_nasc = cliOBJ.date_nasc
    if sDate_nasc == '0':
        return 0
    dictUpdate['date_nasc'] = sDate_nasc

    return dictUpdate

def fValidateRetailerChange(id, cliOBJ):
    fPrint_submenu_title(f'Updating Retailer {id}: {cliOBJ.name}')
    # dictUpdate = {"cpf": 899, "name": "Udo", "manager": "Jota",
    #                       "salary": 1000, "active": True}

    dictUpdate = {}
    print('Enter new value for each field, \nenter to continue with same value or 0 to canecl edit.')

    # input and validate cpf
    sCpf = ''
    while sCpf == '' or len(sCpf) <= 5:
        sCpf = input(
            f"\nRetailer CPF (Currently {cliOBJ.cpf if cliOBJ.cpf != '' else 'EMPTY'}): ")
        sCpf = sCpf.strip()
        if sCpf == '0':
            return 0
        if sCpf == '':
            sCpf = cliOBJ.cpf
        if sCpf == '' or len(sCpf) <= 5:
            print("INFO: Incorrect input. CPF has at least 6 digits.")
    dictUpdate['cpf'] = sCpf
    # input and validate sName
    sName = ''
    while sName == '' or len(sName) <= 5:
        sName = input(
            f"\nRetailer Name (Currently {cliOBJ.name if cliOBJ.name != '' else 'EMPTY'}): ")
        sName = sName.strip()
        if sName == '0':
            return 0
        if sName == '':
            sName = cliOBJ.name
        if sName == '' or len(sName) <= 5:
            print("INFO: Incorrect input. NAME has to be at least 6 digits long.")
    dictUpdate['name'] = sName
    # input manager
    sManager = input(
        f"\nRetailer Manager (Currently {cliOBJ.manager if cliOBJ.manager != '' else 'EMPTY'}): ")
    sManager = sManager.strip()
    if sManager == '':
        sManager = cliOBJ.manager
    if sManager == '0':
        return 0
    dictUpdate['manager'] = sManager
    # input salary
    fSalary = ''
    while fSalary == '':
        fSalary = input(
            f"\nRetailer Salary (Currently {cliOBJ.salary if cliOBJ.salary != '' else 'EMPTY'}): ")
        fSalary = fSalary.strip()
        if fSalary == '':
            fSalary = cliOBJ.salary
        if fSalary == '0':
            return 0
        try:
            fSalary = float(fSalary)
            dictUpdate['salary'] = fSalary
        except Exception as e:
            print("INFO: Incorrect input. Salary has to be a number in format 1200.50.")
            fSalary = ''
    
    # input active
    bActive = ''
    while bActive == '':
        activeVal = ''
        if cliOBJ.active == 'True':
            activeVal = 'yes'
        elif cliOBJ.active == 'False':
            activeVal = 'no'
        elif cliOBJ.active == '':
            activeVal = ''
        else:
            activeVal = cliOBJ.active

        bActive = input(
            f"\nRetailer Active (yes/no) (Currently {activeVal}): ")
        bActive = bActive.strip()
        if bActive == '':
            if cliOBJ.active == 'True':
                bActive = 'yes'
            elif cliOBJ.active == 'False':
                bActive = 'no'
        if bActive == '0':
            return 0
        if bActive in ['y', 'yes']:
            dictUpdate['active'] = 'True'
        elif bActive in ['n', 'no']:
            dictUpdate['active'] = 'False'
        else:
            print("INFO: Incorrect input. Expected 'yes' or 'no'.")
            bActive = ''

    return dictUpdate

def fDelete_Item(table):
    if table == "Clients":
        if len(backend.Client.all_items) > 0:
            fTable_print_items(backend.Client.all_items, "Clients")
            id = input(
                f"\nSelect a {table} ID to delete (Enter or 0 to cancel): ")
            if id == "0" or id == "":
                print("\nINFO: Delete operation cancelled.")
                input("Press any key to continue")
            else:
                try:
                    backend.Client.fDelete_line(id)
                    print("\nINFO: Client deleted successfully.")
                    input("Press any key to continue")
                except Exception as e:
                    print("ERROR: Unable to delete Client: ", e)
                    input("Press any key to continue")
        else:
            fPrint_submenu_title(f"List of {table}")
            print(f"INFO: {table} table has no items. Nothing to delete.")
            input("\nPress any key to continue")
    if table == "Retailers":
        if len(backend.Retailer.all_items) > 0:
            fTable_print_items(backend.Retailer.all_items, "Retailers")
            id = input(
                f"\nSelect a {table} ID to delete (Enter or 0 to cancel): ")
            if id == "0" or id == "":
                print("\nINFO: Delete operation cancelled.")
                input("Press any key to continue")
            else:
                try:
                    backend.Retailer.fDelete_line(id)
                    print("\nINFO: Client deleted successfully.")
                    input("Press any key to continue")
                except Exception as e:
                    print("ERROR: Unable to delete Retailer: ", e)
                    input("Press any key to continue")
        else:
            fPrint_submenu_title(f"List of {table}")
            print(f"INFO: {table} table has no items. Nothing to delete.")
            input("\nPress any key to continue")

def fPrintSellSum():
    fPrint_submenu_title("Sells per retailer")
    tab = backend.Sale.fGetTotalSells()
    if len(tab) > 0:
        head = ["Seller ID", "Seller Name", "Sell Count", "Sell Value"]
        row = "{id:<10}| {name:<20}| {cnt:>12} | {val:>15}".format
        print(row(id=head[0], name=head[1], cnt=head[2], val=head[3]))
        row = "{id:<10}| {name:<20.19}| {cnt:>12} | {val:>15,.2F}".format
        print("-"*80)
        for tup in tab:
            print(row(id=tup[0], name=tup[1], cnt=tup[2], val=tup[3]))
    else:
        print(f"INFO: No sells sum.")

def start_CLI():
    fMain_menu()


if __name__ == "__main__":
    ekbMod.fUpdate_INI_Settings()
    start_CLI()
