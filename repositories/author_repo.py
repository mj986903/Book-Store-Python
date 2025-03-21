from models.author import Author
from database import db

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
        
