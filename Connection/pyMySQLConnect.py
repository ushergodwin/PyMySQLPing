try:
    from decouple import config
    import pymysql
    import pymysql.cursors
    pymysql.install_as_MySQLdb()
except ModuleNotFoundError as err:
    print(err)

class pyMySQLConnect:
    
    _db = None
    def _connect(self):
        self._db = pymysql.connect(
            host=config("DB_HOST"),
            user=config("DB_USER"),
            password=config("DB_PASSWORD"),
            database=config("DB_NAME"),
            port=int(config("DB_PORT")),
            cursorclass=pymysql.cursors.DictCursor
            )
        return self._db
        
    
    
        