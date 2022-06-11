"""
TODO TODO
Urgent
--  Class Sale: test update and delete
Not Urgent:
-- class demands id to be be passed. Implement option to not pass ID 
        so that DB handles ID generation
"""

from tkinter.messagebox import NO
import database
import ekbMod


class Client():
    db_fields = ["Id:integer PRIMARY KEY", "CPF:text", "Name:text",
                 "country:text", "city:text", "phone:integer", "date_nasc:datetime"]
    db_table_name = "client"
    all_items = []

    def __init__(self, id, cpf, name, country, city, phone, date_nasc, source_db=False) -> None:
        self.id = id
        self.cpf = cpf
        self.name = name
        self.country = country
        self.city = city
        self.phone = phone
        self.date_nasc = date_nasc

        if not source_db:
            # get next id to write on DB if 0 or less was passed as ID
            if self.id < 1:
                self.id = Client.fGet_next_id()
            # write on DB
            self.fwrite_to_db()

        Client.all_items.append(self)

    def __repr__(self) -> str:
        # print class
        sPrint = f"{self.__class__.__name__} | {self.id}, {self.cpf}, {self.name}, {self.country}, {self.city}, {self.phone}, {self.date_nasc}\n"
        return sPrint

    def fwrite_to_db(self):
        newValues = {"id": self.id, "cpf": self.cpf, "name": self.name, "country": self.country,
                     "city": self.city, "phone": self.phone, "date_nasc": self.date_nasc}
        database.fSql_add(Client.db_table_name, newValues)

    @staticmethod
    def fCreate_table():
        database.fSql_create_Table(Client.db_table_name, Client.db_fields)

    @staticmethod
    def fRead_all_from_db():
        Client.all_items = []
        items = database.fSql_read_all(Client.db_table_name)
        for item in items:
            Client(item[0], item[1], item[2],
                   item[3], item[4], item[5], item[6], True)

    @staticmethod
    def fUpdate_line(id_search, dictUpdate):
        # search for the object iwht ID x
        objUpdate = next(
            (x for x in Client.all_items if str(x.id) == str(id_search)), None)

        # if object not found raise exception
        if objUpdate == None:
            raise Exception(
                f"Id {id_search} to be updated on table {Client.db_table_name} not found.")

        # UPDATE DATABAS
        database.fsql_update_line(
            Client.db_table_name, "id", id_search, dictUpdate)

        # UPDATE OBJECT
        objUpdate.cpf = dictUpdate["cpf"]
        objUpdate.name = dictUpdate["name"]
        objUpdate.country = dictUpdate["country"]
        objUpdate.city = dictUpdate["city"]
        objUpdate.phone = dictUpdate["phone"]
        objUpdate.date_nasc = dictUpdate["date_nasc"]

    @staticmethod
    def fDelete_line(id_search):
        # search object
        id_search = str(id_search)
        cliDel = next(
            (x for x in Client.all_items if str(x.id) == str(id_search)), None)

        # if object not found raise exception
        if cliDel == None:
            raise Exception(
                f"Id {id_search} to be deleted on table {Client.db_table_name} not found.")

        # delete database item
        database.fsql_delete_line(Client.db_table_name, "id", id_search)

        # delete item from list (making a new list)
        Client.all_items = [
            x for x in Client.all_items if str(x.id) != str(id_search)]

    @staticmethod
    def fGet_next_id():
        # if all items is empty, read all items
        if len(Client.all_items) == 0:
            Client.fRead_all_from_db()

        # define next id
        id_max = int(1)
        for obj in Client.all_items:
            if id_max < int(obj.id):
                id_max = int(obj.id)
        return id_max + 1


class Retailer():
    db_fields = ["id:integer PRIMARY KEY", "cpf:text", "name:text",
                 "manager:text", "salary:real", "active:boolean"]
    db_table_name = "retailer"
    all_items = []

    def __init__(self, id, cpf, name, manager, salary, active, source_db=False) -> None:
        self.id = id
        self.cpf = cpf
        self.name = name
        self.manager = manager
        self.salary = salary
        self.active = active

        if not source_db:
            # get next id to write on DB if 0 or less was passed as ID
            if self.id < 1:
                self.id = Retailer.fGet_next_id()
            # write on DB
            self.fwrite_to_db()

        Retailer.all_items.append(self)

    def __repr__(self) -> str:
        # print class
        sPrint = f"{self.__class__.__name__} | {self.id}, {self.cpf}, {self.name}, {self.manager}, {self.salary}, {self.active}\n"
        return sPrint

    def fwrite_to_db(self):
        newValues = {"id": self.id, "cpf": self.cpf, "name": self.name, "manager": self.manager,
                     "salary": self.salary, "active": self.active}
        database.fSql_add(Retailer.db_table_name, newValues)

    @staticmethod
    def fCreate_table():
        database.fSql_create_Table(Retailer.db_table_name, Retailer.db_fields)

    @staticmethod
    def fRead_all_from_db():
        Retailer.all_items = []
        items = database.fSql_read_all(Retailer.db_table_name)
        for item in items:
            Retailer(item[0], item[1], item[2],
                     item[3], item[4], item[5], True)

    @staticmethod
    def fUpdate_line(id_search, dictUpdate):
        # search for the object iwht ID x
        id_search = str(id_search)
        objUpdate = next(
            (x for x in Retailer.all_items if str(x.id) == str(id_search)), None)

        # if object not found raise exception
        if objUpdate == None:
            raise Exception(
                f"Id {id_search} to be updated on table {Retailer.db_table_name} not found.")

        # UPDATE DATABAS
        database.fsql_update_line(
            Retailer.db_table_name, "id", id_search, dictUpdate)

        # UPDATE OBJECT
        objUpdate.cpf = dictUpdate["cpf"]
        objUpdate.name = dictUpdate["name"]
        objUpdate.manager = dictUpdate["manager"]
        objUpdate.salary = dictUpdate["salary"]
        objUpdate.active = dictUpdate["active"]

    @staticmethod
    def fDelete_line(id_search):
        # search object
        cliDel = next(
            (x for x in Retailer.all_items if str(x.id) == str(id_search)), None)

        # if object not found raise exception
        if cliDel == None:
            raise Exception(
                f"Id {id_search} to be deleted on table {Retailer.db_table_name} not found.")

        # delete database item
        database.fsql_delete_line(Retailer.db_table_name, "id", id_search)

        # delete item from list (making a new list)
        Retailer.all_items = [
            x for x in Retailer.all_items if str(x.id) != str(id_search)]

    @staticmethod
    def fGet_next_id():
        # if all items is empty, read all items
        if len(Retailer.all_items) == 0:
            Retailer.fRead_all_from_db()

        # define next id
        id_max = int(1)
        for obj in Retailer.all_items:
            if id_max < int(obj.id):
                id_max = int(obj.id)
        return id_max + 1


class Sale():
    db_fields = ["Id:integer PRIMARY KEY", "id_retailer:integer", "id_client:integer",
                 "item_sold:text", "price:real"]
    db_table_name = "sale"
    all_items = []

    def __init__(self, id, id_retailer, id_client, item_sold, price, source_db=False) -> None:
        self.id = id
        self.id_retailer = id_retailer
        self.retailer = '-'
        self.id_client = id_client
        self.client = '-'
        self.item_sold = item_sold
        self.price = price

        if not source_db:
            # get next id to write on DB if 0 or less was passed as ID
            if self.id < 1:
                self.id = Sale.fGet_next_id()
            # write on DB
            self.fwrite_to_db()

        Sale.all_items.append(self)

    def __repr__(self) -> str:
        # print class
        sPrint = f"{self.__class__.__name__} | {self.id}, {self.id_retailer}, {self.retailer}, {self.id_client}, {self.client}, {self.item_sold}, {self.price}\n"
        return sPrint

    def fwrite_to_db(self):
        newValues = {"id": self.id, "id_retailer": self.id_retailer,
                     "id_client": self.id_client, "item_sold": self.item_sold, "price": self.price}
        database.fSql_add(Sale.db_table_name, newValues)

    @staticmethod
    def fCreate_table():
        database.fSql_create_Table(Sale.db_table_name, Sale.db_fields)

    @staticmethod
    def fRead_all_from_db():
        Sale.all_items = []
        items = database.fSql_read_all(Sale.db_table_name)
        for item in items:
            Sale(item[0], item[1], item[2],
                 item[3], item[4], True)

    @staticmethod
    def fUpdate_line(id_search, dictUpdate):
        # search for the object wiht ID x
        objUpdate = next(
            (x for x in Sale.all_items if str(x.id) == str(id_search)), None)

        # if object not found raise exception
        if objUpdate == None:
            raise Exception(
                f"Id {id_search} to be updated on table {Sale.db_table_name} not found.")

        # UPDATE DATABAS
        database.fsql_update_line(
            Client.db_table_name, "id", id_search, dictUpdate)

        # UPDATE OBJECT
        objUpdate.cpf = dictUpdate["cpf"]
        objUpdate.name = dictUpdate["name"]
        objUpdate.country = dictUpdate["country"]
        objUpdate.city = dictUpdate["city"]
        objUpdate.phone = dictUpdate["phone"]
        objUpdate.date_nasc = dictUpdate["date_nasc"]

    @staticmethod
    def fDelete_line(id_search):
        # search object
        id_search = str(id_search)
        cliDel = next(
            (x for x in Sale.all_items if str(x.id) == str(id_search)), None)

        # if object not found raise exception
        if cliDel == None:
            raise Exception(
                f"Id {id_search} to be deleted on table {Sale.db_table_name} not found.")

        # delete database item
        database.fsql_delete_line(Client.db_table_name, "id", id_search)

        # delete item from list (making a new list)
        Client.all_items = [
            x for x in Client.all_items if str(x.id) != str(id_search)]

    @staticmethod
    def fGet_next_id():
        # if all items is empty, read all items
        if len(Sale.all_items) == 0:
            Sale.fRead_all_from_db()

        # define next id
        id_max = int(1)
        for obj in Sale.all_items:
            if id_max < int(obj.id):
                id_max = int(obj.id)
        return id_max + 1


if __name__ == "__main__":
    def fTest_print_all_objects(objTest_Class):
        print("--------------------------------------")
        print(f"{objTest_Class} Table:")
        if objTest_Class == "Client":
            print(Client.all_items)
        elif objTest_Class == "Retailer":
            print(Retailer.all_items)
        elif objTest_Class == "Sale":
            print(Sale.all_items)
        print("--------------------------------------")

    def fTest_create_table(objTest_Class):
        if objTest_Class == "Client":
            Client.fCreate_table()
        elif objTest_Class == "Retailer":
            Retailer.fCreate_table()
        elif objTest_Class == "Sale":
            Sale.fCreate_table()

    def fTest_add(objTest_Class):
        if objTest_Class == "Client":
            Client(1, "111", "Eduard", "Croacia",
                   "Semelci", 9977, "17/01/1983")
            Client(2, "222", "Laysa", "USA",
                   "Miami", 8080, "29/12/1990")
            Client(3, "333", "Gabri", "Brasil",
                   "Ponta Grossa", 8989, "14/12/1987")
            Client(4, "444", "Siby", "Brasil",
                   "Guarapuava", 9797, "29/05/1986")
            Client(5, "555", "Helena", "Alemanha",
                   "Munich", 8880, "24/10/1959")
            Client(6, "666", "Mateus", "Japao", "Tokio", 7878, "31/12/1985")
        elif objTest_Class == "Retailer":
            Retailer(1, "119", "Victor", "Luiza", 1500, True)
            Retailer(2, "229", "Julia", "Marco", 3600, True)
            Retailer(3, "339", "Otavio", "Luiza", 1500, False)
            Retailer(0, "888", "aaaa", "aaaa", 1234, True)
        elif objTest_Class == "Sale":
            Sale(0, "1", 6, "Lanterna", 12.49)
            Sale(0, "2", 7, "Celular", 850)
            Sale(0, "3", 8, "Laptop", 2500.99)
            Sale(0, "4", 9, "Livro", 35.15)

    def fTest_read_all(objTest_Class):
        if objTest_Class == "Client":
            Client.fRead_all_from_db()
        elif objTest_Class == "Retailer":
            Retailer.fRead_all_from_db()
        elif objTest_Class == "Sale":
            Sale.fRead_all_from_db()

    def fTest_update_one(objTest_Class, id):
        if objTest_Class == "Client":
            dictUpdate = {"cpf": 999, "name": "Zuleima", "country": "Italy",
                          "city": "Rome", "phone": 9999, "date_nasc": "11/11/1111"}
            a = Client.fUpdate_line(id, dictUpdate)
        elif objTest_Class == "Retailer":
            dictUpdate = {"cpf": 899, "name": "Udo", "manager": "Jota",
                          "salary": 1000, "active": True}
            a = Retailer.fUpdate_line(id, dictUpdate)
        elif objTest_Class == "Sale":
            dictUpdate = {"id_retailer": 2, "id_client": 2, "item_sold": "Tv",
                          "price": 111}
            a = Sale.fUpdate_line(id, dictUpdate)
        print(f"{objTest_Class} {id} updated.")

    def fTest_delete_one(objTest_Class, id):
        if objTest_Class == "Client":
            Client.fDelete_line(id)
        elif objTest_Class == "Retailer":
            Retailer.fDelete_line(id)
        elif objTest_Class == "Sale":
            Sale.fDelete_line(id)
        print(f"ID {id} deleted from table {objTest_Class}")

    ekbMod.clear_scren()
    objTest_Class = "Client"
    objTest_Class = "Retailer"
    objTest_Class = "Sale"

    # fTest_create_table(objTest_Class)
    # fTest_add(objTest_Class)

    fTest_read_all(objTest_Class)

    fTest_print_all_objects(objTest_Class)
    # fTest_update_one(objTest_Class, 2)
    # fTest_delete_one(objTest_Class, 2)

    fTest_print_all_objects(objTest_Class)
