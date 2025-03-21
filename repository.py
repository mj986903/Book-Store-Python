from models import Book,Author,User
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

    

class AuthorRepository:
    @staticmethod
    def get_all_authors():
        return db.session.query(Author).filter(Author.deleted == False).order_by(Author.id).all()
    
    @staticmethod
    def add_author(author):
        db.session.add(author)
        db.session.commit()

    @staticmethod
    def delete_author(author_id):
        author = db.session.query(Author).filter(Author.id == author_id).first()
        if author :
            author.deleted = True
            db.session.commit()
            return True 
        else :
            return False
        

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