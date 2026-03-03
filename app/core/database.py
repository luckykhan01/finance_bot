import asyncpg
from app.core.config import settings

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Opens the pool when starting"""
        try:
            self.pool = await asyncpg.create_pool(
                dsn=settings.database_url,
                min_size=1,
                max_size=10
            )
            print("DB Connection Succeeded")
        except Exception as e:
            print("DB Connection Failure")
            raise e

    async def disconnect(self):
        """Closes the pool if app stopped"""
        if self.pool:
            await self.pool.close()
            print("DB Connection Closed")

db = Database()