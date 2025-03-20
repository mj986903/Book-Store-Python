from database import db
from datetime import datetime

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at
        }

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id",ondelete="CASCADE"), nullable=False)
    isbn = db.Column(db.String(15), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author.name,
            "isbn": self.isbn,
            "price": self.price,
            "created_at": self.created_at
        }

class APIResponse:
    def __init__(self,data,message,status_code,success):
        self.data = data
        self.message = message
        self.status_code = status_code
        self.success = success

    def to_dict(self):
        return {"data": self.data, "message": self.message, "status_code": self.status_code, "success": self.success}
