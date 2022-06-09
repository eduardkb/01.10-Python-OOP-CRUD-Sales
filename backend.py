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
        id_search = str(id_search)
        cliUpdate = next(
            (x for x in Client.all_items if x.id == id_search), None)

        # if object not found raise exception
        if cliUpdate == None:
            raise Exception(
                f"Id {id_search} to be updated on table {Client.db_table_name} not found.")

        # UPDATE DATABAS
        database.fsql_update_line(
            Client.db_table_name, "id", id_search, dictUpdate)

        # UPDATE OBJECT
        cliUpdate.cpf = dictUpdate["cpf"]
        cliUpdate.name = dictUpdate["name"]
        cliUpdate.country = dictUpdate["country"]
        cliUpdate.city = dictUpdate["city"]
        cliUpdate.phone = dictUpdate["phone"]
        cliUpdate.date_nasc = dictUpdate["date_nasc"]

    @staticmethod
    def fDelete_line(id_search):
        # search object
        id_search = str(id_search)
        cliDel = next(
            (x for x in Client.all_items if x.id == id_search), None)
        print(cliDel)

        # if object not found raise exception
        if cliDel == None:
            raise Exception(
                f"Id {id_search} to be deleted on table {Client.db_table_name} not found.")

        # delete database item
        database.fsql_delete_line(Client.db_table_name, "id", id_search)

        # delete item from list
        Client.all_items = [x for x in Client.all_items if x.id != id_search]


class Retailer():
    db_fields = ["Id:integer PRIMARY KEY", "CPF:text", "Name:text",
                 "Manager:text", "sells:integer", "salary:real", "active:boolean"]
    db_table_name = "client"


class Sale():
    pass


if __name__ == "__main__":
    ekbMod.clear_scren()

    def fTest_print_all_objects():
        print("--------------------------------------")
        print("Client Table:")
        print(Client.all_items)
        print("--------------------------------------")

    def fTest_client_create_table():
        Client.fCreate_table()

    def fTest_client_add():
        Client(1, "111", "Eduard", "Croacia",
               "Semelci", 9977, "17/01/1983")
        Client(2, "222", "Laysa", "USA",
               "Miami", 8080, "29/12/1990")
        Client(3, "333", "Gabri", "Brasil",
               "Ponta Grossa", 8989, "14/12/1987")
        Client(4, "444", "Siby", "Brasil",
               "Guarapuava", 9797, "29/05/1986")
        Client(5, "555", "Helena", "Alemanha", "Munich", 8880, "24/10/1959")

    def fTest_client_read_all():
        Client.fRead_all_from_db()

    def fTest_update_one():
        id = 3
        dictUpdate = {"cpf": 999, "name": "Zuleima", "country": "Italy",
                      "city": "Rome", "phone": 9999, "date_nasc": "11/11/1111"}
        a = Client.fUpdate_line(id, dictUpdate)
        print(f"Client {id} updated.")

    def fTest_delete_one():
        Client.fDelete_line(5)

    # fTest_client_create_table()
    # fTest_client_add()

    fTest_client_read_all()
    fTest_print_all_objects()
    # fTest_update_one()
    # fTest_delete_one()
    # fTest_print_all_objects()
