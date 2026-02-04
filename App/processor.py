import spacy
from data import DB, DB_NAME

# Тут можешь его расширять
class SQLhelper:
    def __init__(self)->None:
        self.db = DB()

    def select_all(self) -> list[tuple]:
        return self.db.execute_query(f"SELECT * from {DB_NAME}")
    
    def insert(self, values:list[tuple])->None:
        for v in values:
            self.db.execute_query(f"INSERT INTO {DB_NAME} (lemma, form, part_of_speech, role) VALUES {v}")


class Parser:

    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")
        self.sql = SQLhelper()
    
    def parse(text:str) -> None:
        pass


