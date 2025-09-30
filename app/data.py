from os import getenv
from typing import Optional

from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    load_dotenv()
    db = MongoClient(getenv("DB_URL"))["Database"]["Collection"]

    def seed(self, amount):
        self.db.insert_many(Monster().to_dict() for _ in range(amount))

    def reset(self):
        self.db.delete_many({})

    def count(self) -> int:
        return self.db.count_documents({})

    def dataframe(self) -> DataFrame:
        return DataFrame(self.db.find({}, {"_id": False}))

    def html_table(self) -> Optional[str]:
        return self.dataframe().to_html() if self.count() else None


# if __name__ == '__main__':
#     db = Database()
#     db.reset()
#     db.seed(1024)
#     print(db.html_table())
