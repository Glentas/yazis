import spacy
from data import DB, DB_NAME

# Тут можешь его расширять
class SQLhelper:
    def __init__(self)->None:
        self.db = DB()

    def select_all(self) -> list[tuple]:
        return self.db.select_query(f"SELECT * from {DB_NAME}")
    
    def insert(self, values:list[tuple])->None:
        for v in values:
            self.db.execute_query(f"INSERT OR IGNORE INTO {DB_NAME} (lemma, form, part_of_speech, role) VALUES (?, ?, ?, ?)", v)
    
    # По айди
    def update(self, id:int, lemma:str, form:str, pos:str, role:str)->None:
        self.db.execute_query(
            f"UPDATE {DB_NAME} SET lemma = ?, form = ?, part_of_speech = ?, role = ? WHERE id = ?",
            (lemma, form, pos, role, id)
        )


class Parser:

    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")
        self.sql = SQLhelper()
    
    def parse(self, text:str) -> None:
        if not text.strip():
            return

        doc = self.nlp(text)
        records:list[tuple] = []

        for token in doc:
            if (
                token.is_punct or
                token.is_space or
                token.is_bracket or
                token.like_url or
                token.like_email or
                token.like_num or
                not token.text.strip()
            ):
                continue

            form = token.text.lower().strip()
            lemma = token.lemma_.lower().strip()

            if lemma == "-pron-":
                lemma = form

            if not form.isalpha() or not lemma.isalpha():
                continue

            if len(form) > 31 or len(lemma) > 31:
                continue

            pos = token.pos_
            role = token.dep_.lower()

            records.append((lemma, form, pos, role))

        if records:
            self.sql.insert(records)

# tests = "These are my super tests, I guess. Let's check it out! Words are: run, running, ran."
# Использование:
# prs = Parser()
# prs.parse(tests)
# print(prs.sql.select_all())

