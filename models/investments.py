from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, String, Date
from database import Base
from datetime import datetime


class Investments(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scheme_code = Column(Integer)
    scheme_name = Column(String)
    units = Column(Integer)
    buy_price = Column(Numeric(precision=10, scale=4))
    current_price = Column(Numeric(precision=10, scale=4))
    transaction_date = Column(Date, default=datetime.today().date())
    mutual_fund_family = Column(String)


