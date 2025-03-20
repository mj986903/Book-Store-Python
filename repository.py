from models import Book,Author
from database import db

class BookRepository:
    @staticmethod
    def get_all_books(skip,take):
        total_count = db.session.query(Book).filter(Book.deleted == False).count()
        books = db.session.query(Book).join(Author).filter(Book.deleted == False).order_by(Book.id).offset(skip).limit(take).all()
        return books,total_count
    @staticmethod
    def get_books_by_author(author_id,skip,take):
        total_count = db.session.query(Book).filter(Book.deleted == False,Book.author_id==author_id).count()
        books = db.session.query(Book).join(Author).filter(Book.deleted == False,Book.author_id==author_id).order_by(Book.id).offset(skip).limit(take).all()
        return books,total_count
    
    @staticmethod
    def get_book(book_id):
        return db.session.query(Book).join(Author).filter(Book.id == book_id, Book.deleted == False).first()
    
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