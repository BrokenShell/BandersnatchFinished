from os import getenv
from typing import Optional
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from MonsterLab import Monster
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pandas import DataFrame


class Database:
    load_dotenv()
    client = AsyncIOMotorClient(getenv("DB_URL"))

    def __init__(self, database: str, collection: str):
        self.collection = self.client[database][collection]

    async def seed(self, amount: int) -> None:
        await self.collection.insert_many([Monster().to_dict() for _ in range(amount)])

    async def reset(self) -> None:
        await self.collection.delete_many({})

    async def count(self) -> int:
        return await self.collection.count_documents({})

    async def dataframe(self) -> DataFrame:
        documents = await self.collection.find({}, {"_id": False}).to_list(None)
        return DataFrame(documents)

    async def html_table(self) -> Optional[str]:
        df = await self.dataframe()
        return df.to_html() if not df.empty else None

    def close(self) -> None:
        self.client.close()


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    db = Database("Database", "Collection")
    try:
        yield
    finally:
        db.close()


if __name__ == '__main__':
    import asyncio

    async def main():
        db = Database("Database", "Collection")
        await db.reset()
        await db.seed(1024)
        print(await db.html_table())
        db.close()

    asyncio.run(main())
