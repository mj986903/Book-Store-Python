from models.author import Author
from models.book import Book
from database import db
from sqlalchemy import asc, desc,func

class BookRepository:
    @staticmethod
    def get_all_books(skip,take,parsed_start_date,parsed_end_date,order_by,order_attribute):
        attribute = Book.id if order_attribute == "id" else Book.price
        order_clause = asc(attribute) if order_by == "asc" else desc(attribute)
        
        query = db.session.query(Book).join(Author).filter(Book.deleted == False)

        if parsed_start_date:
            query = query.filter(Book.created_at >= parsed_start_date)

        if parsed_end_date:
            query = query.filter(Book.created_at <= parsed_end_date)

        total_count = query.count()
        books = query.order_by(order_clause).offset(skip).limit(take).all()
        
        return books, total_count
    
    @staticmethod
    def get_books_by_author(author_id,skip,take):
        total_count = db.session.query(Book).filter(Book.deleted == False,Book.author_id==author_id).count()
        books = db.session.query(Book).join(Author).filter(Book.deleted == False,Book.author_id==author_id).order_by(Book.id).offset(skip).limit(take).all()
        return books,total_count
    
    @staticmethod
    def get_book(book_id):
        return db.session.query(Book).join(Author).filter(Book.id == book_id, Book.deleted == False).first()
    
    @staticmethod
    def search_book(title):
        return db.session.query(Book).join(Author).filter(func.lower(Book.title) == title, Book.deleted == False).order_by(Book.id).first()
    
    @staticmethod
    def get_book_by_isbn(isbn):
        return db.session.query(Book).filter(Book.isbn == isbn).first()
    
    @staticmethod
    def add_book(book):
        db.session.add(book)
        db.session.commit()
        
    @staticmethod
    def delete_book(book_id):
        book = db.session.query(Book).filter(Book.id == book_id).first()
        if book :
            book.deleted = True
            db.session.commit()
            return True 
        else :
            return False

    