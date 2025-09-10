from sqlalchemy.orm import Session
from models.investments import Investments


class InvestmentsCrud:
    def __init__(self, db: Session):
        self.db = db
        self.model = Investments
        
    def get_investments(self, user_id: int):
        return self.db.query(self.model).filter(self.model.user_id == user_id).all()

    def get_all_unique_scheme_codes(self):
        return self.db.query(self.model.scheme_code).distinct().all()

    def create_investment(self, investment: dict):
        investment = self.model(**investment)
        self.db.add(investment)
        self.db.commit()
        self.db.refresh(investment)
        return investment
    
    def update_current_price(self, scheme_code: int, new_price: float):
        self.db.query(self.model).filter(
            self.model.scheme_code == scheme_code
        ).update({"current_price": new_price})
        self.db.commit()