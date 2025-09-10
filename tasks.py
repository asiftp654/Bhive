from celery_app import celery
from database import SessionLocal
from models.investments import Investments
from crud.investments import InvestmentsCrud
from api.utils import call_rapidapi
from sqlalchemy import update, case


@celery.task(bind=True, max_retries=3, default_retry_delay=60) 
def update_latest_prices(self):
    db = SessionLocal()
    try:
        investments_crud = InvestmentsCrud(db)
        scheme_codes = investments_crud.get_all_unique_scheme_codes()        
        if not scheme_codes:
            return

        scheme_codes = ",".join(str(code[0]) for code in scheme_codes if code and code[0] is not None)
        querystring = {"Scheme_Code": scheme_codes}
        response = call_rapidapi(querystring)
        latest_prices = {
            mutual_fund["Scheme_Code"]: mutual_fund["Net_Asset_Value"]
            for mutual_fund in response
        }
        
        # we are using a single SQLAlchemy bulk update statement for performance.
        # This is more efficient (updation in single query) than updating one by one
        db_update_statement = (
            update(Investments)
            .where(Investments.scheme_code.in_(latest_prices.keys()))
            .where(Investments.current_price != case( # only update if current price is different from latest price
                *( (code, price) for code, price in latest_prices.items() ),
                value=Investments.scheme_code))
            .values(
                current_price=case(
                    *( (code, price) for code, price in latest_prices.items() ),
                    value=Investments.scheme_code
                )
            )
        )

        executed_statement = db.execute(db_update_statement)
        db.commit()
        print(f"Current prices updated: {executed_statement.rowcount}")
    except Exception as exc:
        print(f"Error occurred: {exc}, retrying...")
        raise self.retry(exc=exc) 
    finally:
        db.close()
