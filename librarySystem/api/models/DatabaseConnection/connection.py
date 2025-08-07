import os
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from librarySystem.tools.credentials import MONGO_URL, DB_NAME


class DatabaseConnection:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect_client(self):
        print(f"Connecting to MongoDB server... {MONGO_URL}  {DB_NAME}")
        self.client  = AsyncIOMotorClient(MONGO_URL)
    
    async def ping(self):
        try:
            await self.client.admin.command("ping")
            return True
        except:
            return False

    async def connect_db(self):
        is_up = await self.ping()
        if not is_up:
            raise HTTPException(status_code=500, detail="Não foi possível conectar ao banco de dados.")

        print('Server is up!')
        self.db = self.client[DB_NAME]
        return self.db
