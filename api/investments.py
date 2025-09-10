from fastapi import APIRouter, Depends, Query
from database import get_db
from datetime import datetime, timezone
from auth import get_current_active_user
from models.user import User
from sqlalchemy.orm import Session
from api.utils import call_rapidapi
from crud.investments import InvestmentsCrud
from fastapi import HTTPException
from schemas.investments import MutualFundsResponse, InvestmentsRequest, InvestmentsResponse
from typing import List

router = APIRouter(prefix="", tags=["investments"])


@router.get("/mutual-funds", response_model=List[MutualFundsResponse])
def get_mutual_funds_for_fund_family(fund_family: str = Query(...), user: User = Depends(get_current_active_user)):
    querystring = {"Mutual_Fund_Family": fund_family, "Scheme_Type":"Open"}
    response = call_rapidapi(querystring)
    return response


@router.get("/mutual-funds/investments")
def get_mutual_funds_investments(user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    investments_crud = InvestmentsCrud(db)
    investments = investments_crud.get_investments(user.id)
    investments_response = []
    total_profit_loss = 0
    for investment in investments:
        profit_loss = (investment.current_price - investment.buy_price) * investment.units
        investments_response.append(
            InvestmentsResponse(
                scheme_code=investment.scheme_code,
                scheme_name=investment.scheme_name,
                units=investment.units,
                buy_price=investment.buy_price,
                current_price=investment.current_price,
                transaction_date=investment.transaction_date,
                mutual_fund_family=investment.mutual_fund_family,
                profit_loss=profit_loss
            )
        )
        total_profit_loss += profit_loss
        
    return {
        "investments": investments_response,
        "total_profit_loss": total_profit_loss
    }


@router.post("/mutual-funds/investments", response_model=InvestmentsResponse)
def create_mutual_funds_investments(data: InvestmentsRequest, user: User = Depends(get_current_active_user), 
                                    db: Session = Depends(get_db)):
    querystring = {"Scheme_Code": data.scheme_code}
    mutual_fund = call_rapidapi(querystring)
    if not mutual_fund:
        raise HTTPException(status_code=404, detail="Mutual fund not found")
        
    mutual_fund = mutual_fund[0]
    investment = {
        "user_id": user.id,
        "scheme_code": data.scheme_code,
        "scheme_name": mutual_fund["Scheme_Name"],
        "units": data.units,
        "buy_price": mutual_fund["Net_Asset_Value"],
        "current_price": mutual_fund["Net_Asset_Value"],
        "mutual_fund_family": mutual_fund["Mutual_Fund_Family"],
    }
    investments_crud = InvestmentsCrud(db)
    investment = investments_crud.create_investment(investment)
    return investment