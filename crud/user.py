from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from api.utils import hash_password


class AsyncUserCrud:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = User
        
    async def get_user(self, email: str):
        result = await self.db.execute(select(self.model).filter(self.model.email == email))
        return result.scalar_one_or_none()
    
    async def create_user(self, email: str, password: str):
        hashed_password = hash_password(password)
        user = self.model(email=email, password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def mark_as_verified(self, user: User):
        user.is_verified = True
        await self.db.commit()
        await self.db.refresh(user)
        return user