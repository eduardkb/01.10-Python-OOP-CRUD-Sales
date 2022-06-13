"""
TODO TODO
-- change app files to /module/ folder
-- read ini file and decide between gui and cli
-- try reading ini file from ekbMod AND USE IN BOTH database.py and SalesInterface.py
-- when printing list format float value
"""
import ekbMod
import backend
from tabulate import tabulate

######################################################
# Print Main menu


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
# Print Main menu


def fPrint_submenu_title(title: str):
    ekbMod.clear_scren()
    title = f"   Submenu - {title}   "
    table = '┄' * len(title)
    print(f"┍{table}┑")
    print(f"┆{title}┆")
    print(f"┕{table}┙")
    print("┄"*80)


######################################################
# Sub Menus

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
            case '2':
                pass
            case '3':
                pass
            case '4':
                pass


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
            case '2':
                pass
            case '3':
                pass
            case '4':
                pass


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
            case '2':
                pass
            case '3':
                pass
            case '4':
                pass


######################################################
# General Functions

def fCreate_database():
    fPrint_submenu_title("Create Databases")
    try:
        backend.Client.fCreate_table()
        backend.Retailer.fCreate_table()
        backend.Sale.fCreate_table()
        print("INFO: All databses created successful if they did not exist.")
    except Exception as e:
        print("ERROR: Database couldn't be created: ", e)

    input("\nPress any key to return to main menu.")


def fTable_print_items(items, table):
    fPrint_submenu_title(f"List of {table}")
    if table == "Clients":
        head = ["ID", "CPF", "Name", "Country", "City", "Phone", "Birthday"]
        row = "{id:<4}| {CPF:<10}| {Name:<15}| {Country:<15}| {City:<15}| {Phone:<10}| {Birthday:^10}".format
        print(row(id=head[0], CPF=head[1], Name=head[2], Country=head[3],
              City=head[4], Phone=head[5], Birthday=head[6]))
        print("-"*80)
        for tup in items:
            print(row(id=tup.id, CPF=tup.cpf, Name=tup.name, Country=tup.country,
                  City=tup.city, Phone=tup.phone, Birthday=tup.date_nasc))
    elif table == "Retailers":
        head = ["ID", "CPF", "Name", "Manager", "Salary"]
        row = "{id:<4}| {CPF:<10}| {Name:<15}| {Manager:<15}| {Salary:<10}".format
        print(row(id=head[0], CPF=head[1], Name=head[2], Manager=head[3],
              Salary=head[4]))
        print("-"*80)
        for tup in items:
            print(row(id=tup.id, CPF=tup.cpf, Name=tup.name, Manager=tup.manager,
                  Salary=tup.salary))
    elif table == "Sells":
        head = ["ID", "Retailer", "Client", "Item Sold", "Price"]
        row = "{id:<4}| {ret:<10}| {cli:<15}| {item:<15}| {price:<10}".format
        print(row(id=head[0], ret=head[1], cli=head[2], item=head[3],
              price=head[4]))
        print("-"*80)
        for tup in items:
            print(row(id=tup.id, ret=tup.retailer, cli=tup.client, item=tup.item_sold,
                  price=tup.price))
    input("\nPress any key to return.")


def start_CLI():
    fMain_menu()


if __name__ == "__main__":
    start_CLI()
