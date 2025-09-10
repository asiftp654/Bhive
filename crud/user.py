from sqlalchemy.orm import Session
from models.user import User
from api.utils import hash_password

class UserCrud:
    def __init__(self, db: Session):
        self.db = db
        self.model = User
        
    def get_user(self, email: str):
        return self.db.query(self.model).filter(self.model.email == email).first()
    
    def create_user(self, email: str, password: str):
        hashed_password = hash_password(password)
        user = self.model(email=email, password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def mark_as_verified(self, user: User):
        user.is_verified = True
        self.db.commit()
        self.db.refresh(user)
        return user