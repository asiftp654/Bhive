from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.investments import Investments


class InvestmentsCrud:
    def __init__(self, db: Session):
        self.db = db
        self.model = Investments

    def get_all_unique_scheme_codes(self):
        return self.db.query(self.model.scheme_code).distinct().all()


class AsyncInvestmentsCrud:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = Investments
        
    async def get_investments(self, user_id: int):
        result = await self.db.execute(select(self.model).filter(self.model.user_id == user_id))
        return result.scalars().all()

    async def get_all_unique_scheme_codes(self):
        result = await self.db.execute(select(self.model.scheme_code).distinct())
        return result.scalars().all()

    async def create_investment(self, investment: dict):
        investment = self.model(**investment)
        self.db.add(investment)
        await self.db.commit()
        await self.db.refresh(investment)
        return investment