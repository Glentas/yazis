import sqlite3 as sql
import os

DIR = "DB"
DATABASE = "mydb.db"
PATH = DIR + "/"+ DATABASE

if not os.path.exists(DIR):
    os.mkdir(DIR)
    print(f"(?) Created folder {DIR}/")

class DB:
    def __init__(self) -> None:
        self.conn = sql.connect(PATH)
        self.crs = self.conn.cursor()
        self.crs.execute(
            """
            CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word VARCHAR(31) NOT NULL UNIQUE
            );
            """
            )
    
    def __del__(self)-> None:
        if self.conn:
            self.conn.close()
    
    def execute_single(self, command:str) -> None:
        try:
            self.crs.execute(command)
            self.conn.commit()

        except sql.Error as e:
            print(f"(!) Error: {e}")
            self.conn.rollback()
    
    def execute_many(self, command:str, params:list[tuple]) -> None:
        try:
            self.crs.executemany(command, params)
            self.conn.commit()

        except sql.Error as e:
            print(f"(!) Error: {e}")
            self.conn.rollback()


    def get_data(self, command:str, params:list[tuple]) -> list[tuple]:
        data:list[tuple] = []
        if command.strip().upper().startswith("SELECT"):

            try:
                self.crs.executemany(command, params)
                data = self.crs.fetchall()

            except sql.Error as e:
                print(f"(!) Error: {e}")
                self.conn.rollback()
        else:
            print("Incorrect 'SELECT' query")

        return data

    def select_all(self)-> list[tuple]:
        self.crs.execute("""SELECT * FROM vocabulary""")
        return self.crs.fetchall()
        
