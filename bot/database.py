import motor.motor_asyncio
from .vars import  DATABASE_URL, DATABASE_NAME


class Database:
    def __init__(self, uri=DATABASE_URL, database_name=DATABASE_NAME):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.cache = {}
    
    def new_user(self, id):
        return {"id": id, "currency": "USD"}
    
    async def add_user(self, id):
        user = self.new_user(id)
        print("🚲 ~ database.py:16 -> user: ",  user)
        await self.col.insert_one(user)
    
    async def get_user(self, id):
        user = self.cache.get(id)
        if user is not None:
            return user
        
        user = await self.col.find_one({"id": int(id)})
        self.cache[id] = user
        return user
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
    
    async def update_currency(self, user_id, currency):
        await self.col.update_one(
            {'id': int(user_id)},
            {'$set': {'currency': currency}}
        )
        if user_id in self.cache:
            self.cache[user_id]['currency'] = currency

db = Database()