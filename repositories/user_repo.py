from models import User
from database import db

class UserRepository:
    @staticmethod
    def add_user(user):
        already_user = db.session.query(User).filter(User.email == user.email).first()
        if not already_user:
            db.session.add(user)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def check_user(user):
        already_user = db.session.query(User).filter(User.email == user.email,User.active == True).first()
        if already_user:
            return already_user.check_password(user.password)
        return False