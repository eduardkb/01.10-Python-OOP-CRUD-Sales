# backend
class Database():
    iniSettings = {}

    @staticmethod
    def fLoadDatabaseSettings():
        Database.iniSettings = {"Database": "File", }
        Database.iniSettings = {"FileDB_path": ".\\FileDB\\", }
        Database.iniSettings = {"FileDB_extension": "tdb", }


Database.fLoadDatabaseSettings()
