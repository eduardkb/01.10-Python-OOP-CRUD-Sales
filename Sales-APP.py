"""
TODO TODO
-- give option to cancel Update and add as well
-- validate some filelds with the class while adding
not urgent
-- when printing list format float value

"""
import resources.backend as backend
import resources.ekbMod as ekbMod
bDEBUG = True


######################################################
# CLI - Print Main menu


def fMain_menu():
    op = '0'
    while str(op) != '5':
        fPrint_main_Menu()

        op = input("Select an option: ")
        match op:
            case '1':
                fCreate_database()
            case '2':
                fEnter_client()
            case '3':
                fEnter_Retailer()
            case '4':
                fEnter_Sells()

        if op not in ['1', '2', '3', '4', '5']:
            print("\nINFO: Invalid option.")
            input("Press any key to return.")


def fPrint_main_Menu():
    ekbMod.clear_scren()
    print(" "*27 + "╔═══════════════════════╗")
    print(" "*27 + "║   Sales - Main Menu   ║")
    print(" "*27 + "╚═══════════════════════╝")

    print("╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                             ║")
    print("║       🢡  1 - Create database                                                ║")
    print("║       🢡  2 - Client Registration                                            ║")
    print("║       🢡  3 - Retailer Registration                                          ║")
    print("║       🢡  4 - Sells Registration                                             ║")
    print("║       🢡  5 - Exit                                                           ║")
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

        match op:
            case '1':
                fTable_print_items(backend.Client.all_items, "Clients")
                input("\nPress any key to return.")
            case '2':
                fAdd_new("Clients")
                input("Press any key to return.")
            case '3':
                pass
            case '4':
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

        match op:
            case '1':
                fTable_print_items(backend.Retailer.all_items, "Retailers")
                input("\nPress any key to return.")
            case '2':
                fAdd_new("Retailers")
                input("Press any key to return.")
            case '3':
                pass
            case '4':
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
        print("5 - Back to Main Menu")

        op = str(input("Select an option: "))
        if op not in ['1', '2', '3', '4', '5']:
            print("\nINFO: Invalid option.")
            input("Press any key to return.")

        match op:
            case '1':
                fTable_print_items(backend.Sale.all_items, "Sells")
                input("\nPress any key to return.")
            case '2':
                fAdd_new("Sells")
                input("Press any key to return.")

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
            row = "{id:<4}| {CPF:<10}| {Name:<15}| {Country:<15}| {City:<15}| {Phone:<10}| {Birthday:^10}".format
            print(row(id=head[0], CPF=head[1], Name=head[2], Country=head[3],
                      City=head[4], Phone=head[5], Birthday=head[6]))
            print("-"*80)
            for tup in items:
                print(row(id=tup.id, CPF=tup.cpf, Name=tup.name, Country=tup.country,
                          City=tup.city, Phone=tup.phone, Birthday=tup.date_nasc))
        else:
            print(f"INFO: {table} table is empty.")
    elif table == "Retailers":
        if len(items) > 0:
            head = ["ID", "CPF", "Name", "Manager", "Salary"]
            row = "{id:<4}| {CPF:<10}| {Name:<15}| {Manager:<15}| {Salary:<10}".format
            print(row(id=head[0], CPF=head[1], Name=head[2], Manager=head[3],
                      Salary=head[4]))
            print("-"*80)
            for tup in items:
                print(row(id=tup.id, CPF=tup.cpf, Name=tup.name, Manager=tup.manager,
                          Salary=tup.salary))
        else:
            fPrint_submenu_title(f"List of {table}")
            print(f"INFO: {table} table is empty.")
    elif table == "Sells":
        if len(items) > 0:
            head = ["ID", "Retailer", "Client", "Item Sold", "Price"]
            row = "{id:<4}| {ret:<10}| {cli:<15}| {item:<15}| {price:<10}".format
            print(row(id=head[0], ret=head[1], cli=head[2], item=head[3],
                      price=head[4]))
            print("-"*80)
            for tup in items:
                print(row(id=tup.id, ret=tup.retailer, cli=tup.client, item=tup.item_sold,
                          price=tup.price))
        else:
            fPrint_submenu_title(f"List of {table}")
            print(f"INFO: {table} table is empty.")


def fAdd_new(table):
    fPrint_submenu_title(f"Adding {table}")
    print("Type a value for each field (0 at any field to cancel):")

    if table == "Clients":
        val = backend.Client.fValidateInput()
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
        pass
    if table == "Sells":
        pass


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


def start_CLI():
    fMain_menu()


if __name__ == "__main__":
    ekbMod.fUpdate_INI_Settings()
    start_CLI()
