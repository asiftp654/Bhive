from pydantic import BaseModel, Field
from datetime import date


class MutualFundsResponse(BaseModel):
    Scheme_Code: int
    Scheme_Name: str
    Net_Asset_Value: float
    Scheme_Category: str


class InvestmentsRequest(BaseModel):
    scheme_code: int
    units: int = Field(gt=0)

class InvestmentsResponse(BaseModel):
    scheme_code: int
    scheme_name: str
    units: float
    buy_price: float
    current_price: float
    transaction_date: date
    mutual_fund_family: str
    profit_loss: float = 0.0